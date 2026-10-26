from __future__ import annotations

import asyncio
import math
import os
import re
import shutil
import sys
import tempfile
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from types import TracebackType
from typing import Any
from urllib.parse import quote

import httpx

from riotskillissue.core.http import RiotSkillIssueError
from riotskillissue.core.types import RiotId
from riotskillissue.replays import _retry_after

_PLATFORM = re.compile(r"[A-Za-z0-9]{2,10}")
_POLL_INTERVAL = 1.0
_LIMIT_MESSAGE = (
    "League's replay download limit was reached (10 downloads per hour, including "
    "downloads in the client). Try again later."
)


class LeagueClientError(RiotSkillIssueError):
    """A local League client request failed without exposing its credentials."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        retry_after: float | None = None,
    ) -> None:
        self.status = status
        self.retry_after = retry_after
        super().__init__(message)


@dataclass(frozen=True)
class ClientReplay:
    """A recent match offered by the running League client's match history."""

    index: int
    game_id: int
    platform_id: str
    game_version: str
    game_type: str
    queue_id: int
    game_end: int
    game_creation: int = 0
    game_duration: int = 0
    game_mode: str = ""

    def __post_init__(self) -> None:
        _integer(self.index, minimum=1)
        _integer(self.game_id, minimum=1)
        if not isinstance(self.platform_id, str) or not _PLATFORM.fullmatch(self.platform_id):
            raise ValueError("Invalid replay identifier")
        _nonempty_string(self.game_version)
        _nonempty_string(self.game_type)
        for value in (self.queue_id, self.game_end, self.game_creation, self.game_duration):
            _integer(value)
        if not isinstance(self.game_mode, str):
            raise ValueError("Invalid game mode")

    @property
    def filename(self) -> str:
        return f"{self.platform_id.upper()}-{self.game_id}.rofl"


@dataclass(frozen=True)
class _Credentials:
    port: int
    password: str = field(repr=False)


def _default_lockfiles() -> list[Path]:
    if sys.platform == "win32":
        drive = os.environ.get("SYSTEMDRIVE", "C:")
        return [Path(f"{drive}/") / "Riot Games" / "League of Legends" / "lockfile"]
    if sys.platform == "darwin":
        suffix = "League of Legends.app/Contents/LoL/lockfile"
        return [Path("/Applications") / suffix, Path.home() / "Applications" / suffix]
    return []


def _read_credentials(lockfile: str | Path | None) -> _Credentials:
    explicit = lockfile or os.environ.get("RIOT_LCU_LOCKFILE")
    candidates = [Path(explicit).expanduser()] if explicit else _default_lockfiles()
    path = next((candidate for candidate in candidates if candidate.is_file()), None)
    if path is None:
        raise LeagueClientError(
            "League lockfile was not found. Open and sign in to League on this computer, "
            "or pass --lockfile for a custom installation."
        )
    try:
        with path.open(encoding="utf-8") as source:
            text = source.read(4097).strip()
        name, pid, port, password, protocol = text.split(":")
        if (
            len(text) > 4096
            or name != "LeagueClient"
            or int(pid) < 1
            or not 1 <= int(port) <= 65535
            or not password
            or any(character.isspace() for character in password)
            or protocol != "https"
        ):
            raise ValueError
        return _Credentials(port=int(port), password=password)
    except (OSError, UnicodeError, ValueError):
        raise LeagueClientError(
            "Could not read a valid League lockfile. Check its path and restart the client."
        ) from None


def _object(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise LeagueClientError("The League client returned an unexpected response.")
    return value


def _integer(value: Any, *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError("Invalid replay integer")
    return value


def _nonempty_string(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Invalid replay string")
    return value


def _metadata_error(metadata: dict[str, Any]) -> None:
    # Newer clients may expose a quota error before it appears in the exported schema.
    values = [metadata.get(key) for key in ("state", "errorCode", "downloadError", "status")]
    for value in values:
        normalized = re.sub(r"[^a-z0-9]", "", str(value).lower())
        if normalized == "429" or any(
            marker in normalized
            for marker in ("ratelimit", "throttl", "toomanyrequests", "downloadquota")
        ):
            raise LeagueClientError(_LIMIT_MESSAGE, status=429)
    state = metadata.get("state")
    if not isinstance(state, str):
        raise LeagueClientError("The League client returned unexpected replay metadata.")
    errors = {
        "incompatible": "This replay belongs to an incompatible League patch.",
        "missingOrExpired": "This replay is missing or has expired.",
        "unsupported": "The League client does not support replays for this match.",
        "lost": "The League client could not find this replay file.",
        "retryDownload": "The League client could not download this replay. Check the client.",
        "error": "The League client reported a replay error. Check the client for details.",
    }
    if state in errors:
        raise LeagueClientError(errors[state])


def _copy_replay(source: Path, destination: Path, *, overwrite: bool) -> Path:
    temporary: Path | None = None
    try:
        with source.open("rb") as input_file, tempfile.NamedTemporaryFile(
            mode="wb",
            prefix=f".{destination.name}.",
            suffix=".part",
            dir=destination.parent,
            delete=False,
        ) as output:
            temporary = Path(output.name)
            expected = os.fstat(input_file.fileno()).st_size
            shutil.copyfileobj(input_file, output, length=1024 * 1024)
            if expected == 0 or output.tell() != expected:
                raise LeagueClientError("The downloaded replay file is empty or incomplete.")
        if overwrite:
            os.replace(temporary, destination)
        else:
            os.link(temporary, destination)
        return destination
    finally:
        if temporary is not None:
            with suppress(OSError):
                temporary.unlink(missing_ok=True)


class LeagueReplayClient:
    """Download one selected replay through a running, signed-in League client.

    This client uses the local League API, which Riot does not officially support.
    All requests stay on the lockfile's loopback port. The League client performs
    the download and enforces Riot's replay availability and download limits.
    """

    def __init__(self, lockfile: str | Path | None = None) -> None:
        credentials = _read_credentials(lockfile)
        self._http = httpx.AsyncClient(
            base_url=f"https://127.0.0.1:{credentials.port}",
            auth=httpx.BasicAuth("riot", credentials.password),
            # Riot's local client uses a self-signed certificate. This exception
            # is confined to the fixed loopback origin; redirects are rejected.
            verify=False,
            trust_env=False,
            follow_redirects=False,
            timeout=httpx.Timeout(10.0, connect=3.0),
        )

    async def __aenter__(self) -> LeagueReplayClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self._http.aclose()

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("League client requests must use a local API path")
        try:
            response = await self._http.request(method, path, **kwargs)
        except httpx.HTTPError:
            raise LeagueClientError(
                "Could not reach the League client. Keep it open and signed in. "
                "A submitted download may still finish; check the client before retrying."
            ) from None
        if response.status_code == 429:
            delay = _retry_after(response.headers.get("Retry-After"))
            message = (
                _LIMIT_MESSAGE if path.startswith("/lol-replays/")
                else "The League client rate limited this request. Try again later."
            )
            if delay is not None and delay > 0:
                message += f" Retry after {math.ceil(delay)} seconds."
            raise LeagueClientError(
                message,
                status=429,
                retry_after=delay,
            )
        if not response.is_success:
            if response.status_code == 401:
                message = "League client authentication expired. Restart this command."
            elif response.status_code == 403:
                message = "The League client denied access to this player or replay."
            elif response.status_code == 404:
                message = "The player or replay was not found in this client's region."
            elif response.is_redirect:
                message = "The League client returned an unexpected redirect."
            else:
                message = "The League client request failed. Check the client for details."
            raise LeagueClientError(message, status=response.status_code)
        if response.status_code == 204 or not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            raise LeagueClientError("The League client returned an unexpected response.") from None

    async def player_replays(self, riot_id: str, *, count: int = 20) -> list[ClientReplay]:
        """List up to 20 recent matches for a Riot ID in the client's region."""
        if not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= 20:
            raise ValueError("count must be between 1 and 20")
        parsed = RiotId.parse(riot_id)
        aliases = await self._request(
            "POST",
            "/lol-summoner/v1/summoners/aliases",
            json=[{"gameName": parsed.game_name, "tagLine": parsed.tag_line}],
        )
        if not isinstance(aliases, list):
            raise LeagueClientError("The League client returned an unexpected player response.")
        players = [
            item for item in aliases
            if isinstance(item, dict)
            and str(item.get("gameName", "")).casefold() == parsed.game_name.casefold()
            and str(item.get("tagLine", "")).casefold() == parsed.tag_line.casefold()
        ]
        if len(players) != 1 or not isinstance(players[0].get("puuid"), str):
            raise LeagueClientError("Player not found in the signed-in League client's region.")
        puuid = players[0]["puuid"]
        if not puuid:
            raise LeagueClientError("Player not found in the signed-in League client's region.")
        history = _object(await self._request(
            "GET",
            f"/lol-match-history/v1/products/lol/{quote(puuid, safe='')}/matches",
            params={"begIndex": 0, "endIndex": count - 1},
        ))
        games = _object(history.get("games")).get("games")
        if not isinstance(games, list):
            raise LeagueClientError("The League client returned an unexpected match history.")
        replays = []
        try:
            for index, item in enumerate(games[:count], start=1):
                game = _object(item)
                creation = _integer(game["gameCreation"])
                duration = _integer(game["gameDuration"])
                replays.append(ClientReplay(
                    index=index,
                    game_id=_integer(game["gameId"], minimum=1),
                    platform_id=_nonempty_string(game["platformId"]),
                    game_version=_nonempty_string(game["gameVersion"]),
                    game_type=_nonempty_string(game["gameType"]),
                    queue_id=_integer(game["queueId"]),
                    game_end=creation + duration * 1000,
                    game_creation=creation,
                    game_duration=duration,
                    game_mode=game.get("gameMode", ""),
                ))
        except (KeyError, TypeError, ValueError):
            raise LeagueClientError(
                "The League client returned an unexpected match history."
            ) from None
        return replays

    async def download_replay(
        self,
        replay: ClientReplay,
        destination: str | Path | None = None,
        *,
        overwrite: bool = False,
        timeout: float = 120.0,
    ) -> Path:
        """Download once, poll completion, and optionally copy the client's file."""
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout must be a finite positive number")
        try:
            async with asyncio.timeout(timeout):
                return await self._download(replay, destination, overwrite=overwrite)
        except TimeoutError:
            raise LeagueClientError(
                "Timed out waiting for the replay. The League client may finish in the "
                "background; check it before retrying."
            ) from None
        except FileExistsError:
            raise LeagueClientError(
                "The output file already exists. Choose another path or pass --overwrite."
            ) from None
        except OSError:
            raise LeagueClientError(
                "Could not read or copy the replay file. Check the path and permissions."
            ) from None

    async def _download(
        self, replay: ClientReplay, destination: str | Path | None, *, overwrite: bool
    ) -> Path:
        authorization = _object(await self._request("GET", "/lol-rso-auth/v1/authorization"))
        platform = authorization.get("currentPlatformId")
        if not isinstance(platform, str) or not _PLATFORM.fullmatch(platform):
            raise LeagueClientError("Could not determine the signed-in League client's region.")
        if platform.casefold() != replay.platform_id.casefold():
            raise LeagueClientError(
                "This match belongs to a different region than the signed-in League client."
            )
        directory = await self._request("GET", "/lol-replays/v1/rofls/path")
        if not isinstance(directory, str) or not directory or not Path(directory).is_absolute():
            raise LeagueClientError("The League client returned an invalid replay folder.")
        source = Path(directory) / replay.filename
        target = Path(destination).expanduser() if destination is not None else source
        copy_file = target.resolve() != source.resolve()
        if copy_file:
            if not overwrite and (target.exists() or target.is_symlink()):
                raise FileExistsError
            target.parent.mkdir(parents=True, exist_ok=True)

        metadata_path = f"/lol-replays/v1/metadata/{replay.game_id}"
        try:
            metadata = _object(await self._request("GET", metadata_path))
        except LeagueClientError as error:
            if error.status != 404:
                raise
            await self._request(
                "POST",
                f"/lol-replays/v2/metadata/{replay.game_id}/create",
                json={
                    "gameVersion": replay.game_version,
                    "gameType": replay.game_type,
                    "queueId": replay.queue_id,
                    "gameEnd": replay.game_end,
                },
            )
            metadata = _object(await self._request("GET", metadata_path))

        requested = False
        while True:
            _metadata_error(metadata)
            if type(metadata.get("gameId")) is not int or metadata["gameId"] != replay.game_id:
                raise LeagueClientError(
                    "The League client returned metadata for a different match."
                )
            state = metadata.get("state")
            if state in {"found", "downloading", "watch"}:
                requested = True
            if state == "watch" and source.is_file() and source.stat().st_size > 0:
                return _copy_replay(source, target, overwrite=overwrite) if copy_file else source
            if state == "download" and not requested:
                requested = True
                await self._request(
                    "POST",
                    f"/lol-replays/v1/rofls/{replay.game_id}/download",
                    json={"componentType": "replay-button_match-history"},
                )
            elif state not in {"checking", "found", "download", "downloading", "watch"}:
                raise LeagueClientError("The League client reported an unknown replay state.")
            await asyncio.sleep(_POLL_INTERVAL)
            metadata = _object(await self._request("GET", metadata_path))

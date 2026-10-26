from __future__ import annotations

import math
import os
import re
import tempfile
from collections.abc import Sequence
from contextlib import suppress
from dataclasses import dataclass, field
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import httpx

from riotskillissue.core.http import RiotSkillIssueError

_MATCH_FILE = re.compile(r"([A-Za-z][A-Za-z0-9]*_[0-9]+)(?:\.(?:replay|rofl))?", re.I)
_SAFE_STEM = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,119}")
_WINDOWS_RESERVED = {"CON", "PRN", "AUX", "NUL"} | {
    f"{prefix}{number}" for prefix in ("COM", "LPT") for number in range(1, 10)
}
_REDIRECT_STATUSES = {301, 302, 303, 307, 308}
_MAX_REDIRECTS = 5


@dataclass(frozen=True)
class ReplayFile:
    """One replay offered by Riot for the authenticated player.

    URLs may contain signed credentials and are intentionally omitted from repr.
    The index identifies the entry within the response that produced it.
    """

    index: int
    filename: str
    url: str = field(repr=False)

    def __post_init__(self) -> None:
        if self.index < 1:
            raise ValueError("Replay index must be positive")
        stem = self.filename.removesuffix(".rofl")
        if not self.filename.endswith(".rofl") or not _safe_stem(stem):
            raise ValueError("Replay filename must be a safe .rofl filename")


class ReplayDownloadError(RiotSkillIssueError):
    """A replay could not be downloaded, without exposing its signed URL."""

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


def _safe_stem(stem: str) -> bool:
    return bool(
        _SAFE_STEM.fullmatch(stem)
        and not stem.endswith((".", " "))
        and stem.split(".")[0].upper() not in _WINDOWS_RESERVED
    )


def _replay_filename(url: str, index: int) -> str:
    try:
        components = [unquote(part) for part in urlsplit(url).path.split("/")]
    except ValueError:
        return f"replay-{index}.rofl"

    # Riot has returned both MATCH_ID.replay and MATCH_ID/0.replay paths.
    # Neither shape is promised by the API, so a match ID is only a naming hint.
    for component in reversed(components):
        match = _MATCH_FILE.fullmatch(component)
        if match and len(match[1]) <= 120:
            return f"{match[1].upper()}.rofl"

    basename = components[-1]
    stem = re.sub(r"\.(?:replay|rofl)$", "", basename, flags=re.I)
    if _safe_stem(stem):
        return f"{stem}.rofl"
    return f"replay-{index}.rofl"


def replay_files(urls: Sequence[str]) -> list[ReplayFile]:
    """Give each URL a safe, unique local name without changing the URL."""
    files: list[ReplayFile] = []
    names: set[str] = set()
    for index, url in enumerate(urls, start=1):
        filename = _replay_filename(url, index)
        stem = filename.removesuffix(".rofl")
        suffix = index
        while filename.casefold() in names:
            filename = f"{stem[:100]}-{suffix}.rofl"
            suffix += 1
        names.add(filename.casefold())
        files.append(ReplayFile(index=index, filename=filename, url=url))
    return files


def _validate_url(url: str) -> None:
    try:
        parsed = urlsplit(url)
        valid = (
            parsed.scheme == "https"
            and bool(parsed.hostname)
            and parsed.username is None
            and parsed.password is None
            and not parsed.fragment
            and not any(ord(character) < 32 or ord(character) == 127 for character in url)
        )
        # Accessing port also rejects malformed and out-of-range port numbers.
        _ = parsed.port
    except ValueError:
        valid = False
    if not valid:
        raise ReplayDownloadError("Replay download requires a valid HTTPS URL without credentials.")


def _retry_after(value: str | None) -> float | None:
    if not value:
        return None
    try:
        delay = float(value)
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=UTC)
            delay = (date - datetime.now(UTC)).total_seconds()
        except (TypeError, ValueError, OverflowError):
            return None
    return max(0.0, delay) if math.isfinite(delay) else None


def _download_error(response: httpx.Response) -> ReplayDownloadError:
    status = response.status_code
    retry_after = _retry_after(response.headers.get("Retry-After"))
    if status in (401, 403):
        message = "Replay access was denied or its URL expired. Refresh the replay list."
    elif status == 404:
        message = "Replay file is no longer available. Refresh the replay list."
    elif status == 429:
        message = "Replay download was rate limited. Try again later."
        if retry_after is not None:
            message = f"Replay download was rate limited; retry after {retry_after:g}s."
    else:
        message = f"Replay download failed with HTTP {status}."
    return ReplayDownloadError(message, status=status, retry_after=retry_after)


async def download_replay(
    replay: ReplayFile,
    destination: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Stream a selected replay to disk, publishing it only after completion.

    Download URLs are used without Riot API credentials. Redirects must also
    use HTTPS. Existing files are preserved unless overwrite is requested, and
    failed or cancelled transfers leave no partial replay behind. HTTP errors
    are reported without retrying or exposing the signed URL.
    """
    url = replay.url
    _validate_url(url)
    path = Path(destination).expanduser()
    temporary: Path | None = None
    try:
        if not overwrite and (path.exists() or path.is_symlink()):
            raise ReplayDownloadError(
                "Destination already exists. Choose another path or overwrite."
            )
        path.parent.mkdir(parents=True, exist_ok=True)
        async with httpx.AsyncClient(
            headers={"Accept-Encoding": "identity"},
            timeout=httpx.Timeout(30.0, connect=5.0),
            follow_redirects=False,
        ) as client:
            for redirects in range(_MAX_REDIRECTS + 1):
                # A signed link needs no cookies, including cookies set by a redirect.
                client.cookies.clear()
                async with client.stream("GET", url) as response:
                    if response.status_code in _REDIRECT_STATUSES:
                        location = response.headers.get("Location")
                        if not location or redirects == _MAX_REDIRECTS:
                            raise ReplayDownloadError(
                                "Replay download exceeded its redirect limit."
                            )
                        url = urljoin(url, location)
                        _validate_url(url)
                        continue
                    if response.status_code != 200:
                        raise _download_error(response)

                    with tempfile.NamedTemporaryFile(
                        mode="wb",
                        prefix=f".{path.name}.",
                        suffix=".part",
                        dir=path.parent,
                        delete=False,
                    ) as output:
                        temporary = Path(output.name)
                        size = 0
                        async for chunk in response.aiter_bytes(chunk_size=65536):
                            output.write(chunk)
                            size += len(chunk)

                    if size == 0:
                        raise ReplayDownloadError("Replay download was empty.")
                    length = response.headers.get("Content-Length")
                    if (
                        length is not None
                        and response.headers.get("Content-Encoding", "identity") == "identity"
                        and (not length.isdecimal() or int(length) != size)
                    ):
                        raise ReplayDownloadError("Replay download was incomplete.")
                    break

        if temporary is None:
            raise ReplayDownloadError("Replay download did not produce a file.")
        if overwrite:
            os.replace(temporary, path)
        else:
            # Atomic, fail-if-present publication also protects a file created
            # by another process while this download was running.
            os.link(temporary, path)
        return path
    except FileExistsError:
        raise ReplayDownloadError(
            "Destination already exists. Choose another path or overwrite."
        ) from None
    except httpx.TimeoutException:
        raise ReplayDownloadError("Replay download timed out. Try again later.") from None
    except (httpx.HTTPError, httpx.InvalidURL, ValueError):
        raise ReplayDownloadError(
            "Replay download failed due to an invalid URL or network error."
        ) from None
    except OSError:
        raise ReplayDownloadError("Could not write the replay file to the destination.") from None
    finally:
        if temporary is not None:
            with suppress(OSError):
                temporary.unlink(missing_ok=True)

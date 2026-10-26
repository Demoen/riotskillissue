from __future__ import annotations

import asyncio
import math
from collections.abc import Awaitable, Callable
from dataclasses import replace
from pathlib import Path
from typing import Annotated, Any

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from .auth import StaticRsoTokenProvider
from .core.client import RiotClient
from .core.config import RiotClientConfig
from .core.http import (
    MalformedResponseError,
    MissingCredentialError,
    RateLimitError,
    ResponseValidationError,
    RiotAPIError,
    RiotTransportError,
)
from .core.types import PlatformRoute, RegionalRoute, RiotId
from .league_client import ClientReplay, LeagueClientError, LeagueReplayClient
from .replays import ReplayDownloadError, ReplayFile, _retry_after

app = typer.Typer(
    help="RiotSkillIssue command-line client",
    rich_markup_mode="rich",
    pretty_exceptions_show_locals=False,
)
replays_app = typer.Typer(
    help="Download your RSO replays or another player's replays through the League client.",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
)
app.add_typer(replays_app, name="replays")
console = Console()


def _value(data: Any, name: str, default: Any = None) -> Any:
    if isinstance(data, dict):
        return data.get(name, default)
    return getattr(data, name, default)


@app.command()
def summoner(
    riot_id: str,
    route: str = typer.Option("euw1", help="LoL platform route"),
    api_key: str | None = typer.Option(None, envvar="RIOT_API_KEY"),
) -> None:
    """Get a focused League of Legends player profile."""

    async def run() -> None:
        async with RiotClient(
            api_key=api_key,
            default_route=PlatformRoute(route.lower()),
        ) as riot:
            profile = await riot.lol.player_profile(riot_id)
            game_profile = profile.game_profile
            table = Table(title=f"Player: {profile.riot_id}")
            table.add_column("Level", style="magenta")
            table.add_column("PUUID", style="cyan", no_wrap=True)
            table.add_row(
                str(_value(game_profile, "summoner_level", "?")),
                profile.puuid,
            )
            console.print(table)

    asyncio.run(run())


@app.command()
def match(
    match_id: str,
    route: str = typer.Option("europe", help="Regional route"),
    api_key: str | None = typer.Option(None, envvar="RIOT_API_KEY"),
) -> None:
    """Get a League of Legends match by ID."""

    async def run() -> None:
        async with RiotClient(api_key=api_key) as riot:
            data = await riot.raw.lol.match.get_match(
                match_id=match_id,
                route=RegionalRoute(route.lower()),
            )
            info = _value(data, "info", {})
            rprint(f"[green]Match {match_id} loaded[/green]")
            rprint(f"Game mode: {_value(info, 'game_mode', '?')}")
            rprint(f"Duration: {_value(info, 'game_duration', '?')}s")

    asyncio.run(run())


@app.command()
def live(
    riot_id: str = typer.Argument(..., help='Riot ID such as "Player#EUW"'),
    route: str = typer.Option("euw1", help="LoL platform route"),
    api_key: str | None = typer.Option(None, envvar="RIOT_API_KEY"),
    refresh: int = typer.Option(30, min=5, help="Refresh interval in seconds"),
) -> None:
    """Launch the optional live-game terminal interface."""
    if "#" not in riot_id:
        raise typer.BadParameter('Riot ID must use the form "GameName#TagLine"')
    if not api_key:
        raise typer.BadParameter("Set RIOT_API_KEY or pass --api-key")

    from .tui import run_tui

    game_name, tag_line = riot_id.rsplit("#", 1)
    run_tui(
        api_key=api_key,
        game_name=game_name,
        tag_line=tag_line,
        region=route,
        auto_refresh=refresh,
    )


def _replay_options(
    route: str, access_token: str | None
) -> tuple[RegionalRoute, RiotClientConfig]:
    allowed_routes = {"americas", "asia", "europe", "sea"}
    normalized = route.strip().lower()
    if normalized not in allowed_routes:
        raise typer.BadParameter(
            "Choose americas, asia, europe, or sea.", param_hint="--route"
        )
    if not access_token or not access_token.strip():
        raise typer.BadParameter(
            "Set RIOT_RSO_ACCESS_TOKEN or pass --access-token with a Riot Sign On "
            "player token. A Riot API key cannot authorize replay requests.",
            param_hint="--access-token",
        )
    try:
        environment_config = RiotClientConfig.from_env()
    except ValueError:
        raise typer.BadParameter(
            "Invalid RIOT_* environment configuration. Check timeout and retry settings.",
            param_hint="environment",
        ) from None
    config = replace(
        environment_config,
        rso_token_provider=StaticRsoTokenProvider(access_token),
        cache_rso_responses=False,
        max_rate_limit_retries=0,
    )
    return RegionalRoute(normalized), config


def _print_replays(replays: list[ReplayFile]) -> None:
    table = Table(title="Available replays")
    table.add_column("#", justify="right")
    table.add_column("File")
    for replay in replays:
        table.add_row(str(replay.index), replay.filename)
    console.print(table)


def _player_riot_id(player: str, route: str | None) -> str:
    if route is not None:
        raise typer.BadParameter(
            "The --player mode uses the logged-in League client's region. Omit --route.",
            param_hint="--route",
        )
    try:
        return str(RiotId.parse(player))
    except ValueError:
        raise typer.BadParameter(
            'Use a full Riot ID such as "GameName#TagLine".', param_hint="--player"
        ) from None


def _print_client_replays(replays: list[ClientReplay]) -> None:
    table = Table(title="Recent matches")
    table.add_column("#", justify="right")
    table.add_column("Match")
    table.add_column("Queue", justify="right")
    table.add_column("Patch")
    for replay in replays:
        table.add_row(
            str(replay.index),
            f"{replay.platform_id}_{replay.game_id}",
            str(replay.queue_id),
            replay.game_version,
        )
    console.print(table)


def _selected_replay(index: int | None, count: int) -> int:
    selected = typer.prompt("Replay number", type=int) if index is None else index
    if selected < 1 or selected > count:
        raise typer.BadParameter(
            f"Choose a replay number between 1 and {count}.", param_hint="INDEX"
        )
    return selected - 1


def _rate_limit_hint(error: RateLimitError) -> str:
    header = error.response.headers.get("Retry-After") if error.response else None
    delay = _retry_after(header)
    if delay is not None and delay > 0:
        return f"Try again in {math.ceil(delay)} seconds."
    return "Try again later."


def _run_replay_command(run: Callable[[], Awaitable[None]]) -> None:
    try:
        asyncio.run(run())
    except RateLimitError as error:
        message = f"Riot's replay API rate limit was reached. {_rate_limit_hint(error)}"
    except MissingCredentialError:
        message = "Set RIOT_RSO_ACCESS_TOKEN to a valid Riot Sign On player token."
    except RiotAPIError as error:
        if error.status == 401:
            message = "The RSO access token is invalid or expired. Sign in again through your RSO application."
        elif error.status == 403:
            message = "Replay access was denied. Check your application's RSO approval and the player's authorization."
        elif error.status == 404:
            message = "No replay data was found. Check the regional route and replay availability."
        else:
            message = f"The replay API returned HTTP {error.status}. Try again later."
    except LeagueClientError as error:
        message = str(error)
    except ReplayDownloadError as error:
        message = str(error)
    except RiotTransportError:
        message = "Could not reach Riot's replay API. Check your connection and try again."
    except (MalformedResponseError, ResponseValidationError):
        message = "Riot returned an invalid replay list. Try again later."
    except FileExistsError:
        message = "The output file already exists. Choose another path or pass --overwrite."
    except OSError:
        message = "Could not write the replay file. Check the output path and permissions."
    else:
        return
    typer.echo(f"Error: {message}", err=True)
    raise typer.Exit(code=1)


@replays_app.command("list")
def list_replays(
    route: str | None = typer.Option(None, help="RSO regional route: americas, asia, europe (default), or sea"),
    access_token: str | None = typer.Option(
        None, envvar="RIOT_RSO_ACCESS_TOKEN", help="RSO player access token", show_default=False
    ),
    player: str | None = typer.Option(None, help='Full Riot ID to look up through the League client, e.g. "Name#TAG"'),
    lockfile: Annotated[
        Path | None,
        typer.Option("--lockfile", envvar="RIOT_LCU_LOCKFILE", help="League client lockfile for --player mode"),
    ] = None,
    count: int | None = typer.Option(None, min=1, max=20, help="Recent matches in --player mode (default: 20)"),
) -> None:
    """List your RSO replays, or another player's recent matches with --player."""
    if player is not None:
        riot_id = _player_riot_id(player, route)

        async def run_player() -> None:
            async with LeagueReplayClient(lockfile=lockfile) as league:
                replays = await league.player_replays(riot_id, count=count or 20)
            if not replays:
                console.print("No recent matches were found for this player on the client's region.")
                return
            _print_client_replays(replays)
            console.print("Use 'replays download --player' with the same Riot ID to choose a match.")

        _run_replay_command(run_player)
        return
    if count is not None:
        raise typer.BadParameter("--count requires --player.", param_hint="--count")
    regional_route, config = _replay_options(route or "europe", access_token)

    async def run() -> None:
        async with RiotClient(config=config) as riot:
            replays = await riot.lol.replays(route=regional_route)
        if not replays:
            console.print("No replays are available for this player on this route.")
            return
        _print_replays(replays)
        console.print("Run 'riotskillissue-cli replays download' to choose a replay.")

    _run_replay_command(run)


@replays_app.command("download")
def download_replay(
    index: int | None = typer.Argument(
        None, min=1, help="One-based replay number; omit to choose from the current list"
    ),
    route: str | None = typer.Option(None, help="RSO regional route: americas, asia, europe (default), or sea"),
    access_token: str | None = typer.Option(
        None, envvar="RIOT_RSO_ACCESS_TOKEN", help="RSO player access token", show_default=False
    ),
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Destination file; --player defaults to the client's replay folder"),
    ] = None,
    overwrite: bool = typer.Option(False, help="Replace an existing output file after a complete download"),
    player: str | None = typer.Option(None, help='Download through the League client for a Riot ID, e.g. "Name#TAG"'),
    lockfile: Annotated[
        Path | None,
        typer.Option("--lockfile", envvar="RIOT_LCU_LOCKFILE", help="League client lockfile for --player mode"),
    ] = None,
    count: int | None = typer.Option(None, min=1, max=20, help="Recent matches in --player mode (default: 20)"),
    timeout: float | None = typer.Option(None, min=1, max=600, help="Seconds to wait for a --player download (default: 120)"),
) -> None:
    """Download one .rofl; --player uses the running League client's replay access."""
    if timeout is not None and not math.isfinite(timeout):
        raise typer.BadParameter("Use a finite timeout in seconds.", param_hint="--timeout")
    if player is not None:
        riot_id = _player_riot_id(player, route)

        async def run_player() -> None:
            async with LeagueReplayClient(lockfile=lockfile) as league:
                replays = await league.player_replays(riot_id, count=count or 20)
                if not replays:
                    typer.echo("No recent matches were found for this player on the client's region.", err=True)
                    raise typer.Exit(code=1)
                if index is None:
                    _print_client_replays(replays)
                replay = replays[_selected_replay(index, len(replays))]
                console.print(f"Requesting {replay.filename} through the League client...", markup=False)
                saved = await league.download_replay(
                    replay, output, overwrite=overwrite, timeout=timeout or 120
                )
                typer.echo(f"Saved replay to {saved}")

        _run_replay_command(run_player)
        return
    if count is not None or timeout is not None:
        raise typer.BadParameter("--count and --timeout require --player.")
    regional_route, config = _replay_options(route or "europe", access_token)

    async def run() -> None:
        async with RiotClient(config=config) as riot:
            replays = await riot.lol.replays(route=regional_route)
            if not replays:
                typer.echo("No replays are available for this player on this route.", err=True)
                raise typer.Exit(code=1)
            if index is None:
                _print_replays(replays)
            replay = replays[_selected_replay(index, len(replays))]
            destination = (output if output is not None else Path(replay.filename)).expanduser()
            if not overwrite and (destination.exists() or destination.is_symlink()):
                raise FileExistsError
            console.print(f"Downloading {replay.filename}...", markup=False)
            saved = await riot.lol.download_replay(replay, destination, overwrite=overwrite)
            typer.echo(f"Saved replay to {saved}")

    _run_replay_command(run)


def main() -> None:
    app()

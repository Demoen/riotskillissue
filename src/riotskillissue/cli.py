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
from .core.types import PlatformRoute, RegionalRoute
from .replays import ReplayDownloadError, ReplayFile, _retry_after

app = typer.Typer(
    help="RiotSkillIssue command-line client",
    rich_markup_mode="rich",
    pretty_exceptions_show_locals=False,
)
replays_app = typer.Typer(
    help="List and download League replays available to an authorized RSO player.",
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
    route: str = typer.Option("europe", help="Regional route: americas, asia, europe, or sea"),
    access_token: str | None = typer.Option(
        None, envvar="RIOT_RSO_ACCESS_TOKEN", help="RSO player access token", show_default=False
    ),
) -> None:
    """List replay files returned for the player authorized by your RSO token."""
    regional_route, config = _replay_options(route, access_token)

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
    route: str = typer.Option("europe", help="Regional route: americas, asia, europe, or sea"),
    access_token: str | None = typer.Option(
        None, envvar="RIOT_RSO_ACCESS_TOKEN", help="RSO player access token", show_default=False
    ),
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Destination file; defaults to the replay filename"),
    ] = None,
    overwrite: bool = typer.Option(False, help="Replace an existing output file after a complete download"),
) -> None:
    """Download one authorized replay as a .rofl file."""
    regional_route, config = _replay_options(route, access_token)

    async def run() -> None:
        async with RiotClient(config=config) as riot:
            replays = await riot.lol.replays(route=regional_route)
            if not replays:
                typer.echo("No replays are available for this player on this route.", err=True)
                raise typer.Exit(code=1)
            selected = index
            if selected is None:
                _print_replays(replays)
                selected = typer.prompt("Replay number", type=int)
            if selected < 1 or selected > len(replays):
                raise typer.BadParameter(
                    f"Choose a replay number between 1 and {len(replays)}.",
                    param_hint="INDEX",
                )
            replay = replays[selected - 1]
            destination = (output if output is not None else Path(replay.filename)).expanduser()
            if not overwrite and (destination.exists() or destination.is_symlink()):
                raise FileExistsError
            console.print(f"Downloading {replay.filename}...", markup=False)
            saved = await riot.lol.download_replay(replay, destination, overwrite=overwrite)
            console.print(f"Saved replay to {saved}", markup=False)

    _run_replay_command(run)


def main() -> None:
    app()

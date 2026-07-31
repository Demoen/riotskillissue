from __future__ import annotations

import asyncio
from typing import Any

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from .core.client import RiotClient
from .core.types import PlatformRoute, RegionalRoute

app = typer.Typer(help="RiotSkillIssue command-line client", rich_markup_mode="rich")
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


def main() -> None:
    app()

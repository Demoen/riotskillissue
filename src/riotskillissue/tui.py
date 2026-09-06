"""
Live Game TUI — Terminal User Interface for spectating League of Legends matches.

Usage:
    riotskillissue-cli live "GameName#TagLine" --route euw1
"""

from __future__ import annotations

import asyncio
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional, Tuple

from textual.app import App, ComposeResult
from textual import work
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.timer import Timer
from textual.widgets import Footer, Header, Label, LoadingIndicator, Static
from textual.binding import Binding

from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.console import Group

from .core.client import RiotClient
from .core.http import NotFoundError
from .core.types import PlatformRoute


# ── Static Mappings ──────────────────────────────────────────────────────────

SUMMONER_SPELLS: Dict[int, str] = {
    1: "Cleanse",
    3: "Exhaust",
    4: "Flash",
    6: "Ghost",
    7: "Heal",
    11: "Smite",
    12: "Teleport",
    13: "Clarity",
    14: "Ignite",
    21: "Barrier",
    30: "To the King!",
    31: "Poro Toss",
    32: "Mark",
    39: "Mark",
    54: "Placeholder",
    55: "Placeholder",
}

QUEUE_TYPES: Dict[int, str] = {
    0: "Custom",
    400: "Normal Draft",
    420: "Ranked Solo/Duo",
    430: "Normal Blind",
    440: "Ranked Flex",
    450: "ARAM",
    490: "Quickplay",
    700: "Clash",
    720: "ARAM Clash",
    830: "Co-op vs. AI (Intro)",
    840: "Co-op vs. AI (Beginner)",
    850: "Co-op vs. AI (Intermediate)",
    900: "ARURF",
    1020: "One for All",
    1090: "TFT Normal",
    1100: "TFT Ranked",
    1300: "Nexus Blitz",
    1400: "Ultimate Spellbook",
    1700: "Arena",
    1710: "Arena",
    1900: "Pick URF",
}

TIER_ORDER = {
    "IRON": 0, "BRONZE": 1, "SILVER": 2, "GOLD": 3,
    "PLATINUM": 4, "EMERALD": 5, "DIAMOND": 6,
    "MASTER": 7, "GRANDMASTER": 8, "CHALLENGER": 9,
}

TIER_COLORS = {
    "IRON": "#8B8682",
    "BRONZE": "#CD7F32",
    "SILVER": "#C0C0C0",
    "GOLD": "#FFD700",
    "PLATINUM": "#40E0D0",
    "EMERALD": "#50C878",
    "DIAMOND": "#B9F2FF",
    "MASTER": "#9B59B6",
    "GRANDMASTER": "#E74C3C",
    "CHALLENGER": "#F39C12",
}


def _spell_name(spell_id: int) -> str:
    return SUMMONER_SPELLS.get(spell_id, f"?({spell_id})")


def _queue_name(queue_id: int) -> str:
    return QUEUE_TYPES.get(queue_id, f"Queue {queue_id}")


def _format_duration(seconds: int) -> str:
    """Format game duration as MM:SS."""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def _rank_string(entry: Optional[Dict[str, Any]]) -> str:
    """Format a league entry into a rank string like 'Diamond II 45 LP'."""
    if not entry:
        return "Unranked"
    tier = entry.get("tier", "?")
    rank = entry.get("rank", "")
    lp = entry.get("league_points", 0)
    return f"{tier.capitalize()} {rank} {lp} LP"


def _rank_color(entry: Optional[Dict[str, Any]]) -> str:
    if not entry:
        return "#808080"
    tier = entry.get("tier", "").upper()
    return TIER_COLORS.get(tier, "#FFFFFF")


def _win_rate(entry: Optional[Dict[str, Any]]) -> str:
    if not entry:
        return ""
    wins = entry.get("wins", 0)
    losses = entry.get("losses", 0)
    total = wins + losses
    if total == 0:
        return "0 games"
    wr = (wins / total) * 100
    return f"{wins}W {losses}L ({wr:.0f}%)"


# ── Data Fetching ────────────────────────────────────────────────────────────

async def fetch_live_game_data(
    api_key: str,
    game_name: str,
    tag_line: str,
    region: str,
    *,
    client: RiotClient | None = None,
) -> Dict[str, Any]:
    riot_id = f"{game_name}#{tag_line}"
    platform_route = PlatformRoute(region.lower())
    async with AsyncExitStack() as stack:
        if client is None:
            client = await stack.enter_async_context(
                RiotClient(api_key=api_key, default_route=platform_route)
            )
        try:
            game = await client.lol.live_game(riot_id, route=platform_route)
        except NotFoundError as exc:
            if exc.response is None or "/lol/spectator/" not in exc.response.request.url.path:
                raise
            return {"error": "not_in_game", "player": riot_id}

        participants = getattr(game, "participants", None) or []

        async def resolve_participant(p: Any) -> Dict[str, Any]:
            champion_id = getattr(p, "champion_id", 0)
            puuid = getattr(p, "puuid", "")
            warnings = []
            try:
                champ_data = await client.lol.static.get_champion(champion_id)
            except Exception:
                champ_data = None
                warnings.append(f"Champion data unavailable for champion {champion_id}.")
            champ_name = champ_data["name"] if champ_data else f"Champion {champion_id}"
            champ_image = champ_data.get("image", {}).get("full", "") if champ_data else ""
            rank_entry = None
            rank_available = bool(puuid) and not getattr(p, "bot", False)
            if rank_available:
                try:
                    entries = await client.raw.lol.league.get_league_entries_by_puuid(
                        encrypted_puuid=puuid, route=platform_route
                    )
                    for e in entries:
                        qt = getattr(e, "queue_type", None)
                        if qt == "RANKED_SOLO_5x5":
                            rank_entry = e
                            break
                    if not rank_entry:
                        for e in entries:
                            qt = getattr(e, "queue_type", None)
                            if qt == "RANKED_FLEX_SR":
                                rank_entry = e
                                break
                except Exception:
                    rank_available = False
                    player = getattr(p, "riot_id", None) or champ_name
                    warnings.append(f"Rank unavailable for {player}.")

            rank_dict = None
            if rank_entry:
                if hasattr(rank_entry, "model_dump"):
                    rank_dict = rank_entry.model_dump()
                elif isinstance(rank_entry, dict):
                    rank_dict = rank_entry

            return {
                "champion": champ_name,
                "champion_image": champ_image,
                "champion_id": champion_id,
                "riot_id": getattr(p, "riot_id", None) or "Unknown",
                "puuid": puuid,
                "team_id": getattr(p, "team_id", 0),
                "spell1": _spell_name(getattr(p, "spell1_id", 0)),
                "spell2": _spell_name(getattr(p, "spell2_id", 0)),
                "is_bot": getattr(p, "bot", False),
                "rank": rank_dict,
                "rank_available": rank_available,
                "warnings": warnings,
            }

        player_data = await asyncio.gather(
            *[resolve_participant(p) for p in participants],
        )
        warnings = [warning for p in player_data for warning in p["warnings"]]
        blue_team = [p for p in player_data if p["team_id"] == 100]
        red_team = [p for p in player_data if p["team_id"] == 200]

        bans_raw = getattr(game, "banned_champions", []) or []
        bans = []
        for b in bans_raw:
            cid = getattr(b, "champion_id", -1)
            if cid > 0:
                try:
                    cd = await client.lol.static.get_champion(cid)
                except Exception:
                    cd = None
                    warnings.append(f"Ban data unavailable for champion {cid}.")
                bans.append(cd["name"] if cd else f"#{cid}")

        game_length = getattr(game, "game_length", 0) or 0
        queue_id = getattr(game, "game_queue_config_id", 0) or 0
        game_mode = getattr(game, "game_mode", "CLASSIC")

        return {
            "error": None,
            "player": riot_id,
            "game_mode": game_mode,
            "queue": _queue_name(queue_id),
            "queue_id": queue_id,
            "game_length": game_length,
            "blue_team": blue_team,
            "red_team": red_team,
            "bans": bans,
            "game_id": getattr(game, "game_id", "?"),
            "platform_id": getattr(game, "platform_id", region.upper()),
            "warnings": warnings,
        }


# ── TUI Widgets ──────────────────────────────────────────────────────────────

class GameHeader(Static):
    """Displays game info header (mode, duration, etc.)."""

    def render_header(self, data: Dict[str, Any]) -> Table:
        grid = Table.grid(padding=(0, 2))
        grid.add_column(justify="center")
        grid.add_column(justify="center")
        grid.add_column(justify="center")

        queue = data.get("queue", "Unknown")
        duration = _format_duration(data.get("game_length", 0))
        game_id = data.get("game_id", "?")
        platform = data.get("platform_id", "?")

        grid.add_row(
            Text(f"⏱  {duration}", style="bold white"),
            Text(f"🎮  {queue}", style="bold cyan"),
            Text(f"📍  {platform}", style="dim"),
        )

        return grid


class TeamTable(Static):
    """Renders a team as a Rich table."""

    def build_table(
        self, team_name: str, players: List[Dict[str, Any]], color: str
    ) -> Table:
        table = Table(
            title=f"  {team_name}",
            title_style=f"bold {color}",
            border_style=color,
            expand=True,
            show_edge=True,
            pad_edge=True,
        )

        table.add_column("Champion", style="bold white", min_width=14)
        table.add_column("Player", style="white", min_width=18)
        table.add_column("Rank", min_width=20)
        table.add_column("Win Rate", min_width=16)
        table.add_column("Spells", style="yellow", min_width=14)

        for p in players:
            rank_text = Text(
                _rank_string(p.get("rank")) if p.get("rank_available", True) else "Unavailable",
                style=_rank_color(p.get("rank")),
            )

            wr_text = _win_rate(p.get("rank"))
            wr_style = ""
            if wr_text:
                # Color win rate
                try:
                    pct = float(wr_text.split("(")[1].rstrip("%)"))
                    if pct >= 55:
                        wr_style = "green"
                    elif pct <= 45:
                        wr_style = "red"
                    else:
                        wr_style = "white"
                except (IndexError, ValueError):
                    wr_style = "white"

            spells = f"{p['spell1']} / {p['spell2']}"
            bot_tag = " 🤖" if p.get("is_bot") else ""

            table.add_row(
                Text(p["champion"], style="bold"),
                Text(f"{p['riot_id']}{bot_tag}"),
                rank_text,
                Text(wr_text, style=wr_style),
                spells,
            )

        return table


class BansWidget(Static):
    """Displays banned champions."""

    def build_bans(self, bans: List[str]) -> Text:
        if not bans:
            return Text("No bans", style="dim")
        text = Text("🚫 Bans: ", style="bold red")
        for i, ban in enumerate(bans):
            text.append(ban, style="white")
            if i < len(bans) - 1:
                text.append(" · ", style="dim")
        return text


class NotInGameWidget(Static):
    """Shown when the player is not currently in a game."""
    pass


class ErrorWidget(Static):
    """Shown when an error occurs."""
    pass


class LiveGameContent(Static):
    """Main content area that composes the game display."""
    pass


# ── Main TUI App ─────────────────────────────────────────────────────────────

LIVE_GAME_CSS = """
Screen {
    background: $surface;
}

#main-container {
    width: 100%;
    height: 100%;
    padding: 1 2;
}

#loading-container {
    width: 100%;
    height: 100%;
    align: center middle;
    content-align: center middle;
}

#loading-label {
    text-align: center;
    width: 100%;
    margin-bottom: 1;
    color: $text;
}

#game-header {
    width: 100%;
    height: auto;
    content-align: center middle;
    margin-bottom: 1;
    padding: 1;
    border: solid $primary;
}

#team-blue {
    width: 100%;
    height: auto;
    margin-bottom: 1;
}

#team-red {
    width: 100%;
    height: auto;
    margin-bottom: 1;
}

#bans-widget {
    width: 100%;
    height: auto;
    padding: 0 1;
    margin-bottom: 1;
    content-align: center middle;
    text-align: center;
}

#warnings-widget {
    width: 100%;
    height: auto;
    color: $warning;
    margin-bottom: 1;
}

#status-bar {
    dock: bottom;
    width: 100%;
    height: 1;
    background: $primary-background;
    color: $text;
    padding: 0 2;
}

#not-in-game {
    width: 100%;
    height: 100%;
    align: center middle;
    content-align: center middle;
    padding: 4;
}

#error-widget {
    width: 100%;
    height: 100%;
    align: center middle;
    content-align: center middle;
    padding: 4;
}

.team-label {
    text-align: center;
    width: 100%;
    text-style: bold;
    margin-bottom: 0;
}
"""


class LiveGameApp(App):
    """TUI application for viewing live League of Legends matches."""

    CSS = LIVE_GAME_CSS

    TITLE = "RiotSkillIssue — Live Game"
    SUB_TITLE = "League of Legends"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("escape", "quit", "Quit", show=False),
        Binding("r", "refresh", "Refresh", show=True),
    ]

    game_data: reactive[Optional[Dict[str, Any]]] = reactive(None)
    is_loading: reactive[bool] = reactive(True)
    last_error: reactive[Optional[str]] = reactive(None)
    refresh_countdown: reactive[int] = reactive(30)

    def __init__(
        self,
        api_key: str,
        game_name: str,
        tag_line: str,
        region: str = "euw1",
        auto_refresh: int = 30,
        **kwargs: Any,
    ):
        if auto_refresh < 5:
            raise ValueError("Auto-refresh interval must be at least 5 seconds.")
        super().__init__(**kwargs)
        self.api_key = api_key
        self.game_name = game_name
        self.tag_line = tag_line
        self.region = region
        self.auto_refresh_interval = auto_refresh
        self.refresh_countdown = auto_refresh
        self._countdown_timer: Optional[Timer] = None
        self._client: RiotClient | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="main-container")
        yield Static(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        self._load_data()
        self._countdown_timer = self.set_interval(1, self._tick_countdown)

    async def on_unmount(self) -> None:
        workers = self.workers.cancel_group(self, "live-game")
        await asyncio.gather(*(worker.wait() for worker in workers), return_exceptions=True)
        if self._client is not None:
            client, self._client = self._client, None
            await client.close()

    def _tick_countdown(self) -> None:
        if self.is_loading:
            return
        if self.refresh_countdown > 0:
            self.refresh_countdown -= 1
        if self.refresh_countdown == 0:
            self.action_refresh()

    def action_refresh(self) -> None:
        if self.is_loading:
            return
        self.is_loading = True
        self._load_data()

    def watch_refresh_countdown(self) -> None:
        self._update_status()

    def _update_status(self) -> None:
        if not self.is_running:
            return
        status = Text()
        if self.last_error and self.game_data is not None:
            status.append("Showing previous data  •  ", style="bold yellow")
        if self.is_loading:
            status.append("Refreshing game data…", style="dim")
        else:
            status.append(f"Next refresh in {self.refresh_countdown}s  •  [R] refresh  [Q] quit")
        if self.last_error and self.game_data is not None:
            status.append(f"  •  {self.last_error}", style="yellow")
        for widget in self.query("#status-bar").results(Static):
            widget.update(status)

    @work(exclusive=True, group="live-game")
    async def _load_data(self) -> None:
        self.is_loading = True
        self._update_status()
        try:
            if self.game_data is None:
                container = self.query_one("#main-container")
                await container.remove_children()
                await container.mount(
                    Vertical(
                        Label("🔄 Fetching live game data...", id="loading-label"),
                        LoadingIndicator(),
                        id="loading-container",
                    )
                )
            if self._client is None:
                self._client = RiotClient(
                    api_key=self.api_key,
                    default_route=PlatformRoute(self.region.lower()),
                )
            data = await fetch_live_game_data(
                api_key=self.api_key,
                game_name=self.game_name,
                tag_line=self.tag_line,
                region=self.region,
                client=self._client,
            )
            self.game_data = data
            self.last_error = None
            await self._render_game(data)
        except Exception as e:
            self.last_error = str(e)
            if self.api_key:
                self.last_error = self.last_error.replace(self.api_key, "[REDACTED]")
            if self.game_data is None:
                await self._render_error(self.last_error)
        finally:
            self.is_loading = False
            self.refresh_countdown = self.auto_refresh_interval
            self._update_status()

    async def _render_game(self, data: Dict[str, Any]) -> None:
        """Render the game data into the TUI."""
        container = self.query_one("#main-container")
        await container.remove_children()

        # Not in game
        if data.get("error") == "not_in_game":
            player = data.get("player", "?")
            widget = NotInGameWidget(id="not-in-game")
            widget.update(
                Panel(
                    Align.center(
                        Group(
                            Text(f"\n🎮  {player}", style="bold white", justify="center"),
                            Text(""),
                            Text(
                                "Not currently in a game.",
                                style="bold yellow",
                                justify="center",
                            ),
                            Text(""),
                            Text(
                                "The TUI will auto-refresh and show the game once it starts.",
                                style="dim",
                                justify="center",
                            ),
                        )
                    ),
                    title="Live Game",
                    border_style="yellow",
                    padding=(2, 4),
                )
            )
            await container.mount(widget)
            return

        # ── Game Header ──
        header = GameHeader(id="game-header")

        header_table = header.render_header(data)
        game_title = Text(
            f"🎮  LIVE GAME  —  {data['queue']}",
            style="bold cyan",
            justify="center",
        )
        header.update(
            Panel(
                Align.center(Group(game_title, Text(""), header_table)),
                border_style="cyan",
                padding=(0, 2),
            )
        )
        await container.mount(header)
        if data.get("warnings"):
            await container.mount(
                Static(Text("\n".join(data["warnings"])), id="warnings-widget")
            )

        # ── Blue Team ──
        blue_widget = TeamTable(id="team-blue")
        blue_table = blue_widget.build_table(
            "🔵  BLUE TEAM", data.get("blue_team", []), "#3498DB"
        )
        blue_widget.update(blue_table)
        await container.mount(blue_widget)

        # ── Bans ──
        bans_widget = BansWidget(id="bans-widget")
        bans_text = bans_widget.build_bans(data.get("bans", []))
        bans_widget.update(bans_text)
        await container.mount(bans_widget)

        # ── Red Team ──
        red_widget = TeamTable(id="team-red")
        red_table = red_widget.build_table(
            "🔴  RED TEAM", data.get("red_team", []), "#E74C3C"
        )
        red_widget.update(red_table)
        await container.mount(red_widget)

    async def _render_error(self, error: str) -> None:
        """Render an error message."""
        container = self.query_one("#main-container")
        await container.remove_children()

        widget = ErrorWidget(id="error-widget")
        widget.update(
            Panel(
                Align.center(
                    Group(
                        Text("❌  Error", style="bold red", justify="center"),
                        Text(""),
                        Text(str(error), style="white", justify="center"),
                        Text(""),
                        Text(
                            "Press [R] to retry  •  Press [Q] to quit",
                            style="dim italic",
                            justify="center",
                        ),
                    )
                ),
                title="Error",
                border_style="red",
                padding=(2, 4),
            )
        )
        await container.mount(widget)


def run_tui(
    api_key: str,
    game_name: str,
    tag_line: str,
    region: str = "euw1",
    auto_refresh: int = 30,
) -> None:
    """
    Launch the Live Game TUI.

    Args:
        api_key: Riot API key.
        game_name: Player's game name (e.g. "Agurin").
        tag_line: Player's tag line (e.g. "EUW").
        region: Regional server (e.g. "euw1", "na1").
        auto_refresh: Auto-refresh interval in seconds (default: 30).
    """
    app = LiveGameApp(
        api_key=api_key,
        game_name=game_name,
        tag_line=tag_line,
        region=region,
        auto_refresh=auto_refresh,
    )
    app.run()

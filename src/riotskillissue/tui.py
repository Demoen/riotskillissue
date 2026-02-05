"""
Live Game TUI — Terminal User Interface for spectating League of Legends matches.

Usage:
    riotskillissue-cli live "GameName#TagLine" --region euw1
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional, Tuple

from textual.app import App, ComposeResult
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

from .core.client import RiotClient, RiotClientConfig
from .core.types import Region, Platform, REGION_TO_PLATFORM


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
    lp = entry.get("leaguePoints", 0)
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
) -> Dict[str, Any]:
    """
    Fetch all data needed for the live game TUI.
    Returns a dict with game info, player data, champion names, and ranks.
    """
    region_lower = region.lower()

    # Map region to platform cluster for account API
    try:
        region_enum = Region(region_lower)
        platform = REGION_TO_PLATFORM[region_enum]
        cluster = platform.value
    except (ValueError, KeyError):
        cluster = "americas"

    config = RiotClientConfig(api_key=api_key)
    async with RiotClient(config=config) as client:
        # 1) Resolve Riot ID → PUUID
        account = await client.account.get_by_riot_id(
            region=cluster, gameName=game_name, tagLine=tag_line
        )
        puuid = account.puuid

        # 2) Get live game
        try:
            game = await client.spectator.get_current_game_info_by_puuid(
                region=region_lower, encryptedPUUID=puuid
            )
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower() or "Data not found" in error_msg:
                return {"error": "not_in_game", "player": f"{game_name}#{tag_line}"}
            raise

        # 3) Resolve champion data & ranks for all participants concurrently
        participants = game.participants or []

        async def resolve_participant(p: Any) -> Dict[str, Any]:
            """Resolve champion name and rank for a single participant."""
            champ_data = await client.static.get_champion(p.championId)
            champ_name = champ_data["name"] if champ_data else f"Champion {p.championId}"
            champ_image = champ_data.get("image", {}).get("full", "") if champ_data else ""

            # Get rank
            rank_entry = None
            try:
                entries = await client.league.get_league_entries_by_puuid(
                    region=region_lower, encryptedPUUID=p.puuid
                )
                # Find Solo/Duo rank first, then Flex
                for e in entries:
                    qt = getattr(e, "queueType", None) or e.get("queueType", "")
                    if qt == "RANKED_SOLO_5x5":
                        rank_entry = e
                        break
                if not rank_entry:
                    for e in entries:
                        qt = getattr(e, "queueType", None) or e.get("queueType", "")
                        if qt == "RANKED_FLEX_SR":
                            rank_entry = e
                            break
            except Exception:
                pass

            # Convert model to dict if needed
            rank_dict = None
            if rank_entry:
                if hasattr(rank_entry, "model_dump"):
                    rank_dict = rank_entry.model_dump()
                elif hasattr(rank_entry, "__dict__"):
                    rank_dict = vars(rank_entry)
                elif isinstance(rank_entry, dict):
                    rank_dict = rank_entry

            riot_id = getattr(p, "riotId", None) or "Unknown"

            return {
                "champion": champ_name,
                "champion_image": champ_image,
                "champion_id": p.championId,
                "riot_id": riot_id,
                "puuid": p.puuid,
                "team_id": p.teamId,
                "spell1": _spell_name(p.spell1Id),
                "spell2": _spell_name(p.spell2Id),
                "is_bot": getattr(p, "bot", False),
                "rank": rank_dict,
            }

        # Fetch all participant data concurrently
        player_data = await asyncio.gather(
            *[resolve_participant(p) for p in participants],
            return_exceptions=True,
        )

        # Filter out any exceptions
        resolved_players: List[Dict[str, Any]] = []
        for pd in player_data:
            if isinstance(pd, Exception):
                resolved_players.append({
                    "champion": "Unknown",
                    "champion_image": "",
                    "champion_id": 0,
                    "riot_id": "Error",
                    "puuid": "",
                    "team_id": 0,
                    "spell1": "?",
                    "spell2": "?",
                    "is_bot": False,
                    "rank": None,
                })
            else:
                resolved_players.append(pd)

        # Split teams
        blue_team = [p for p in resolved_players if p["team_id"] == 100]
        red_team = [p for p in resolved_players if p["team_id"] == 200]

        # Banned champions
        bans_raw = getattr(game, "bannedChampions", []) or []
        bans = []
        for b in bans_raw:
            cid = getattr(b, "championId", -1)
            if cid > 0:
                cd = await client.static.get_champion(cid)
                bans.append(cd["name"] if cd else f"#{cid}")

        game_length = getattr(game, "gameLength", 0) or 0
        queue_id = getattr(game, "gameQueueConfigId", 0) or 0
        game_mode = getattr(game, "gameMode", "CLASSIC")

        return {
            "error": None,
            "player": f"{game_name}#{tag_line}",
            "game_mode": game_mode,
            "queue": _queue_name(queue_id),
            "queue_id": queue_id,
            "game_length": game_length,
            "blue_team": blue_team,
            "red_team": red_team,
            "bans": bans,
            "game_id": getattr(game, "gameId", "?"),
            "platform_id": getattr(game, "platformId", region_lower.upper()),
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
                _rank_string(p.get("rank")),
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

    CSS = LIVE_GAME_CSS. \
        replace("    ", "    ")  # keep as-is

    TITLE = "RiotSkillIssue — Live Game"
    SUB_TITLE = "League of Legends"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("escape", "quit", "Quit", show=False),
        Binding("r", "refresh", "Refresh", show=True),
    ]

    # Reactive data
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
        super().__init__(**kwargs)
        self.api_key = api_key
        self.game_name = game_name
        self.tag_line = tag_line
        self.region = region
        self.auto_refresh_interval = auto_refresh
        self.refresh_countdown = auto_refresh
        self._refresh_timer: Optional[Timer] = None
        self._countdown_timer: Optional[Timer] = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(id="main-container")
        yield Footer()

    async def on_mount(self) -> None:
        """Called when the app is mounted — start first data fetch."""
        await self._load_data()
        # Start auto-refresh
        self._refresh_timer = self.set_interval(
            self.auto_refresh_interval, self._auto_refresh
        )
        self._countdown_timer = self.set_interval(1, self._tick_countdown)

    async def _auto_refresh(self) -> None:
        """Auto-refresh callback."""
        self.refresh_countdown = self.auto_refresh_interval
        await self._load_data()

    def _tick_countdown(self) -> None:
        """Count down the refresh timer."""
        if self.refresh_countdown > 0:
            self.refresh_countdown -= 1

    async def action_refresh(self) -> None:
        """Manual refresh triggered by 'r' key."""
        self.refresh_countdown = self.auto_refresh_interval
        await self._load_data()

    async def _load_data(self) -> None:
        """Fetch live game data and update the display."""
        self.is_loading = True
        self.last_error = None

        container = self.query_one("#main-container")

        # Show loading state
        await container.remove_children()
        await container.mount(
            Vertical(
                Label("🔄 Fetching live game data...", id="loading-label"),
                LoadingIndicator(),
                id="loading-container",
            )
        )

        try:
            data = await fetch_live_game_data(
                api_key=self.api_key,
                game_name=self.game_name,
                tag_line=self.tag_line,
                region=self.region,
            )
            self.game_data = data
            self.is_loading = False
            await self._render_game(data)
        except Exception as e:
            self.is_loading = False
            self.last_error = str(e)
            await self._render_error(str(e))

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
                            Text(
                                f"Next refresh in {self.refresh_countdown}s  •  Press [R] to refresh now",
                                style="dim italic",
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
        countdown_text = Text(
            f"Auto-refresh in {self.refresh_countdown}s",
            style="dim italic",
            justify="center",
        )
        header.update(
            Panel(
                Align.center(Group(game_title, Text(""), header_table, countdown_text)),
                border_style="cyan",
                padding=(0, 2),
            )
        )
        await container.mount(header)

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

# Live Game TUI

RiotSkillIssue includes a built-in **Terminal User Interface** (TUI) for spectating live League of Legends matches directly from your terminal. One command gives you a full dashboard with teams, champions, ranks, and more.

## Quick Start

```bash
riotskillissue-cli live "Agurin#EUW" --route euw1
```

That's it. This single command opens an interactive, auto-refreshing dashboard.

## What You See

### When a Game is Active

The TUI displays a full-screen dashboard with:

![Live Game TUI](live_game_tui.gif)

### When Not in a Game

If the player isn't currently in a match, the TUI shows a waiting screen and keeps checking:

![Waiting Screen](live_game_tui_not_found.gif)

## Features

- **Real-time game data** — see the current match as it happens
- **Both teams at a glance** — champions, summoner spells, ranks, win rates
- **Auto-refresh** — data updates every 30 seconds (configurable)
- **Rank colors** — each player's rank is color-coded (Iron → Challenger)
- **Win rate highlighting** — green for >55%, red for <45%
- **Ban display** — all banned champions listed
- **Waiting mode** — if the player isn't in a game, the TUI waits and checks periodically
- **Resilient refreshes** — keep the previous dashboard visible when a refresh fails, with a visible stale-data notice
- **Partial-data diagnostics** — retain players when champion or ranked lookups fail and show which enrichment is unavailable
- **Keyboard controls** — refresh manually or quit with a single keypress

The status bar counts down to the next refresh. Refreshes run in the background, so quitting remains responsive during slow requests. Repeated refresh keypresses share the active fetch; the next interval starts after it finishes.

The dashboard keeps one Riot client open for its lifetime, preserving learned rate limits, pooled connections, and cached Data Dragon content between refreshes. Quitting cancels the current fetch before closing that client.

## Installation

The TUI requires the `tui` optional extra:

```bash
pip install "riotskillissue[tui]"
```

!!! note "Dependencies"
    The TUI uses [Textual](https://textual.textualize.io/) and [Rich](https://rich.readthedocs.io/), 
    which are installed when you include the `[tui]` extra.

## Usage

### Basic

```bash
export RIOT_API_KEY="RGAPI-your-key-here"
riotskillissue-cli live "GameName#TagLine"
```

### With Options

```bash
riotskillissue-cli live "Faker#KR1" --route kr --refresh 15
```

### All Options

| Option | Default | Description |
|--------|---------|-------------|
| `name` | *(required)* | Riot ID in `GameName#TagLine` format |
| `--route` | `euw1` | LoL platform route (`euw1`, `na1`, `kr`, `eun1`, etc.) |
| `--api-key` | `$RIOT_API_KEY` | Riot API key |
| `--refresh` | `30` | Seconds between completed fetch and the next refresh (minimum 5) |

### Regions

All standard League of Legends regions are supported:

| Region | Code |
|--------|------|
| North America | `na1` |
| Europe West | `euw1` |
| Europe Nordic & East | `eun1` |
| Korea | `kr` |
| Japan | `jp1` |
| Brazil | `br1` |
| Latin America North | `la1` |
| Latin America South | `la2` |
| Oceania | `oc1` |
| Turkey | `tr1` |
| Russia | `ru` |
| Philippines | `ph2` |
| Singapore | `sg2` |
| Thailand | `th2` |
| Taiwan | `tw2` |
| Vietnam | `vn2` |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| ++r++ | Refresh game data immediately |
| ++q++ | Quit the TUI |
| ++escape++ | Quit the TUI |

## Rank Colors

Each player's rank is displayed with a color matching their tier:

| Tier | Color |
|------|-------|
| Iron | Gray |
| Bronze | Bronze |
| Silver | Silver |
| Gold | Gold |
| Platinum | Teal |
| Emerald | Green |
| Diamond | Light Blue |
| Master | Purple |
| Grandmaster | Red |
| Challenger | Orange |

## Programmatic Usage

You can also launch the TUI from Python code:

```python
from riotskillissue.tui import run_tui

run_tui(
    api_key="RGAPI-your-key",
    game_name="Agurin",
    tag_line="EUW",
    region="euw1",
    auto_refresh=30,
)
```

Or use the lower-level app class for more control:

```python
from riotskillissue.tui import LiveGameApp

app = LiveGameApp(
    api_key="RGAPI-your-key",
    game_name="Agurin",
    tag_line="EUW",
    region="euw1",
    auto_refresh=15,
)
app.run()
```

`fetch_live_game_data` also accepts an optional `client=` argument for repeated programmatic fetches. That caller owns the supplied client's credentials and lifecycle; `region` still selects the lookup route. Without `client=`, each call creates and closes its own client.

## API Key

The TUI requires a valid Riot API key. You can get one from the [Riot Developer Portal](https://developer.riotgames.com/).

Set it as an environment variable for convenience:

=== "Linux / macOS"

    ```bash
    export RIOT_API_KEY="RGAPI-your-key-here"
    ```

=== "Windows (PowerShell)"

    ```powershell
    $env:RIOT_API_KEY = "RGAPI-your-key-here"
    ```

=== "Windows (CMD)"

    ```cmd
    set RIOT_API_KEY=RGAPI-your-key-here
    ```

!!! tip "Development Keys"
    Riot development API keys expire every 24 hours. For persistent usage, 
    apply for a personal or production key through the Developer Portal.

## Troubleshooting

### "Not currently in a game"

The player must be in an **active** League of Legends match (loading screen or in-game). 
Champion select does not count — the Spectator API only reports data once the game has started.

### "404 - Data not found"

- Double-check the Riot ID spelling and tag line
- Make sure you're using the correct `--route` for the player's server
- Verify your API key is valid and not expired

A missing Riot account produces an error. Only a missing active spectator game enters the waiting screen.

### Partial or previous data

Champion metadata outages leave champion IDs visible and preserve each player's team. Failed ranked lookups display **Unavailable**; a successful lookup with no ranked entries displays **Unranked**. Anonymous players and bots do not trigger ranked requests.

If a refresh fails after a successful fetch, the dashboard retains that snapshot and the status bar displays **Showing previous data** until a refresh succeeds. The displayed game duration then belongs to the retained snapshot.

### Rate Limiting

The TUI makes multiple API calls per refresh, including account resolution, spectator data, and ranks for eligible players. Request usage also depends on retries and other applications sharing your key. The default refresh interval is 30 seconds; longer intervals reduce API usage.

# Live Game TUI

Follow an active League of Legends game in your terminal. The dashboard combines spectator data with champion metadata and ranked records, and keeps checking when the player is between games.

## Installation

Install the optional `tui` extra in your Python environment:

```bash
pip install "riotskillissue[tui]"
```

This includes the Textual interface; Rich and the CLI are included in the base package. See [getting started](getting-started.md) for Python requirements.

## API Key

Create a key in the [Riot Developer Portal](https://developer.riotgames.com/) and set it in your current terminal:

=== "macOS / Linux"

    ```bash
    export RIOT_API_KEY="RGAPI-your-key-here"
    ```

=== "Windows PowerShell"

    ```powershell
    $env:RIOT_API_KEY = "RGAPI-your-key-here"
    ```

=== "Windows CMD"

    ```cmd
    set RIOT_API_KEY=RGAPI-your-key-here
    ```

## Quick Start

Use the player's exact Riot ID and their platform route:

```bash
riotskillissue-cli live "GameName#TagLine" --route euw1
```

Press `r` to refresh, or `q` / `Esc` to quit. The default refresh interval is 30 seconds.

!!! note "Active games only"
    The dashboard uses Riot's spectator API. Champion select does not provide an active game, and live data is less complete than a post-game match result.

## What You See

### When a Game is Active

![Live-game dashboard showing blue and red teams, champions, ranks, and bans](live_game_tui.gif)

| Area | Contents |
| --- | --- |
| Game | Queue, duration, and platform |
| Teams | Player names, champions, summoner spells, ranks, and ranked win rates |
| Bans | Banned champions |
| Status | Refresh countdown, fetch progress, and data-quality warnings |

### When Not in a Game

The waiting screen continues checking for an active game on the same refresh schedule. A missing Riot account is an error; only a missing active spectator game enters this state.

??? example "Preview the waiting screen"
    ![Waiting screen while the player is not in an active game](live_game_tui_not_found.gif)

## Usage

### Basic

```bash
riotskillissue-cli live "GameName#TagLine" --route euw1
```

### With Options

Use a different platform or refresh interval:

```bash
riotskillissue-cli live "GameName#TagLine" --route kr --refresh 15
```

### All Options

| Argument or option | Default | Meaning |
| --- | --- | --- |
| `riot_id` | Required | Exact `GameName#TagLine` Riot ID |
| `--route` | `euw1` | LoL platform route, such as `na1`, `kr`, or `eun1` |
| `--api-key` | `RIOT_API_KEY` | Riot API key |
| `--refresh` | `30` | Seconds between a completed fetch and the next refresh; minimum `5` |

### Regions

Use a platform route for the player's server: for example, `euw1` for Europe West, `na1` for North America, or `kr` for Korea. A regional cluster such as `europe` is not a platform route. See [routing](routing.md) for route families and inference.

## Keyboard Shortcuts

| Key | Action |
| --- | --- |
| `r` | Refresh immediately |
| `q` | Quit |
| `Esc` | Quit |

## Features

Refreshes run in the background, so the interface remains responsive during slow requests. Repeated refresh keypresses share the active fetch; the countdown starts again after that fetch finishes.

The dashboard keeps a Riot client open until you quit, preserving pooled connections, learned rate limits, and cached Data Dragon content. Quitting cancels any active fetch and closes the client.

!!! info "Missing data stays visible"
    A failed refresh keeps the last successful dashboard and shows **Showing previous data**. Partial lookup failures keep affected players visible and identify unavailable enrichment. See [partial or previous data](#partial-or-previous-data) for how to interpret those states.

## Rank Colors

Ranks use tier colors. Ranked win rates of 55% or higher appear green; those of 45% or lower appear red.

??? info "Tier color reference"

    | Tier | Color |
    | --- | --- |
    | Iron | Gray |
    | Bronze | Bronze |
    | Silver | Silver |
    | Gold | Gold |
    | Platinum | Teal |
    | Emerald | Green |
    | Diamond | Light blue |
    | Master | Purple |
    | Grandmaster | Red |
    | Challenger | Orange |

## Programmatic Usage

=== "Launch the dashboard"

    ```python
    import os

    from riotskillissue.tui import run_tui

    run_tui(
        api_key=os.environ["RIOT_API_KEY"],
        game_name="GameName",
        tag_line="TagLine",
        region="euw1",
        auto_refresh=30,
    )
    ```

=== "Create the app"

    ```python
    import os

    from riotskillissue.tui import LiveGameApp

    app = LiveGameApp(
        api_key=os.environ["RIOT_API_KEY"],
        game_name="GameName",
        tag_line="TagLine",
        region="euw1",
        auto_refresh=30,
    )
    app.run()
    ```

For repeated programmatic fetches, `fetch_live_game_data` accepts an optional `client=` argument. The caller owns that client's credentials and lifecycle; `region` still selects the lookup route. Without `client=`, each call creates and closes its own client.

## Troubleshooting

### "Not currently in a game"

The player needs an active game reported by Riot's spectator API. Champion select does not count. Leave the dashboard open to keep checking, or press `r` after the game starts.

### "404 - Data not found"

Verify the exact Riot ID and tag line, then check `--route` against the player's server. A missing account produces an error instead of entering the waiting screen. If the key is rejected, check or renew it in the Developer Portal.

### Partial or previous data

| Display | Meaning |
| --- | --- |
| Champion ID instead of a name | Champion metadata could not be loaded; the player's team is still preserved. |
| **Unavailable** rank | The ranked lookup failed. |
| **Unranked** | The lookup succeeded and returned no ranked entries. |
| **Showing previous data** | The latest refresh failed; the dashboard and game duration belong to the retained snapshot. |

Anonymous players and bots do not trigger ranked requests. A successful refresh clears the stale-data notice.

### Rate Limiting

Each refresh can make multiple requests for account resolution, spectator data, and eligible players' ranks. Retries and other applications using the same key also affect request usage. Increase `--refresh` above the 30-second default to reduce API usage.

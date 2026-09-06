# Command Line Interface

Look up a League player, inspect a match, or open the live-game dashboard from your terminal. The CLI prints a focused summary; use the [Python client](getting-started.md) or [MCP server](mcp.md) for richer results.

## Installation

=== "CLI"

    ```bash
    pip install riotskillissue
    ```

=== "CLI with live dashboard"

    ```bash
    pip install "riotskillissue[tui]"
    ```

See [getting started](getting-started.md) for supported Python versions.

## Configuration

Set `RIOT_API_KEY` in the terminal where you will run the command:

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

Every command also accepts `--api-key`. The environment variable keeps the key out of the command itself.

!!! tip "Choose the right route"
    `summoner` and `live` use a **platform route**, such as `euw1`. `match` uses a **regional route**, such as `europe`. See [routing](routing.md) for how the families relate.

## Commands

| Command | Result | Default route |
| --- | --- | --- |
| [`summoner`](#summoner) | Player level and PUUID | `euw1` |
| [`match`](#match) | Game mode and duration | `europe` |
| [`live`](#live) | Interactive live-game dashboard | `euw1` |

Run `riotskillissue-cli --help` to list commands, or append `--help` to a command to inspect its options.

### summoner

Look up a League player by their full Riot ID:

```bash
riotskillissue-cli summoner "GameName#TagLine" --route euw1
```

The result is a table containing the player's summoner level and PUUID.

| Argument or option | Default | Meaning |
| --- | --- | --- |
| `riot_id` | Required | Exact `GameName#TagLine` Riot ID |
| `--route` | `euw1` | LoL platform route |
| `--api-key` | `RIOT_API_KEY` | Riot API key |

### match

Load a completed match by its match ID:

```bash
riotskillissue-cli match "EUW1_7654321098" --route europe
```

The command prints the match ID, game mode, and duration in seconds. Supply the regional cluster that holds the match; the CLI does not infer it from the ID.

| Argument or option | Default | Meaning |
| --- | --- | --- |
| `match_id` | Required | Match ID, such as `EUW1_7654321098` |
| `--route` | `europe` | Regional route |
| `--api-key` | `RIOT_API_KEY` | Riot API key |

### live

Open the [Live Game TUI](live-game-tui.md) for a player:

```bash
riotskillissue-cli live "GameName#TagLine" --route euw1 --refresh 30
```

The dashboard shows teams, champions, summoner spells, ranked records, and bans. It waits and checks again when no active game is available.

| Argument or option | Default | Meaning |
| --- | --- | --- |
| `riot_id` | Required | Exact `GameName#TagLine` Riot ID |
| `--route` | `euw1` | LoL platform route |
| `--api-key` | `RIOT_API_KEY` | Riot API key |
| `--refresh` | `30` | Seconds after a completed fetch before the next refresh; minimum `5` |

Press `r` to refresh, or `q` / `Esc` to quit. The [`tui` extra](#installation) is required. See the [TUI guide](live-game-tui.md) for previews, controls, and refresh behavior.

## Error Handling

| Symptom | What to check |
| --- | --- |
| Command not found | Install the package in the active Python environment, then use that environment's terminal. |
| Invalid Riot ID | Include both parts and the separator: `"GameName#TagLine"`. |
| Missing or rejected API key | Set `RIOT_API_KEY` in this terminal and verify the key in the [Riot Developer Portal](https://developer.riotgames.com/). |
| Player or match not found | Check the identifier and the command's route family. |
| Live command cannot import Textual | Install `"riotskillissue[tui]"` in the same environment as the CLI. |
| Live dashboard shows previous or partial data | Read the status bar and the [TUI troubleshooting guide](live-game-tui.md#troubleshooting). |

To process results in your own application, start with the [Python client](getting-started.md) and [game examples](examples/index.md).

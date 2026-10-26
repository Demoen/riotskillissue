# Command Line Interface

Look up a League player, inspect a match, download an available replay, or open the live-game dashboard from your terminal. Use the [Python client](getting-started.md) or [MCP server](mcp.md) to process richer results.

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

For `summoner`, `match`, and `live`, set `RIOT_API_KEY` in the terminal where you will run the command:

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

These commands also accept `--api-key`. The environment variable keeps the key out of the command itself.

With `--player "GameName#TagLine"`, the `replays` commands connect to your running, logged-in League Client on Windows or macOS. No API key or RSO token is needed. Without `--player`, they use `RIOT_RSO_ACCESS_TOKEN` or `--access-token` from an approved Riot Sign On integration. See the [replay guide](replays.md) for both workflows.

!!! tip "Choose the right route"
    `summoner` and `live` use a **platform route**, such as `euw1`. `match` and RSO replay requests use a **regional route**, such as `europe`. Replay requests with `--player` use the League Client's current region. See [routing](routing.md) for how the families relate.

## Commands

| Command | Result | Default route |
| --- | --- | --- |
| [`summoner`](#summoner) | Player level and PUUID | `euw1` |
| [`match`](#match) | Game mode and duration | `europe` |
| [`live`](#live) | Interactive live-game dashboard | `euw1` |
| [`replays list`](#replays) | A player's recent matches or the RSO replay list | Client region with `--player`; otherwise `europe` |
| [`replays download`](#replays) | A selected replay saved to a local `.rofl` file | Client region with `--player`; otherwise `europe` |

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

### replays

Open League, sign in, and look up another player's recent matches by full Riot
ID:

```bash
riotskillissue-cli replays list --player "GameName#TagLine"
riotskillissue-cli replays download --player "GameName#TagLine"
```

`download` prompts for a one-based selection from the list it just fetched. To
select an entry directly and set the destination:

```bash
riotskillissue-cli replays download 1 --player "GameName#TagLine" --output ./replays/my-game.rofl
```

Player mode needs the League Client running on the same Windows or macOS
machine. It uses the client's replay folder by default; `--output` copies the
completed file elsewhere. Riot's download limit applies, including downloads
started through the client UI. Use `--lockfile` for a custom installation and
`--count` to show between 1 and 20 recent matches.

For the public API workflow, set `RIOT_RSO_ACCESS_TOKEN` and omit `--player`:

```bash
riotskillissue-cli replays list --route europe
riotskillissue-cli replays download --route europe
```

That endpoint returns replays for the token's player and has no player-name or
match-ID lookup. Neither workflow needs a Riot API key. Existing `--output`
files are preserved unless you pass `--overwrite`. See the [replay guide](replays.md)
for client requirements, RSO authentication, selection behavior, options, and
Python examples.

## Error Handling

| Symptom | What to check |
| --- | --- |
| Command not found | Install the package in the active Python environment, then use that environment's terminal. |
| Invalid Riot ID | Include both parts and the separator: `"GameName#TagLine"`. |
| Missing or rejected API key | Set `RIOT_API_KEY` in this terminal and verify the key in the [Riot Developer Portal](https://developer.riotgames.com/). |
| Player or match not found | Check the identifier and the command's route family. |
| Live command cannot import Textual | Install `"riotskillissue[tui]"` in the same environment as the CLI. |
| Live dashboard shows previous or partial data | Read the status bar and the [TUI troubleshooting guide](live-game-tui.md#troubleshooting). |
| Replay token, selection, or download error | Follow the [replay troubleshooting guide](replays.md#troubleshooting). |

To process results in your own application, start with the [Python client](getting-started.md) and [game examples](examples/index.md).

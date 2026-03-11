# Command Line Interface

RiotSkillIssue includes a CLI tool for quick lookups and debugging.

## Installation

The CLI is included with the package:

```bash
pip install riotskillissue
```

For enhanced output formatting, install with dev dependencies:

```bash
pip install "riotskillissue[dev]"
```

## Configuration

Set your API key via environment variable:

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

Or pass it directly with `--api-key`:

```bash
riotskillissue-cli summoner "Player#EUW" --api-key "RGAPI-..."
```

## Commands

### summoner

Look up a summoner by Riot ID.

```bash
riotskillissue-cli summoner "GameName#TagLine" --region euw1
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `name` | Riot ID in format `GameName#TagLine` |
| `--region` | Regional server (default: `na1`) |
| `--api-key` | API key (or use `RIOT_API_KEY` env var) |

**Example:**

```bash
$ riotskillissue-cli summoner "Agurin#EUW" --region euw1

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     Summoner: Agurin#EUW         ┃
┣━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Level     │ PUUID                 ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ 523       │ abc123...             │
└───────────┴───────────────────────┘
```

### match

Get match details by match ID.

```bash
riotskillissue-cli match "EUW1_7654321098" --region europe
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `match_id` | Match ID (e.g., `EUW1_7654321098`) |
| `--region` | Platform routing (default: `americas`) |
| `--api-key` | API key (or use `RIOT_API_KEY` env var) |

**Example:**

```bash
$ riotskillissue-cli match "EUW1_7654321098" --region europe

Match EUW1_7654321098 loaded!
Game Mode: CLASSIC
Duration: 1847s
```

### live

🎮 Launch an interactive Live Game TUI (Terminal User Interface) that shows real-time information about an ongoing League of Legends match.

```bash
riotskillissue-cli live "GameName#TagLine" --region euw1
```

This is the fastest way to spectate a match from your terminal — **one command, instant dashboard**.

**Arguments:**

| Argument | Description |
|----------|-------------|
| `name` | Riot ID in format `GameName#TagLine` |
| `--region` | Regional server (default: `euw1`) |
| `--api-key` | API key (or use `RIOT_API_KEY` env var) |
| `--refresh` | Auto-refresh interval in seconds (default: `30`) |

**Example:**

```bash
$ riotskillissue-cli live "Agurin#EUW" --region euw1
```

This opens a full-screen terminal dashboard showing:

- **Game info** — queue type, game duration, platform
- **Blue Team** — champions, player names, ranks, win rates, summoner spells
- **Red Team** — champions, player names, ranks, win rates, summoner spells  
- **Bans** — all banned champions

The TUI auto-refreshes every 30 seconds (configurable with `--refresh`). If the player isn't in a game yet, it will keep checking until one starts.

**Keyboard shortcuts:**

| Key | Action |
|-----|--------|
| `R` | Manual refresh |
| `Q` / `Esc` | Quit |

See the [Live Game TUI](live-game-tui.md) page for more details and screenshots.

## Error Handling

The CLI displays user-friendly error messages:

```bash
$ riotskillissue-cli summoner "InvalidName"

Error: Name must be format GameName#TagLine for Account V1 lookup
```

```bash
$ riotskillissue-cli summoner "NonExistent#USER" --region euw1

Error: 404 - Data not found
```


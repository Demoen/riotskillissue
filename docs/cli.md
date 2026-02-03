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

```bash
export RIOT_API_KEY="RGAPI-your-key-here"
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

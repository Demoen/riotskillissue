# Examples

Working code examples demonstrating common usage patterns for the Riot Games API.

## Available Examples

<div class="grid cards" markdown>

-   **[League of Legends](league-of-legends.md)**

    ---

    Summoner lookups, match history, champion mastery, live game spectator

-   **[Teamfight Tactics](teamfight-tactics.md)**

    ---

    TFT summoner data, match history, ranked leaderboards

-   **[VALORANT](valorant.md)**

    ---

    Content data, platform status

</div>

## Running the Examples

All examples require:

1. A valid Riot API key set as `RIOT_API_KEY` environment variable
2. The `riotskillissue` package installed

```bash
# Set your API key
export RIOT_API_KEY="RGAPI-your-key-here"

# Run an example
python examples/basic_usage.py
```

## Included Example Scripts

The `/examples` directory in the repository contains runnable Python scripts:

| Script | Description |
|--------|-------------|
| `basic_usage.py` | Account lookup and summoner data |
| `match_history.py` | Fetching and processing match history |
| `champion_mastery.py` | Champion mastery rankings |

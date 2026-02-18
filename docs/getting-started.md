# Getting Started

This guide will walk you through installing riotskillissue and making your first API call.

## Prerequisites

- Python 3.8 or higher
- A Riot Games API key from [developer.riotgames.com](https://developer.riotgames.com/)

## Installation

Install the package from PyPI:

```bash
pip install riotskillissue
```

For development with testing tools:

```bash
pip install "riotskillissue[dev]"
```

## Configuration

### Option 1: Environment Variable (Recommended)

Set the `RIOT_API_KEY` environment variable:

=== "Windows (PowerShell)"

    ```powershell
    $env:RIOT_API_KEY = "RGAPI-your-key-here"
    ```

=== "Windows (CMD)"

    ```batch
    set RIOT_API_KEY=RGAPI-your-key-here
    ```

=== "Linux/macOS"

    ```bash
    export RIOT_API_KEY="RGAPI-your-key-here"
    ```

### Option 2: Direct Initialization

Pass the API key directly to the client:

```python
from riotskillissue import RiotClient

async with RiotClient(api_key="RGAPI-your-key-here") as client:
    # ...
```

## Your First API Call (Async)

Here's a complete example that looks up a player by their Riot ID:

```python
import asyncio
from riotskillissue import RiotClient, Platform, Region

async def main():
    async with RiotClient() as client:
        
        # Step 1: Look up account by Riot ID
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Player",
            tagLine="EUW"
        )
        print(f"Account: {account.gameName}#{account.tagLine}")
        print(f"PUUID: {account.puuid}")
        
        # Step 2: Get summoner data using the PUUID
        summoner = await client.summoner.get_by_puuid(
            region=Region.EUW1,
            encryptedPUUID=account.puuid
        )
        print(f"Summoner Level: {summoner.summonerLevel}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Your First API Call (Sync)

Don't need async? Use `SyncRiotClient` — it has the same API but works in plain synchronous code:

```python
from riotskillissue import SyncRiotClient, Platform, Region

with SyncRiotClient() as client:
    account = client.account.get_by_riot_id(
        region=Platform.EUROPE,
        gameName="Player",
        tagLine="EUW"
    )
    print(f"Account: {account.gameName}#{account.tagLine}")

    summoner = client.summoner.get_by_puuid(
        region=Region.EUW1,
        encryptedPUUID=account.puuid
    )
    print(f"Summoner Level: {summoner.summonerLevel}")
```

!!! tip "When to use which?"
    Use `RiotClient` (async) in web servers, bots, and high-throughput applications.
    Use `SyncRiotClient` for scripts, notebooks, CLI tools, and quick prototyping.

## Error Handling

v0.2.0 introduces typed exceptions so you can handle specific error conditions:

```python
from riotskillissue import RiotClient, NotFoundError, RateLimitError, RiotAPIError

async with RiotClient() as client:
    try:
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Nonexistent",
            tagLine="0000"
        )
    except NotFoundError:
        print("Player not found!")
    except RateLimitError as e:
        print(f"Rate limited — retry after {e.response.headers.get('Retry-After')}s")
    except RiotAPIError as e:
        print(f"API error [{e.status}]: {e.message}")
```

## Understanding Regions vs Platforms

The Riot API uses two types of routing:

| Type | Values | Used For |
|------|--------|----------|
| **Platform** | `AMERICAS`, `EUROPE`, `ASIA`, `SEA` | Account lookups, Match history |
| **Region** | `NA1`, `EUW1`, `KR`, `BR1`, etc. | Summoner data, Live game, Ranked |

```python
from riotskillissue import Region, Platform

# Platform for account/match APIs
account = await client.account.get_by_riot_id(
    region=Platform.AMERICAS,
    gameName="Player",
    tagLine="NA1"
)

# Region for summoner/ranked APIs  
summoner = await client.summoner.get_by_puuid(
    region=Region.NA1,
    encryptedPUUID=account.puuid
)
```

## Next Steps

- [Configuration Guide](configuration.md) - Redis caching, rate limiting, timeouts
- [Examples](examples/index.md) - Working code for common tasks
- [API Reference](api-reference.md) - Complete endpoint documentation

# RiotSkillIssue

<div align="center">

![riotskillissue](docs/assets/logo.png)


[![PyPI version](https://badge.fury.io/py/riotskillissue.svg)](https://badge.fury.io/py/riotskillissue)
[![Python Versions](https://img.shields.io/pypi/pyversions/riotskillissue.svg)](https://pypi.org/project/riotskillissue/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Tests](https://github.com/Demoen/riotskillissue/actions/workflows/test.yml/badge.svg)](https://github.com/Demoen/riotskillissue/actions/workflows/test.yml)

**Production-ready, auto-updating, and fully typed Python wrapper for the Riot Games API.**

[Documentation](https://demoen.github.io/riotskillissue/) · [Examples](https://demoen.github.io/riotskillissue/examples/) · [API Reference](https://demoen.github.io/riotskillissue/api-reference/)

</div>

---

## Features

| Feature | Description |
|---------|-------------|
| **Type-Safe** | 100% Pydantic models for all requests and responses |
| **Auto-Updated** | Generated daily from the Official OpenAPI Spec |
| **Sync & Async** | First-class async client and a synchronous `SyncRiotClient` for scripts & notebooks |
| **Resilient** | Automatic `Retry-After` handling, exponential backoff, and a rich error hierarchy |
| **Distributed** | Pluggable Redis support for shared rate limiting and caching |
| **Multi-Game** | Full support for LoL, TFT, LoR, and VALORANT APIs |

## Installation

Requires Python 3.8+.

```bash
pip install riotskillissue
```

## Quick Start (Async)

```python
import asyncio
from riotskillissue import RiotClient, Platform, Region

async def main():
    async with RiotClient() as client:
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Agurin",
            tagLine="EUW"
        )
        print(f"Found: {account.gameName}#{account.tagLine}")

        summoner = await client.summoner.get_by_puuid(
            region=Region.EUW1,
            encryptedPUUID=account.puuid
        )
        print(f"Level: {summoner.summonerLevel}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Quick Start (Sync)

```python
from riotskillissue import SyncRiotClient, Platform

with SyncRiotClient() as client:
    account = client.account.get_by_riot_id(
        region=Platform.EUROPE,
        gameName="Agurin",
        tagLine="EUW"
    )
    print(f"Found: {account.gameName}#{account.tagLine}")
```

Set your API key via environment variable:

```bash
export RIOT_API_KEY="RGAPI-your-key-here"
```

Or pass it directly:

```python
async with RiotClient(api_key="RGAPI-...") as client:
    ...
```

## Configuration

```python
from riotskillissue import RiotClient, RiotClientConfig
from riotskillissue.core.cache import RedisCache, MemoryCache

config = RiotClientConfig(
    api_key="RGAPI-...",
    max_retries=5,
    cache_ttl=120,
    redis_url="redis://localhost:6379/0",  # Distributed rate limiting
    proxy="http://127.0.0.1:8080",        # Optional HTTP proxy
    log_level="DEBUG",                     # DEBUG, INFO, WARNING
)

cache = MemoryCache(max_size=2048)  # LRU in-memory cache
# or: cache = RedisCache("redis://localhost:6379/1")

async with RiotClient(config=config, cache=cache) as client:
    ...
```

## Error Handling

```python
from riotskillissue import NotFoundError, RateLimitError, RiotAPIError

try:
    account = await client.account.get_by_riot_id(...)
except NotFoundError:
    print("Player not found")
except RiotAPIError as e:
    print(f"[{e.status}] {e.message}")
```

## Documentation

Full documentation is available at [demoen.github.io/riotskillissue](https://demoen.github.io/riotskillissue/).

- [Getting Started](https://demoen.github.io/riotskillissue/getting-started/)
- [Configuration](https://demoen.github.io/riotskillissue/configuration/)
- [Examples](https://demoen.github.io/riotskillissue/examples/)
- [API Reference](https://demoen.github.io/riotskillissue/api-reference/)
- [CLI](https://demoen.github.io/riotskillissue/cli/)

## Legal

RiotSkillIssue is not endorsed by Riot Games and does not reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

## License

MIT. See the [LICENSE](LICENSE) file for details.

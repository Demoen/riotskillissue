# RiotSkillIssue

<div align="center">

[![PyPI version](https://badge.fury.io/py/riotskillissue.svg)](https://badge.fury.io/py/riotskillissue)
[![Python Versions](https://img.shields.io/pypi/pyversions/riotskillissue.svg)](https://pypi.org/project/riotskillissue/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Tests](https://github.com/Demoen/riotskillissue/actions/workflows/test.yml/badge.svg)](https://github.com/Demoen/riotskillissue/actions/workflows/test.yml)

**The production-ready, auto-updating, and fully typed Python wrapper for the Riot Games API.**

[Features](#-features) • [Installation](#-installation) • [Quickstart](#-quickstart) • [Documentation](#-documentation) • [Contributing](docs/CONTRIBUTING.md)

</div>

---

## 🚀 Features

- **🛡️ Type-Safe**: 100% Pydantic models for all requests and responses. No more dictionary guessing.
- **🔄 Auto-Updated**: Generated weekly from the [Official OpenAPI Spec](https://github.com/MingweiSamuel/riotapi-schema). Supports LoL, TFT, LoR, and VALORANT.
- **⚡ Resilient by Design**: Built-in exponential backoff, circuit breakers, and correct `Retry-After` handling.
- **🌍 Distributed**: Pluggable **Redis** support for shared Rate Limiting and Caching across multiple processes.
- **🛠️ Developer Friendly**: Includes a powerful CLI, smart pagination helpers, and RSO (OAuth2) support.

## 📦 Installation

Requires **Python 3.8+**.

```bash
pip install riotskillissue
```

*Or install with extra dev dependencies:*
```bash
pip install "riotskillissue[dev]"
```

## ⚡ Quickstart

```python
import asyncio
from riotskillissue import RiotClient, Region

async def main():
    # 1. Initialize Client (Auto-loads RIOT_API_KEY from env)
    async with RiotClient() as client:
    
        # 2. Type-Safe API Calls
        summoner = await client.summoner.get_by_puuid(
             region=Region.NA1,
             encryptedPUUID="<YOUR_PUUID>"
        )
        print(f"Summoner Level: {summoner.summonerLevel}")
        
        # 3. Smart Pagination (Async Iterator)
        from riotskillissue import paginate
        async for match_id in paginate(client.match.get_ids_by_puuid, puuid=summoner.puuid, count=20):
             print(f"Match: {match_id}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🛠 Configuration

Define your configuration using `RiotClientConfig` or environment variables.

| Parameter | Environment Variable | Default | Description |
| :--- | :--- | :--- | :--- |
| **API Key** | `RIOT_API_KEY` | `None` | Your Riot Games API Key. |
| **Redis URL** | - | `None` | `redis://host:port` for distributed limits. |
| **Max Retries** | - | `3` | Retries for 5xx/Network errors. |
| **Timeout** | - | `5s`/`10s` | Connect/Read timeouts. |

```python
config = RiotClientConfig(
    api_key="RGAPI-...",
    redis_url="redis://localhost:6379/0", # Enables distributed rate limiting
    max_retries=5
)
async with RiotClient(config=config) as client:
    ...
```

## 🧠 Advanced Usage

### Caching
Reduce your API calls with built-in caching.

```python
from riotskillissue.core.cache import RedisCache

cache = RedisCache("redis://localhost:6379/1")
async with RiotClient(cache=cache) as client:
    # Requests are now cached!
    ...
```

### Data Dragon (Static Data)
Fetch champions, items, and versions without hassle.

```python
# Automatically picks the latest version and caches the result
annie = await client.static.get_champion(1)
print(annie["name"])  # "Annie"
```

### CLI Tool
Debug your API keys or look up players instantly from the terminal.

```bash
$ riotskillissue-cli summoner "Faker#SKT" --region kr
{
  "id": "...",
  "accountId": "...",
  "puuid": "...",
  "name": "Faker",
  "profileIconId": 6,
  "revisionDate": 1703894832000,
  "summonerLevel": 678
}
```

## ⚖️ Legal

`riotskillissue` isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.

## 📝 License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.
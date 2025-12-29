# Riot API Wrapper

Production-ready, auto-updating, and fully typed Python wrapper for the Riot Games API.

## 🚀 Features

- **100% Coverage**: Auto-generated from the [Official OpenAPI Spec](https://github.com/MingweiSamuel/riotapi-schema). Supports League of Legends, TFT, LoR, and VALORANT.
- **Type-Safe**: All requests and responses use **Pydantic** models. No more `KeyError` or dictionary guessing.
- **Resilient**: Built-in **Exponential Backoff**, **Circuit Breakers** (for 5xx), and **Rate Limiting** (Respects `Retry-After`).
- **Distributed Ready**: Pluggable **Redis Rate Limiting** (Lua Scripted) and **Caching**.
- **Developer Experience**: Includes **CLI**, **Smart Pagination**, **Data Dragon** helpers, and **Hooks**.

---

## 📦 Installation

This package requires **Python 3.8+**.

```bash
# Install from source
pip install -e .
```

---

## ⚡ Quickstart

```python
import asyncio
from riotskillissue import RiotClient, Region

async def main():
    # 1. Initialize Client (Auto-loads RIOT_API_KEY from env)
    async with RiotClient() as client:
    
        # 2. Call API (Type-hinted!)
        # Automatically converts "getByPUUID" -> "get_by_puuid"
        summoner = await client.summoner.get_by_puuid(
             region=Region.NA1,
             encryptedPUUID="<YOUR_PUUID>"
        )
        
        print(f"Level: {summoner.summonerLevel}")
        
        # 3. Match History (with Pagination)
        from riotskillissue import paginate
        async for match_id in paginate(client.match.get_ids_by_puuid, puuid=summoner.puuid, count=20):
             print(f"Match: {match_id}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🛠 Configuration

The client is highly configurable via `RiotClientConfig`.

```python
from riotskillissue import RiotClientConfig, RiotClient

config = RiotClientConfig(
    api_key="RGAPI-...",          # Or set RIOT_API_KEY env var
    connect_timeout=5.0,          # Initial connection timeout (s)
    read_timeout=10.0,            # Response read timeout (s)
    max_retries=3,                # Max attempts for 5xx/Connectivity errors
    redis_url="redis://localhost" # Enable Distributed Rate Limiting
)
```

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `api_key` | `str` | `None` | Riot API Key. Defaults to `os.environ["RIOT_API_KEY"]`. |
| `redis_url` | `str` | `None` | Connection string for Redis (e.g. `redis://127.0.0.1:6379`). Required for **Distributed Rate Limiting**. |
| `max_retries` | `int` | `3` | Attempts for network/server errors. |
| `connect_timeout` | `float` | `5.0` | Headers wait timeout. |
| `read_timeout` | `float` | `10.0` | Body wait timeout. |

---

## 🧠 Advanced Features

### 1. Caching
Reduce API usage by enabling the caching layer.

```python
from riotskillissue.core.cache import RedisCache, MemoryCache

# In-Memory (Single Process)
cache = MemoryCache()

# Redis (Distributed)
cache = RedisCache("redis://localhost:6379/1")

async with RiotClient(cache=cache) as client:
    # 200 OK GET requests are cached automatically (Default TTL: 60s)
    # Static Data is cached longer (versions: 1h, champions: 24h)
    ...
```

### 2. Static Data (Data Dragon)
Auto-fetch champion info without managing version strings.

```python
# Fetches latest version -> fetches champion.json -> caches it
annie = await client.static.get_champion(1)
print(annie["name"]) # "Annie"
```

### 3. Riot Sign-On (RSO)
OAuth2 helper for web apps.

```python
from riotskillissue.auth import RsoClient, RsoConfig

rso = RsoClient(RsoConfig(
    client_id="...", 
    client_secret="...", 
    redirect_uri="http://localhost/callback"
))

# 1. Redirect user here
auth_url = rso.get_auth_url() 

# 2. Exchange code for tokens
tokens = await rso.exchange_code("authorization_code")
```

### 4. CLI Tool
Quick debug from terminal.

```bash
# Basic Lookup
riotskillissue-cli summoner "Faker#SKT" --region kr

# Match Details
riotskillissue-cli match "KR_1234567890"

# Help
riotskillissue-cli --help
```

---

## 🧪 Testing

This repo comes with a comprehensive test suite.

```bash
# Run all tests (Unit + Integration + Mocked Edge Cases)
pytest tests/

# Run specific suite
pytest tests/test_resiliency.py
```

## 🤖 Automation

How this library stays up to date:
1. **Weekly Action**: `.github/workflows/update_sdk.yml` runs.
2. **Fetch**: Downloads `openapi.json` from [MingweiSamuel/riotapi-schema](https://github.com/MingweiSamuel/riotapi-schema).
3. **Diff**: Compares with current generated definitions.
4. **Generate**: Re-runs `tools/generator/core.py`.
5. **PR**: Opens a Pull Request with the changes and a changelog.

---

## 📄 License

MIT

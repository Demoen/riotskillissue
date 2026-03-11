# Configuration

This guide covers all configuration options for the RiotClient.

## RiotClientConfig

The `RiotClientConfig` class controls client behavior:

```python
from riotskillissue import RiotClient, RiotClientConfig

config = RiotClientConfig(
    api_key="RGAPI-...",
    max_retries=5,
    connect_timeout=5.0,
    read_timeout=10.0,
    cache_ttl=120,
    log_level="DEBUG",
)

async with RiotClient(config=config) as client:
    # Use the configured client
    pass
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | `None` | Your Riot Games API key. Falls back to `RIOT_API_KEY` env var. |
| `max_retries` | `int` | `3` | Maximum retry attempts for failed requests (5xx, network errors). |
| `connect_timeout` | `float` | `5.0` | Connection timeout in seconds. |
| `read_timeout` | `float` | `10.0` | Read timeout in seconds. |
| `redis_url` | `str` | `None` | Redis URL for distributed rate limiting. |
| `cache_ttl` | `int` | `60` | Default cache time-to-live in seconds for GET responses. |
| `proxy` | `str` | `None` | HTTP proxy URL (e.g. `http://127.0.0.1:8080`). |
| `base_url` | `str` | `None` | Override the Riot API base URL (useful for testing or custom endpoints). |
| `log_level` | `str` | `"WARNING"` | Logging level for the library (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |

## Environment Variables

All config fields can be set via environment variables:

| Variable | Config Field | Description |
|----------|-------------|-------------|
| `RIOT_API_KEY` | `api_key` | Default API key if not provided in config. |
| `RIOT_REDIS_URL` | `redis_url` | Redis connection string. |
| `RIOT_MAX_RETRIES` | `max_retries` | Maximum retry attempts. |
| `RIOT_CACHE_TTL` | `cache_ttl` | Cache time-to-live in seconds. |
| `RIOT_PROXY` | `proxy` | HTTP proxy URL. |
| `RIOT_BASE_URL` | `base_url` | Custom API base URL. |
| `RIOT_LOG_LEVEL` | `log_level` | Logging level. |

```python
from riotskillissue import RiotClientConfig

# Load everything from environment variables
config = RiotClientConfig.from_env()
```

## Redis Integration

Enable distributed rate limiting and caching with Redis. First install the `redis` extra:

```bash
pip install "riotskillissue[redis]"
```

### Rate Limiting

For applications running multiple processes or pods:

```python
config = RiotClientConfig(
    api_key="RGAPI-...",
    redis_url="redis://localhost:6379/0"
)

async with RiotClient(config=config) as client:
    # Rate limits are now shared across all instances
    pass
```

### Caching

Reduce API calls with built-in response caching:

!!! warning "Upgrading from v0.2.x"
    `RedisCache` serialization switched from `pickle` to JSON + base64 in v0.3.0.
    Existing cached entries are **incompatible** — flush your Redis cache after upgrading.

```python
from riotskillissue import RiotClient
from riotskillissue.core.cache import RedisCache

cache = RedisCache("redis://localhost:6379/1")

async with RiotClient(cache=cache) as client:
    # First call hits the API
    summoner = await client.summoner.get_by_puuid(
        region="euw1",
        encryptedPUUID="..."
    )
    
    # Second call returns cached data (within cache_ttl)
    summoner = await client.summoner.get_by_puuid(
        region="euw1",
        encryptedPUUID="..."
    )
```

### In-Memory Cache (LRU)

The default `MemoryCache` uses LRU eviction to bound memory usage:

```python
from riotskillissue.core.cache import MemoryCache

cache = MemoryCache(max_size=2048)  # Default: 1024 entries

async with RiotClient(cache=cache) as client:
    # Least-recently-used entries are evicted when max_size is reached
    pass
```

## Retry Behavior

The client automatically retries requests on:

- **HTTP 5xx** server errors — up to `max_retries` attempts with exponential backoff
- **Network errors** — connection failures, timeouts
- **HTTP 429** rate limits — sleeps for the `Retry-After` header value, then retries (does **not** count against `max_retries`)

```python
config = RiotClientConfig(
    api_key="RGAPI-...",
    max_retries=5,  # More retries for unreliable networks
)
```

## Error Handling

v0.2.0 introduces a typed error hierarchy. All exceptions inherit from `RiotAPIError`:

```python
from riotskillissue import (
    RiotAPIError,
    BadRequestError,    # 400
    UnauthorizedError,  # 401
    ForbiddenError,     # 403
    NotFoundError,      # 404
    RateLimitError,     # 429
    ServerError,        # 5xx
)
```

Each error carries the original `status`, `message`, and `response` object:

```python
try:
    data = await client.summoner.get_by_puuid(region="euw1", encryptedPUUID="...")
except NotFoundError:
    print("Summoner not found")
except RiotAPIError as e:
    print(f"[{e.status}] {e.message}")
```

## Proxy Support

Route all API traffic through an HTTP proxy:

```python
config = RiotClientConfig(
    api_key="RGAPI-...",
    proxy="http://127.0.0.1:8080",
)

async with RiotClient(config=config) as client:
    # All requests go through the proxy
    pass
```

## Logging

The library uses Python's standard `logging` module. Set the level via config:

```python
config = RiotClientConfig(
    api_key="RGAPI-...",
    log_level="DEBUG",  # See every request, retry, and cache hit/miss
)
```

Or configure logging directly:

```python
import logging
logging.getLogger("riotskillissue").setLevel(logging.DEBUG)
```

## Timeouts

Configure connection and read timeouts separately:

```python
config = RiotClientConfig(
    api_key="RGAPI-...",
    connect_timeout=3.0,   # Fast fail on connection issues
    read_timeout=30.0,     # Allow slow responses for heavy endpoints
)
```

## Synchronous Client

For scripts, notebooks, and non-async contexts, use `SyncRiotClient`:

```python
from riotskillissue import SyncRiotClient

with SyncRiotClient(api_key="RGAPI-...") as client:
    account = client.account.get_by_riot_id(
        region="americas",
        gameName="Faker",
        tagLine="KR1"
    )
    print(account.gameName)
```

`SyncRiotClient` accepts the same `config` and `cache` arguments as `RiotClient`. It runs a background event loop on a daemon thread, so it's safe to use even inside Jupyter notebooks.

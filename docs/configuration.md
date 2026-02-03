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

## Environment Variables

| Variable | Description |
|----------|-------------|
| `RIOT_API_KEY` | Default API key if not provided in config. |

## Redis Integration

Enable distributed rate limiting and caching with Redis:

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
    
    # Second call returns cached data
    summoner = await client.summoner.get_by_puuid(
        region="euw1",
        encryptedPUUID="..."
    )
```

## Retry Behavior

The client automatically retries requests on:

- HTTP 5xx server errors
- Network connection failures
- Rate limit responses (HTTP 429)

Retries use exponential backoff with jitter. For rate limits, the client respects the `Retry-After` header.

```python
# Customize retry behavior
config = RiotClientConfig(
    api_key="RGAPI-...",
    max_retries=5,  # More retries for unreliable networks
)
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

## Loading from Environment

The simplest approach is to use environment variables:

```python
from riotskillissue import RiotClient

# Automatically loads RIOT_API_KEY from environment
async with RiotClient() as client:
    pass
```

For explicit environment loading:

```python
from riotskillissue import RiotClientConfig

config = RiotClientConfig.from_env()
```

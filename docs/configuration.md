# Configuration

Configuration may be supplied directly or through environment variables.

```python
from riotskillissue import PlatformRoute, RiotClient, RiotClientConfig

config = RiotClientConfig(
    api_key="RGAPI-...",
    default_route=PlatformRoute.EUW1,
    read_timeout=20.0,
    max_retries=3,
    max_rate_limit_retries=2,
)

riot = RiotClient(config=config)
```

The primary environment variables are:

| Variable | Purpose |
| --- | --- |
| `RIOT_API_KEY` | Riot development or production API key |
| `RIOT_DEFAULT_ROUTE` | Default platform, regional, or VALORANT route |
| `RIOT_CONNECT_TIMEOUT` | Connection timeout in seconds |
| `RIOT_READ_TIMEOUT` | Response-read timeout in seconds |
| `RIOT_WRITE_TIMEOUT` | Request-write timeout in seconds |
| `RIOT_POOL_TIMEOUT` | Connection-pool timeout in seconds |
| `RIOT_MAX_RETRIES` | Network and server retry limit |
| `RIOT_MAX_RATE_LIMIT_RETRIES` | HTTP 429 retry limit |
| `RIOT_CACHE_TTL` | Default cache lifetime |
| `RIOT_LOG_LEVEL` | Library log level |

Empty API keys are rejected. RSO credentials use a token provider and are not
accepted as endpoint arguments.

Network and server retries apply to idempotent HTTP methods, including `GET`,
`PUT`, and `DELETE`. `POST` and `PATCH` retry connection failures that occur before
the request is sent, but do not retry read/write failures or server errors that
could have occurred after a mutation was applied. HTTP 429 responses use the
separate rate-limit retry budget for every method.

Closing a client also closes the Redis rate limiter created from `redis_url`.
If you pass a shared rate limiter directly to `HttpClient`, close that limiter
yourself after all clients using it have closed.

## Caching

Pass an `AbstractCache` implementation to either client. RSO operations are not
cached unless explicitly enabled. If enabled, cache entries are partitioned by a
non-reversible credential fingerprint.

```python
from riotskillissue import MemoryCache, RiotClient

riot = RiotClient(cache=MemoryCache(max_size=1024))
```

The optional `RedisCache` stores its entries under `riot:cache:`. Its `clear()`
method removes only entries in that namespace, preserving rate-limit counters
and unrelated application data in the same database. Existing entries from
versions using unprefixed cache keys expire according to their original TTL;
the first request after upgrading repopulates the cache.

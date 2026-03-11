# RiotSkillIssue

**The production-ready, auto-updating, and fully typed Python wrapper for the Riot Games API.**

---

<div class="grid cards" markdown>

-   **Type-Safe**

    ---

    100% Pydantic models for all requests and responses. No more dictionary guessing.

-   **Auto-Updated**

    ---

    Generated daily from the Official OpenAPI Spec. Supports LoL, TFT, LoR, and VALORANT.

-   **Resilient by Design**

    ---

    Built-in exponential backoff, automatic `Retry-After` handling, and a rich error hierarchy.

-   **Distributed**

    ---

    Pluggable Redis support for shared rate limiting and caching across multiple processes.

-   **Sync & Async**

    ---

    First-class async client *and* a synchronous `SyncRiotClient` for scripts, notebooks, and CLI tools.

-   **Secure Auth**

    ---

    RSO OAuth2 with PKCE and CSRF state parameter out of the box.

</div>

## Quick Installation

```bash
pip install riotskillissue
```

## Quick Example (Async)

```python
import asyncio
from riotskillissue import RiotClient, Platform

async def main():
    async with RiotClient() as client:
        account = await client.account.get_by_riot_id(
            region=Platform.AMERICAS,
            gameName="Faker",
            tagLine="KR1"
        )
        print(f"Found: {account.gameName}#{account.tagLine}")
        print(f"PUUID: {account.puuid}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Quick Example (Sync)

```python
from riotskillissue import SyncRiotClient, Platform

with SyncRiotClient() as client:
    account = client.account.get_by_riot_id(
        region=Platform.AMERICAS,
        gameName="Faker",
        tagLine="KR1"
    )
    print(f"Found: {account.gameName}#{account.tagLine}")
```

!!! tip "API Key Setup"
    Set the `RIOT_API_KEY` environment variable, or pass it directly to `RiotClient(api_key="...")`.
    Get your key at [developer.riotgames.com](https://developer.riotgames.com/).

## What's New in v0.3.0

!!! warning "Breaking Changes"
    - Python **3.10+** is now required (3.8 and 3.9 dropped)
    - `redis` and `textual` are now **optional extras** — install with `pip install riotskillissue[redis]` or `[tui]`
    - `RedisCache` serialization switched from pickle to JSON+base64 — flush your Redis cache after upgrading

- **`py.typed`** — PEP 561 marker for downstream type-checking support
- **Context managers** — `RsoClient` and `DataDragonClient` now support `async with`
- **Safer caching** — `RedisCache` no longer uses `pickle`, eliminating code execution risk from tampered entries
- **Better rate limiting** — `MemoryRateLimiter` releases its lock while sleeping, unblocking other keys
- **More exports** — `AbstractRateLimiter`, `MemoryRateLimiter`, `gather_limited`, `DataDragonClient`, `RsoClient`, `RsoConfig`, `TokenResponse`

See the full [Changelog](https://github.com/Demoen/riotskillissue/blob/main/CHANGELOG.md) for details.

## Next Steps

<div class="grid cards" markdown>

-   :material-rocket-launch: **[Getting Started](getting-started.md)**

    ---

    Complete installation and setup guide

-   :material-cog: **[Configuration](configuration.md)**

    ---

    Redis caching, rate limiting, and advanced options

-   :material-code-tags: **[Examples](examples/index.md)**

    ---

    Working code examples for LoL, TFT, and VALORANT

-   :material-api: **[API Reference](api-reference.md)**

    ---

    Complete endpoint documentation

</div>

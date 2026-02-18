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

## What's New in v0.2.0

- **`SyncRiotClient`** — Use the full API without async/await
- **Rich error hierarchy** — Catch `NotFoundError`, `RateLimitError`, etc. instead of generic exceptions
- **Automatic 429 retry** — Rate-limited requests are retried transparently with `Retry-After`
- **PKCE + CSRF** — RSO OAuth2 now includes PKCE code challenge and state parameter
- **Expanded Data Dragon** — Summoner spells, runes, queues, maps, and game modes
- **LRU cache** — In-memory cache with configurable max size and automatic eviction
- **Proxy & base URL** — Route traffic through a proxy or point at a custom API endpoint

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

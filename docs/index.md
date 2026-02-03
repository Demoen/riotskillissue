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

    Built-in exponential backoff, circuit breakers, and correct `Retry-After` handling.

-   **Distributed**

    ---

    Pluggable Redis support for shared rate limiting and caching across multiple processes.

</div>

## Quick Installation

```bash
pip install riotskillissue
```

## Quick Example

```python
import asyncio
from riotskillissue import RiotClient, Platform

async def main():
    async with RiotClient() as client:
        # Look up an account by Riot ID
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

!!! tip "API Key Setup"
    Set the `RIOT_API_KEY` environment variable, or pass it directly to `RiotClient(api_key="...")`.
    Get your key at [developer.riotgames.com](https://developer.riotgames.com/).

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

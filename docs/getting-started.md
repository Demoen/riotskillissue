---
description: Install RiotSkillIssue, configure your API key, and make your first async or sync request.
---

# Getting started

Install the package, set your Riot API key, and fetch a League of Legends player
profile. Choose the async client for an async application or the sync client for
a script.

## Installation

RiotSkillIssue requires Python `>=3.14,<3.17`. Run the installation command with
the Python interpreter you use for your application.

=== "macOS / Linux"

    ```bash
    python3 -m pip install riotskillissue
    ```

=== "Windows PowerShell"

    ```powershell
    py -m pip install riotskillissue
    ```

??? info "Optional integrations"

    The base package includes both Python clients and the CLI. Install an extra
    when you need its integration; extras can be combined, for example
    `riotskillissue[mcp,tui]`.

    | Integration | Package | Guide |
    | --- | --- | --- |
    | Local MCP server | `riotskillissue[mcp]` | [MCP setup](mcp.md) |
    | Live game terminal dashboard | `riotskillissue[tui]` | [TUI setup](live-game-tui.md) |
    | Redis cache and rate limiter | `riotskillissue[redis]` | [Configuration](configuration.md) |

## Set your API key

Create a development key in the [Riot Developer Portal](https://developer.riotgames.com/docs/portal#getting-started),
then set it in the shell where you will run your application. The clients read
`RIOT_API_KEY` automatically.

=== "macOS / Linux"

    ```bash
    export RIOT_API_KEY="RGAPI-..."
    ```

=== "Windows PowerShell"

    ```powershell
    $env:RIOT_API_KEY = "RGAPI-..."
    ```

## Async client

Save this as `profile.py`. Replace `Player#EUW` with a Riot ID and `EUW1` with
the player's [platform route](routing.md).

```python title="profile.py"
import asyncio

from riotskillissue import PlatformRoute, RiotClient


async def main() -> None:
    async with RiotClient(default_route=PlatformRoute.EUW1) as riot:
        profile = await riot.lol.player_profile("Player#EUW")
        print(profile.model_dump_json(indent=2))


asyncio.run(main())
```

=== "macOS / Linux"

    ```bash
    python3 profile.py
    ```

=== "Windows PowerShell"

    ```powershell
    py profile.py
    ```

The result contains the Riot ID, PUUID, account data, and game profile. The
context manager closes the client's connections when the block exits. Reuse
one client for related requests inside that block.

## Sync client

Use this version of `profile.py` when your application makes blocking calls.
It returns the same typed profile without `await`.

```python title="profile.py"
from riotskillissue import PlatformRoute, SyncRiotClient

with SyncRiotClient(default_route=PlatformRoute.EUW1) as riot:
    profile = riot.lol.player_profile("Player#EUW")
    print(profile.model_dump_json(indent=2))
```

The synchronous client owns a background event loop. In an async application,
prefer `RiotClient` so API calls do not block the application's event loop.

## Raw operations

Workflows such as `player_profile` combine several API calls. Use `riot.raw`
when you need a specific Riot endpoint and its full response. This complete
example fetches League of Legends service status:

```python title="status.py"
import asyncio

from riotskillissue import PlatformRoute, RiotClient


async def main() -> None:
    async with RiotClient(default_route=PlatformRoute.EUW1) as riot:
        status = await riot.raw.lol.status.get_platform_data()
        print(status.model_dump_json(indent=2))


asyncio.run(main())
```

Raw parameters are keyword-only and use `snake_case`; the client handles Riot's
wire names. Both clients expose `riot.raw` with the same endpoint names. Browse
the [API reference](reference/index.md) for operations, parameters, and routes.

## Next steps

<div class="grid cards" markdown>

-   :lucide-braces: **Build a game workflow**

    Fetch match history, champion mastery, ranked entries, or a leaderboard.

    [Explore examples :lucide-arrow-right:](examples/index.md)

-   :lucide-sliders-horizontal: **Configure your application**

    Set timeouts, retry budgets, route defaults, and caching.

    [Configure the client :lucide-arrow-right:](configuration.md)

</div>

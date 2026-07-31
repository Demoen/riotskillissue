# Getting started

## Installation

```bash
pip install riotskillissue
```

RiotSkillIssue 1.0 requires Python `>=3.14,<3.17`, covering Python 3.14,
3.15, and 3.16. As of July 2026, CI gates releases on Python 3.14 and the
current Python 3.15 prerelease. Python 3.16 is still in development, so it is
covered by a non-blocking nightly compatibility probe until its stable release.

Create a Riot development key and set it in the server or application
environment:

```bash
export RIOT_API_KEY="RGAPI-..."
```

PowerShell:

```powershell
$env:RIOT_API_KEY = "RGAPI-..."
```

## Async client

```python
import asyncio

from riotskillissue import PlatformRoute, RiotClient


async def main() -> None:
    async with RiotClient(default_route=PlatformRoute.EUW1) as riot:
        profile = await riot.lol.player_profile("Player#EUW")
        history = await riot.lol.match_history("Player#EUW", count=5)
        print(profile)
        print(history)


asyncio.run(main())
```

## Sync client

```python
from riotskillissue import PlatformRoute, SyncRiotClient

with SyncRiotClient(default_route=PlatformRoute.EUW1) as riot:
    profile = riot.lol.player_profile("Player#EUW")
    print(profile)
```

The synchronous surface is explicit and typed. It uses a background event loop
internally, so it also works in environments that already have an event loop.

## Raw operations

Workflows intentionally stay focused. Use the generated raw API for complete
coverage:

```python
match = await riot.raw.lol.match.get_match(match_id="EUW1_...")
status = await riot.raw.valorant.status.get_platform_data(
    route=ValorantRoute.EU
)
```

Raw parameters are keyword-only and use snake_case. Riot wire names are handled
internally.

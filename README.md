# RiotSkillIssue

<div align="center">

![riotskillissue](docs/assets/logo.png)

[![PyPI version](https://badge.fury.io/py/riotskillissue.svg)](https://pypi.org/project/riotskillissue)
[![Python Versions](https://img.shields.io/pypi/pyversions/riotskillissue.svg)](https://pypi.org/project/riotskillissue/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/Demoen/riotskillissue/actions/workflows/test.yml/badge.svg)](https://github.com/Demoen/riotskillissue/actions/workflows/test.yml)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/riotskillissue?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/riotskillissue)

**Typed async and sync Riot Games APIs, plus an optional local MCP server.**

[Documentation](https://demoen.github.io/riotskillissue/) · [Migration guide](https://demoen.github.io/riotskillissue/migration/) · [API reference](https://demoen.github.io/riotskillissue/api-reference/)

</div>

## Install

RiotSkillIssue 1.0 requires Python `>=3.14,<3.17`, covering Python 3.14,
3.15, and 3.16. As of July 2026, CI gates releases on Python 3.14 and the
current Python 3.15 prerelease. Python 3.16 is still in development, so it is
covered by a non-blocking nightly compatibility probe until its stable release.

```bash
pip install riotskillissue
```

Set `RIOT_API_KEY` or pass a key directly:

```python
import asyncio

from riotskillissue import PlatformRoute, RiotClient


async def main() -> None:
    async with RiotClient(
        api_key="RGAPI-...",
        default_route=PlatformRoute.EUW1,
    ) as riot:
        profile = await riot.lol.player_profile("Player#EUW")
        history = await riot.lol.match_history("Player#EUW", count=5)
        match = await riot.raw.lol.match.get_match(match_id="EUW1_...")
        print(profile, history, match)


asyncio.run(main())
```

The explicit synchronous client provides the same workflows and raw operation
groups:

```python
from riotskillissue import PlatformRoute, SyncRiotClient

with SyncRiotClient(default_route=PlatformRoute.EUW1) as riot:
    print(riot.lol.player_profile("Player#EUW"))
```

## Local MCP server

Install the optional server and run it over stdio:

```bash
pip install "riotskillissue[mcp]"
riotskillissue-mcp
```

The server reads credentials from its environment. API keys and RSO tokens are
never tool arguments. Raw write operations are hidden unless
`RIOT_MCP_ALLOW_WRITES=true`; enabled writes still require human confirmation.

## Coverage and generation

The generated raw API covers every operation in the bundled community-maintained
OpenAPI feed. That feed is not an official Riot Games specification. One
committed operation registry drives raw dispatch, reference documentation, and
MCP discovery.

RiotSkillIssue is not endorsed by Riot Games and does not reflect the views or
opinions of Riot Games or anyone officially involved in producing or managing
Riot Games properties. Riot Games and all associated properties are trademarks
or registered trademarks of Riot Games, Inc.

## License

MIT. See [LICENSE](LICENSE).

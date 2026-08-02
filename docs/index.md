# RiotSkillIssue 1.1

RiotSkillIssue provides typed asynchronous and synchronous Python clients for
Riot Games APIs and an optional local MCP server. The MCP surface can assemble
League match timelines, objective conversion, player history, and patch-aware
game knowledge into evidence bundles for natural-language analysis. Its League
fundamentals include minion-wave gold and XP, shared experience, passive income,
structures, objective allocations, and patch-matched item raw-stat efficiency.

The public client has two layers:

- Game workflows such as `riot.lol.player_profile()` and
  `riot.valorant.leaderboard()`.
- Complete generated coverage under `riot.raw`, grouped by game and service.

```python
async with RiotClient(default_route=PlatformRoute.EUW1) as riot:
    profile = await riot.lol.player_profile("Player#EUW")
    history = await riot.lol.match_history("Player#EUW")
    match = await riot.raw.lol.match.get_match(match_id="EUW1_...")
```

Generated code is based on a community-maintained OpenAPI feed. It is not an
official Riot Games specification.

## Choose an interface

| Interface | Best for |
| --- | --- |
| `RiotClient` | Async applications and concurrent workflows |
| `SyncRiotClient` | Scripts, notebooks, and synchronous applications |
| `riotskillissue-mcp` | Local AI clients using MCP over stdio |

Start with the [getting started guide](getting-started.md), or read the
[migration guide](migration.md) when upgrading from 0.3.

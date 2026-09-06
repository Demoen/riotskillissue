---
description: Python recipes for League of Legends, Teamfight Tactics, and VALORANT.
hide:
  - toc
---

# Examples

Start with the game you are building for. These recipes use the workflow
services to resolve Riot IDs and fetch player data. Complete
[getting started](../getting-started.md) first to install the package and set
your API key.

<div class="grid cards rsi-interface-cards" markdown>

-   :lucide-swords: **League of Legends**

    Look up a player, summarize recent matches, and inspect champion mastery.
    The code is included directly from the repository's `examples/` files.

    [Player profile :lucide-arrow-right:](league-of-legends.md#player-profile)
    · [Match history](league-of-legends.md#match-history)
    · [Champion mastery](league-of-legends.md#champion-mastery)

-   :lucide-chess-knight: **Teamfight Tactics**

    Retrieve a TFT profile, ranked entries, and recent match summaries using
    a platform route such as `EUW1`.

    [TFT examples :lucide-arrow-right:](teamfight-tactics.md)

-   :lucide-crosshair: **VALORANT**

    Resolve a player profile, fetch recent matches, and request an act
    leaderboard using a VALORANT route such as `EU`.

    [VALORANT examples :lucide-arrow-right:](valorant.md)

</div>

## Adapt a recipe

| To change | Use |
| --- | --- |
| The player | A full Riot ID in `GameName#TagLine` format |
| The server or region | The appropriate [route family](../routing.md) |
| Async calls to blocking calls | [`SyncRiotClient`](../getting-started.md#sync-client), `with`, and calls without `await` |
| Timeout, retries, or caching | [Client configuration](../configuration.md) |
| An endpoint or field outside a workflow | The [generated raw API](../reference/index.md) |

`match_history` returns up to 20 summaries and fetches match details with
bounded concurrency. For League of Legends and TFT, `match_ids` also accepts
`start` and `count` to page through IDs before fetching individual matches.

For Legends of Runeterra, Riftbound, and the complete operation catalog, use the
[API reference](../reference/index.md). Operations that require player
authorization are covered in [Riot Sign On](../rso.md).

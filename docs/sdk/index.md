---
description: Build with the RiotSkillIssue Python SDK, from your first request to routing, caching, and authentication.
---

# Python SDK

Use `RiotClient` or `SyncRiotClient` to call Riot APIs from Python. Start with
game workflows for common player tasks, then use the generated raw API for
individual endpoints.

<div class="grid cards" markdown>

-   :lucide-code-2: **Make your first request**

    Install the package, set your API key, and run an async or sync client.

    [Get started :lucide-arrow-right:](../getting-started.md)

-   :lucide-braces: **Build with examples**

    Fetch player profiles, match histories, ranked entries, and leaderboards.

    [Find a recipe :lucide-arrow-right:](../examples/index.md)

-   :lucide-sliders-horizontal: **Configure the client**

    Choose timeouts, retry budgets, environment variables, and cache backends.

    [Open configuration :lucide-arrow-right:](../configuration.md)

-   :lucide-globe: **Choose the right route**

    Understand platform, regional, and VALORANT routes and how defaults resolve.

    [Understand routing :lucide-arrow-right:](../routing.md)

</div>

## Choose an API surface

Both clients expose the same service and endpoint names. The async client uses
`await`; the sync client makes blocking calls.

| When you need | Surface | Example |
| --- | --- | --- |
| A common task starting from a Riot ID | Game workflow | `riot.lol.player_profile("Player#EUW")` |
| A specific endpoint and its full response | Generated raw API | `riot.raw.lol.match.get_match(match_id="EUW1_...")` |
| An operation selected at runtime | Operation dispatcher | `riot.call_operation(operation, arguments)` |

The [API reference](../reference/index.md) explains how to find operations and
read their generated signatures. [Game examples](../examples/index.md) show how
to use the workflow services.

## Authentication and upgrades

Most endpoints use `RIOT_API_KEY`. For operations that act on behalf of a
player, follow the [Riot Sign On guide](../rso.md) to configure a token provider.

Moving from the 0.3 API? The [migration guide](../migration.md) maps old calls to
the 1.x client, workflows, raw operations, and MCP tools.

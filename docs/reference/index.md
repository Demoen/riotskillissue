---
description: Find Riot API operations by game, and understand routing, authentication, and generated coverage.
---

# API reference

The raw API maps Riot endpoints to typed Python methods under `riot.raw`.
Async and sync clients expose the same operation names and keyword-only
parameters. Use this reference when you know the endpoint you need; use
[game workflows](../examples/index.md) for tasks such as resolving a player
and fetching their match history.

## Browse by game

<div class="grid cards" markdown>

-   :lucide-user-round: **Accounts**

    Resolve Riot IDs and PUUIDs, and discover a player's active shard or region.

    [Common operations :lucide-arrow-right:](../api-reference.md#common)

-   :lucide-swords: **League of Legends**

    Matches, timelines, ranked entries, spectator data, mastery, and challenges.

    [League operations :lucide-arrow-right:](../api-reference.md#league-of-legends)

-   :lucide-chess-knight: **Teamfight Tactics**

    Match history, ranked ladders, summoners, and spectator data.

    [TFT operations :lucide-arrow-right:](../api-reference.md#teamfight-tactics)

-   :lucide-crosshair: **VALORANT**

    Matches, ranked leaderboards, content, and service status.

    [VALORANT operations :lucide-arrow-right:](../api-reference.md#valorant)

-   :lucide-layers: **Legends of Runeterra**

    Match data, ranked leaderboards, and service status.

    [Runeterra operations :lucide-arrow-right:](../api-reference.md#legends-of-runeterra)

-   :lucide-sparkles: **Riftbound**

    Card-set content from the generated Riftbound API surface.

    [Riftbound operations :lucide-arrow-right:](../api-reference.md#riftbound)

</div>

For public League champion and item assets, see
[Data Dragon](../api-reference.md#data-dragon).

## Read an operation entry

The [raw operation inventory](../api-reference.md#generated-raw-operation-inventory)
is generated with the SDK. Each row links a stable Riot operation ID to its
Python accessor, HTTP method, route family, authentication mode, and response
type.

| Column | How to use it |
| --- | --- |
| Operation ID | Identify an operation in the registry, dispatcher, or MCP discovery. |
| Python accessor | Call the endpoint on `riot.raw` with keyword-only arguments. |
| Method | Check whether the endpoint reads or changes data. |
| Route | Choose a supported platform, regional, or VALORANT route. |
| Auth | Determine whether the operation requires an API key or an RSO token. |
| Result | See the response type returned after validation. |

### Inspect inputs in Python

The registry includes input schemas and allowed routes for runtime discovery:

```python
from riotskillissue.api.registry import OPERATION_REGISTRY

operation = OPERATION_REGISTRY["match-v5.getMatch"]
print(operation.accessor_path)
print(operation.input_schema)
print(operation.allowed_routes)
```

To make your first raw request, follow the
[runnable status example](../getting-started.md#raw-operations).

## Coverage and authentication

Generated endpoints follow the community-maintained
[riotapi-schema feed](https://github.com/MingweiSamuel/riotapi-schema), which
scrapes Riot's API reference. The feed is not an official Riot specification.
An operation's presence in the SDK does not grant access to it: availability
depends on your Riot application, game permissions, and credentials.

| Requirement | Guide |
| --- | --- |
| Set an API key and client defaults | [Configuration](../configuration.md#configuration){ data-preview } |
| Choose a route or override the default | [Routing](../routing.md#routing){ data-preview } |
| Call an endpoint that requires a player's authorization | [Riot Sign On](../rso.md) |
| Understand how the schema stays current | [Code generation](../CONTRIBUTING.md#code-generation){ data-preview } |

!!! tip "Changing the generated reference"

    Update `tools/templates/api_reference.md.j2` and regenerate the SDK.
    Direct edits to `docs/api-reference.md` are replaced during generation.

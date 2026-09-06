---
title: Home
template: home.html
description: Typed Riot Games APIs for Python, a live-game terminal, and a local MCP server.
hide:
  - navigation
  - toc
  - path
---

<div class="rsi-hero" markdown>
<div class="rsi-hero__copy" markdown>

<p class="rsi-eyebrow">Riot Games · Python SDK</p>

<span id="riotskillissue-11"></span>

# Build with the<br>Riot Games API.

Typed clients for your applications. A live-game terminal for your next match.
A local MCP server for your AI tools.
{ .rsi-lead }

[Get started :lucide-arrow-right:](getting-started.md){ .md-button .md-button--primary }
[Explore the API](reference/index.md){ .md-button }

<p class="rsi-hero__meta">Async + sync <span aria-hidden="true">/</span> Typed responses <span aria-hidden="true">/</span> Open source</p>

</div>
<div class="rsi-hero__example" markdown>

<div class="rsi-window-bar"><span class="rsi-window-dot" aria-hidden="true"></span><span>Start with a Riot ID</span><span class="rsi-window-tag">Python</span></div>

=== "Async"

    ```python
    import asyncio

    from riotskillissue import PlatformRoute, RiotClient

    async def main():
        async with RiotClient(
            default_route=PlatformRoute.EUW1
        ) as riot:
            player = await riot.lol.player_profile("Player#EUW")
            print(player)

    asyncio.run(main())
    ```

=== "Sync"

    ```python
    from riotskillissue import PlatformRoute, SyncRiotClient

    with SyncRiotClient(
        default_route=PlatformRoute.EUW1
    ) as riot:
        player = riot.lol.player_profile("Player#EUW")
        print(player)
    ```

Set `RIOT_API_KEY` in your environment, then run.
[Get your first response :lucide-arrow-right:](getting-started.md#async-client)
{ .rsi-example-caption }

</div>
</div>

<div class="rsi-game-strip" markdown>

**One package. Five games.**
[League of Legends](api-reference.md#league-of-legends) ·
[Teamfight Tactics](api-reference.md#teamfight-tactics) ·
[VALORANT](api-reference.md#valorant) ·
[Legends of Runeterra](api-reference.md#legends-of-runeterra) ·
[Riftbound](api-reference.md#riftbound)

</div>

<span id="choose-an-interface"></span>

## Choose your starting point

<div class="grid cards rsi-interface-cards" markdown>

-   :lucide-code-2: **Python SDK**

    ---

    Resolve players, fetch match history, and call individual endpoints with
    typed asynchronous or synchronous clients.

    [Build an integration :lucide-arrow-right:](sdk/index.md)

-   :lucide-terminal: **Live game TUI**

    ---

    See teams, champions, ranks, and bans in your terminal, with automatic
    refreshes and visible data-quality warnings.

    [Open the dashboard :lucide-arrow-right:](live-game-tui.md)

-   :lucide-messages-square: **MCP server**

    ---

    Connect a local AI client to Riot data and League analysis tools that
    return structured match and player evidence.

    [Connect your AI client :lucide-arrow-right:](mcp.md)

</div>

## Find the right level of detail

<div class="grid rsi-reading-paths" markdown>
<div markdown>

### Work with a player or a match

Use game workflows when you want a complete task, such as a profile or a short
match history. Start from runnable examples and choose the route for your game.

[Browse examples](examples/index.md) ·
[Understand routing](routing.md#routing){ data-preview }

</div>
<div markdown>

### Call a specific endpoint

Use `riot.raw` for individual Riot operations. The reference lists Python
accessors, HTTP methods, authentication, and supported route families.

[Browse the operation reference](reference/index.md) ·
[Configure your client](configuration.md#configuration){ data-preview }

</div>
</div>

!!! note "About API coverage"

    The generated API follows a community-maintained OpenAPI feed, not an
    official Riot specification. Available endpoints depend on your key's game
    access and permissions. See [coverage and authentication](reference/index.md#coverage-and-authentication).

<div class="rsi-help-strip" markdown>

**Upgrading an existing project?**
Read the [migration guide](migration.md) or check the
[release notes](https://github.com/Demoen/riotskillissue/releases).

</div>

---
description: Choose the command line, live-game terminal dashboard, or local MCP server.
hide:
  - toc
---

# Tools

Use RiotSkillIssue from a terminal or an MCP host. Each tool shares the same Riot client, routing, and rate-limit handling as the [Python SDK](../getting-started.md).

<div class="grid cards rsi-interface-cards" markdown>

-   :lucide-terminal: **Command line**

    ---

    Look up a player's level and PUUID, inspect a match's mode and duration, or launch the live dashboard.

    Included in the base package.

    [Use the CLI :lucide-arrow-right:](../cli.md)

-   :lucide-panels-top-left: **Live Game TUI**

    ---

    Follow teams, champions, ranks, and bans in an interactive terminal dashboard with background refreshes.

    Requires the `tui` extra.

    [Open the dashboard :lucide-arrow-right:](../live-game-tui.md)

-   :lucide-bot: **MCP server**

    ---

    Give an MCP host structured League analysis and discoverable access to eligible Riot API operations.

    Requires the `mcp` extra.

    [Connect an MCP host :lucide-arrow-right:](../mcp.md)

</div>

## Install what you need

Use a supported [Python environment](../getting-started.md), then select the tools you want:

=== "CLI"

    ```bash
    pip install riotskillissue
    riotskillissue-cli --help
    ```

=== "Live Game TUI"

    ```bash
    pip install "riotskillissue[tui]"
    riotskillissue-cli live --help
    ```

=== "MCP server"

    ```bash
    pip install "riotskillissue[mcp]"
    ```

    Configure your host to launch `riotskillissue-mcp` over stdio. The [MCP setup](../mcp.md#connect-your-host) includes a server configuration.

=== "All tools"

    ```bash
    pip install "riotskillissue[tui,mcp]"
    ```

## Before your first request

The tools require a Riot API key. Set `RIOT_API_KEY` in your terminal for the CLI and TUI, or in the MCP server's environment. Each guide includes setup instructions.

For player lookups, use an exact Riot ID such as `GameName#TagLine` and a platform route such as `euw1`. Match lookups use regional routes such as `europe`; the MCP match-context tool can infer that route from a standard match ID. See [routing](../routing.md) for the distinction.

!!! note "Choose the output for your task"
    The CLI prints short summaries, the TUI presents live spectator data, and MCP returns structured evidence to a host. Use the [Python SDK](../getting-started.md) when you need to process results directly in your application.

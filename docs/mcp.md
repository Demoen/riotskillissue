# League-aware MCP server

Connect an MCP host to Riot data with a local stdio server. League analysis tools combine match, timeline, account, ranked, mastery, and Data Dragon data into structured evidence; the operation gateway exposes the complete eligible Riot API surface.

## Installation

Install the optional dependency:

```bash
pip install "riotskillissue[mcp]"
```

## Connect your host

Add the following server definition to your MCP host's configuration. The surrounding configuration format depends on the host; `command` and `env` describe the local process it needs to launch.

```json
{
  "command": "riotskillissue-mcp",
  "env": {
    "RIOT_API_KEY": "RGAPI-...",
    "RIOT_DEFAULT_ROUTE": "euw1"
  }
}
```

The `riotskillissue-mcp` command must be available to the host. If you installed it in a virtual environment, use that environment's executable path as `command`.

| Environment variable | Purpose |
| --- | --- |
| `RIOT_API_KEY` | Required Riot API key, supplied to the server process |
| `RIOT_DEFAULT_ROUTE` | Default route; a platform such as `euw1` supports player lookups |
| `RIOT_MCP_DEFAULT_ROUTE` | Optional MCP-specific default, taking precedence over `RIOT_DEFAULT_ROUTE` |
| `RIOT_MCP_ALLOW_WRITES` | `false` by default; see [writes](#writes) before enabling |

Protocol messages go to stdout and diagnostics to stderr. The API key stays in the server environment and is never accepted as a tool argument.

!!! tip "First request"
    Ask your host to analyze the most recent game for an exact Riot ID and platform, such as `GameName#TagLine` on `euw1`. The host can use `riot_lol_match_context` to resolve the player and load the evidence.

## League question tools

Use these tools first for League questions:

| Tool | Use |
| --- | --- |
| `riot_lol_match_context` | Analyze a match from a match ID or a player's recent-match index |
| `riot_lol_player_context` | Combine identity, summoner profile, ranked entries, mastery, and recent performance |
| `riot_lol_knowledge` | Load patch-banded mechanics, economy, minions, XP, structures, wave management, or telemetry limits |
| `riot_lol_item_economy` | Calculate patch-matched component-baseline raw-stat efficiency for an item |

The tools return structured evidence. Your MCP host explains that evidence in the language and level of detail you request. The JSON examples below are tool arguments, not server configuration.

!!! warning "Mechanics coverage is patch-bounded"
    The bundled economy registry is verified for standard Summoner's Rift patches **26.1–26.15** (internal **16.1–16.15**). API schema updates do not extend that knowledge range. Responses outside the verified patch or mode scope do not return a numeric wave model.

### Analyze a known match

Tool: `riot_lol_match_context`.

```json
{
  "request": {
    "match_id": "EUW1_1234567890",
    "question": "How much impact did void grubs have this game?",
    "detail": "standard"
  }
}
```

The server infers the regional route from a standard match-ID prefix. An explicit regional route can be supplied when a match ID cannot be inferred.

### Resolve “this game” from a player

Tool: `riot_lol_match_context`.

```json
{
  "request": {
    "riot_id": "Player#EUW",
    "route": "euw1",
    "match_index": 0,
    "question": "Why did we lose the most recent game?"
  }
}
```

`match_index` is zero-based. Resolving a player requires the exact `GameName#TagLine` Riot ID and a platform route unless the server has a platform default.

### Analyze a player

Tool: `riot_lol_player_context`.

```json
{
  "request": {
    "riot_id": "Player#EUW",
    "route": "euw1",
    "count": 5,
    "question": "What role and champions have they played recently?"
  }
}
```

The result distinguishes requested, successfully loaded, and unavailable matches. Optional upstream failures are reported as warnings instead of silently changing the sample.

### Ask about game mechanics

Tool: `riot_lol_knowledge`.

```json
{
  "request": {
    "topic": "void_grubs",
    "patch": "26.15",
    "question": "What should taking this objective accomplish?"
  }
}
```

Mechanics output includes its applicable patch band and source URLs. Mechanics lookup accepts public seasonal patch labels such as `26.15` and Match/Data Dragon versions such as `16.15`.

For champion abilities, items, runes, or summoner spells, use `riot_game_content`. Its `champion_detail` kind returns the full passive and ability payload for a numeric champion key. Supply `patch` and, optionally, `locale` to load a strict historical Data Dragon release. Queue, map, and game-mode metadata are unversioned and reject those selectors.

### Load strategic economy fundamentals

Tool: `riot_lol_knowledge`. Supported economy topics are `economy`, `minions`, `experience`, `structures`, `item_efficiency`, and `wave_management`.

```json
{
  "request": {
    "topic": "minions",
    "patch": "26.15",
    "question": "How much gold and XP is a wave worth?"
  }
}
```

Every quantitative response labels its patch and mode scope, separates sourced rules from derived arithmetic, and includes source URLs. Wave values describe theoretical collection opportunities for standard Map 11 CLASSIC; they do not establish what a player earned. Swiftplay, ARAM, Arena, unknown modes, and patches outside the verified range return no numeric wave model.

??? info "What the economy registry contains"

    | Topic | Coverage |
    | --- | --- |
    | Minions and waves | Melee, caster, siege, and super-minion rewards; spawn intervals; cannon cadence; composition changes |
    | Experience | Per-recipient shared-XP multipliers for one through six nearby allies |
    | Income | Passive-gold timing and rate, assigned-lane modifiers, and role-quest modifiers |
    | Structures and objectives | Plates, first-turret allocation, structures, and neutral-objective rewards |
    | Decisions | Opportunity costs for roams, recalls, objectives, and cross-map trades |

    In the verified registry, a base three-melee/three-caster wave is modelled as 102 last-hit gold and 279 solo XP. An early cannon wave starts at 152 gold and 354 solo XP; cannon gold scaling is reported separately. Derived examples include their formulas and assumptions.

Official Riot patch notes are the primary rules source. Patch-pinned CommunityDragon client extracts are identified as community-extracted corroboration for fields Riot does not publish in an API; historical analysis never uses a `latest` CommunityDragon URL.

### Calculate item raw-stat efficiency

Tool: `riot_lol_item_economy`. Supply an exact item name or an `item_id`.

=== "From a patch"

    ```json
    {
      "request": {
        "item_name": "Trinity Force",
        "patch": "26.15",
        "map_id": 11
      }
    }
    ```

=== "From a match"

    ```json
    {
      "request": {
        "item_name": "Trinity Force",
        "match_id": "EUW1_1234567890"
      }
    }
    ```

With `match_id`, the tool reads the exact match patch, queue, and map before loading static data. Public patch 26.15 is explicitly normalized to Data Dragon 16.15; an unavailable historical release fails closed and is never replaced with another patch.

The calculation derives per-stat prices from pure component items in the same Data Dragon release. It returns purchase, combine, and sell costs; each priceable structured stat and formula; unpriced stats; coverage; and raw-stat efficiency.

!!! note "Raw stats are only part of an item's value"
    Data Dragon omits some structured tooltip stats. Passives, actives, conditional effects, transformations, and mode-specific effects are not priced, so this result is not total item value or a build recommendation.

## Match evidence

A match context joins the Match V5 result, its timeline, and patch-matched Data Dragon content when available. It derives compact sections for:

- team results, gold, combat totals, and objectives;
- each participant's role, build, KDA, kill participation, damage, economy, farming, vision, and objective contribution;
- lane-opponent comparisons and minute checkpoints;
- major kills, epic monsters, buildings, item milestones, and clustered fights;
- objective conversion, including nearby gold movement, trades, and later turret pressure;
- question-relevant evidence and data-quality warnings.

Void Grub analysis reports observed captures, killers, timing, nearby trades, later turret/building results, and whether the team converted the objective into map pressure. Match V5 does not expose per-attack Hunger/Touch of the Void bonus damage, so the server labels the result as an association rather than inventing a causal damage number.

| `detail` | Use |
| --- | --- |
| `summary` | Minimize timeline detail |
| `standard` | Default evidence bundle |
| `full` | Retain more checkpoints and events |

Use `riot_call_read_operation` for an exact raw field not represented in the compact context.

## Other tools

High-level tools also cover profiles, match history, ranked entries, live games, mastery, challenges, service status, and game content.

Use the raw gateway when a high-level tool does not cover the request:

| Tool | Next step |
| --- | --- |
| `riot_find_operations` | Find eligible operations by query or game |
| `riot_describe_operation` | Inspect an operation's parameters and routing |
| `riot_call_read_operation` | Call a discovered read operation with its arguments |
| `riot_read_result` | Read a retained result by handle, JSON Pointer, and page |
| `riot_call_write_operation` | Execute a confirmed write, when [writes](#writes) are enabled |

Only explicitly supported `api_key` and unauthenticated operations are discoverable. RSO, OAuth, unknown authentication modes, and credential parameters fail closed.

## Large results

Small results are returned inline. Larger results are retained only in memory and represented by an opaque handle. `riot_read_result` supports RFC 6901 JSON Pointers plus paginated list or mapping slices. Reading a handle refreshes its LRU position but not its expiry.

All limits are validated at startup:

| Environment variable | Default | Meaning |
| --- | --- | --- |
| `RIOT_MCP_INLINE_LIMIT` | `32768` (32 KiB) | Maximum inline JSON bytes |
| `RIOT_MCP_MAX_RESULT_SIZE` | `10485760` (10 MiB) | Maximum JSON bytes for one result |
| `RIOT_MCP_MAX_RETAINED_BYTES` | `67108864` (64 MiB) | Aggregate retained JSON byte ceiling |
| `RIOT_MCP_MAX_RESULTS` | `64` | Maximum retained result count |
| `RIOT_MCP_RESULT_TTL` | `600` | Retention lifetime in seconds |

The aggregate ceiling must be at least the individual result ceiling, which must be at least the inline limit. LRU entries are evicted before either aggregate limit is exceeded.

## Writes

Writes are hidden by default. Set `RIOT_MCP_ALLOW_WRITES=true` in the server environment to register the write tool.

!!! warning "Confirmation is required for each write"
    Enabling the tool does not authorize individual writes. Every write requires resolver-driven human confirmation and fails closed if confirmation is declined, cancelled, or unsupported by the host.

## Scope and data limits

The server can analyze data Riot exposes; it cannot manufacture telemetry that does not exist.

- Match timelines do not contain every attack, spell cast, buff application, or exact source of structure damage.
- Match timelines do not identify every minion type, missed last hit, or nearby XP recipient, so missed-wave values remain explicitly modelled estimates.
- Public Riot APIs do not expose hidden MMR, unrestricted player search, player biographies, esports rosters, or private information.
- Live spectator data is less complete than post-game Match V5 data.
- Historical static enrichment requires a matching Data Dragon major/minor release. If it is unavailable, versioned enrichment is omitted and the rejected version is reported; cross-patch fallback is prohibited.
- Riot policies restrict custom-match history and information that would give an unfair in-game advantage.

Riot recommends PUUID-based endpoints and exact Riot IDs for player-facing applications. Review the [League API documentation](https://developer.riotgames.com/docs/lol), register player-facing products, and use a production key for a deployed service.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Host cannot start the server | Install the `mcp` extra and use the executable from that Python environment. Read the host's server log for stderr diagnostics. |
| Missing or rejected credentials | Provide `RIOT_API_KEY` in the server environment and verify it in the Riot Developer Portal. |
| Player cannot be resolved | Use the full `GameName#TagLine` Riot ID and a platform route, or configure a platform default. |
| Match cannot be loaded | Check the match ID and its regional cluster. The match-context tool infers standard match-ID prefixes. |
| Missing timeline, matches, or static content | Read the returned warnings. Optional failures and unavailable historical enrichment are reported separately. |
| Mechanics response has no numeric wave model | Check the verified patch range and mode scope under [League question tools](#league-question-tools). |
| Result handle is unavailable | It may have expired, been evicted, or belonged to a restarted server. Repeat the original tool call to obtain a fresh result. |
| Write tool is absent or a write is declined | Check `RIOT_MCP_ALLOW_WRITES` and the host's human-confirmation support. |

Rate limits, timeouts, credential rejection, and upstream unavailability are reported separately without exposing credentials.

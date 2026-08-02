# League-aware MCP server

RiotSkillIssue exposes both compact League analysis tools and the complete eligible Riot API surface. An MCP host can answer a natural-language question by requesting one evidence bundle instead of discovering and joining Match V5, timeline, account, ranked, mastery, and Data Dragon calls itself.

Install the optional dependency:

```bash
pip install "riotskillissue[mcp]"
```

Configure the MCP client to launch the local stdio server:

```json
{
  "command": "riotskillissue-mcp",
  "env": {
    "RIOT_API_KEY": "RGAPI-...",
    "RIOT_DEFAULT_ROUTE": "euw1"
  }
}
```

Protocol messages are written to stdout and diagnostics to stderr. The API key stays in the server environment and is never accepted as a tool argument.

## League question tools

Use these tools first for League questions:

| Tool | Use |
| --- | --- |
| `riot_lol_match_context` | Analyze a match from a match ID or a player's recent-match index |
| `riot_lol_player_context` | Combine identity, summoner profile, ranked entries, mastery, and recent performance |
| `riot_lol_knowledge` | Load patch-banded mechanics, economy, minions, XP, structures, wave management, or telemetry limits |
| `riot_lol_item_economy` | Calculate patch-matched component-baseline raw-stat efficiency for an item |

The tools return structured evidence. The MCP host remains responsible for explaining that evidence in the language and level of detail requested by the user.

### Analyze a known match

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

```json
{
  "request": {
    "topic": "void_grubs",
    "patch": "26.15",
    "question": "What should taking this objective accomplish?"
  }
}
```

Mechanics output includes its applicable patch band and source URLs. Champion abilities, items, runes, and summoner spells are available through `riot_game_content`; `champion_detail` returns the full passive and ability payload for a numeric champion key. Supply `patch` and, optionally, `locale` to load a strict historical Data Dragon release. Queue, map, and game-mode metadata are unversioned and reject those selectors.

Mechanics lookup accepts both public seasonal patch labels such as `26.15` and Match/Data Dragon versions such as `16.15`.

### Load strategic economy fundamentals

```json
{
  "request": {
    "topic": "minions",
    "patch": "26.15",
    "question": "How much gold and XP is a wave worth?"
  }
}
```

The bundled standard Summoner's Rift economy registry covers public patches 26.1 through 26.15 (internal 16.1 through 16.15). It includes:

- melee, caster, siege, and super-minion gold and XP;
- wave spawn intervals, cannon cadence, composition changes, and super-minion additions;
- per-recipient shared-XP multipliers for one through six nearby allies;
- passive-gold timing and rate, assigned-lane and role-quest modifiers;
- turret plates, first-turret allocation, structures, and neutral-objective rewards;
- formulas and derived normal/cannon-wave examples with their assumptions;
- an opportunity-cost framework for roams, recalls, objectives, and cross-map trades.

For the current registry, a base three-melee/three-caster wave is modelled as 102 last-hit gold and 279 solo XP. An early cannon wave starts at 152 gold and 354 solo XP; cannon gold scaling is reported separately. These are theoretical collection opportunities for standard Map 11 CLASSIC, not proof of what a player earned. Swiftplay, ARAM, Arena, unknown modes, and patches outside the verified range return no numeric wave model.

Use `economy`, `minions`, `experience`, `structures`, `item_efficiency`, or `wave_management` as the topic. Every quantitative response labels its patch and mode scope, separates sourced rules from derived arithmetic, and includes source URLs.

Official Riot patch notes are the primary rules source. Patch-pinned CommunityDragon client extracts are identified as community-extracted corroboration for fields Riot does not publish in an API; historical analysis never uses a `latest` CommunityDragon URL.

### Calculate item raw-stat efficiency

```json
{
  "request": {
    "item_name": "Trinity Force",
    "patch": "26.15",
    "map_id": 11
  }
}
```

Alternatively, supply `item_id`, or replace `patch` with `match_id` so the tool reads the exact match patch, queue, and map before loading static data. Public patch 26.15 is explicitly normalized to Data Dragon 16.15; an unavailable historical release fails closed and is never replaced with another patch.

The calculation derives per-stat prices from pure component items in the same Data Dragon release. It returns purchase, combine, and sell costs; each priceable structured stat and formula; unpriced stats; coverage; and raw-stat efficiency. Data Dragon omits some structured tooltip stats, and passives, actives, conditional effects, transformations, and mode-specific effects are not priced. The result is therefore not total item value or a build recommendation.

## Match evidence

A match context joins the Match V5 result, its timeline, and patch-matched Data Dragon content when available. It derives compact sections for:

- team results, gold, combat totals, and objectives;
- each participant's role, build, KDA, kill participation, damage, economy, farming, vision, and objective contribution;
- lane-opponent comparisons and minute checkpoints;
- major kills, epic monsters, buildings, item milestones, and clustered fights;
- objective conversion, including nearby gold movement, trades, and later turret pressure;
- question-relevant evidence and data-quality warnings.

Void Grub analysis reports observed captures, killers, timing, nearby trades, later turret/building results, and whether the team converted the objective into map pressure. Match V5 does not expose per-attack Hunger/Touch of the Void bonus damage, so the server labels the result as an association rather than inventing a causal damage number.

`summary` detail minimizes the timeline, `standard` is the default evidence bundle, and `full` retains more checkpoints and events. Use `riot_call_read_operation` for an exact raw field not represented in the compact context.

## Other tools

High-level tools also cover profiles, match history, ranked entries, live games, mastery, challenges, service status, and game content.

The raw gateway provides exhaustive eligible API access through:

- `riot_find_operations`
- `riot_describe_operation`
- `riot_call_read_operation`
- `riot_call_write_operation` when writes are enabled
- `riot_read_result`

Only explicitly supported `api_key` and unauthenticated operations are discoverable. RSO, OAuth, unknown authentication modes, and credential parameters fail closed.

## Large results

Small results are returned inline. Larger results are retained only in memory and represented by an opaque handle. `riot_read_result` supports RFC 6901 JSON Pointers plus paginated list or mapping slices. Reading a handle refreshes its LRU position but not its expiry.

Default retention limits are:

| Setting | Default |
| --- | ---: |
| Inline result | 32 KiB |
| Individual result | 10 MiB |
| Aggregate retained data | 64 MiB |
| Retained result count | 64 |
| Result lifetime | 600 seconds |

All limits are validated at startup:

| Environment variable | Meaning |
| --- | --- |
| `RIOT_MCP_INLINE_LIMIT` | Maximum inline JSON bytes |
| `RIOT_MCP_MAX_RESULT_SIZE` | Maximum JSON bytes for one result |
| `RIOT_MCP_MAX_RETAINED_BYTES` | Aggregate retained JSON byte ceiling |
| `RIOT_MCP_MAX_RESULTS` | Maximum retained result count |
| `RIOT_MCP_RESULT_TTL` | Retention lifetime in seconds |

The aggregate ceiling must be at least the individual result ceiling, which must be at least the inline limit. LRU entries are evicted before either aggregate limit is exceeded.

## Writes

Writes are hidden by default. Set `RIOT_MCP_ALLOW_WRITES=true` to register the write tool. Every write still requires resolver-driven human confirmation and fails closed if confirmation is declined, cancelled, or unsupported.

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

If a player cannot be resolved, verify the full Riot ID and platform route. If a match cannot be loaded, verify that its regional cluster matches the route. A development key can expire or be rate-limited; the server reports credential rejection, rate limits, timeouts, upstream unavailability, and missing timeline/static enrichment separately without exposing credentials.

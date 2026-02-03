# API Reference

Complete reference for all available API endpoints.

## Client Initialization

```python
from riotskillissue import RiotClient, RiotClientConfig

# Simple initialization (uses RIOT_API_KEY env var)
async with RiotClient() as client:
    pass

# With explicit API key
async with RiotClient(api_key="RGAPI-...") as client:
    pass

# With full configuration
config = RiotClientConfig(
    api_key="RGAPI-...",
    max_retries=5,
    redis_url="redis://localhost:6379/0"
)
async with RiotClient(config=config) as client:
    pass
```

---

## Region and Platform Types

```python
from riotskillissue import Region, Platform
```

### Platform (Routing)

Used for account lookups and match history APIs.

| Value | Description |
|-------|-------------|
| `Platform.AMERICAS` | North/South America |
| `Platform.EUROPE` | Europe |
| `Platform.ASIA` | Korea, Japan |
| `Platform.SEA` | Southeast Asia, Oceania |

### Region (Server)

Used for summoner, ranked, and spectator APIs.

| Value | Server |
|-------|--------|
| `Region.NA1` | North America |
| `Region.EUW1` | Europe West |
| `Region.EUN1` | Europe Nordic & East |
| `Region.KR` | Korea |
| `Region.BR1` | Brazil |
| `Region.LA1` | Latin America North |
| `Region.LA2` | Latin America South |
| `Region.OC1` | Oceania |
| `Region.JP1` | Japan |
| `Region.TR1` | Turkey |
| `Region.RU` | Russia |
| `Region.PH2` | Philippines |
| `Region.SG2` | Singapore |
| `Region.TH2` | Thailand |
| `Region.TW2` | Taiwan |
| `Region.VN2` | Vietnam |

---

## League of Legends APIs

### Account API

`client.account`

| Method | Description |
|--------|-------------|
| `get_by_puuid(region, puuid)` | Get account by PUUID |
| `get_by_riot_id(region, gameName, tagLine)` | Get account by Riot ID |
| `get_by_access_token(region)` | Get account using RSO token |
| `get_active_shard(region, game, puuid)` | Get active shard for player |

### Summoner API

`client.summoner`

| Method | Description |
|--------|-------------|
| `get_by_puuid(region, encryptedPUUID)` | Get summoner by PUUID |
| `get_by_access_token(region)` | Get summoner using RSO token |

### Match API

`client.match`

| Method | Description |
|--------|-------------|
| `get_match_ids_by_puuid(region, puuid, ...)` | Get list of match IDs |
| `get_match(region, matchId)` | Get match details |
| `get_timeline(region, matchId)` | Get match timeline |
| `get_replay(region, puuid)` | Get player replays |

Optional parameters for `get_match_ids_by_puuid`:

- `count` - Number of matches (default: 20, max: 100)
- `start` - Offset for pagination
- `startTime` / `endTime` - Time filters (epoch seconds)
- `queue` - Queue ID filter
- `type` - Game type filter

### Champion Mastery API

`client.champion_mastery`

| Method | Description |
|--------|-------------|
| `get_all_masteries(region, encryptedPUUID)` | Get all champion masteries |
| `get_by_champion(region, encryptedPUUID, championId)` | Get mastery for champion |
| `get_top_masteries(region, encryptedPUUID, count)` | Get top N masteries |
| `get_mastery_score(region, encryptedPUUID)` | Get total mastery score |

### League API

`client.league`

| Method | Description |
|--------|-------------|
| `get_entries_by_summoner(region, encryptedSummonerId)` | Get ranked entries |
| `get_challenger_league(region, queue)` | Get challenger league |
| `get_grandmaster_league(region, queue)` | Get grandmaster league |
| `get_master_league(region, queue)` | Get master league |

### Spectator API

`client.spectator`

| Method | Description |
|--------|-------------|
| `get_current_game_info(region, encryptedPUUID)` | Get live game data |
| `get_featured_games(region)` | Get featured games |

### Champion API

`client.champion`

| Method | Description |
|--------|-------------|
| `get_champion_rotations(region)` | Get free champion rotation |

### Status API

`client.lol_status`

| Method | Description |
|--------|-------------|
| `get_platform_data(region)` | Get platform status |

---

## TFT APIs

### TFT Summoner API

`client.tft_summoner`

| Method | Description |
|--------|-------------|
| `get_by_puuid(region, encryptedPUUID)` | Get TFT summoner by PUUID |

### TFT Match API

`client.tft_match`

| Method | Description |
|--------|-------------|
| `get_match_ids_by_puuid(region, puuid, count)` | Get TFT match IDs |
| `get_match(region, matchId)` | Get TFT match details |

### TFT League API

`client.tft_league`

| Method | Description |
|--------|-------------|
| `get_challenger_league(region)` | Get TFT challenger league |
| `get_grandmaster_league(region)` | Get TFT grandmaster league |
| `get_master_league(region)` | Get TFT master league |
| `get_entries_by_summoner(region, summonerId)` | Get ranked entries |

### TFT Status API

`client.tft_status`

| Method | Description |
|--------|-------------|
| `get_platform_data(region)` | Get TFT platform status |

---

## VALORANT APIs

### VALORANT Content API

`client.val_content`

| Method | Description |
|--------|-------------|
| `get_content(region, locale)` | Get game content (agents, maps, etc.) |

### VALORANT Ranked API

`client.val_ranked`

| Method | Description |
|--------|-------------|
| `get_leaderboard(region, actId, ...)` | Get ranked leaderboard |

### VALORANT Status API

`client.val_status`

| Method | Description |
|--------|-------------|
| `get_platform_data(region)` | Get VALORANT platform status |

---

## Legends of Runeterra APIs

### LoR Match API

`client.lor_match`

| Method | Description |
|--------|-------------|
| `get_match_ids_by_puuid(region, puuid)` | Get LoR match IDs |
| `get_match(region, matchId)` | Get LoR match details |

### LoR Ranked API

`client.lor_ranked`

| Method | Description |
|--------|-------------|
| `get_leaderboards(region)` | Get LoR leaderboards |

### LoR Status API

`client.lor_status`

| Method | Description |
|--------|-------------|
| `get_platform_data(region)` | Get LoR platform status |

---

## Static Data (Data Dragon)

`client.static`

| Method | Description |
|--------|-------------|
| `get_latest_version()` | Get latest Data Dragon version |
| `get_champion(champion_key)` | Get champion data by ID |
| `get_item(item_id)` | Get item data by ID |

---

## Pagination Helper

```python
from riotskillissue import paginate

async for match_id in paginate(
    client.match.get_match_ids_by_puuid,
    region=Platform.EUROPE,
    puuid="...",
    count=100,       # Items per page
    max_results=500  # Total items to fetch
):
    print(match_id)
```

| Parameter | Description |
|-----------|-------------|
| `method` | The API method to paginate |
| `start` | Initial offset (default: 0) |
| `count` | Items per page (default: 100) |
| `max_results` | Maximum items to yield (default: infinity) |
| `**kwargs` | Arguments passed to the method |

# API reference

The committed `OperationRegistry` is the inventory for generated raw clients,
documentation, validation, and MCP discovery. Each entry records:

- Stable operation ID and Python accessor path
- Game and Riot service
- HTTP method and read/write classification
- Route family and allowed routes
- Authentication mode and scopes
- Keyword-only input schema
- Response adapter, including no-content responses

Use discovery in Python:

```python
from riotskillissue.api.registry import OPERATION_REGISTRY

operation = OPERATION_REGISTRY["match-v5.getMatch"]
print(operation.accessor_path)
print(operation.input_schema)
```

Or call a known operation through the typed raw hierarchy:

```python
match = await riot.raw.lol.match.get_match(match_id="EUW1_...")
```

The raw hierarchy is grouped under:

- `riot.raw.common`
- `riot.raw.lol`
- `riot.raw.tft`
- `riot.raw.valorant`
- `riot.raw.lor`
- `riot.raw.riftbound`

All endpoint parameters are keyword-only snake_case. A `route=` override is
optional when the configured default route can be mapped unambiguously.

## Generated raw operation inventory

This inventory is generated from the same community-maintained OpenAPI contract
as the raw clients and registry.

### Common

#### account

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `account-v1.getByPuuid` | `riot.raw.common.account.get_by_puuid` | GET | regional | api_key | `Account` |
| `account-v1.getByRiotId` | `riot.raw.common.account.get_by_riot_id` | GET | regional | api_key | `Account` |
| `account-v1.getByAccessToken` | `riot.raw.common.account.get_by_access_token` | GET | regional | rso | `Account` |
| `account-v1.getActiveShard` | `riot.raw.common.account.get_active_shard` | GET | regional | api_key | `ActiveShard` |
| `account-v1.getActiveRegion` | `riot.raw.common.account.get_active_region` | GET | regional | api_key | `AccountRegion` |

### League of Legends

#### challenges

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `lol-challenges-v1.getAllChallengeConfigs` | `riot.raw.lol.challenges.get_all_challenge_configs` | GET | platform | api_key | `List[ChallengeConfigInfo]` |
| `lol-challenges-v1.getAllChallengePercentiles` | `riot.raw.lol.challenges.get_all_challenge_percentiles` | GET | platform | api_key | `Dict[str, Dict[str, float]]` |
| `lol-challenges-v1.getChallengeConfigs` | `riot.raw.lol.challenges.get_challenge_configs` | GET | platform | api_key | `ChallengeConfigInfo` |
| `lol-challenges-v1.getChallengeLeaderboards` | `riot.raw.lol.challenges.get_challenge_leaderboards` | GET | platform | api_key | `List[ApexPlayerInfo]` |
| `lol-challenges-v1.getChallengePercentiles` | `riot.raw.lol.challenges.get_challenge_percentiles` | GET | platform | api_key | `Dict[str, float]` |
| `lol-challenges-v1.getPlayerData` | `riot.raw.lol.challenges.get_player_data` | GET | platform | api_key | `PlayerInfo` |

#### champion

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `champion-v3.getChampionInfo` | `riot.raw.lol.champion.get_champion_info` | GET | platform | api_key | `ChampionInfo` |

#### champion_mastery

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `champion-mastery-v4.getAllChampionMasteriesByPUUID` | `riot.raw.lol.champion_mastery.get_all_champion_masteries_by_puuid` | GET | platform | api_key | `List[ChampionMastery]` |
| `champion-mastery-v4.getChampionMasteryByPUUID` | `riot.raw.lol.champion_mastery.get_champion_mastery_by_puuid` | GET | platform | api_key | `ChampionMastery` |
| `champion-mastery-v4.getTopChampionMasteriesByPUUID` | `riot.raw.lol.champion_mastery.get_top_champion_masteries_by_puuid` | GET | platform | api_key | `List[ChampionMastery]` |
| `champion-mastery-v4.getChampionMasteryScoreByPUUID` | `riot.raw.lol.champion_mastery.get_champion_mastery_score_by_puuid` | GET | platform | api_key | `int` |

#### clash

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `clash-v1.getPlayersByPUUID` | `riot.raw.lol.clash.get_players_by_puuid` | GET | platform | api_key | `List[Player]` |
| `clash-v1.getTeamById` | `riot.raw.lol.clash.get_team_by_id` | GET | platform | api_key | `Team` |
| `clash-v1.getTournaments` | `riot.raw.lol.clash.get_tournaments` | GET | platform | api_key | `List[Tournament]` |
| `clash-v1.getTournamentByTeam` | `riot.raw.lol.clash.get_tournament_by_team` | GET | platform | api_key | `Tournament` |
| `clash-v1.getTournamentById` | `riot.raw.lol.clash.get_tournament_by_id` | GET | platform | api_key | `Tournament` |

#### league

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `league-v4.getChallengerLeague` | `riot.raw.lol.league.get_challenger_league` | GET | platform | api_key | `LeagueList` |
| `league-v4.getLeagueEntriesByPUUID` | `riot.raw.lol.league.get_league_entries_by_puuid` | GET | platform | api_key | `List[LeagueEntry]` |
| `league-v4.getLeagueEntries` | `riot.raw.lol.league.get_league_entries` | GET | platform | api_key | `List[LeagueEntry]` |
| `league-v4.getGrandmasterLeague` | `riot.raw.lol.league.get_grandmaster_league` | GET | platform | api_key | `LeagueList` |
| `league-v4.getMasterLeague` | `riot.raw.lol.league.get_master_league` | GET | platform | api_key | `LeagueList` |

#### league_exp

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `league-exp-v4.getLeagueEntries` | `riot.raw.lol.league_exp.get_league_entries` | GET | platform | api_key | `List[LeagueEntry]` |

#### match

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `match-v5.getMatchIdsByPUUID` | `riot.raw.lol.match.get_match_ids_by_puuid` | GET | regional | api_key | `List[str]` |
| `match-v5.getReplay` | `riot.raw.lol.match.get_replay` | GET | regional | api_key | `Replay` |
| `match-v5.getMatch` | `riot.raw.lol.match.get_match` | GET | regional | api_key | `Match` |
| `match-v5.getTimeline` | `riot.raw.lol.match.get_timeline` | GET | regional | api_key | `Timeline` |

#### rso_match

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `lol-rso-match-v1.getMatchIds` | `riot.raw.lol.rso_match.get_match_ids` | GET | regional | rso | `List[str]` |
| `lol-rso-match-v1.getMatch` | `riot.raw.lol.rso_match.get_match` | GET | regional | rso | `Match` |
| `lol-rso-match-v1.getTimeline` | `riot.raw.lol.rso_match.get_timeline` | GET | regional | rso | `Timeline` |

#### spectator

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `spectator-v5.getCurrentGameInfoByPuuid` | `riot.raw.lol.spectator.get_current_game_info_by_puuid` | GET | platform | api_key | `CurrentGameInfo` |

#### status

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `lol-status-v4.getPlatformData` | `riot.raw.lol.status.get_platform_data` | GET | platform | api_key | `PlatformData` |

#### summoner

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `summoner-v4.getByPUUID` | `riot.raw.lol.summoner.get_by_puuid` | GET | platform | api_key | `Summoner` |
| `summoner-v4.getByAccessToken` | `riot.raw.lol.summoner.get_by_access_token` | GET | platform | rso | `Summoner` |

#### tournament

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `tournament-v5.createTournamentCode` | `riot.raw.lol.tournament.create_tournament_code` | POST (write) | regional | api_key | `List[str]` |
| `tournament-v5.getTournamentCode` | `riot.raw.lol.tournament.get_tournament_code` | GET | regional | api_key | `TournamentCodeV5` |
| `tournament-v5.updateCode` | `riot.raw.lol.tournament.update_code` | PUT (write) | regional | api_key | `None` |
| `tournament-v5.getGames` | `riot.raw.lol.tournament.get_games` | GET | regional | api_key | `List[TournamentGamesV5]` |
| `tournament-v5.getLobbyEventsByCode` | `riot.raw.lol.tournament.get_lobby_events_by_code` | GET | regional | api_key | `LobbyEventV5Wrapper` |
| `tournament-v5.registerProviderData` | `riot.raw.lol.tournament.register_provider_data` | POST (write) | regional | api_key | `int` |
| `tournament-v5.registerTournament` | `riot.raw.lol.tournament.register_tournament` | POST (write) | regional | api_key | `int` |

#### tournament_stub

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `tournament-stub-v5.createTournamentCode` | `riot.raw.lol.tournament_stub.create_tournament_code` | POST (write) | regional | api_key | `List[str]` |
| `tournament-stub-v5.getTournamentCode` | `riot.raw.lol.tournament_stub.get_tournament_code` | GET | regional | api_key | `TournamentCodeV5` |
| `tournament-stub-v5.getLobbyEventsByCode` | `riot.raw.lol.tournament_stub.get_lobby_events_by_code` | GET | regional | api_key | `LobbyEventV5Wrapper` |
| `tournament-stub-v5.registerProviderData` | `riot.raw.lol.tournament_stub.register_provider_data` | POST (write) | regional | api_key | `int` |
| `tournament-stub-v5.registerTournament` | `riot.raw.lol.tournament_stub.register_tournament` | POST (write) | regional | api_key | `int` |

### Teamfight Tactics

#### league

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `tft-league-v1.getLeagueEntriesByPUUID` | `riot.raw.tft.league.get_league_entries_by_puuid` | GET | platform | api_key | `List[LeagueEntry]` |
| `tft-league-v1.getChallengerLeague` | `riot.raw.tft.league.get_challenger_league` | GET | platform | api_key | `LeagueList` |
| `tft-league-v1.getLeagueEntries` | `riot.raw.tft.league.get_league_entries` | GET | platform | api_key | `List[LeagueEntry]` |
| `tft-league-v1.getGrandmasterLeague` | `riot.raw.tft.league.get_grandmaster_league` | GET | platform | api_key | `LeagueList` |
| `tft-league-v1.getMasterLeague` | `riot.raw.tft.league.get_master_league` | GET | platform | api_key | `LeagueList` |
| `tft-league-v1.getTopRatedLadder` | `riot.raw.tft.league.get_top_rated_ladder` | GET | platform | api_key | `List[TopRatedLadderEntry]` |

#### match

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `tft-match-v1.getMatchIdsByPUUID` | `riot.raw.tft.match.get_match_ids_by_puuid` | GET | regional | api_key | `List[str]` |
| `tft-match-v1.getMatch` | `riot.raw.tft.match.get_match` | GET | regional | api_key | `Match` |

#### spectator

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `spectator-tft-v5.getCurrentGameInfoByPuuid` | `riot.raw.tft.spectator.get_current_game_info_by_puuid` | GET | platform | api_key | `CurrentGameInfo` |

#### status

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `tft-status-v1.getPlatformData` | `riot.raw.tft.status.get_platform_data` | GET | platform | api_key | `PlatformData` |

#### summoner

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `tft-summoner-v1.getByPUUID` | `riot.raw.tft.summoner.get_by_puuid` | GET | platform | api_key | `Summoner` |
| `tft-summoner-v1.getByAccessToken` | `riot.raw.tft.summoner.get_by_access_token` | GET | platform | rso | `Summoner` |

### VALORANT

#### console_match

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `val-console-match-v1.getMatch` | `riot.raw.valorant.console_match.get_match` | GET | val-platform | api_key | `Match` |
| `val-console-match-v1.getMatchlist` | `riot.raw.valorant.console_match.get_matchlist` | GET | val-platform | api_key | `Matchlist` |
| `val-console-match-v1.getRecent` | `riot.raw.valorant.console_match.get_recent` | GET | val-platform | api_key | `RecentMatches` |

#### console_ranked

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `val-console-ranked-v1.getLeaderboard` | `riot.raw.valorant.console_ranked.get_leaderboard` | GET | val-platform | api_key | `Leaderboard` |

#### content

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `val-content-v1.getContent` | `riot.raw.valorant.content.get_content` | GET | val-platform | api_key | `Content` |

#### match

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `val-match-v1.getMatch` | `riot.raw.valorant.match.get_match` | GET | val-platform | api_key | `Match` |
| `val-match-v1.getMatchlist` | `riot.raw.valorant.match.get_matchlist` | GET | val-platform | api_key | `Matchlist` |
| `val-match-v1.getRecent` | `riot.raw.valorant.match.get_recent` | GET | val-platform | api_key | `RecentMatches` |

#### ranked

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `val-ranked-v1.getLeaderboard` | `riot.raw.valorant.ranked.get_leaderboard` | GET | val-platform | api_key | `Leaderboard` |

#### status

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `val-status-v1.getPlatformData` | `riot.raw.valorant.status.get_platform_data` | GET | val-platform | api_key | `PlatformData` |

### Legends of Runeterra

#### deck

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `lor-deck-v1.getDecks` | `riot.raw.lor.deck.get_decks` | GET | regional | rso | `List[Deck]` |
| `lor-deck-v1.createDeck` | `riot.raw.lor.deck.create_deck` | POST (write) | regional | rso | `str` |

#### inventory

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `lor-inventory-v1.getCards` | `riot.raw.lor.inventory.get_cards` | GET | regional | rso | `List[Card]` |

#### match

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `lor-match-v1.getMatchIdsByPUUID` | `riot.raw.lor.match.get_match_ids_by_puuid` | GET | regional | api_key | `List[str]` |
| `lor-match-v1.getMatch` | `riot.raw.lor.match.get_match` | GET | regional | api_key | `Match` |

#### ranked

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `lor-ranked-v1.getLeaderboards` | `riot.raw.lor.ranked.get_leaderboards` | GET | regional | api_key | `Leaderboard` |

#### status

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `lor-status-v1.getPlatformData` | `riot.raw.lor.status.get_platform_data` | GET | regional | api_key | `PlatformData` |

### Riftbound

#### content

| Operation ID | Python accessor | Method | Route | Auth | Result |
| --- | --- | --- | --- | --- | --- |
| `riftbound-content-v1.getContent` | `riot.raw.riftbound.content.get_content` | GET | regional | api_key | `RiftboundContent` |

### Data Dragon

| Operation ID | Python accessor | Result |
| --- | --- | --- |
| `static.get_latest_version` | `riot.static.get_latest_version` | `str` |
| `static.get_champion` | `riot.static.get_champion` | `Optional[Dict[str, Any]]` |
| `static.get_all_champions` | `riot.static.get_all_champions` | `Dict[int, Dict[str, Any]]` |
| `static.get_item` | `riot.static.get_item` | `Optional[Dict[str, Any]]` |
| `static.get_all_items` | `riot.static.get_all_items` | `Dict[int, Dict[str, Any]]` |
| `static.get_summoner_spells` | `riot.static.get_summoner_spells` | `Dict[int, Dict[str, Any]]` |
| `static.get_summoner_spell` | `riot.static.get_summoner_spell` | `Optional[Dict[str, Any]]` |
| `static.get_runes` | `riot.static.get_runes` | `List[Dict[str, Any]]` |
| `static.get_queues` | `riot.static.get_queues` | `List[Dict[str, Any]]` |
| `static.get_maps` | `riot.static.get_maps` | `List[Dict[str, Any]]` |
| `static.get_game_modes` | `riot.static.get_game_modes` | `List[Dict[str, Any]]` |

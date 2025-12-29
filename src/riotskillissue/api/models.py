# Generated Code. Do not edit.
from __future__ import annotations
from typing import List, Optional, Dict, Any, Union, Literal
from pydantic import BaseModel, Field
from riotskillissue.core.types import Region, Platform


class Error(BaseModel):
    """
    No description provided.
    """
    
    
    status: Optional[Dict[str, Any]] = Field(default=None, alias="status")
    
    


class account_v1_AccountDto(BaseModel):
    """
    No description provided.
    """
    
    
    gameName: Optional[str] = Field(default=None, alias="gameName")
    
    puuid: str = Field(default=None, alias="puuid")
    
    tagLine: Optional[str] = Field(default=None, alias="tagLine")
    
    


class account_v1_AccountRegionDTO(BaseModel):
    """
    Account region
    """
    
    
    game: str = Field(default=None, alias="game")
    
    puuid: str = Field(default=None, alias="puuid")
    
    region: str = Field(default=None, alias="region")
    
    


class account_v1_ActiveShardDto(BaseModel):
    """
    No description provided.
    """
    
    
    activeShard: str = Field(default=None, alias="activeShard")
    
    game: str = Field(default=None, alias="game")
    
    puuid: str = Field(default=None, alias="puuid")
    
    


class champion_mastery_v4_ChampionMasteryDto(BaseModel):
    """
    This object contains single Champion Mastery information for player and champion combination.
    """
    
    
    championId: int = Field(default=None, alias="championId")
    
    championLevel: int = Field(default=None, alias="championLevel")
    
    championPoints: int = Field(default=None, alias="championPoints")
    
    championPointsSinceLastLevel: int = Field(default=None, alias="championPointsSinceLastLevel")
    
    championPointsUntilNextLevel: int = Field(default=None, alias="championPointsUntilNextLevel")
    
    championSeasonMilestone: int = Field(default=None, alias="championSeasonMilestone")
    
    chestGranted: Optional[bool] = Field(default=None, alias="chestGranted")
    
    lastPlayTime: int = Field(default=None, alias="lastPlayTime")
    
    markRequiredForNextLevel: int = Field(default=None, alias="markRequiredForNextLevel")
    
    milestoneGrades: Optional[List[str]] = Field(default=None, alias="milestoneGrades")
    
    nextSeasonMilestone: champion_mastery_v4_NextSeasonMilestonesDto = Field(default=None, alias="nextSeasonMilestone")
    
    puuid: str = Field(default=None, alias="puuid")
    
    tokensEarned: int = Field(default=None, alias="tokensEarned")
    
    


class champion_mastery_v4_NextSeasonMilestonesDto(BaseModel):
    """
    This object contains required next season milestone information.
    """
    
    
    bonus: bool = Field(default=None, alias="bonus")
    
    requireGradeCounts: Dict[str, int] = Field(default=None, alias="requireGradeCounts")
    
    rewardConfig: Optional[champion_mastery_v4_RewardConfigDto] = Field(default=None, alias="rewardConfig")
    
    rewardMarks: int = Field(default=None, alias="rewardMarks")
    
    totalGamesRequires: int = Field(default=None, alias="totalGamesRequires")
    
    


class champion_mastery_v4_RewardConfigDto(BaseModel):
    """
    This object contains required reward config information.
    """
    
    
    maximumReward: int = Field(default=None, alias="maximumReward")
    
    rewardType: str = Field(default=None, alias="rewardType")
    
    rewardValue: str = Field(default=None, alias="rewardValue")
    
    


class champion_v3_ChampionInfo(BaseModel):
    """
    No description provided.
    """
    
    
    freeChampionIds: List[int] = Field(default=None, alias="freeChampionIds")
    
    freeChampionIdsForNewPlayers: List[int] = Field(default=None, alias="freeChampionIdsForNewPlayers")
    
    maxNewPlayerLevel: int = Field(default=None, alias="maxNewPlayerLevel")
    
    


class clash_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    position: str = Field(default=None, alias="position")
    
    puuid: str = Field(default=None, alias="puuid")
    
    role: str = Field(default=None, alias="role")
    
    teamId: Optional[str] = Field(default=None, alias="teamId")
    
    


class clash_v1_TeamDto(BaseModel):
    """
    No description provided.
    """
    
    
    abbreviation: str = Field(default=None, alias="abbreviation")
    
    captain: str = Field(default=None, alias="captain")
    
    iconId: int = Field(default=None, alias="iconId")
    
    id: str = Field(default=None, alias="id")
    
    name: str = Field(default=None, alias="name")
    
    players: List[clash_v1_PlayerDto] = Field(default=None, alias="players")
    
    tier: int = Field(default=None, alias="tier")
    
    tournamentId: int = Field(default=None, alias="tournamentId")
    
    


class clash_v1_TournamentDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: int = Field(default=None, alias="id")
    
    nameKey: str = Field(default=None, alias="nameKey")
    
    nameKeySecondary: str = Field(default=None, alias="nameKeySecondary")
    
    schedule: List[clash_v1_TournamentPhaseDto] = Field(default=None, alias="schedule")
    
    themeId: int = Field(default=None, alias="themeId")
    
    


class clash_v1_TournamentPhaseDto(BaseModel):
    """
    No description provided.
    """
    
    
    cancelled: bool = Field(default=None, alias="cancelled")
    
    id: int = Field(default=None, alias="id")
    
    registrationTime: int = Field(default=None, alias="registrationTime")
    
    startTime: int = Field(default=None, alias="startTime")
    
    


class league_exp_v4_LeagueEntryDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: bool = Field(default=None, alias="freshBlood")
    
    hotStreak: bool = Field(default=None, alias="hotStreak")
    
    inactive: bool = Field(default=None, alias="inactive")
    
    leagueId: str = Field(default=None, alias="leagueId")
    
    leaguePoints: int = Field(default=None, alias="leaguePoints")
    
    losses: int = Field(default=None, alias="losses")
    
    miniSeries: Optional[league_exp_v4_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    puuid: str = Field(default=None, alias="puuid")
    
    queueType: str = Field(default=None, alias="queueType")
    
    rank: str = Field(default=None, alias="rank")
    
    summonerId: Optional[str] = Field(default=None, alias="summonerId")
    
    tier: str = Field(default=None, alias="tier")
    
    veteran: bool = Field(default=None, alias="veteran")
    
    wins: int = Field(default=None, alias="wins")
    
    


class league_exp_v4_MiniSeriesDTO(BaseModel):
    """
    No description provided.
    """
    
    
    losses: int = Field(default=None, alias="losses")
    
    progress: str = Field(default=None, alias="progress")
    
    target: int = Field(default=None, alias="target")
    
    wins: int = Field(default=None, alias="wins")
    
    


class league_v4_LeagueEntryDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: bool = Field(default=None, alias="freshBlood")
    
    hotStreak: bool = Field(default=None, alias="hotStreak")
    
    inactive: bool = Field(default=None, alias="inactive")
    
    leagueId: Optional[str] = Field(default=None, alias="leagueId")
    
    leaguePoints: int = Field(default=None, alias="leaguePoints")
    
    losses: int = Field(default=None, alias="losses")
    
    miniSeries: Optional[league_v4_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    puuid: str = Field(default=None, alias="puuid")
    
    queueType: str = Field(default=None, alias="queueType")
    
    rank: Optional[str] = Field(default=None, alias="rank")
    
    summonerId: Optional[str] = Field(default=None, alias="summonerId")
    
    tier: Optional[str] = Field(default=None, alias="tier")
    
    veteran: bool = Field(default=None, alias="veteran")
    
    wins: int = Field(default=None, alias="wins")
    
    


class league_v4_LeagueItemDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: bool = Field(default=None, alias="freshBlood")
    
    hotStreak: bool = Field(default=None, alias="hotStreak")
    
    inactive: bool = Field(default=None, alias="inactive")
    
    leaguePoints: int = Field(default=None, alias="leaguePoints")
    
    losses: int = Field(default=None, alias="losses")
    
    miniSeries: Optional[league_v4_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    puuid: str = Field(default=None, alias="puuid")
    
    rank: str = Field(default=None, alias="rank")
    
    summonerId: Optional[str] = Field(default=None, alias="summonerId")
    
    veteran: bool = Field(default=None, alias="veteran")
    
    wins: int = Field(default=None, alias="wins")
    
    


class league_v4_LeagueListDTO(BaseModel):
    """
    No description provided.
    """
    
    
    entries: List[league_v4_LeagueItemDTO] = Field(default=None, alias="entries")
    
    leagueId: Optional[str] = Field(default=None, alias="leagueId")
    
    name: Optional[str] = Field(default=None, alias="name")
    
    queue: Optional[str] = Field(default=None, alias="queue")
    
    tier: str = Field(default=None, alias="tier")
    
    


class league_v4_MiniSeriesDTO(BaseModel):
    """
    No description provided.
    """
    
    
    losses: int = Field(default=None, alias="losses")
    
    progress: str = Field(default=None, alias="progress")
    
    target: int = Field(default=None, alias="target")
    
    wins: int = Field(default=None, alias="wins")
    
    


class lol_challenges_v1_ApexPlayerInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    position: int = Field(default=None, alias="position")
    
    puuid: str = Field(default=None, alias="puuid")
    
    value: float = Field(default=None, alias="value")
    
    


class lol_challenges_v1_ChallengeConfigInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    endTimestamp: Optional[int] = Field(default=None, alias="endTimestamp")
    
    id: int = Field(default=None, alias="id")
    
    leaderboard: bool = Field(default=None, alias="leaderboard")
    
    localizedNames: Dict[str, Dict[str, str]] = Field(default=None, alias="localizedNames")
    
    startTimestamp: Optional[int] = Field(default=None, alias="startTimestamp")
    
    state: str = Field(default=None, alias="state")
    
    thresholds: Dict[str, float] = Field(default=None, alias="thresholds")
    
    tracking: Optional[str] = Field(default=None, alias="tracking")
    
    


class lol_challenges_v1_ChallengeInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    achievedTime: Optional[int] = Field(default=None, alias="achievedTime")
    
    challengeId: int = Field(default=None, alias="challengeId")
    
    level: str = Field(default=None, alias="level")
    
    percentile: float = Field(default=None, alias="percentile")
    
    playersInLevel: Optional[int] = Field(default=None, alias="playersInLevel")
    
    position: Optional[int] = Field(default=None, alias="position")
    
    value: float = Field(default=None, alias="value")
    
    


class lol_challenges_v1_ChallengePointDto(BaseModel):
    """
    No description provided.
    """
    
    
    current: int = Field(default=None, alias="current")
    
    level: str = Field(default=None, alias="level")
    
    max: int = Field(default=None, alias="max")
    
    percentile: Optional[float] = Field(default=None, alias="percentile")
    
    


class lol_challenges_v1_Level(BaseModel):
    """
    0 NONE,
1 IRON,
2 BRONZE,
3 SILVER,
4 GOLD,
5 PLATINUM,
6 DIAMOND,
7 MASTER,
8 GRANDMASTER,
9 CHALLENGER
    """
    
    
    


class lol_challenges_v1_PlayerClientPreferencesDto(BaseModel):
    """
    No description provided.
    """
    
    
    bannerAccent: Optional[str] = Field(default=None, alias="bannerAccent")
    
    challengeIds: Optional[List[int]] = Field(default=None, alias="challengeIds")
    
    crestBorder: Optional[str] = Field(default=None, alias="crestBorder")
    
    prestigeCrestBorderLevel: Optional[int] = Field(default=None, alias="prestigeCrestBorderLevel")
    
    title: Optional[str] = Field(default=None, alias="title")
    
    


class lol_challenges_v1_PlayerInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    categoryPoints: Dict[str, lol_challenges_v1_ChallengePointDto] = Field(default=None, alias="categoryPoints")
    
    challenges: List[lol_challenges_v1_ChallengeInfoDto] = Field(default=None, alias="challenges")
    
    preferences: lol_challenges_v1_PlayerClientPreferencesDto = Field(default=None, alias="preferences")
    
    totalPoints: lol_challenges_v1_ChallengePointDto = Field(default=None, alias="totalPoints")
    
    


class lol_challenges_v1_State(BaseModel):
    """
    DISABLED - not visible and not calculated,
HIDDEN - not visible, but calculated,
ENABLED - visible and calculated,
ARCHIVED - visible, but not calculated
    """
    
    
    


class lol_challenges_v1_Tracking(BaseModel):
    """
    LIFETIME - stats are incremented without reset,
SEASON - stats are accumulated by season and reset at the beginning of new season
    """
    
    
    


class lol_rso_match_v1_MatchDto(BaseModel):
    """
    UNKNOWN TYPE.
    """
    
    
    


class lol_rso_match_v1_TimelineDto(BaseModel):
    """
    UNKNOWN TYPE.
    """
    
    
    


class lol_status_v4_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    content: str = Field(default=None, alias="content")
    
    locale: str = Field(default=None, alias="locale")
    
    


class lol_status_v4_PlatformDataDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(default=None, alias="id")
    
    incidents: List[lol_status_v4_StatusDto] = Field(default=None, alias="incidents")
    
    locales: List[str] = Field(default=None, alias="locales")
    
    maintenances: List[lol_status_v4_StatusDto] = Field(default=None, alias="maintenances")
    
    name: str = Field(default=None, alias="name")
    
    


class lol_status_v4_StatusDto(BaseModel):
    """
    No description provided.
    """
    
    
    archive_at: Optional[str] = Field(default=None, alias="archive_at")
    
    created_at: str = Field(default=None, alias="created_at")
    
    id: int = Field(default=None, alias="id")
    
    incident_severity: Optional[str] = Field(default=None, alias="incident_severity")
    
    maintenance_status: Optional[str] = Field(default=None, alias="maintenance_status")
    
    platforms: List[str] = Field(default=None, alias="platforms")
    
    titles: List[lol_status_v4_ContentDto] = Field(default=None, alias="titles")
    
    updated_at: Optional[str] = Field(default=None, alias="updated_at")
    
    updates: List[lol_status_v4_UpdateDto] = Field(default=None, alias="updates")
    
    


class lol_status_v4_UpdateDto(BaseModel):
    """
    No description provided.
    """
    
    
    author: str = Field(default=None, alias="author")
    
    created_at: str = Field(default=None, alias="created_at")
    
    id: int = Field(default=None, alias="id")
    
    publish: bool = Field(default=None, alias="publish")
    
    publish_locations: List[str] = Field(default=None, alias="publish_locations")
    
    translations: List[lol_status_v4_ContentDto] = Field(default=None, alias="translations")
    
    updated_at: str = Field(default=None, alias="updated_at")
    
    


class lor_deck_v1_DeckDto(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(default=None, alias="code")
    
    id: str = Field(default=None, alias="id")
    
    name: str = Field(default=None, alias="name")
    
    


class lor_deck_v1_NewDeckDto(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(default=None, alias="code")
    
    name: str = Field(default=None, alias="name")
    
    


class lor_inventory_v1_CardDto(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(default=None, alias="code")
    
    count: str = Field(default=None, alias="count")
    
    


class lor_match_v1_InfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    game_format: str = Field(default=None, alias="game_format")
    
    game_mode: str = Field(default=None, alias="game_mode")
    
    game_start_time_utc: str = Field(default=None, alias="game_start_time_utc")
    
    game_type: str = Field(default=None, alias="game_type")
    
    game_version: str = Field(default=None, alias="game_version")
    
    players: List[lor_match_v1_PlayerDto] = Field(default=None, alias="players")
    
    total_turn_count: int = Field(default=None, alias="total_turn_count")
    
    


class lor_match_v1_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    info: lor_match_v1_InfoDto = Field(default=None, alias="info")
    
    metadata: lor_match_v1_MetadataDto = Field(default=None, alias="metadata")
    
    


class lor_match_v1_MetadataDto(BaseModel):
    """
    No description provided.
    """
    
    
    data_version: str = Field(default=None, alias="data_version")
    
    match_id: str = Field(default=None, alias="match_id")
    
    participants: List[str] = Field(default=None, alias="participants")
    
    


class lor_match_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    deck_code: str = Field(default=None, alias="deck_code")
    
    deck_id: str = Field(default=None, alias="deck_id")
    
    factions: List[str] = Field(default=None, alias="factions")
    
    game_outcome: str = Field(default=None, alias="game_outcome")
    
    order_of_play: int = Field(default=None, alias="order_of_play")
    
    puuid: str = Field(default=None, alias="puuid")
    
    


class lor_ranked_v1_LeaderboardDto(BaseModel):
    """
    No description provided.
    """
    
    
    players: List[lor_ranked_v1_PlayerDto] = Field(default=None, alias="players")
    
    


class lor_ranked_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    lp: int = Field(default=None, alias="lp")
    
    name: str = Field(default=None, alias="name")
    
    rank: int = Field(default=None, alias="rank")
    
    


class lor_status_v1_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    content: str = Field(default=None, alias="content")
    
    locale: str = Field(default=None, alias="locale")
    
    


class lor_status_v1_PlatformDataDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(default=None, alias="id")
    
    incidents: List[lor_status_v1_StatusDto] = Field(default=None, alias="incidents")
    
    locales: List[str] = Field(default=None, alias="locales")
    
    maintenances: List[lor_status_v1_StatusDto] = Field(default=None, alias="maintenances")
    
    name: str = Field(default=None, alias="name")
    
    


class lor_status_v1_StatusDto(BaseModel):
    """
    No description provided.
    """
    
    
    archive_at: str = Field(default=None, alias="archive_at")
    
    created_at: str = Field(default=None, alias="created_at")
    
    id: int = Field(default=None, alias="id")
    
    incident_severity: str = Field(default=None, alias="incident_severity")
    
    maintenance_status: str = Field(default=None, alias="maintenance_status")
    
    platforms: List[str] = Field(default=None, alias="platforms")
    
    titles: List[lor_status_v1_ContentDto] = Field(default=None, alias="titles")
    
    updated_at: str = Field(default=None, alias="updated_at")
    
    updates: List[lor_status_v1_UpdateDto] = Field(default=None, alias="updates")
    
    


class lor_status_v1_UpdateDto(BaseModel):
    """
    No description provided.
    """
    
    
    author: str = Field(default=None, alias="author")
    
    created_at: str = Field(default=None, alias="created_at")
    
    id: int = Field(default=None, alias="id")
    
    publish: bool = Field(default=None, alias="publish")
    
    publish_locations: List[str] = Field(default=None, alias="publish_locations")
    
    translations: List[lor_status_v1_ContentDto] = Field(default=None, alias="translations")
    
    updated_at: str = Field(default=None, alias="updated_at")
    
    


class match_v5_BanDto(BaseModel):
    """
    No description provided.
    """
    
    
    championId: int = Field(default=None, alias="championId")
    
    pickTurn: int = Field(default=None, alias="pickTurn")
    
    


class match_v5_ChallengesDto(BaseModel):
    """
    Challenges DTO
    """
    
    
    param_12AssistStreakCount: Optional[int] = Field(default=None, alias="12AssistStreakCount")
    
    HealFromMapSources: Optional[float] = Field(default=None, alias="HealFromMapSources")
    
    InfernalScalePickup: Optional[int] = Field(default=None, alias="InfernalScalePickup")
    
    SWARM_DefeatAatrox: Optional[int] = Field(default=None, alias="SWARM_DefeatAatrox")
    
    SWARM_DefeatBriar: Optional[int] = Field(default=None, alias="SWARM_DefeatBriar")
    
    SWARM_DefeatMiniBosses: Optional[int] = Field(default=None, alias="SWARM_DefeatMiniBosses")
    
    SWARM_EvolveWeapon: Optional[int] = Field(default=None, alias="SWARM_EvolveWeapon")
    
    SWARM_Have3Passives: Optional[int] = Field(default=None, alias="SWARM_Have3Passives")
    
    SWARM_KillEnemy: Optional[int] = Field(default=None, alias="SWARM_KillEnemy")
    
    SWARM_PickupGold: Optional[float] = Field(default=None, alias="SWARM_PickupGold")
    
    SWARM_ReachLevel50: Optional[int] = Field(default=None, alias="SWARM_ReachLevel50")
    
    SWARM_Survive15Min: Optional[int] = Field(default=None, alias="SWARM_Survive15Min")
    
    SWARM_WinWith5EvolvedWeapons: Optional[int] = Field(default=None, alias="SWARM_WinWith5EvolvedWeapons")
    
    abilityUses: Optional[int] = Field(default=None, alias="abilityUses")
    
    acesBefore15Minutes: Optional[int] = Field(default=None, alias="acesBefore15Minutes")
    
    alliedJungleMonsterKills: Optional[float] = Field(default=None, alias="alliedJungleMonsterKills")
    
    baronBuffGoldAdvantageOverThreshold: Optional[int] = Field(default=None, alias="baronBuffGoldAdvantageOverThreshold")
    
    baronTakedowns: Optional[int] = Field(default=None, alias="baronTakedowns")
    
    blastConeOppositeOpponentCount: Optional[int] = Field(default=None, alias="blastConeOppositeOpponentCount")
    
    bountyGold: Optional[float] = Field(default=None, alias="bountyGold")
    
    buffsStolen: Optional[int] = Field(default=None, alias="buffsStolen")
    
    completeSupportQuestInTime: Optional[int] = Field(default=None, alias="completeSupportQuestInTime")
    
    controlWardTimeCoverageInRiverOrEnemyHalf: Optional[float] = Field(default=None, alias="controlWardTimeCoverageInRiverOrEnemyHalf")
    
    controlWardsPlaced: Optional[int] = Field(default=None, alias="controlWardsPlaced")
    
    damagePerMinute: Optional[float] = Field(default=None, alias="damagePerMinute")
    
    damageTakenOnTeamPercentage: Optional[float] = Field(default=None, alias="damageTakenOnTeamPercentage")
    
    dancedWithRiftHerald: Optional[int] = Field(default=None, alias="dancedWithRiftHerald")
    
    deathsByEnemyChamps: Optional[int] = Field(default=None, alias="deathsByEnemyChamps")
    
    dodgeSkillShotsSmallWindow: Optional[int] = Field(default=None, alias="dodgeSkillShotsSmallWindow")
    
    doubleAces: Optional[int] = Field(default=None, alias="doubleAces")
    
    dragonTakedowns: Optional[int] = Field(default=None, alias="dragonTakedowns")
    
    earliestBaron: Optional[float] = Field(default=None, alias="earliestBaron")
    
    earliestDragonTakedown: Optional[float] = Field(default=None, alias="earliestDragonTakedown")
    
    earliestElderDragon: Optional[float] = Field(default=None, alias="earliestElderDragon")
    
    earlyLaningPhaseGoldExpAdvantage: Optional[float] = Field(default=None, alias="earlyLaningPhaseGoldExpAdvantage")
    
    effectiveHealAndShielding: Optional[float] = Field(default=None, alias="effectiveHealAndShielding")
    
    elderDragonKillsWithOpposingSoul: Optional[int] = Field(default=None, alias="elderDragonKillsWithOpposingSoul")
    
    elderDragonMultikills: Optional[int] = Field(default=None, alias="elderDragonMultikills")
    
    enemyChampionImmobilizations: Optional[int] = Field(default=None, alias="enemyChampionImmobilizations")
    
    enemyJungleMonsterKills: Optional[float] = Field(default=None, alias="enemyJungleMonsterKills")
    
    epicMonsterKillsNearEnemyJungler: Optional[int] = Field(default=None, alias="epicMonsterKillsNearEnemyJungler")
    
    epicMonsterKillsWithin30SecondsOfSpawn: Optional[int] = Field(default=None, alias="epicMonsterKillsWithin30SecondsOfSpawn")
    
    epicMonsterSteals: Optional[int] = Field(default=None, alias="epicMonsterSteals")
    
    epicMonsterStolenWithoutSmite: Optional[int] = Field(default=None, alias="epicMonsterStolenWithoutSmite")
    
    fasterSupportQuestCompletion: Optional[int] = Field(default=None, alias="fasterSupportQuestCompletion")
    
    fastestLegendary: Optional[float] = Field(default=None, alias="fastestLegendary")
    
    firstTurretKilled: Optional[float] = Field(default=None, alias="firstTurretKilled")
    
    firstTurretKilledTime: Optional[float] = Field(default=None, alias="firstTurretKilledTime")
    
    fistBumpParticipation: Optional[int] = Field(default=None, alias="fistBumpParticipation")
    
    flawlessAces: Optional[int] = Field(default=None, alias="flawlessAces")
    
    fullTeamTakedown: Optional[int] = Field(default=None, alias="fullTeamTakedown")
    
    gameLength: Optional[float] = Field(default=None, alias="gameLength")
    
    getTakedownsInAllLanesEarlyJungleAsLaner: Optional[int] = Field(default=None, alias="getTakedownsInAllLanesEarlyJungleAsLaner")
    
    goldPerMinute: Optional[float] = Field(default=None, alias="goldPerMinute")
    
    hadAfkTeammate: Optional[int] = Field(default=None, alias="hadAfkTeammate")
    
    hadOpenNexus: Optional[int] = Field(default=None, alias="hadOpenNexus")
    
    highestChampionDamage: Optional[int] = Field(default=None, alias="highestChampionDamage")
    
    highestCrowdControlScore: Optional[int] = Field(default=None, alias="highestCrowdControlScore")
    
    highestWardKills: Optional[int] = Field(default=None, alias="highestWardKills")
    
    immobilizeAndKillWithAlly: Optional[int] = Field(default=None, alias="immobilizeAndKillWithAlly")
    
    initialBuffCount: Optional[int] = Field(default=None, alias="initialBuffCount")
    
    initialCrabCount: Optional[int] = Field(default=None, alias="initialCrabCount")
    
    jungleCsBefore10Minutes: Optional[float] = Field(default=None, alias="jungleCsBefore10Minutes")
    
    junglerKillsEarlyJungle: Optional[int] = Field(default=None, alias="junglerKillsEarlyJungle")
    
    junglerTakedownsNearDamagedEpicMonster: Optional[int] = Field(default=None, alias="junglerTakedownsNearDamagedEpicMonster")
    
    kTurretsDestroyedBeforePlatesFall: Optional[int] = Field(default=None, alias="kTurretsDestroyedBeforePlatesFall")
    
    kda: Optional[float] = Field(default=None, alias="kda")
    
    killAfterHiddenWithAlly: Optional[int] = Field(default=None, alias="killAfterHiddenWithAlly")
    
    killParticipation: Optional[float] = Field(default=None, alias="killParticipation")
    
    killedChampTookFullTeamDamageSurvived: Optional[int] = Field(default=None, alias="killedChampTookFullTeamDamageSurvived")
    
    killingSprees: Optional[int] = Field(default=None, alias="killingSprees")
    
    killsNearEnemyTurret: Optional[int] = Field(default=None, alias="killsNearEnemyTurret")
    
    killsOnLanersEarlyJungleAsJungler: Optional[int] = Field(default=None, alias="killsOnLanersEarlyJungleAsJungler")
    
    killsOnOtherLanesEarlyJungleAsLaner: Optional[int] = Field(default=None, alias="killsOnOtherLanesEarlyJungleAsLaner")
    
    killsOnRecentlyHealedByAramPack: Optional[int] = Field(default=None, alias="killsOnRecentlyHealedByAramPack")
    
    killsUnderOwnTurret: Optional[int] = Field(default=None, alias="killsUnderOwnTurret")
    
    killsWithHelpFromEpicMonster: Optional[int] = Field(default=None, alias="killsWithHelpFromEpicMonster")
    
    knockEnemyIntoTeamAndKill: Optional[int] = Field(default=None, alias="knockEnemyIntoTeamAndKill")
    
    landSkillShotsEarlyGame: Optional[int] = Field(default=None, alias="landSkillShotsEarlyGame")
    
    laneMinionsFirst10Minutes: Optional[int] = Field(default=None, alias="laneMinionsFirst10Minutes")
    
    laningPhaseGoldExpAdvantage: Optional[int] = Field(default=None, alias="laningPhaseGoldExpAdvantage")
    
    legendaryCount: Optional[int] = Field(default=None, alias="legendaryCount")
    
    legendaryItemUsed: Optional[List[int]] = Field(default=None, alias="legendaryItemUsed")
    
    lostAnInhibitor: Optional[int] = Field(default=None, alias="lostAnInhibitor")
    
    maxCsAdvantageOnLaneOpponent: Optional[float] = Field(default=None, alias="maxCsAdvantageOnLaneOpponent")
    
    maxKillDeficit: Optional[int] = Field(default=None, alias="maxKillDeficit")
    
    maxLevelLeadLaneOpponent: Optional[int] = Field(default=None, alias="maxLevelLeadLaneOpponent")
    
    mejaisFullStackInTime: Optional[int] = Field(default=None, alias="mejaisFullStackInTime")
    
    moreEnemyJungleThanOpponent: Optional[float] = Field(default=None, alias="moreEnemyJungleThanOpponent")
    
    mostWardsDestroyedOneSweeper: Optional[int] = Field(default=None, alias="mostWardsDestroyedOneSweeper")
    
    multiKillOneSpell: Optional[int] = Field(default=None, alias="multiKillOneSpell")
    
    multiTurretRiftHeraldCount: Optional[int] = Field(default=None, alias="multiTurretRiftHeraldCount")
    
    multikills: Optional[int] = Field(default=None, alias="multikills")
    
    multikillsAfterAggressiveFlash: Optional[int] = Field(default=None, alias="multikillsAfterAggressiveFlash")
    
    mythicItemUsed: Optional[int] = Field(default=None, alias="mythicItemUsed")
    
    outerTurretExecutesBefore10Minutes: Optional[int] = Field(default=None, alias="outerTurretExecutesBefore10Minutes")
    
    outnumberedKills: Optional[int] = Field(default=None, alias="outnumberedKills")
    
    outnumberedNexusKill: Optional[int] = Field(default=None, alias="outnumberedNexusKill")
    
    perfectDragonSoulsTaken: Optional[int] = Field(default=None, alias="perfectDragonSoulsTaken")
    
    perfectGame: Optional[int] = Field(default=None, alias="perfectGame")
    
    pickKillWithAlly: Optional[int] = Field(default=None, alias="pickKillWithAlly")
    
    playedChampSelectPosition: Optional[int] = Field(default=None, alias="playedChampSelectPosition")
    
    poroExplosions: Optional[int] = Field(default=None, alias="poroExplosions")
    
    quickCleanse: Optional[int] = Field(default=None, alias="quickCleanse")
    
    quickFirstTurret: Optional[int] = Field(default=None, alias="quickFirstTurret")
    
    quickSoloKills: Optional[int] = Field(default=None, alias="quickSoloKills")
    
    riftHeraldTakedowns: Optional[int] = Field(default=None, alias="riftHeraldTakedowns")
    
    saveAllyFromDeath: Optional[int] = Field(default=None, alias="saveAllyFromDeath")
    
    scuttleCrabKills: Optional[int] = Field(default=None, alias="scuttleCrabKills")
    
    shortestTimeToAceFromFirstTakedown: Optional[float] = Field(default=None, alias="shortestTimeToAceFromFirstTakedown")
    
    skillshotsDodged: Optional[int] = Field(default=None, alias="skillshotsDodged")
    
    skillshotsHit: Optional[int] = Field(default=None, alias="skillshotsHit")
    
    snowballsHit: Optional[int] = Field(default=None, alias="snowballsHit")
    
    soloBaronKills: Optional[int] = Field(default=None, alias="soloBaronKills")
    
    soloKills: Optional[int] = Field(default=None, alias="soloKills")
    
    soloTurretsLategame: Optional[int] = Field(default=None, alias="soloTurretsLategame")
    
    stealthWardsPlaced: Optional[int] = Field(default=None, alias="stealthWardsPlaced")
    
    survivedSingleDigitHpCount: Optional[int] = Field(default=None, alias="survivedSingleDigitHpCount")
    
    survivedThreeImmobilizesInFight: Optional[int] = Field(default=None, alias="survivedThreeImmobilizesInFight")
    
    takedownOnFirstTurret: Optional[int] = Field(default=None, alias="takedownOnFirstTurret")
    
    takedowns: Optional[int] = Field(default=None, alias="takedowns")
    
    takedownsAfterGainingLevelAdvantage: Optional[int] = Field(default=None, alias="takedownsAfterGainingLevelAdvantage")
    
    takedownsBeforeJungleMinionSpawn: Optional[int] = Field(default=None, alias="takedownsBeforeJungleMinionSpawn")
    
    takedownsFirst25Minutes: Optional[int] = Field(default=None, alias="takedownsFirst25Minutes")
    
    takedownsFirstXMinutes: Optional[int] = Field(default=None, alias="takedownsFirstXMinutes")
    
    takedownsInAlcove: Optional[int] = Field(default=None, alias="takedownsInAlcove")
    
    takedownsInEnemyFountain: Optional[int] = Field(default=None, alias="takedownsInEnemyFountain")
    
    teamBaronKills: Optional[int] = Field(default=None, alias="teamBaronKills")
    
    teamDamagePercentage: Optional[float] = Field(default=None, alias="teamDamagePercentage")
    
    teamElderDragonKills: Optional[int] = Field(default=None, alias="teamElderDragonKills")
    
    teamRiftHeraldKills: Optional[int] = Field(default=None, alias="teamRiftHeraldKills")
    
    teleportTakedowns: Optional[int] = Field(default=None, alias="teleportTakedowns")
    
    thirdInhibitorDestroyedTime: Optional[float] = Field(default=None, alias="thirdInhibitorDestroyedTime")
    
    threeWardsOneSweeperCount: Optional[int] = Field(default=None, alias="threeWardsOneSweeperCount")
    
    tookLargeDamageSurvived: Optional[int] = Field(default=None, alias="tookLargeDamageSurvived")
    
    turretPlatesTaken: Optional[int] = Field(default=None, alias="turretPlatesTaken")
    
    turretTakedowns: Optional[int] = Field(default=None, alias="turretTakedowns")
    
    turretsTakenWithRiftHerald: Optional[int] = Field(default=None, alias="turretsTakenWithRiftHerald")
    
    twentyMinionsIn3SecondsCount: Optional[int] = Field(default=None, alias="twentyMinionsIn3SecondsCount")
    
    twoWardsOneSweeperCount: Optional[int] = Field(default=None, alias="twoWardsOneSweeperCount")
    
    unseenRecalls: Optional[int] = Field(default=None, alias="unseenRecalls")
    
    visionScoreAdvantageLaneOpponent: Optional[float] = Field(default=None, alias="visionScoreAdvantageLaneOpponent")
    
    visionScorePerMinute: Optional[float] = Field(default=None, alias="visionScorePerMinute")
    
    voidMonsterKill: Optional[int] = Field(default=None, alias="voidMonsterKill")
    
    wardTakedowns: Optional[int] = Field(default=None, alias="wardTakedowns")
    
    wardTakedownsBefore20M: Optional[int] = Field(default=None, alias="wardTakedownsBefore20M")
    
    wardsGuarded: Optional[int] = Field(default=None, alias="wardsGuarded")
    
    


class match_v5_ChampionStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    abilityHaste: Optional[int] = Field(default=None, alias="abilityHaste")
    
    abilityPower: int = Field(default=None, alias="abilityPower")
    
    armor: int = Field(default=None, alias="armor")
    
    armorPen: int = Field(default=None, alias="armorPen")
    
    armorPenPercent: int = Field(default=None, alias="armorPenPercent")
    
    attackDamage: int = Field(default=None, alias="attackDamage")
    
    attackSpeed: int = Field(default=None, alias="attackSpeed")
    
    bonusArmorPenPercent: int = Field(default=None, alias="bonusArmorPenPercent")
    
    bonusMagicPenPercent: int = Field(default=None, alias="bonusMagicPenPercent")
    
    ccReduction: int = Field(default=None, alias="ccReduction")
    
    cooldownReduction: int = Field(default=None, alias="cooldownReduction")
    
    health: int = Field(default=None, alias="health")
    
    healthMax: int = Field(default=None, alias="healthMax")
    
    healthRegen: int = Field(default=None, alias="healthRegen")
    
    lifesteal: int = Field(default=None, alias="lifesteal")
    
    magicPen: int = Field(default=None, alias="magicPen")
    
    magicPenPercent: int = Field(default=None, alias="magicPenPercent")
    
    magicResist: int = Field(default=None, alias="magicResist")
    
    movementSpeed: int = Field(default=None, alias="movementSpeed")
    
    omnivamp: Optional[int] = Field(default=None, alias="omnivamp")
    
    physicalVamp: Optional[int] = Field(default=None, alias="physicalVamp")
    
    power: int = Field(default=None, alias="power")
    
    powerMax: int = Field(default=None, alias="powerMax")
    
    powerRegen: int = Field(default=None, alias="powerRegen")
    
    spellVamp: int = Field(default=None, alias="spellVamp")
    
    


class match_v5_DamageStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    magicDamageDone: int = Field(default=None, alias="magicDamageDone")
    
    magicDamageDoneToChampions: int = Field(default=None, alias="magicDamageDoneToChampions")
    
    magicDamageTaken: int = Field(default=None, alias="magicDamageTaken")
    
    physicalDamageDone: int = Field(default=None, alias="physicalDamageDone")
    
    physicalDamageDoneToChampions: int = Field(default=None, alias="physicalDamageDoneToChampions")
    
    physicalDamageTaken: int = Field(default=None, alias="physicalDamageTaken")
    
    totalDamageDone: int = Field(default=None, alias="totalDamageDone")
    
    totalDamageDoneToChampions: int = Field(default=None, alias="totalDamageDoneToChampions")
    
    totalDamageTaken: int = Field(default=None, alias="totalDamageTaken")
    
    trueDamageDone: int = Field(default=None, alias="trueDamageDone")
    
    trueDamageDoneToChampions: int = Field(default=None, alias="trueDamageDoneToChampions")
    
    trueDamageTaken: int = Field(default=None, alias="trueDamageTaken")
    
    


class match_v5_EventsTimeLineDto(BaseModel):
    """
    No description provided.
    """
    
    
    actualStartTime: Optional[int] = Field(default=None, alias="actualStartTime")
    
    afterId: Optional[int] = Field(default=None, alias="afterId")
    
    assistingParticipantIds: Optional[List[int]] = Field(default=None, alias="assistingParticipantIds")
    
    beforeId: Optional[int] = Field(default=None, alias="beforeId")
    
    bounty: Optional[int] = Field(default=None, alias="bounty")
    
    buildingType: Optional[str] = Field(default=None, alias="buildingType")
    
    creatorId: Optional[int] = Field(default=None, alias="creatorId")
    
    featType: Optional[int] = Field(default=None, alias="featType")
    
    featValue: Optional[int] = Field(default=None, alias="featValue")
    
    gameId: Optional[int] = Field(default=None, alias="gameId")
    
    goldGain: Optional[int] = Field(default=None, alias="goldGain")
    
    itemId: Optional[int] = Field(default=None, alias="itemId")
    
    killStreakLength: Optional[int] = Field(default=None, alias="killStreakLength")
    
    killType: Optional[str] = Field(default=None, alias="killType")
    
    killerId: Optional[int] = Field(default=None, alias="killerId")
    
    killerTeamId: Optional[int] = Field(default=None, alias="killerTeamId")
    
    laneType: Optional[str] = Field(default=None, alias="laneType")
    
    level: Optional[int] = Field(default=None, alias="level")
    
    levelUpType: Optional[str] = Field(default=None, alias="levelUpType")
    
    monsterSubType: Optional[str] = Field(default=None, alias="monsterSubType")
    
    monsterType: Optional[str] = Field(default=None, alias="monsterType")
    
    multiKillLength: Optional[int] = Field(default=None, alias="multiKillLength")
    
    name: Optional[str] = Field(default=None, alias="name")
    
    participantId: Optional[int] = Field(default=None, alias="participantId")
    
    position: Optional[match_v5_PositionDto] = Field(default=None, alias="position")
    
    realTimestamp: Optional[int] = Field(default=None, alias="realTimestamp")
    
    shutdownBounty: Optional[int] = Field(default=None, alias="shutdownBounty")
    
    skillSlot: Optional[int] = Field(default=None, alias="skillSlot")
    
    teamId: Optional[int] = Field(default=None, alias="teamId")
    
    timestamp: int = Field(default=None, alias="timestamp")
    
    towerType: Optional[str] = Field(default=None, alias="towerType")
    
    transformType: Optional[str] = Field(default=None, alias="transformType")
    
    type: str = Field(default=None, alias="type")
    
    victimDamageDealt: Optional[List[match_v5_MatchTimelineVictimDamage]] = Field(default=None, alias="victimDamageDealt")
    
    victimDamageReceived: Optional[List[match_v5_MatchTimelineVictimDamage]] = Field(default=None, alias="victimDamageReceived")
    
    victimId: Optional[int] = Field(default=None, alias="victimId")
    
    wardType: Optional[str] = Field(default=None, alias="wardType")
    
    winningTeam: Optional[int] = Field(default=None, alias="winningTeam")
    
    


class match_v5_FeatDto(BaseModel):
    """
    No description provided.
    """
    
    
    featState: Optional[int] = Field(default=None, alias="featState")
    
    


class match_v5_FeatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    EPIC_MONSTER_KILL: Optional[match_v5_FeatDto] = Field(default=None, alias="EPIC_MONSTER_KILL")
    
    FIRST_BLOOD: Optional[match_v5_FeatDto] = Field(default=None, alias="FIRST_BLOOD")
    
    FIRST_TURRET: Optional[match_v5_FeatDto] = Field(default=None, alias="FIRST_TURRET")
    
    


class match_v5_FramesTimeLineDto(BaseModel):
    """
    No description provided.
    """
    
    
    events: List[match_v5_EventsTimeLineDto] = Field(default=None, alias="events")
    
    participantFrames: Optional[Dict[str, match_v5_ParticipantFrameDto]] = Field(default=None, alias="participantFrames")
    
    timestamp: int = Field(default=None, alias="timestamp")
    
    


class match_v5_InfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    endOfGameResult: Optional[str] = Field(default=None, alias="endOfGameResult")
    
    gameCreation: int = Field(default=None, alias="gameCreation")
    
    gameDuration: int = Field(default=None, alias="gameDuration")
    
    gameEndTimestamp: Optional[int] = Field(default=None, alias="gameEndTimestamp")
    
    gameId: int = Field(default=None, alias="gameId")
    
    gameMode: str = Field(default=None, alias="gameMode")
    
    gameModeMutators: Optional[List[str]] = Field(default=None, alias="gameModeMutators")
    
    gameName: str = Field(default=None, alias="gameName")
    
    gameStartTimestamp: int = Field(default=None, alias="gameStartTimestamp")
    
    gameType: str = Field(default=None, alias="gameType")
    
    gameVersion: str = Field(default=None, alias="gameVersion")
    
    mapId: int = Field(default=None, alias="mapId")
    
    participants: List[match_v5_ParticipantDto] = Field(default=None, alias="participants")
    
    platformId: str = Field(default=None, alias="platformId")
    
    queueId: int = Field(default=None, alias="queueId")
    
    teams: List[match_v5_TeamDto] = Field(default=None, alias="teams")
    
    tournamentCode: Optional[str] = Field(default=None, alias="tournamentCode")
    
    


class match_v5_InfoTimeLineDto(BaseModel):
    """
    No description provided.
    """
    
    
    endOfGameResult: Optional[str] = Field(default=None, alias="endOfGameResult")
    
    frameInterval: int = Field(default=None, alias="frameInterval")
    
    frames: List[match_v5_FramesTimeLineDto] = Field(default=None, alias="frames")
    
    gameId: Optional[int] = Field(default=None, alias="gameId")
    
    participants: Optional[List[match_v5_ParticipantTimeLineDto]] = Field(default=None, alias="participants")
    
    


class match_v5_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    info: match_v5_InfoDto = Field(default=None, alias="info")
    
    metadata: match_v5_MetadataDto = Field(default=None, alias="metadata")
    
    


class match_v5_MatchTimelineVictimDamage(BaseModel):
    """
    No description provided.
    """
    
    
    basic: bool = Field(default=None, alias="basic")
    
    magicDamage: int = Field(default=None, alias="magicDamage")
    
    name: str = Field(default=None, alias="name")
    
    participantId: int = Field(default=None, alias="participantId")
    
    physicalDamage: int = Field(default=None, alias="physicalDamage")
    
    spellName: str = Field(default=None, alias="spellName")
    
    spellSlot: int = Field(default=None, alias="spellSlot")
    
    trueDamage: int = Field(default=None, alias="trueDamage")
    
    type: str = Field(default=None, alias="type")
    
    


class match_v5_MetadataDto(BaseModel):
    """
    No description provided.
    """
    
    
    dataVersion: str = Field(default=None, alias="dataVersion")
    
    matchId: str = Field(default=None, alias="matchId")
    
    participants: List[str] = Field(default=None, alias="participants")
    
    


class match_v5_MetadataTimeLineDto(BaseModel):
    """
    No description provided.
    """
    
    
    dataVersion: str = Field(default=None, alias="dataVersion")
    
    matchId: str = Field(default=None, alias="matchId")
    
    participants: List[str] = Field(default=None, alias="participants")
    
    


class match_v5_MissionsDto(BaseModel):
    """
    Missions DTO
    """
    
    
    playerScore0: Optional[float] = Field(default=None, alias="playerScore0")
    
    playerScore1: Optional[float] = Field(default=None, alias="playerScore1")
    
    playerScore10: Optional[float] = Field(default=None, alias="playerScore10")
    
    playerScore11: Optional[float] = Field(default=None, alias="playerScore11")
    
    playerScore2: Optional[float] = Field(default=None, alias="playerScore2")
    
    playerScore3: Optional[float] = Field(default=None, alias="playerScore3")
    
    playerScore4: Optional[float] = Field(default=None, alias="playerScore4")
    
    playerScore5: Optional[float] = Field(default=None, alias="playerScore5")
    
    playerScore6: Optional[float] = Field(default=None, alias="playerScore6")
    
    playerScore7: Optional[float] = Field(default=None, alias="playerScore7")
    
    playerScore8: Optional[float] = Field(default=None, alias="playerScore8")
    
    playerScore9: Optional[float] = Field(default=None, alias="playerScore9")
    
    


class match_v5_ObjectiveDto(BaseModel):
    """
    No description provided.
    """
    
    
    first: bool = Field(default=None, alias="first")
    
    kills: int = Field(default=None, alias="kills")
    
    


class match_v5_ObjectivesDto(BaseModel):
    """
    No description provided.
    """
    
    
    atakhan: Optional[match_v5_ObjectiveDto] = Field(default=None, alias="atakhan")
    
    baron: match_v5_ObjectiveDto = Field(default=None, alias="baron")
    
    champion: match_v5_ObjectiveDto = Field(default=None, alias="champion")
    
    dragon: match_v5_ObjectiveDto = Field(default=None, alias="dragon")
    
    horde: Optional[match_v5_ObjectiveDto] = Field(default=None, alias="horde")
    
    inhibitor: match_v5_ObjectiveDto = Field(default=None, alias="inhibitor")
    
    riftHerald: match_v5_ObjectiveDto = Field(default=None, alias="riftHerald")
    
    tower: match_v5_ObjectiveDto = Field(default=None, alias="tower")
    
    


class match_v5_ParticipantDto(BaseModel):
    """
    No description provided.
    """
    
    
    allInPings: Optional[int] = Field(default=None, alias="allInPings")
    
    assistMePings: Optional[int] = Field(default=None, alias="assistMePings")
    
    assists: int = Field(default=None, alias="assists")
    
    baitPings: Optional[int] = Field(default=None, alias="baitPings")
    
    baronKills: int = Field(default=None, alias="baronKills")
    
    basicPings: Optional[int] = Field(default=None, alias="basicPings")
    
    bountyLevel: Optional[int] = Field(default=None, alias="bountyLevel")
    
    challenges: Optional[match_v5_ChallengesDto] = Field(default=None, alias="challenges")
    
    champExperience: int = Field(default=None, alias="champExperience")
    
    champLevel: int = Field(default=None, alias="champLevel")
    
    championId: int = Field(default=None, alias="championId")
    
    championName: str = Field(default=None, alias="championName")
    
    championSkinId: Optional[int] = Field(default=None, alias="championSkinId")
    
    championTransform: int = Field(default=None, alias="championTransform")
    
    commandPings: Optional[int] = Field(default=None, alias="commandPings")
    
    consumablesPurchased: int = Field(default=None, alias="consumablesPurchased")
    
    damageDealtToBuildings: Optional[int] = Field(default=None, alias="damageDealtToBuildings")
    
    damageDealtToEpicMonsters: Optional[int] = Field(default=None, alias="damageDealtToEpicMonsters")
    
    damageDealtToObjectives: int = Field(default=None, alias="damageDealtToObjectives")
    
    damageDealtToTurrets: int = Field(default=None, alias="damageDealtToTurrets")
    
    damageSelfMitigated: int = Field(default=None, alias="damageSelfMitigated")
    
    dangerPings: Optional[int] = Field(default=None, alias="dangerPings")
    
    deaths: int = Field(default=None, alias="deaths")
    
    detectorWardsPlaced: int = Field(default=None, alias="detectorWardsPlaced")
    
    doubleKills: int = Field(default=None, alias="doubleKills")
    
    dragonKills: int = Field(default=None, alias="dragonKills")
    
    eligibleForProgression: Optional[bool] = Field(default=None, alias="eligibleForProgression")
    
    enemyMissingPings: Optional[int] = Field(default=None, alias="enemyMissingPings")
    
    enemyVisionPings: Optional[int] = Field(default=None, alias="enemyVisionPings")
    
    firstBloodAssist: bool = Field(default=None, alias="firstBloodAssist")
    
    firstBloodKill: bool = Field(default=None, alias="firstBloodKill")
    
    firstTowerAssist: bool = Field(default=None, alias="firstTowerAssist")
    
    firstTowerKill: bool = Field(default=None, alias="firstTowerKill")
    
    gameEndedInEarlySurrender: bool = Field(default=None, alias="gameEndedInEarlySurrender")
    
    gameEndedInSurrender: bool = Field(default=None, alias="gameEndedInSurrender")
    
    getBackPings: Optional[int] = Field(default=None, alias="getBackPings")
    
    goldEarned: int = Field(default=None, alias="goldEarned")
    
    goldSpent: int = Field(default=None, alias="goldSpent")
    
    holdPings: Optional[int] = Field(default=None, alias="holdPings")
    
    individualPosition: str = Field(default=None, alias="individualPosition")
    
    inhibitorKills: int = Field(default=None, alias="inhibitorKills")
    
    inhibitorTakedowns: Optional[int] = Field(default=None, alias="inhibitorTakedowns")
    
    inhibitorsLost: Optional[int] = Field(default=None, alias="inhibitorsLost")
    
    item0: int = Field(default=None, alias="item0")
    
    item1: int = Field(default=None, alias="item1")
    
    item2: int = Field(default=None, alias="item2")
    
    item3: int = Field(default=None, alias="item3")
    
    item4: int = Field(default=None, alias="item4")
    
    item5: int = Field(default=None, alias="item5")
    
    item6: int = Field(default=None, alias="item6")
    
    itemsPurchased: int = Field(default=None, alias="itemsPurchased")
    
    killingSprees: int = Field(default=None, alias="killingSprees")
    
    kills: int = Field(default=None, alias="kills")
    
    lane: str = Field(default=None, alias="lane")
    
    largestCriticalStrike: int = Field(default=None, alias="largestCriticalStrike")
    
    largestKillingSpree: int = Field(default=None, alias="largestKillingSpree")
    
    largestMultiKill: int = Field(default=None, alias="largestMultiKill")
    
    longestTimeSpentLiving: int = Field(default=None, alias="longestTimeSpentLiving")
    
    magicDamageDealt: int = Field(default=None, alias="magicDamageDealt")
    
    magicDamageDealtToChampions: int = Field(default=None, alias="magicDamageDealtToChampions")
    
    magicDamageTaken: int = Field(default=None, alias="magicDamageTaken")
    
    missions: Optional[match_v5_MissionsDto] = Field(default=None, alias="missions")
    
    needVisionPings: Optional[int] = Field(default=None, alias="needVisionPings")
    
    neutralMinionsKilled: int = Field(default=None, alias="neutralMinionsKilled")
    
    nexusKills: int = Field(default=None, alias="nexusKills")
    
    nexusLost: Optional[int] = Field(default=None, alias="nexusLost")
    
    nexusTakedowns: Optional[int] = Field(default=None, alias="nexusTakedowns")
    
    objectivesStolen: int = Field(default=None, alias="objectivesStolen")
    
    objectivesStolenAssists: int = Field(default=None, alias="objectivesStolenAssists")
    
    onMyWayPings: Optional[int] = Field(default=None, alias="onMyWayPings")
    
    participantId: int = Field(default=None, alias="participantId")
    
    pentaKills: int = Field(default=None, alias="pentaKills")
    
    perks: match_v5_PerksDto = Field(default=None, alias="perks")
    
    physicalDamageDealt: int = Field(default=None, alias="physicalDamageDealt")
    
    physicalDamageDealtToChampions: int = Field(default=None, alias="physicalDamageDealtToChampions")
    
    physicalDamageTaken: int = Field(default=None, alias="physicalDamageTaken")
    
    placement: Optional[int] = Field(default=None, alias="placement")
    
    playerAugment1: Optional[int] = Field(default=None, alias="playerAugment1")
    
    playerAugment2: Optional[int] = Field(default=None, alias="playerAugment2")
    
    playerAugment3: Optional[int] = Field(default=None, alias="playerAugment3")
    
    playerAugment4: Optional[int] = Field(default=None, alias="playerAugment4")
    
    playerAugment5: Optional[int] = Field(default=None, alias="playerAugment5")
    
    playerAugment6: Optional[int] = Field(default=None, alias="playerAugment6")
    
    playerScore0: Optional[float] = Field(default=None, alias="playerScore0")
    
    playerScore1: Optional[float] = Field(default=None, alias="playerScore1")
    
    playerScore10: Optional[float] = Field(default=None, alias="playerScore10")
    
    playerScore11: Optional[float] = Field(default=None, alias="playerScore11")
    
    playerScore2: Optional[float] = Field(default=None, alias="playerScore2")
    
    playerScore3: Optional[float] = Field(default=None, alias="playerScore3")
    
    playerScore4: Optional[float] = Field(default=None, alias="playerScore4")
    
    playerScore5: Optional[float] = Field(default=None, alias="playerScore5")
    
    playerScore6: Optional[float] = Field(default=None, alias="playerScore6")
    
    playerScore7: Optional[float] = Field(default=None, alias="playerScore7")
    
    playerScore8: Optional[float] = Field(default=None, alias="playerScore8")
    
    playerScore9: Optional[float] = Field(default=None, alias="playerScore9")
    
    playerSubteamId: Optional[int] = Field(default=None, alias="playerSubteamId")
    
    profileIcon: int = Field(default=None, alias="profileIcon")
    
    pushPings: Optional[int] = Field(default=None, alias="pushPings")
    
    puuid: str = Field(default=None, alias="puuid")
    
    quadraKills: int = Field(default=None, alias="quadraKills")
    
    retreatPings: Optional[int] = Field(default=None, alias="retreatPings")
    
    riotIdGameName: Optional[str] = Field(default=None, alias="riotIdGameName")
    
    riotIdName: Optional[str] = Field(default=None, alias="riotIdName")
    
    riotIdTagline: Optional[str] = Field(default=None, alias="riotIdTagline")
    
    role: str = Field(default=None, alias="role")
    
    sightWardsBoughtInGame: int = Field(default=None, alias="sightWardsBoughtInGame")
    
    spell1Casts: int = Field(default=None, alias="spell1Casts")
    
    spell2Casts: int = Field(default=None, alias="spell2Casts")
    
    spell3Casts: int = Field(default=None, alias="spell3Casts")
    
    spell4Casts: int = Field(default=None, alias="spell4Casts")
    
    subteamPlacement: Optional[int] = Field(default=None, alias="subteamPlacement")
    
    summoner1Casts: int = Field(default=None, alias="summoner1Casts")
    
    summoner1Id: int = Field(default=None, alias="summoner1Id")
    
    summoner2Casts: int = Field(default=None, alias="summoner2Casts")
    
    summoner2Id: int = Field(default=None, alias="summoner2Id")
    
    summonerId: str = Field(default=None, alias="summonerId")
    
    summonerLevel: int = Field(default=None, alias="summonerLevel")
    
    summonerName: str = Field(default=None, alias="summonerName")
    
    teamEarlySurrendered: bool = Field(default=None, alias="teamEarlySurrendered")
    
    teamId: int = Field(default=None, alias="teamId")
    
    teamPosition: str = Field(default=None, alias="teamPosition")
    
    timeCCingOthers: int = Field(default=None, alias="timeCCingOthers")
    
    timePlayed: int = Field(default=None, alias="timePlayed")
    
    totalAllyJungleMinionsKilled: Optional[int] = Field(default=None, alias="totalAllyJungleMinionsKilled")
    
    totalDamageDealt: int = Field(default=None, alias="totalDamageDealt")
    
    totalDamageDealtToChampions: int = Field(default=None, alias="totalDamageDealtToChampions")
    
    totalDamageShieldedOnTeammates: int = Field(default=None, alias="totalDamageShieldedOnTeammates")
    
    totalDamageTaken: int = Field(default=None, alias="totalDamageTaken")
    
    totalEnemyJungleMinionsKilled: Optional[int] = Field(default=None, alias="totalEnemyJungleMinionsKilled")
    
    totalHeal: int = Field(default=None, alias="totalHeal")
    
    totalHealsOnTeammates: int = Field(default=None, alias="totalHealsOnTeammates")
    
    totalMinionsKilled: int = Field(default=None, alias="totalMinionsKilled")
    
    totalTimeCCDealt: int = Field(default=None, alias="totalTimeCCDealt")
    
    totalTimeSpentDead: int = Field(default=None, alias="totalTimeSpentDead")
    
    totalUnitsHealed: int = Field(default=None, alias="totalUnitsHealed")
    
    tripleKills: int = Field(default=None, alias="tripleKills")
    
    trueDamageDealt: int = Field(default=None, alias="trueDamageDealt")
    
    trueDamageDealtToChampions: int = Field(default=None, alias="trueDamageDealtToChampions")
    
    trueDamageTaken: int = Field(default=None, alias="trueDamageTaken")
    
    turretKills: int = Field(default=None, alias="turretKills")
    
    turretTakedowns: Optional[int] = Field(default=None, alias="turretTakedowns")
    
    turretsLost: Optional[int] = Field(default=None, alias="turretsLost")
    
    unrealKills: int = Field(default=None, alias="unrealKills")
    
    visionClearedPings: Optional[int] = Field(default=None, alias="visionClearedPings")
    
    visionScore: int = Field(default=None, alias="visionScore")
    
    visionWardsBoughtInGame: int = Field(default=None, alias="visionWardsBoughtInGame")
    
    wardsKilled: int = Field(default=None, alias="wardsKilled")
    
    wardsPlaced: int = Field(default=None, alias="wardsPlaced")
    
    win: bool = Field(default=None, alias="win")
    
    


class match_v5_ParticipantFrameDto(BaseModel):
    """
    No description provided.
    """
    
    
    championStats: match_v5_ChampionStatsDto = Field(default=None, alias="championStats")
    
    currentGold: int = Field(default=None, alias="currentGold")
    
    damageStats: match_v5_DamageStatsDto = Field(default=None, alias="damageStats")
    
    goldPerSecond: int = Field(default=None, alias="goldPerSecond")
    
    jungleMinionsKilled: int = Field(default=None, alias="jungleMinionsKilled")
    
    level: int = Field(default=None, alias="level")
    
    minionsKilled: int = Field(default=None, alias="minionsKilled")
    
    participantId: int = Field(default=None, alias="participantId")
    
    position: match_v5_PositionDto = Field(default=None, alias="position")
    
    timeEnemySpentControlled: int = Field(default=None, alias="timeEnemySpentControlled")
    
    totalGold: int = Field(default=None, alias="totalGold")
    
    xp: int = Field(default=None, alias="xp")
    
    


class match_v5_ParticipantFramesDto(BaseModel):
    """
    No description provided.
    """
    
    
    param_1_9: match_v5_ParticipantFrameDto = Field(default=None, alias="1-9")
    
    


class match_v5_ParticipantTimeLineDto(BaseModel):
    """
    No description provided.
    """
    
    
    participantId: int = Field(default=None, alias="participantId")
    
    puuid: str = Field(default=None, alias="puuid")
    
    


class match_v5_PerkStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    defense: int = Field(default=None, alias="defense")
    
    flex: int = Field(default=None, alias="flex")
    
    offense: int = Field(default=None, alias="offense")
    
    


class match_v5_PerkStyleDto(BaseModel):
    """
    No description provided.
    """
    
    
    description: str = Field(default=None, alias="description")
    
    selections: List[match_v5_PerkStyleSelectionDto] = Field(default=None, alias="selections")
    
    style: int = Field(default=None, alias="style")
    
    


class match_v5_PerkStyleSelectionDto(BaseModel):
    """
    No description provided.
    """
    
    
    perk: int = Field(default=None, alias="perk")
    
    var1: int = Field(default=None, alias="var1")
    
    var2: int = Field(default=None, alias="var2")
    
    var3: int = Field(default=None, alias="var3")
    
    


class match_v5_PerksDto(BaseModel):
    """
    No description provided.
    """
    
    
    statPerks: match_v5_PerkStatsDto = Field(default=None, alias="statPerks")
    
    styles: List[match_v5_PerkStyleDto] = Field(default=None, alias="styles")
    
    


class match_v5_PositionDto(BaseModel):
    """
    No description provided.
    """
    
    
    x: int = Field(default=None, alias="x")
    
    y: int = Field(default=None, alias="y")
    
    


class match_v5_ReplayDTO(BaseModel):
    """
    No description provided.
    """
    
    
    matchFileURLs: List[str] = Field(default=None, alias="matchFileURLs")
    
    total: int = Field(default=None, alias="total")
    
    


class match_v5_TeamDto(BaseModel):
    """
    No description provided.
    """
    
    
    bans: List[match_v5_BanDto] = Field(default=None, alias="bans")
    
    feats: Optional[match_v5_FeatsDto] = Field(default=None, alias="feats")
    
    objectives: match_v5_ObjectivesDto = Field(default=None, alias="objectives")
    
    teamId: int = Field(default=None, alias="teamId")
    
    win: bool = Field(default=None, alias="win")
    
    


class match_v5_TimelineDto(BaseModel):
    """
    No description provided.
    """
    
    
    info: match_v5_InfoTimeLineDto = Field(default=None, alias="info")
    
    metadata: match_v5_MetadataTimeLineDto = Field(default=None, alias="metadata")
    
    


class riftbound_content_v1_CardArtDTO(BaseModel):
    """
    No description provided.
    """
    
    
    artist: str = Field(default=None, alias="artist")
    
    fullURL: str = Field(default=None, alias="fullURL")
    
    thumbnailURL: str = Field(default=None, alias="thumbnailURL")
    
    


class riftbound_content_v1_CardDTO(BaseModel):
    """
    No description provided.
    """
    
    
    art: riftbound_content_v1_CardArtDTO = Field(default=None, alias="art")
    
    collectorNumber: int = Field(default=None, alias="collectorNumber")
    
    description: str = Field(default=None, alias="description")
    
    faction: str = Field(default=None, alias="faction")
    
    flavorText: str = Field(default=None, alias="flavorText")
    
    id: str = Field(default=None, alias="id")
    
    keywords: List[str] = Field(default=None, alias="keywords")
    
    name: str = Field(default=None, alias="name")
    
    rarity: str = Field(default=None, alias="rarity")
    
    set: str = Field(default=None, alias="set")
    
    stats: riftbound_content_v1_CardStatsDTO = Field(default=None, alias="stats")
    
    tags: List[str] = Field(default=None, alias="tags")
    
    type: str = Field(default=None, alias="type")
    
    


class riftbound_content_v1_CardStatsDTO(BaseModel):
    """
    No description provided.
    """
    
    
    cost: int = Field(default=None, alias="cost")
    
    energy: int = Field(default=None, alias="energy")
    
    might: int = Field(default=None, alias="might")
    
    power: int = Field(default=None, alias="power")
    
    


class riftbound_content_v1_RiftboundContentDTO(BaseModel):
    """
    No description provided.
    """
    
    
    game: str = Field(default=None, alias="game")
    
    lastUpdated: str = Field(default=None, alias="lastUpdated")
    
    sets: List[riftbound_content_v1_SetDTO] = Field(default=None, alias="sets")
    
    version: str = Field(default=None, alias="version")
    
    


class riftbound_content_v1_SetDTO(BaseModel):
    """
    No description provided.
    """
    
    
    cards: List[riftbound_content_v1_CardDTO] = Field(default=None, alias="cards")
    
    id: str = Field(default=None, alias="id")
    
    name: str = Field(default=None, alias="name")
    
    


class spectator_tft_v5_BannedChampion(BaseModel):
    """
    No description provided.
    """
    
    
    championId: int = Field(default=None, alias="championId")
    
    pickTurn: int = Field(default=None, alias="pickTurn")
    
    teamId: int = Field(default=None, alias="teamId")
    
    


class spectator_tft_v5_CurrentGameInfo(BaseModel):
    """
    No description provided.
    """
    
    
    bannedChampions: List[spectator_tft_v5_BannedChampion] = Field(default=None, alias="bannedChampions")
    
    gameId: int = Field(default=None, alias="gameId")
    
    gameLength: int = Field(default=None, alias="gameLength")
    
    gameMode: str = Field(default=None, alias="gameMode")
    
    gameQueueConfigId: Optional[int] = Field(default=None, alias="gameQueueConfigId")
    
    gameStartTime: int = Field(default=None, alias="gameStartTime")
    
    gameType: str = Field(default=None, alias="gameType")
    
    mapId: int = Field(default=None, alias="mapId")
    
    observers: spectator_tft_v5_Observer = Field(default=None, alias="observers")
    
    participants: List[spectator_tft_v5_CurrentGameParticipant] = Field(default=None, alias="participants")
    
    platformId: str = Field(default=None, alias="platformId")
    
    


class spectator_tft_v5_CurrentGameParticipant(BaseModel):
    """
    No description provided.
    """
    
    
    championId: int = Field(default=None, alias="championId")
    
    gameCustomizationObjects: List[spectator_tft_v5_GameCustomizationObject] = Field(default=None, alias="gameCustomizationObjects")
    
    perks: Optional[spectator_tft_v5_Perks] = Field(default=None, alias="perks")
    
    profileIconId: int = Field(default=None, alias="profileIconId")
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    riotId: Optional[str] = Field(default=None, alias="riotId")
    
    spell1Id: int = Field(default=None, alias="spell1Id")
    
    spell2Id: int = Field(default=None, alias="spell2Id")
    
    teamId: int = Field(default=None, alias="teamId")
    
    


class spectator_tft_v5_GameCustomizationObject(BaseModel):
    """
    No description provided.
    """
    
    
    category: str = Field(default=None, alias="category")
    
    content: str = Field(default=None, alias="content")
    
    


class spectator_tft_v5_Observer(BaseModel):
    """
    No description provided.
    """
    
    
    encryptionKey: str = Field(default=None, alias="encryptionKey")
    
    


class spectator_tft_v5_Perks(BaseModel):
    """
    No description provided.
    """
    
    
    perkIds: List[int] = Field(default=None, alias="perkIds")
    
    perkStyle: int = Field(default=None, alias="perkStyle")
    
    perkSubStyle: int = Field(default=None, alias="perkSubStyle")
    
    


class spectator_v5_BannedChampion(BaseModel):
    """
    No description provided.
    """
    
    
    championId: int = Field(default=None, alias="championId")
    
    pickTurn: int = Field(default=None, alias="pickTurn")
    
    teamId: int = Field(default=None, alias="teamId")
    
    


class spectator_v5_CurrentGameInfo(BaseModel):
    """
    No description provided.
    """
    
    
    bannedChampions: List[spectator_v5_BannedChampion] = Field(default=None, alias="bannedChampions")
    
    gameId: int = Field(default=None, alias="gameId")
    
    gameLength: int = Field(default=None, alias="gameLength")
    
    gameMode: str = Field(default=None, alias="gameMode")
    
    gameQueueConfigId: Optional[int] = Field(default=None, alias="gameQueueConfigId")
    
    gameStartTime: int = Field(default=None, alias="gameStartTime")
    
    gameType: str = Field(default=None, alias="gameType")
    
    mapId: int = Field(default=None, alias="mapId")
    
    observers: spectator_v5_Observer = Field(default=None, alias="observers")
    
    participants: List[spectator_v5_CurrentGameParticipant] = Field(default=None, alias="participants")
    
    platformId: str = Field(default=None, alias="platformId")
    
    


class spectator_v5_CurrentGameParticipant(BaseModel):
    """
    No description provided.
    """
    
    
    bot: bool = Field(default=None, alias="bot")
    
    championId: int = Field(default=None, alias="championId")
    
    gameCustomizationObjects: List[spectator_v5_GameCustomizationObject] = Field(default=None, alias="gameCustomizationObjects")
    
    perks: Optional[spectator_v5_Perks] = Field(default=None, alias="perks")
    
    profileIconId: int = Field(default=None, alias="profileIconId")
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    riotId: Optional[str] = Field(default=None, alias="riotId")
    
    spell1Id: int = Field(default=None, alias="spell1Id")
    
    spell2Id: int = Field(default=None, alias="spell2Id")
    
    teamId: int = Field(default=None, alias="teamId")
    
    


class spectator_v5_GameCustomizationObject(BaseModel):
    """
    No description provided.
    """
    
    
    category: str = Field(default=None, alias="category")
    
    content: str = Field(default=None, alias="content")
    
    


class spectator_v5_Observer(BaseModel):
    """
    No description provided.
    """
    
    
    encryptionKey: str = Field(default=None, alias="encryptionKey")
    
    


class spectator_v5_Perks(BaseModel):
    """
    No description provided.
    """
    
    
    perkIds: List[int] = Field(default=None, alias="perkIds")
    
    perkStyle: int = Field(default=None, alias="perkStyle")
    
    perkSubStyle: int = Field(default=None, alias="perkSubStyle")
    
    


class summoner_v4_SummonerDTO(BaseModel):
    """
    represents a summoner
    """
    
    
    id: Optional[str] = Field(default=None, alias="id")
    
    profileIconId: int = Field(default=None, alias="profileIconId")
    
    puuid: str = Field(default=None, alias="puuid")
    
    revisionDate: int = Field(default=None, alias="revisionDate")
    
    summonerLevel: int = Field(default=None, alias="summonerLevel")
    
    


class tft_league_v1_LeagueEntryDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: Optional[bool] = Field(default=None, alias="freshBlood")
    
    hotStreak: Optional[bool] = Field(default=None, alias="hotStreak")
    
    inactive: Optional[bool] = Field(default=None, alias="inactive")
    
    leagueId: Optional[str] = Field(default=None, alias="leagueId")
    
    leaguePoints: Optional[int] = Field(default=None, alias="leaguePoints")
    
    losses: int = Field(default=None, alias="losses")
    
    miniSeries: Optional[tft_league_v1_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    queueType: str = Field(default=None, alias="queueType")
    
    rank: Optional[str] = Field(default=None, alias="rank")
    
    ratedRating: Optional[int] = Field(default=None, alias="ratedRating")
    
    ratedTier: Optional[str] = Field(default=None, alias="ratedTier")
    
    tier: Optional[str] = Field(default=None, alias="tier")
    
    veteran: Optional[bool] = Field(default=None, alias="veteran")
    
    wins: int = Field(default=None, alias="wins")
    
    


class tft_league_v1_LeagueItemDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: bool = Field(default=None, alias="freshBlood")
    
    hotStreak: bool = Field(default=None, alias="hotStreak")
    
    inactive: bool = Field(default=None, alias="inactive")
    
    leaguePoints: int = Field(default=None, alias="leaguePoints")
    
    losses: int = Field(default=None, alias="losses")
    
    miniSeries: Optional[tft_league_v1_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    puuid: str = Field(default=None, alias="puuid")
    
    rank: str = Field(default=None, alias="rank")
    
    veteran: bool = Field(default=None, alias="veteran")
    
    wins: int = Field(default=None, alias="wins")
    
    


class tft_league_v1_LeagueListDTO(BaseModel):
    """
    No description provided.
    """
    
    
    entries: List[tft_league_v1_LeagueItemDTO] = Field(default=None, alias="entries")
    
    leagueId: Optional[str] = Field(default=None, alias="leagueId")
    
    name: Optional[str] = Field(default=None, alias="name")
    
    queue: Optional[str] = Field(default=None, alias="queue")
    
    tier: str = Field(default=None, alias="tier")
    
    


class tft_league_v1_MiniSeriesDTO(BaseModel):
    """
    No description provided.
    """
    
    
    losses: int = Field(default=None, alias="losses")
    
    progress: str = Field(default=None, alias="progress")
    
    target: int = Field(default=None, alias="target")
    
    wins: int = Field(default=None, alias="wins")
    
    


class tft_league_v1_TopRatedLadderEntryDto(BaseModel):
    """
    No description provided.
    """
    
    
    previousUpdateLadderPosition: int = Field(default=None, alias="previousUpdateLadderPosition")
    
    puuid: str = Field(default=None, alias="puuid")
    
    ratedRating: int = Field(default=None, alias="ratedRating")
    
    ratedTier: str = Field(default=None, alias="ratedTier")
    
    wins: int = Field(default=None, alias="wins")
    
    


class tft_match_v1_CompanionDto(BaseModel):
    """
    No description provided.
    """
    
    
    content_ID: str = Field(default=None, alias="content_ID")
    
    item_ID: int = Field(default=None, alias="item_ID")
    
    skin_ID: int = Field(default=None, alias="skin_ID")
    
    species: str = Field(default=None, alias="species")
    
    


class tft_match_v1_InfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    endOfGameResult: Optional[str] = Field(default=None, alias="endOfGameResult")
    
    gameCreation: Optional[int] = Field(default=None, alias="gameCreation")
    
    gameId: Optional[int] = Field(default=None, alias="gameId")
    
    game_datetime: int = Field(default=None, alias="game_datetime")
    
    game_length: float = Field(default=None, alias="game_length")
    
    game_variation: Optional[str] = Field(default=None, alias="game_variation")
    
    game_version: str = Field(default=None, alias="game_version")
    
    mapId: Optional[int] = Field(default=None, alias="mapId")
    
    participants: List[tft_match_v1_ParticipantDto] = Field(default=None, alias="participants")
    
    queueId: Optional[int] = Field(default=None, alias="queueId")
    
    queue_id: int = Field(default=None, alias="queue_id")
    
    tft_game_type: Optional[str] = Field(default=None, alias="tft_game_type")
    
    tft_set_core_name: Optional[str] = Field(default=None, alias="tft_set_core_name")
    
    tft_set_number: int = Field(default=None, alias="tft_set_number")
    
    


class tft_match_v1_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    info: tft_match_v1_InfoDto = Field(default=None, alias="info")
    
    metadata: tft_match_v1_MetadataDto = Field(default=None, alias="metadata")
    
    


class tft_match_v1_MetadataDto(BaseModel):
    """
    No description provided.
    """
    
    
    data_version: str = Field(default=None, alias="data_version")
    
    match_id: str = Field(default=None, alias="match_id")
    
    participants: List[str] = Field(default=None, alias="participants")
    
    


class tft_match_v1_ParticipantDto(BaseModel):
    """
    No description provided.
    """
    
    
    augments: Optional[List[str]] = Field(default=None, alias="augments")
    
    companion: tft_match_v1_CompanionDto = Field(default=None, alias="companion")
    
    gold_left: int = Field(default=None, alias="gold_left")
    
    last_round: int = Field(default=None, alias="last_round")
    
    level: int = Field(default=None, alias="level")
    
    missions: Optional[tft_match_v1_ParticipantMissionsDto] = Field(default=None, alias="missions")
    
    partner_group_id: Optional[int] = Field(default=None, alias="partner_group_id")
    
    placement: int = Field(default=None, alias="placement")
    
    players_eliminated: int = Field(default=None, alias="players_eliminated")
    
    puuid: str = Field(default=None, alias="puuid")
    
    pve_score: Optional[int] = Field(default=None, alias="pve_score")
    
    pve_wonrun: Optional[bool] = Field(default=None, alias="pve_wonrun")
    
    riotIdGameName: Optional[str] = Field(default=None, alias="riotIdGameName")
    
    riotIdTagline: Optional[str] = Field(default=None, alias="riotIdTagline")
    
    skill_tree: Optional[Dict[str, int]] = Field(default=None, alias="skill_tree")
    
    time_eliminated: float = Field(default=None, alias="time_eliminated")
    
    total_damage_to_players: int = Field(default=None, alias="total_damage_to_players")
    
    traits: List[tft_match_v1_TraitDto] = Field(default=None, alias="traits")
    
    units: List[tft_match_v1_UnitDto] = Field(default=None, alias="units")
    
    win: Optional[bool] = Field(default=None, alias="win")
    
    


class tft_match_v1_ParticipantMissionsDto(BaseModel):
    """
    No description provided.
    """
    
    
    Assists: Optional[int] = Field(default=None, alias="Assists")
    
    DamageDealt: Optional[int] = Field(default=None, alias="DamageDealt")
    
    DamageDealtToObjectives: Optional[int] = Field(default=None, alias="DamageDealtToObjectives")
    
    DamageDealtToTurrets: Optional[int] = Field(default=None, alias="DamageDealtToTurrets")
    
    DamageTaken: Optional[int] = Field(default=None, alias="DamageTaken")
    
    Deaths: Optional[int] = Field(default=None, alias="Deaths")
    
    DoubleKills: Optional[int] = Field(default=None, alias="DoubleKills")
    
    GoldEarned: Optional[int] = Field(default=None, alias="GoldEarned")
    
    GoldSpent: Optional[int] = Field(default=None, alias="GoldSpent")
    
    InhibitorsDestroyed: Optional[int] = Field(default=None, alias="InhibitorsDestroyed")
    
    KillingSprees: Optional[int] = Field(default=None, alias="KillingSprees")
    
    Kills: Optional[int] = Field(default=None, alias="Kills")
    
    LargestKillingSpree: Optional[int] = Field(default=None, alias="LargestKillingSpree")
    
    LargestMultiKill: Optional[int] = Field(default=None, alias="LargestMultiKill")
    
    MagicDamageDealt: Optional[int] = Field(default=None, alias="MagicDamageDealt")
    
    MagicDamageDealtToChampions: Optional[int] = Field(default=None, alias="MagicDamageDealtToChampions")
    
    MagicDamageTaken: Optional[int] = Field(default=None, alias="MagicDamageTaken")
    
    NeutralMinionsKilledTeamJungle: Optional[int] = Field(default=None, alias="NeutralMinionsKilledTeamJungle")
    
    PentaKills: Optional[int] = Field(default=None, alias="PentaKills")
    
    PhysicalDamageDealt: Optional[int] = Field(default=None, alias="PhysicalDamageDealt")
    
    PhysicalDamageDealtToChampions: Optional[int] = Field(default=None, alias="PhysicalDamageDealtToChampions")
    
    PhysicalDamageTaken: Optional[int] = Field(default=None, alias="PhysicalDamageTaken")
    
    PlayerScore0: Optional[int] = Field(default=None, alias="PlayerScore0")
    
    PlayerScore1: Optional[int] = Field(default=None, alias="PlayerScore1")
    
    PlayerScore10: Optional[int] = Field(default=None, alias="PlayerScore10")
    
    PlayerScore11: Optional[int] = Field(default=None, alias="PlayerScore11")
    
    PlayerScore2: Optional[int] = Field(default=None, alias="PlayerScore2")
    
    PlayerScore3: Optional[int] = Field(default=None, alias="PlayerScore3")
    
    PlayerScore4: Optional[int] = Field(default=None, alias="PlayerScore4")
    
    PlayerScore5: Optional[int] = Field(default=None, alias="PlayerScore5")
    
    PlayerScore6: Optional[int] = Field(default=None, alias="PlayerScore6")
    
    PlayerScore9: Optional[int] = Field(default=None, alias="PlayerScore9")
    
    QuadraKills: Optional[int] = Field(default=None, alias="QuadraKills")
    
    Spell1Casts: Optional[int] = Field(default=None, alias="Spell1Casts")
    
    Spell2Casts: Optional[int] = Field(default=None, alias="Spell2Casts")
    
    Spell3Casts: Optional[int] = Field(default=None, alias="Spell3Casts")
    
    Spell4Casts: Optional[int] = Field(default=None, alias="Spell4Casts")
    
    SummonerSpell1Casts: Optional[int] = Field(default=None, alias="SummonerSpell1Casts")
    
    TimeCCOthers: Optional[int] = Field(default=None, alias="TimeCCOthers")
    
    TotalDamageDealtToChampions: Optional[int] = Field(default=None, alias="TotalDamageDealtToChampions")
    
    TotalMinionsKilled: Optional[int] = Field(default=None, alias="TotalMinionsKilled")
    
    TripleKills: Optional[int] = Field(default=None, alias="TripleKills")
    
    TrueDamageDealt: Optional[int] = Field(default=None, alias="TrueDamageDealt")
    
    TrueDamageDealtToChampions: Optional[int] = Field(default=None, alias="TrueDamageDealtToChampions")
    
    TrueDamageTaken: Optional[int] = Field(default=None, alias="TrueDamageTaken")
    
    UnrealKills: Optional[int] = Field(default=None, alias="UnrealKills")
    
    VisionScore: Optional[int] = Field(default=None, alias="VisionScore")
    
    WardsKilled: Optional[int] = Field(default=None, alias="WardsKilled")
    
    


class tft_match_v1_TraitDto(BaseModel):
    """
    No description provided.
    """
    
    
    name: str = Field(default=None, alias="name")
    
    num_units: int = Field(default=None, alias="num_units")
    
    style: Optional[int] = Field(default=None, alias="style")
    
    tier_current: int = Field(default=None, alias="tier_current")
    
    tier_total: Optional[int] = Field(default=None, alias="tier_total")
    
    


class tft_match_v1_UnitDto(BaseModel):
    """
    No description provided.
    """
    
    
    character_id: str = Field(default=None, alias="character_id")
    
    chosen: Optional[str] = Field(default=None, alias="chosen")
    
    itemNames: Optional[List[str]] = Field(default=None, alias="itemNames")
    
    items: Optional[List[int]] = Field(default=None, alias="items")
    
    name: str = Field(default=None, alias="name")
    
    rarity: int = Field(default=None, alias="rarity")
    
    tier: int = Field(default=None, alias="tier")
    
    


class tft_status_v1_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    content: str = Field(default=None, alias="content")
    
    locale: str = Field(default=None, alias="locale")
    
    


class tft_status_v1_PlatformDataDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(default=None, alias="id")
    
    incidents: List[tft_status_v1_StatusDto] = Field(default=None, alias="incidents")
    
    locales: List[str] = Field(default=None, alias="locales")
    
    maintenances: List[tft_status_v1_StatusDto] = Field(default=None, alias="maintenances")
    
    name: str = Field(default=None, alias="name")
    
    


class tft_status_v1_StatusDto(BaseModel):
    """
    No description provided.
    """
    
    
    archive_at: str = Field(default=None, alias="archive_at")
    
    created_at: str = Field(default=None, alias="created_at")
    
    id: int = Field(default=None, alias="id")
    
    incident_severity: str = Field(default=None, alias="incident_severity")
    
    maintenance_status: str = Field(default=None, alias="maintenance_status")
    
    platforms: List[str] = Field(default=None, alias="platforms")
    
    titles: List[tft_status_v1_ContentDto] = Field(default=None, alias="titles")
    
    updated_at: str = Field(default=None, alias="updated_at")
    
    updates: List[tft_status_v1_UpdateDto] = Field(default=None, alias="updates")
    
    


class tft_status_v1_UpdateDto(BaseModel):
    """
    No description provided.
    """
    
    
    author: str = Field(default=None, alias="author")
    
    created_at: str = Field(default=None, alias="created_at")
    
    id: int = Field(default=None, alias="id")
    
    publish: bool = Field(default=None, alias="publish")
    
    publish_locations: List[str] = Field(default=None, alias="publish_locations")
    
    translations: List[tft_status_v1_ContentDto] = Field(default=None, alias="translations")
    
    updated_at: str = Field(default=None, alias="updated_at")
    
    


class tft_summoner_v1_SummonerDTO(BaseModel):
    """
    represents a summoner
    """
    
    
    id: Optional[str] = Field(default=None, alias="id")
    
    profileIconId: int = Field(default=None, alias="profileIconId")
    
    puuid: str = Field(default=None, alias="puuid")
    
    revisionDate: int = Field(default=None, alias="revisionDate")
    
    summonerLevel: int = Field(default=None, alias="summonerLevel")
    
    


class tournament_stub_v5_LobbyEventV5DTO(BaseModel):
    """
    No description provided.
    """
    
    
    eventType: str = Field(default=None, alias="eventType")
    
    puuid: str = Field(default=None, alias="puuid")
    
    timestamp: str = Field(default=None, alias="timestamp")
    
    


class tournament_stub_v5_LobbyEventV5DTOWrapper(BaseModel):
    """
    No description provided.
    """
    
    
    eventList: List[tournament_stub_v5_LobbyEventV5DTO] = Field(default=None, alias="eventList")
    
    


class tournament_stub_v5_ProviderRegistrationParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    region: str = Field(default=None, alias="region")
    
    url: str = Field(default=None, alias="url")
    
    


class tournament_stub_v5_TournamentCodeParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    allowedParticipants: Optional[List[str]] = Field(default=None, alias="allowedParticipants")
    
    enoughPlayers: bool = Field(default=None, alias="enoughPlayers")
    
    mapType: str = Field(default=None, alias="mapType")
    
    metadata: Optional[str] = Field(default=None, alias="metadata")
    
    pickType: str = Field(default=None, alias="pickType")
    
    spectatorType: str = Field(default=None, alias="spectatorType")
    
    teamSize: int = Field(default=None, alias="teamSize")
    
    


class tournament_stub_v5_TournamentCodeV5DTO(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(default=None, alias="code")
    
    id: int = Field(default=None, alias="id")
    
    lobbyName: str = Field(default=None, alias="lobbyName")
    
    map: str = Field(default=None, alias="map")
    
    metaData: str = Field(default=None, alias="metaData")
    
    participants: List[str] = Field(default=None, alias="participants")
    
    password: str = Field(default=None, alias="password")
    
    pickType: str = Field(default=None, alias="pickType")
    
    providerId: int = Field(default=None, alias="providerId")
    
    region: str = Field(default=None, alias="region")
    
    teamSize: int = Field(default=None, alias="teamSize")
    
    tournamentId: int = Field(default=None, alias="tournamentId")
    
    


class tournament_stub_v5_TournamentRegistrationParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    name: Optional[str] = Field(default=None, alias="name")
    
    providerId: int = Field(default=None, alias="providerId")
    
    


class tournament_v5_LobbyEventV5DTO(BaseModel):
    """
    No description provided.
    """
    
    
    eventType: str = Field(default=None, alias="eventType")
    
    puuid: str = Field(default=None, alias="puuid")
    
    timestamp: str = Field(default=None, alias="timestamp")
    
    


class tournament_v5_LobbyEventV5DTOWrapper(BaseModel):
    """
    No description provided.
    """
    
    
    eventList: List[tournament_v5_LobbyEventV5DTO] = Field(default=None, alias="eventList")
    
    


class tournament_v5_ProviderRegistrationParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    region: str = Field(default=None, alias="region")
    
    url: str = Field(default=None, alias="url")
    
    


class tournament_v5_TournamentCodeParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    allowedParticipants: Optional[List[str]] = Field(default=None, alias="allowedParticipants")
    
    enoughPlayers: bool = Field(default=None, alias="enoughPlayers")
    
    mapType: str = Field(default=None, alias="mapType")
    
    metadata: Optional[str] = Field(default=None, alias="metadata")
    
    pickType: str = Field(default=None, alias="pickType")
    
    spectatorType: str = Field(default=None, alias="spectatorType")
    
    teamSize: int = Field(default=None, alias="teamSize")
    
    


class tournament_v5_TournamentCodeUpdateParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    allowedParticipants: Optional[List[str]] = Field(default=None, alias="allowedParticipants")
    
    mapType: str = Field(default=None, alias="mapType")
    
    pickType: str = Field(default=None, alias="pickType")
    
    spectatorType: str = Field(default=None, alias="spectatorType")
    
    


class tournament_v5_TournamentCodeV5DTO(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(default=None, alias="code")
    
    id: int = Field(default=None, alias="id")
    
    lobbyName: str = Field(default=None, alias="lobbyName")
    
    map: str = Field(default=None, alias="map")
    
    metaData: str = Field(default=None, alias="metaData")
    
    participants: List[str] = Field(default=None, alias="participants")
    
    password: str = Field(default=None, alias="password")
    
    pickType: str = Field(default=None, alias="pickType")
    
    providerId: int = Field(default=None, alias="providerId")
    
    region: str = Field(default=None, alias="region")
    
    spectators: str = Field(default=None, alias="spectators")
    
    teamSize: int = Field(default=None, alias="teamSize")
    
    tournamentId: int = Field(default=None, alias="tournamentId")
    
    


class tournament_v5_TournamentGamesV5(BaseModel):
    """
    No description provided.
    """
    
    
    gameId: int = Field(default=None, alias="gameId")
    
    gameMap: int = Field(default=None, alias="gameMap")
    
    gameMode: str = Field(default=None, alias="gameMode")
    
    gameName: str = Field(default=None, alias="gameName")
    
    gameType: str = Field(default=None, alias="gameType")
    
    losingTeam: List[tournament_v5_TournamentTeamV5] = Field(default=None, alias="losingTeam")
    
    metaData: Optional[str] = Field(default=None, alias="metaData")
    
    region: str = Field(default=None, alias="region")
    
    shortCode: str = Field(default=None, alias="shortCode")
    
    startTime: int = Field(default=None, alias="startTime")
    
    winningTeam: List[tournament_v5_TournamentTeamV5] = Field(default=None, alias="winningTeam")
    
    


class tournament_v5_TournamentRegistrationParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    name: Optional[str] = Field(default=None, alias="name")
    
    providerId: int = Field(default=None, alias="providerId")
    
    


class tournament_v5_TournamentTeamV5(BaseModel):
    """
    No description provided.
    """
    
    
    puuid: str = Field(default=None, alias="puuid")
    
    


class val_console_match_v1_AbilityCastsDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability1Casts: int = Field(default=None, alias="ability1Casts")
    
    ability2Casts: int = Field(default=None, alias="ability2Casts")
    
    grenadeCasts: int = Field(default=None, alias="grenadeCasts")
    
    ultimateCasts: int = Field(default=None, alias="ultimateCasts")
    
    


class val_console_match_v1_AbilityDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability1Effects: Optional[str] = Field(default=None, alias="ability1Effects")
    
    ability2Effects: Optional[str] = Field(default=None, alias="ability2Effects")
    
    grenadeEffects: Optional[str] = Field(default=None, alias="grenadeEffects")
    
    ultimateEffects: Optional[str] = Field(default=None, alias="ultimateEffects")
    
    


class val_console_match_v1_CoachDto(BaseModel):
    """
    No description provided.
    """
    
    
    puuid: str = Field(default=None, alias="puuid")
    
    teamId: str = Field(default=None, alias="teamId")
    
    


class val_console_match_v1_DamageDto(BaseModel):
    """
    No description provided.
    """
    
    
    bodyshots: int = Field(default=None, alias="bodyshots")
    
    damage: int = Field(default=None, alias="damage")
    
    headshots: int = Field(default=None, alias="headshots")
    
    legshots: int = Field(default=None, alias="legshots")
    
    receiver: str = Field(default=None, alias="receiver")
    
    


class val_console_match_v1_EconomyDto(BaseModel):
    """
    No description provided.
    """
    
    
    armor: str = Field(default=None, alias="armor")
    
    loadoutValue: int = Field(default=None, alias="loadoutValue")
    
    remaining: int = Field(default=None, alias="remaining")
    
    spent: int = Field(default=None, alias="spent")
    
    weapon: str = Field(default=None, alias="weapon")
    
    


class val_console_match_v1_FinishingDamageDto(BaseModel):
    """
    No description provided.
    """
    
    
    damageItem: str = Field(default=None, alias="damageItem")
    
    damageType: str = Field(default=None, alias="damageType")
    
    isSecondaryFireMode: bool = Field(default=None, alias="isSecondaryFireMode")
    
    


class val_console_match_v1_KillDto(BaseModel):
    """
    No description provided.
    """
    
    
    assistants: List[str] = Field(default=None, alias="assistants")
    
    finishingDamage: val_console_match_v1_FinishingDamageDto = Field(default=None, alias="finishingDamage")
    
    killer: str = Field(default=None, alias="killer")
    
    playerLocations: List[val_console_match_v1_PlayerLocationsDto] = Field(default=None, alias="playerLocations")
    
    timeSinceGameStartMillis: int = Field(default=None, alias="timeSinceGameStartMillis")
    
    timeSinceRoundStartMillis: int = Field(default=None, alias="timeSinceRoundStartMillis")
    
    victim: str = Field(default=None, alias="victim")
    
    victimLocation: val_console_match_v1_LocationDto = Field(default=None, alias="victimLocation")
    
    


class val_console_match_v1_LocationDto(BaseModel):
    """
    No description provided.
    """
    
    
    x: int = Field(default=None, alias="x")
    
    y: int = Field(default=None, alias="y")
    
    


class val_console_match_v1_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    coaches: List[val_console_match_v1_CoachDto] = Field(default=None, alias="coaches")
    
    matchInfo: val_console_match_v1_MatchInfoDto = Field(default=None, alias="matchInfo")
    
    players: List[val_console_match_v1_PlayerDto] = Field(default=None, alias="players")
    
    roundResults: Optional[List[val_console_match_v1_RoundResultDto]] = Field(default=None, alias="roundResults")
    
    teams: Optional[List[val_console_match_v1_TeamDto]] = Field(default=None, alias="teams")
    
    


class val_console_match_v1_MatchInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    customGameName: str = Field(default=None, alias="customGameName")
    
    gameLengthMillis: Optional[int] = Field(default=None, alias="gameLengthMillis")
    
    gameMode: str = Field(default=None, alias="gameMode")
    
    gameStartMillis: int = Field(default=None, alias="gameStartMillis")
    
    isCompleted: bool = Field(default=None, alias="isCompleted")
    
    isRanked: bool = Field(default=None, alias="isRanked")
    
    mapId: str = Field(default=None, alias="mapId")
    
    matchId: str = Field(default=None, alias="matchId")
    
    provisioningFlowId: str = Field(default=None, alias="provisioningFlowId")
    
    queueId: str = Field(default=None, alias="queueId")
    
    seasonId: str = Field(default=None, alias="seasonId")
    
    


class val_console_match_v1_MatchlistDto(BaseModel):
    """
    No description provided.
    """
    
    
    history: List[val_console_match_v1_MatchlistEntryDto] = Field(default=None, alias="history")
    
    puuid: str = Field(default=None, alias="puuid")
    
    


class val_console_match_v1_MatchlistEntryDto(BaseModel):
    """
    No description provided.
    """
    
    
    gameStartTimeMillis: int = Field(default=None, alias="gameStartTimeMillis")
    
    matchId: str = Field(default=None, alias="matchId")
    
    queueId: str = Field(default=None, alias="queueId")
    
    


class val_console_match_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    characterId: Optional[str] = Field(default=None, alias="characterId")
    
    competitiveTier: int = Field(default=None, alias="competitiveTier")
    
    gameName: str = Field(default=None, alias="gameName")
    
    partyId: str = Field(default=None, alias="partyId")
    
    playerCard: str = Field(default=None, alias="playerCard")
    
    playerTitle: str = Field(default=None, alias="playerTitle")
    
    puuid: str = Field(default=None, alias="puuid")
    
    stats: Optional[val_console_match_v1_PlayerStatsDto] = Field(default=None, alias="stats")
    
    tagLine: str = Field(default=None, alias="tagLine")
    
    teamId: str = Field(default=None, alias="teamId")
    
    


class val_console_match_v1_PlayerLocationsDto(BaseModel):
    """
    No description provided.
    """
    
    
    location: val_console_match_v1_LocationDto = Field(default=None, alias="location")
    
    puuid: str = Field(default=None, alias="puuid")
    
    viewRadians: float = Field(default=None, alias="viewRadians")
    
    


class val_console_match_v1_PlayerRoundStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability: val_console_match_v1_AbilityDto = Field(default=None, alias="ability")
    
    damage: List[val_console_match_v1_DamageDto] = Field(default=None, alias="damage")
    
    economy: val_console_match_v1_EconomyDto = Field(default=None, alias="economy")
    
    kills: List[val_console_match_v1_KillDto] = Field(default=None, alias="kills")
    
    puuid: str = Field(default=None, alias="puuid")
    
    score: int = Field(default=None, alias="score")
    
    


class val_console_match_v1_PlayerStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    abilityCasts: Optional[val_console_match_v1_AbilityCastsDto] = Field(default=None, alias="abilityCasts")
    
    assists: int = Field(default=None, alias="assists")
    
    deaths: int = Field(default=None, alias="deaths")
    
    kills: int = Field(default=None, alias="kills")
    
    playtimeMillis: int = Field(default=None, alias="playtimeMillis")
    
    roundsPlayed: int = Field(default=None, alias="roundsPlayed")
    
    score: int = Field(default=None, alias="score")
    
    


class val_console_match_v1_RecentMatchesDto(BaseModel):
    """
    No description provided.
    """
    
    
    currentTime: int = Field(default=None, alias="currentTime")
    
    matchIds: List[str] = Field(default=None, alias="matchIds")
    
    


class val_console_match_v1_RoundResultDto(BaseModel):
    """
    No description provided.
    """
    
    
    bombDefuser: Optional[str] = Field(default=None, alias="bombDefuser")
    
    bombPlanter: Optional[str] = Field(default=None, alias="bombPlanter")
    
    defuseLocation: val_console_match_v1_LocationDto = Field(default=None, alias="defuseLocation")
    
    defusePlayerLocations: Optional[List[val_console_match_v1_PlayerLocationsDto]] = Field(default=None, alias="defusePlayerLocations")
    
    defuseRoundTime: int = Field(default=None, alias="defuseRoundTime")
    
    plantLocation: val_console_match_v1_LocationDto = Field(default=None, alias="plantLocation")
    
    plantPlayerLocations: Optional[List[val_console_match_v1_PlayerLocationsDto]] = Field(default=None, alias="plantPlayerLocations")
    
    plantRoundTime: int = Field(default=None, alias="plantRoundTime")
    
    plantSite: str = Field(default=None, alias="plantSite")
    
    playerStats: List[val_console_match_v1_PlayerRoundStatsDto] = Field(default=None, alias="playerStats")
    
    roundCeremony: str = Field(default=None, alias="roundCeremony")
    
    roundNum: int = Field(default=None, alias="roundNum")
    
    roundResult: str = Field(default=None, alias="roundResult")
    
    roundResultCode: str = Field(default=None, alias="roundResultCode")
    
    winningTeam: str = Field(default=None, alias="winningTeam")
    
    


class val_console_match_v1_TeamDto(BaseModel):
    """
    No description provided.
    """
    
    
    numPoints: int = Field(default=None, alias="numPoints")
    
    roundsPlayed: int = Field(default=None, alias="roundsPlayed")
    
    roundsWon: int = Field(default=None, alias="roundsWon")
    
    teamId: str = Field(default=None, alias="teamId")
    
    won: bool = Field(default=None, alias="won")
    
    


class val_console_ranked_v1_LeaderboardDto(BaseModel):
    """
    No description provided.
    """
    
    
    actId: str = Field(default=None, alias="actId")
    
    players: List[val_console_ranked_v1_PlayerDto] = Field(default=None, alias="players")
    
    query: Optional[str] = Field(default=None, alias="query")
    
    shard: str = Field(default=None, alias="shard")
    
    tierDetails: Optional[List[val_console_ranked_v1_TierDto]] = Field(default=None, alias="tierDetails")
    
    totalPlayers: int = Field(default=None, alias="totalPlayers")
    
    


class val_console_ranked_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    gameName: Optional[str] = Field(default=None, alias="gameName")
    
    leaderboardRank: int = Field(default=None, alias="leaderboardRank")
    
    numberOfWins: int = Field(default=None, alias="numberOfWins")
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    rankedRating: int = Field(default=None, alias="rankedRating")
    
    tagLine: Optional[str] = Field(default=None, alias="tagLine")
    
    


class val_console_ranked_v1_TierDto(BaseModel):
    """
    UNKNOWN TYPE.
    """
    
    
    


class val_content_v1_ActDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(default=None, alias="id")
    
    isActive: bool = Field(default=None, alias="isActive")
    
    localizedNames: Optional[val_content_v1_LocalizedNamesDto] = Field(default=None, alias="localizedNames")
    
    name: str = Field(default=None, alias="name")
    
    parentId: Optional[str] = Field(default=None, alias="parentId")
    
    type: Optional[str] = Field(default=None, alias="type")
    
    


class val_content_v1_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    acts: List[val_content_v1_ActDto] = Field(default=None, alias="acts")
    
    ceremonies: Optional[List[val_content_v1_ContentItemDto]] = Field(default=None, alias="ceremonies")
    
    characters: List[val_content_v1_ContentItemDto] = Field(default=None, alias="characters")
    
    charmLevels: List[val_content_v1_ContentItemDto] = Field(default=None, alias="charmLevels")
    
    charms: List[val_content_v1_ContentItemDto] = Field(default=None, alias="charms")
    
    chromas: List[val_content_v1_ContentItemDto] = Field(default=None, alias="chromas")
    
    equips: List[val_content_v1_ContentItemDto] = Field(default=None, alias="equips")
    
    gameModes: List[val_content_v1_ContentItemDto] = Field(default=None, alias="gameModes")
    
    maps: List[val_content_v1_ContentItemDto] = Field(default=None, alias="maps")
    
    playerCards: List[val_content_v1_ContentItemDto] = Field(default=None, alias="playerCards")
    
    playerTitles: List[val_content_v1_ContentItemDto] = Field(default=None, alias="playerTitles")
    
    skinLevels: List[val_content_v1_ContentItemDto] = Field(default=None, alias="skinLevels")
    
    skins: List[val_content_v1_ContentItemDto] = Field(default=None, alias="skins")
    
    sprayLevels: List[val_content_v1_ContentItemDto] = Field(default=None, alias="sprayLevels")
    
    sprays: List[val_content_v1_ContentItemDto] = Field(default=None, alias="sprays")
    
    totems: Optional[List[val_content_v1_ContentItemDto]] = Field(default=None, alias="totems")
    
    version: str = Field(default=None, alias="version")
    
    


class val_content_v1_ContentItemDto(BaseModel):
    """
    No description provided.
    """
    
    
    assetName: str = Field(default=None, alias="assetName")
    
    assetPath: Optional[str] = Field(default=None, alias="assetPath")
    
    id: str = Field(default=None, alias="id")
    
    localizedNames: Optional[val_content_v1_LocalizedNamesDto] = Field(default=None, alias="localizedNames")
    
    name: str = Field(default=None, alias="name")
    
    


class val_content_v1_LocalizedNamesDto(BaseModel):
    """
    No description provided.
    """
    
    
    ar_AE: str = Field(default=None, alias="ar-AE")
    
    de_DE: str = Field(default=None, alias="de-DE")
    
    en_GB: Optional[str] = Field(default=None, alias="en-GB")
    
    en_US: str = Field(default=None, alias="en-US")
    
    es_ES: str = Field(default=None, alias="es-ES")
    
    es_MX: str = Field(default=None, alias="es-MX")
    
    fr_FR: str = Field(default=None, alias="fr-FR")
    
    id_ID: str = Field(default=None, alias="id-ID")
    
    it_IT: str = Field(default=None, alias="it-IT")
    
    ja_JP: str = Field(default=None, alias="ja-JP")
    
    ko_KR: str = Field(default=None, alias="ko-KR")
    
    pl_PL: str = Field(default=None, alias="pl-PL")
    
    pt_BR: str = Field(default=None, alias="pt-BR")
    
    ru_RU: str = Field(default=None, alias="ru-RU")
    
    th_TH: str = Field(default=None, alias="th-TH")
    
    tr_TR: str = Field(default=None, alias="tr-TR")
    
    vi_VN: str = Field(default=None, alias="vi-VN")
    
    zh_CN: str = Field(default=None, alias="zh-CN")
    
    zh_TW: str = Field(default=None, alias="zh-TW")
    
    


class val_match_v1_AbilityCastsDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability1Casts: int = Field(default=None, alias="ability1Casts")
    
    ability2Casts: int = Field(default=None, alias="ability2Casts")
    
    grenadeCasts: int = Field(default=None, alias="grenadeCasts")
    
    ultimateCasts: int = Field(default=None, alias="ultimateCasts")
    
    


class val_match_v1_AbilityDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability1Effects: Optional[str] = Field(default=None, alias="ability1Effects")
    
    ability2Effects: Optional[str] = Field(default=None, alias="ability2Effects")
    
    grenadeEffects: Optional[str] = Field(default=None, alias="grenadeEffects")
    
    ultimateEffects: Optional[str] = Field(default=None, alias="ultimateEffects")
    
    


class val_match_v1_CoachDto(BaseModel):
    """
    No description provided.
    """
    
    
    puuid: str = Field(default=None, alias="puuid")
    
    teamId: str = Field(default=None, alias="teamId")
    
    


class val_match_v1_DamageDto(BaseModel):
    """
    No description provided.
    """
    
    
    bodyshots: int = Field(default=None, alias="bodyshots")
    
    damage: int = Field(default=None, alias="damage")
    
    headshots: int = Field(default=None, alias="headshots")
    
    legshots: int = Field(default=None, alias="legshots")
    
    receiver: str = Field(default=None, alias="receiver")
    
    


class val_match_v1_EconomyDto(BaseModel):
    """
    No description provided.
    """
    
    
    armor: str = Field(default=None, alias="armor")
    
    loadoutValue: int = Field(default=None, alias="loadoutValue")
    
    remaining: int = Field(default=None, alias="remaining")
    
    spent: int = Field(default=None, alias="spent")
    
    weapon: str = Field(default=None, alias="weapon")
    
    


class val_match_v1_FinishingDamageDto(BaseModel):
    """
    No description provided.
    """
    
    
    damageItem: str = Field(default=None, alias="damageItem")
    
    damageType: str = Field(default=None, alias="damageType")
    
    isSecondaryFireMode: bool = Field(default=None, alias="isSecondaryFireMode")
    
    


class val_match_v1_KillDto(BaseModel):
    """
    No description provided.
    """
    
    
    assistants: List[str] = Field(default=None, alias="assistants")
    
    finishingDamage: val_match_v1_FinishingDamageDto = Field(default=None, alias="finishingDamage")
    
    killer: str = Field(default=None, alias="killer")
    
    playerLocations: List[val_match_v1_PlayerLocationsDto] = Field(default=None, alias="playerLocations")
    
    timeSinceGameStartMillis: int = Field(default=None, alias="timeSinceGameStartMillis")
    
    timeSinceRoundStartMillis: int = Field(default=None, alias="timeSinceRoundStartMillis")
    
    victim: str = Field(default=None, alias="victim")
    
    victimLocation: val_match_v1_LocationDto = Field(default=None, alias="victimLocation")
    
    


class val_match_v1_LocationDto(BaseModel):
    """
    No description provided.
    """
    
    
    x: int = Field(default=None, alias="x")
    
    y: int = Field(default=None, alias="y")
    
    


class val_match_v1_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    coaches: List[val_match_v1_CoachDto] = Field(default=None, alias="coaches")
    
    matchInfo: val_match_v1_MatchInfoDto = Field(default=None, alias="matchInfo")
    
    players: List[val_match_v1_PlayerDto] = Field(default=None, alias="players")
    
    roundResults: Optional[List[val_match_v1_RoundResultDto]] = Field(default=None, alias="roundResults")
    
    teams: Optional[List[val_match_v1_TeamDto]] = Field(default=None, alias="teams")
    
    


class val_match_v1_MatchInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    customGameName: str = Field(default=None, alias="customGameName")
    
    gameLengthMillis: Optional[int] = Field(default=None, alias="gameLengthMillis")
    
    gameMode: str = Field(default=None, alias="gameMode")
    
    gameStartMillis: int = Field(default=None, alias="gameStartMillis")
    
    gameVersion: str = Field(default=None, alias="gameVersion")
    
    isCompleted: bool = Field(default=None, alias="isCompleted")
    
    isRanked: bool = Field(default=None, alias="isRanked")
    
    mapId: str = Field(default=None, alias="mapId")
    
    matchId: str = Field(default=None, alias="matchId")
    
    premierMatchInfo: Dict[str, Any] = Field(default=None, alias="premierMatchInfo")
    
    provisioningFlowId: str = Field(default=None, alias="provisioningFlowId")
    
    queueId: str = Field(default=None, alias="queueId")
    
    region: str = Field(default=None, alias="region")
    
    seasonId: str = Field(default=None, alias="seasonId")
    
    


class val_match_v1_MatchlistDto(BaseModel):
    """
    No description provided.
    """
    
    
    history: List[val_match_v1_MatchlistEntryDto] = Field(default=None, alias="history")
    
    puuid: str = Field(default=None, alias="puuid")
    
    


class val_match_v1_MatchlistEntryDto(BaseModel):
    """
    No description provided.
    """
    
    
    gameStartTimeMillis: int = Field(default=None, alias="gameStartTimeMillis")
    
    matchId: str = Field(default=None, alias="matchId")
    
    queueId: str = Field(default=None, alias="queueId")
    
    


class val_match_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    accountLevel: int = Field(default=None, alias="accountLevel")
    
    characterId: Optional[str] = Field(default=None, alias="characterId")
    
    competitiveTier: int = Field(default=None, alias="competitiveTier")
    
    gameName: str = Field(default=None, alias="gameName")
    
    isObserver: bool = Field(default=None, alias="isObserver")
    
    partyId: str = Field(default=None, alias="partyId")
    
    playerCard: str = Field(default=None, alias="playerCard")
    
    playerTitle: str = Field(default=None, alias="playerTitle")
    
    puuid: str = Field(default=None, alias="puuid")
    
    stats: Optional[val_match_v1_PlayerStatsDto] = Field(default=None, alias="stats")
    
    tagLine: str = Field(default=None, alias="tagLine")
    
    teamId: str = Field(default=None, alias="teamId")
    
    


class val_match_v1_PlayerLocationsDto(BaseModel):
    """
    No description provided.
    """
    
    
    location: val_match_v1_LocationDto = Field(default=None, alias="location")
    
    puuid: str = Field(default=None, alias="puuid")
    
    viewRadians: float = Field(default=None, alias="viewRadians")
    
    


class val_match_v1_PlayerRoundStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability: val_match_v1_AbilityDto = Field(default=None, alias="ability")
    
    damage: List[val_match_v1_DamageDto] = Field(default=None, alias="damage")
    
    economy: val_match_v1_EconomyDto = Field(default=None, alias="economy")
    
    kills: List[val_match_v1_KillDto] = Field(default=None, alias="kills")
    
    puuid: str = Field(default=None, alias="puuid")
    
    score: int = Field(default=None, alias="score")
    
    


class val_match_v1_PlayerStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    abilityCasts: Optional[val_match_v1_AbilityCastsDto] = Field(default=None, alias="abilityCasts")
    
    assists: int = Field(default=None, alias="assists")
    
    deaths: int = Field(default=None, alias="deaths")
    
    kills: int = Field(default=None, alias="kills")
    
    playtimeMillis: int = Field(default=None, alias="playtimeMillis")
    
    roundsPlayed: int = Field(default=None, alias="roundsPlayed")
    
    score: int = Field(default=None, alias="score")
    
    


class val_match_v1_RecentMatchesDto(BaseModel):
    """
    No description provided.
    """
    
    
    currentTime: int = Field(default=None, alias="currentTime")
    
    matchIds: List[str] = Field(default=None, alias="matchIds")
    
    


class val_match_v1_RoundResultDto(BaseModel):
    """
    No description provided.
    """
    
    
    bombDefuser: Optional[str] = Field(default=None, alias="bombDefuser")
    
    bombPlanter: Optional[str] = Field(default=None, alias="bombPlanter")
    
    defuseLocation: val_match_v1_LocationDto = Field(default=None, alias="defuseLocation")
    
    defusePlayerLocations: Optional[List[val_match_v1_PlayerLocationsDto]] = Field(default=None, alias="defusePlayerLocations")
    
    defuseRoundTime: int = Field(default=None, alias="defuseRoundTime")
    
    plantLocation: val_match_v1_LocationDto = Field(default=None, alias="plantLocation")
    
    plantPlayerLocations: Optional[List[val_match_v1_PlayerLocationsDto]] = Field(default=None, alias="plantPlayerLocations")
    
    plantRoundTime: int = Field(default=None, alias="plantRoundTime")
    
    plantSite: str = Field(default=None, alias="plantSite")
    
    playerStats: List[val_match_v1_PlayerRoundStatsDto] = Field(default=None, alias="playerStats")
    
    roundCeremony: str = Field(default=None, alias="roundCeremony")
    
    roundNum: int = Field(default=None, alias="roundNum")
    
    roundResult: str = Field(default=None, alias="roundResult")
    
    roundResultCode: str = Field(default=None, alias="roundResultCode")
    
    winningTeam: str = Field(default=None, alias="winningTeam")
    
    winningTeamRole: str = Field(default=None, alias="winningTeamRole")
    
    


class val_match_v1_TeamDto(BaseModel):
    """
    No description provided.
    """
    
    
    numPoints: int = Field(default=None, alias="numPoints")
    
    roundsPlayed: int = Field(default=None, alias="roundsPlayed")
    
    roundsWon: int = Field(default=None, alias="roundsWon")
    
    teamId: str = Field(default=None, alias="teamId")
    
    won: bool = Field(default=None, alias="won")
    
    


class val_ranked_v1_LeaderboardDto(BaseModel):
    """
    No description provided.
    """
    
    
    actId: str = Field(default=None, alias="actId")
    
    immortalStartingIndex: Optional[int] = Field(default=None, alias="immortalStartingIndex")
    
    immortalStartingPage: Optional[int] = Field(default=None, alias="immortalStartingPage")
    
    players: List[val_ranked_v1_PlayerDto] = Field(default=None, alias="players")
    
    query: Optional[str] = Field(default=None, alias="query")
    
    shard: str = Field(default=None, alias="shard")
    
    startIndex: Optional[int] = Field(default=None, alias="startIndex")
    
    tierDetails: Optional[Dict[str, val_ranked_v1_TierDetailDto]] = Field(default=None, alias="tierDetails")
    
    topTierRRThreshold: Optional[int] = Field(default=None, alias="topTierRRThreshold")
    
    totalPlayers: int = Field(default=None, alias="totalPlayers")
    
    


class val_ranked_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    competitiveTier: Optional[int] = Field(default=None, alias="competitiveTier")
    
    gameName: Optional[str] = Field(default=None, alias="gameName")
    
    leaderboardRank: int = Field(default=None, alias="leaderboardRank")
    
    numberOfWins: int = Field(default=None, alias="numberOfWins")
    
    prefix: Optional[str] = Field(default=None, alias="prefix")
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    rankedRating: int = Field(default=None, alias="rankedRating")
    
    tagLine: Optional[str] = Field(default=None, alias="tagLine")
    
    


class val_ranked_v1_TierDetailDto(BaseModel):
    """
    No description provided.
    """
    
    
    rankedRatingThreshold: int = Field(default=None, alias="rankedRatingThreshold")
    
    startingIndex: int = Field(default=None, alias="startingIndex")
    
    startingPage: int = Field(default=None, alias="startingPage")
    
    


class val_status_v1_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    content: str = Field(default=None, alias="content")
    
    locale: str = Field(default=None, alias="locale")
    
    


class val_status_v1_PlatformDataDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(default=None, alias="id")
    
    incidents: List[val_status_v1_StatusDto] = Field(default=None, alias="incidents")
    
    locales: List[str] = Field(default=None, alias="locales")
    
    maintenances: List[val_status_v1_StatusDto] = Field(default=None, alias="maintenances")
    
    name: str = Field(default=None, alias="name")
    
    


class val_status_v1_StatusDto(BaseModel):
    """
    No description provided.
    """
    
    
    archive_at: str = Field(default=None, alias="archive_at")
    
    created_at: str = Field(default=None, alias="created_at")
    
    id: int = Field(default=None, alias="id")
    
    incident_severity: str = Field(default=None, alias="incident_severity")
    
    maintenance_status: str = Field(default=None, alias="maintenance_status")
    
    platforms: List[str] = Field(default=None, alias="platforms")
    
    titles: List[val_status_v1_ContentDto] = Field(default=None, alias="titles")
    
    updated_at: str = Field(default=None, alias="updated_at")
    
    updates: List[val_status_v1_UpdateDto] = Field(default=None, alias="updates")
    
    


class val_status_v1_UpdateDto(BaseModel):
    """
    No description provided.
    """
    
    
    author: str = Field(default=None, alias="author")
    
    created_at: str = Field(default=None, alias="created_at")
    
    id: int = Field(default=None, alias="id")
    
    publish: bool = Field(default=None, alias="publish")
    
    publish_locations: List[str] = Field(default=None, alias="publish_locations")
    
    translations: List[val_status_v1_ContentDto] = Field(default=None, alias="translations")
    
    updated_at: str = Field(default=None, alias="updated_at")
    
    


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
    
    
    

    model_config = {"populate_by_name": True}




class account_v1_AccountDto(BaseModel):
    """
    No description provided.
    """
    
    
    gameName: Optional[str] = Field(default=None, alias="gameName")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    tagLine: Optional[str] = Field(default=None, alias="tagLine")
    
    
    

    model_config = {"populate_by_name": True}




class account_v1_AccountRegionDTO(BaseModel):
    """
    Account region
    """
    
    
    game: str = Field(alias="game")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    region: str = Field(alias="region")
    
    
    

    model_config = {"populate_by_name": True}




class account_v1_ActiveShardDto(BaseModel):
    """
    No description provided.
    """
    
    
    activeShard: str = Field(alias="activeShard")
    
    
    
    game: str = Field(alias="game")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    

    model_config = {"populate_by_name": True}




class champion_mastery_v4_ChampionMasteryDto(BaseModel):
    """
    This object contains single Champion Mastery information for player and champion combination.
    """
    
    
    championId: int = Field(alias="championId")
    
    
    
    championLevel: int = Field(alias="championLevel")
    
    
    
    championPoints: int = Field(alias="championPoints")
    
    
    
    championPointsSinceLastLevel: int = Field(alias="championPointsSinceLastLevel")
    
    
    
    championPointsUntilNextLevel: int = Field(alias="championPointsUntilNextLevel")
    
    
    
    championSeasonMilestone: int = Field(alias="championSeasonMilestone")
    
    
    
    chestGranted: Optional[bool] = Field(default=None, alias="chestGranted")
    
    
    
    lastPlayTime: int = Field(alias="lastPlayTime")
    
    
    
    markRequiredForNextLevel: int = Field(alias="markRequiredForNextLevel")
    
    
    
    milestoneGrades: Optional[List[str]] = Field(default=None, alias="milestoneGrades")
    
    
    
    nextSeasonMilestone: champion_mastery_v4_NextSeasonMilestonesDto = Field(alias="nextSeasonMilestone")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    tokensEarned: int = Field(alias="tokensEarned")
    
    
    

    model_config = {"populate_by_name": True}




class champion_mastery_v4_NextSeasonMilestonesDto(BaseModel):
    """
    This object contains required next season milestone information.
    """
    
    
    bonus: bool = Field(alias="bonus")
    
    
    
    requireGradeCounts: Dict[str, int] = Field(alias="requireGradeCounts")
    
    
    
    rewardConfig: Optional[champion_mastery_v4_RewardConfigDto] = Field(default=None, alias="rewardConfig")
    
    
    
    rewardMarks: int = Field(alias="rewardMarks")
    
    
    
    totalGamesRequires: int = Field(alias="totalGamesRequires")
    
    
    

    model_config = {"populate_by_name": True}




class champion_mastery_v4_RewardConfigDto(BaseModel):
    """
    This object contains required reward config information.
    """
    
    
    maximumReward: int = Field(alias="maximumReward")
    
    
    
    rewardType: str = Field(alias="rewardType")
    
    
    
    rewardValue: str = Field(alias="rewardValue")
    
    
    

    model_config = {"populate_by_name": True}




class champion_v3_ChampionInfo(BaseModel):
    """
    No description provided.
    """
    
    
    freeChampionIds: List[int] = Field(alias="freeChampionIds")
    
    
    
    freeChampionIdsForNewPlayers: List[int] = Field(alias="freeChampionIdsForNewPlayers")
    
    
    
    maxNewPlayerLevel: int = Field(alias="maxNewPlayerLevel")
    
    
    

    model_config = {"populate_by_name": True}




class clash_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    position: str = Field(alias="position")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    role: str = Field(alias="role")
    
    
    
    teamId: Optional[str] = Field(default=None, alias="teamId")
    
    
    

    model_config = {"populate_by_name": True}




class clash_v1_TeamDto(BaseModel):
    """
    No description provided.
    """
    
    
    abbreviation: str = Field(alias="abbreviation")
    
    
    
    captain: str = Field(alias="captain")
    
    
    
    iconId: int = Field(alias="iconId")
    
    
    
    id: str = Field(alias="id")
    
    
    
    name: str = Field(alias="name")
    
    
    
    players: List[clash_v1_PlayerDto] = Field(alias="players")
    
    
    
    tier: int = Field(alias="tier")
    
    
    
    tournamentId: int = Field(alias="tournamentId")
    
    
    

    model_config = {"populate_by_name": True}




class clash_v1_TournamentDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: int = Field(alias="id")
    
    
    
    nameKey: str = Field(alias="nameKey")
    
    
    
    nameKeySecondary: str = Field(alias="nameKeySecondary")
    
    
    
    schedule: List[clash_v1_TournamentPhaseDto] = Field(alias="schedule")
    
    
    
    themeId: int = Field(alias="themeId")
    
    
    

    model_config = {"populate_by_name": True}




class clash_v1_TournamentPhaseDto(BaseModel):
    """
    No description provided.
    """
    
    
    cancelled: bool = Field(alias="cancelled")
    
    
    
    id: int = Field(alias="id")
    
    
    
    registrationTime: int = Field(alias="registrationTime")
    
    
    
    startTime: int = Field(alias="startTime")
    
    
    

    model_config = {"populate_by_name": True}




class league_exp_v4_LeagueEntryDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: bool = Field(alias="freshBlood")
    
    
    
    hotStreak: bool = Field(alias="hotStreak")
    
    
    
    inactive: bool = Field(alias="inactive")
    
    
    
    leagueId: str = Field(alias="leagueId")
    
    
    
    leaguePoints: int = Field(alias="leaguePoints")
    
    
    
    losses: int = Field(alias="losses")
    
    
    
    miniSeries: Optional[league_exp_v4_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    queueType: str = Field(alias="queueType")
    
    
    
    rank: str = Field(alias="rank")
    
    
    
    summonerId: Optional[str] = Field(default=None, alias="summonerId")
    
    
    
    tier: str = Field(alias="tier")
    
    
    
    veteran: bool = Field(alias="veteran")
    
    
    
    wins: int = Field(alias="wins")
    
    
    

    model_config = {"populate_by_name": True}




class league_exp_v4_MiniSeriesDTO(BaseModel):
    """
    No description provided.
    """
    
    
    losses: int = Field(alias="losses")
    
    
    
    progress: str = Field(alias="progress")
    
    
    
    target: int = Field(alias="target")
    
    
    
    wins: int = Field(alias="wins")
    
    
    

    model_config = {"populate_by_name": True}




class league_v4_LeagueEntryDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: bool = Field(alias="freshBlood")
    
    
    
    hotStreak: bool = Field(alias="hotStreak")
    
    
    
    inactive: bool = Field(alias="inactive")
    
    
    
    leagueId: Optional[str] = Field(default=None, alias="leagueId")
    
    
    
    leaguePoints: int = Field(alias="leaguePoints")
    
    
    
    losses: int = Field(alias="losses")
    
    
    
    miniSeries: Optional[league_v4_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    queueType: str = Field(alias="queueType")
    
    
    
    rank: Optional[str] = Field(default=None, alias="rank")
    
    
    
    summonerId: Optional[str] = Field(default=None, alias="summonerId")
    
    
    
    tier: Optional[str] = Field(default=None, alias="tier")
    
    
    
    veteran: bool = Field(alias="veteran")
    
    
    
    wins: int = Field(alias="wins")
    
    
    

    model_config = {"populate_by_name": True}




class league_v4_LeagueItemDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: bool = Field(alias="freshBlood")
    
    
    
    hotStreak: bool = Field(alias="hotStreak")
    
    
    
    inactive: bool = Field(alias="inactive")
    
    
    
    leaguePoints: int = Field(alias="leaguePoints")
    
    
    
    losses: int = Field(alias="losses")
    
    
    
    miniSeries: Optional[league_v4_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    rank: str = Field(alias="rank")
    
    
    
    summonerId: Optional[str] = Field(default=None, alias="summonerId")
    
    
    
    veteran: bool = Field(alias="veteran")
    
    
    
    wins: int = Field(alias="wins")
    
    
    

    model_config = {"populate_by_name": True}




class league_v4_LeagueListDTO(BaseModel):
    """
    No description provided.
    """
    
    
    entries: List[league_v4_LeagueItemDTO] = Field(alias="entries")
    
    
    
    leagueId: Optional[str] = Field(default=None, alias="leagueId")
    
    
    
    name: Optional[str] = Field(default=None, alias="name")
    
    
    
    queue: Optional[str] = Field(default=None, alias="queue")
    
    
    
    tier: str = Field(alias="tier")
    
    
    

    model_config = {"populate_by_name": True}




class league_v4_MiniSeriesDTO(BaseModel):
    """
    No description provided.
    """
    
    
    losses: int = Field(alias="losses")
    
    
    
    progress: str = Field(alias="progress")
    
    
    
    target: int = Field(alias="target")
    
    
    
    wins: int = Field(alias="wins")
    
    
    

    model_config = {"populate_by_name": True}




class lol_challenges_v1_ApexPlayerInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    position: int = Field(alias="position")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    value: float = Field(alias="value")
    
    
    

    model_config = {"populate_by_name": True}




class lol_challenges_v1_ChallengeConfigInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    endTimestamp: Optional[int] = Field(default=None, alias="endTimestamp")
    
    
    
    id: int = Field(alias="id")
    
    
    
    leaderboard: bool = Field(alias="leaderboard")
    
    
    
    localizedNames: Dict[str, Dict[str, str]] = Field(alias="localizedNames")
    
    
    
    startTimestamp: Optional[int] = Field(default=None, alias="startTimestamp")
    
    
    
    state: str = Field(alias="state")
    
    
    
    thresholds: Dict[str, float] = Field(alias="thresholds")
    
    
    
    tracking: Optional[str] = Field(default=None, alias="tracking")
    
    
    

    model_config = {"populate_by_name": True}




class lol_challenges_v1_ChallengeInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    achievedTime: Optional[int] = Field(default=None, alias="achievedTime")
    
    
    
    challengeId: int = Field(alias="challengeId")
    
    
    
    level: str = Field(alias="level")
    
    
    
    percentile: float = Field(alias="percentile")
    
    
    
    playersInLevel: Optional[int] = Field(default=None, alias="playersInLevel")
    
    
    
    position: Optional[int] = Field(default=None, alias="position")
    
    
    
    value: float = Field(alias="value")
    
    
    

    model_config = {"populate_by_name": True}




class lol_challenges_v1_ChallengePointDto(BaseModel):
    """
    No description provided.
    """
    
    
    current: int = Field(alias="current")
    
    
    
    level: str = Field(alias="level")
    
    
    
    max: int = Field(alias="max")
    
    
    
    percentile: Optional[float] = Field(default=None, alias="percentile")
    
    
    
    position: Optional[int] = Field(default=None, alias="position")
    
    
    

    model_config = {"populate_by_name": True}




lol_challenges_v1_Level = Literal["NONE", "IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER"]
"""0 NONE,
1 IRON,
2 BRONZE,
3 SILVER,
4 GOLD,
5 PLATINUM,
6 DIAMOND,
7 MASTER,
8 GRANDMASTER,
9 CHALLENGER"""



class lol_challenges_v1_PlayerClientPreferencesDto(BaseModel):
    """
    No description provided.
    """
    
    
    bannerAccent: Optional[str] = Field(default=None, alias="bannerAccent")
    
    
    
    challengeIds: Optional[List[int]] = Field(default=None, alias="challengeIds")
    
    
    
    crestBorder: Optional[str] = Field(default=None, alias="crestBorder")
    
    
    
    prestigeCrestBorderLevel: Optional[int] = Field(default=None, alias="prestigeCrestBorderLevel")
    
    
    
    title: Optional[str] = Field(default=None, alias="title")
    
    
    

    model_config = {"populate_by_name": True}




class lol_challenges_v1_PlayerInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    categoryPoints: Dict[str, lol_challenges_v1_ChallengePointDto] = Field(alias="categoryPoints")
    
    
    
    challenges: List[lol_challenges_v1_ChallengeInfoDto] = Field(alias="challenges")
    
    
    
    preferences: lol_challenges_v1_PlayerClientPreferencesDto = Field(alias="preferences")
    
    
    
    totalPoints: lol_challenges_v1_ChallengePointDto = Field(alias="totalPoints")
    
    
    

    model_config = {"populate_by_name": True}




lol_challenges_v1_State = Literal["DISABLED", "HIDDEN", "ENABLED", "ARCHIVED"]
"""DISABLED - not visible and not calculated,
HIDDEN - not visible, but calculated,
ENABLED - visible and calculated,
ARCHIVED - visible, but not calculated"""



lol_challenges_v1_Tracking = Literal["LIFETIME", "SEASON"]
"""LIFETIME - stats are incremented without reset,
SEASON - stats are accumulated by season and reset at the beginning of new season"""



class lol_rso_match_v1_MatchDto(BaseModel):
    """
    UNKNOWN TYPE.
    """
    
    
    pass
    

    model_config = {"populate_by_name": True}




class lol_rso_match_v1_TimelineDto(BaseModel):
    """
    UNKNOWN TYPE.
    """
    
    
    pass
    

    model_config = {"populate_by_name": True}




class lol_status_v4_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    content: str = Field(alias="content")
    
    
    
    locale: str = Field(alias="locale")
    
    
    

    model_config = {"populate_by_name": True}




class lol_status_v4_PlatformDataDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(alias="id")
    
    
    
    incidents: List[lol_status_v4_StatusDto] = Field(alias="incidents")
    
    
    
    locales: List[str] = Field(alias="locales")
    
    
    
    maintenances: List[lol_status_v4_StatusDto] = Field(alias="maintenances")
    
    
    
    name: str = Field(alias="name")
    
    
    

    model_config = {"populate_by_name": True}




class lol_status_v4_StatusDto(BaseModel):
    """
    No description provided.
    """
    
    
    archive_at: Optional[str] = Field(default=None, alias="archive_at")
    
    
    
    created_at: str = Field(alias="created_at")
    
    
    
    id: int = Field(alias="id")
    
    
    
    incident_severity: Optional[str] = Field(default=None, alias="incident_severity")
    
    
    
    maintenance_status: Optional[str] = Field(default=None, alias="maintenance_status")
    
    
    
    platforms: List[str] = Field(alias="platforms")
    
    
    
    titles: List[lol_status_v4_ContentDto] = Field(alias="titles")
    
    
    
    updated_at: Optional[str] = Field(default=None, alias="updated_at")
    
    
    
    updates: List[lol_status_v4_UpdateDto] = Field(alias="updates")
    
    
    

    model_config = {"populate_by_name": True}




class lol_status_v4_UpdateDto(BaseModel):
    """
    No description provided.
    """
    
    
    author: str = Field(alias="author")
    
    
    
    created_at: str = Field(alias="created_at")
    
    
    
    id: int = Field(alias="id")
    
    
    
    publish: bool = Field(alias="publish")
    
    
    
    publish_locations: List[str] = Field(alias="publish_locations")
    
    
    
    translations: List[lol_status_v4_ContentDto] = Field(alias="translations")
    
    
    
    updated_at: str = Field(alias="updated_at")
    
    
    

    model_config = {"populate_by_name": True}




class lor_deck_v1_DeckDto(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(alias="code")
    
    
    
    id: str = Field(alias="id")
    
    
    
    name: str = Field(alias="name")
    
    
    

    model_config = {"populate_by_name": True}




class lor_deck_v1_NewDeckDto(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(alias="code")
    
    
    
    name: str = Field(alias="name")
    
    
    

    model_config = {"populate_by_name": True}




class lor_inventory_v1_CardDto(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(alias="code")
    
    
    
    count: str = Field(alias="count")
    
    
    

    model_config = {"populate_by_name": True}




class lor_match_v1_InfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    game_format: str = Field(alias="game_format")
    
    
    
    game_mode: str = Field(alias="game_mode")
    
    
    
    game_start_time_utc: str = Field(alias="game_start_time_utc")
    
    
    
    game_type: str = Field(alias="game_type")
    
    
    
    game_version: str = Field(alias="game_version")
    
    
    
    players: List[lor_match_v1_PlayerDto] = Field(alias="players")
    
    
    
    total_turn_count: int = Field(alias="total_turn_count")
    
    
    

    model_config = {"populate_by_name": True}




class lor_match_v1_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    info: lor_match_v1_InfoDto = Field(alias="info")
    
    
    
    metadata: lor_match_v1_MetadataDto = Field(alias="metadata")
    
    
    

    model_config = {"populate_by_name": True}




class lor_match_v1_MetadataDto(BaseModel):
    """
    No description provided.
    """
    
    
    data_version: str = Field(alias="data_version")
    
    
    
    match_id: str = Field(alias="match_id")
    
    
    
    participants: List[str] = Field(alias="participants")
    
    
    

    model_config = {"populate_by_name": True}




class lor_match_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    deck_code: str = Field(alias="deck_code")
    
    
    
    deck_id: str = Field(alias="deck_id")
    
    
    
    factions: List[str] = Field(alias="factions")
    
    
    
    game_outcome: str = Field(alias="game_outcome")
    
    
    
    order_of_play: int = Field(alias="order_of_play")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    

    model_config = {"populate_by_name": True}




class lor_ranked_v1_LeaderboardDto(BaseModel):
    """
    No description provided.
    """
    
    
    players: List[lor_ranked_v1_PlayerDto] = Field(alias="players")
    
    
    

    model_config = {"populate_by_name": True}




class lor_ranked_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    lp: int = Field(alias="lp")
    
    
    
    name: str = Field(alias="name")
    
    
    
    rank: int = Field(alias="rank")
    
    
    

    model_config = {"populate_by_name": True}




class lor_status_v1_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    content: str = Field(alias="content")
    
    
    
    locale: str = Field(alias="locale")
    
    
    

    model_config = {"populate_by_name": True}




class lor_status_v1_PlatformDataDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(alias="id")
    
    
    
    incidents: List[lor_status_v1_StatusDto] = Field(alias="incidents")
    
    
    
    locales: List[str] = Field(alias="locales")
    
    
    
    maintenances: List[lor_status_v1_StatusDto] = Field(alias="maintenances")
    
    
    
    name: str = Field(alias="name")
    
    
    

    model_config = {"populate_by_name": True}




class lor_status_v1_StatusDto(BaseModel):
    """
    No description provided.
    """
    
    
    archive_at: str = Field(alias="archive_at")
    
    
    
    created_at: str = Field(alias="created_at")
    
    
    
    id: int = Field(alias="id")
    
    
    
    incident_severity: str = Field(alias="incident_severity")
    
    
    
    maintenance_status: str = Field(alias="maintenance_status")
    
    
    
    platforms: List[str] = Field(alias="platforms")
    
    
    
    titles: List[lor_status_v1_ContentDto] = Field(alias="titles")
    
    
    
    updated_at: str = Field(alias="updated_at")
    
    
    
    updates: List[lor_status_v1_UpdateDto] = Field(alias="updates")
    
    
    

    model_config = {"populate_by_name": True}




class lor_status_v1_UpdateDto(BaseModel):
    """
    No description provided.
    """
    
    
    author: str = Field(alias="author")
    
    
    
    created_at: str = Field(alias="created_at")
    
    
    
    id: int = Field(alias="id")
    
    
    
    publish: bool = Field(alias="publish")
    
    
    
    publish_locations: List[str] = Field(alias="publish_locations")
    
    
    
    translations: List[lor_status_v1_ContentDto] = Field(alias="translations")
    
    
    
    updated_at: str = Field(alias="updated_at")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_BanDto(BaseModel):
    """
    No description provided.
    """
    
    
    championId: int = Field(alias="championId")
    
    
    
    pickTurn: int = Field(alias="pickTurn")
    
    
    

    model_config = {"populate_by_name": True}




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
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_ChampionStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    abilityHaste: Optional[int] = Field(default=None, alias="abilityHaste")
    
    
    
    abilityPower: int = Field(alias="abilityPower")
    
    
    
    armor: int = Field(alias="armor")
    
    
    
    armorPen: int = Field(alias="armorPen")
    
    
    
    armorPenPercent: int = Field(alias="armorPenPercent")
    
    
    
    attackDamage: int = Field(alias="attackDamage")
    
    
    
    attackSpeed: int = Field(alias="attackSpeed")
    
    
    
    bonusArmorPenPercent: int = Field(alias="bonusArmorPenPercent")
    
    
    
    bonusMagicPenPercent: int = Field(alias="bonusMagicPenPercent")
    
    
    
    ccReduction: int = Field(alias="ccReduction")
    
    
    
    cooldownReduction: int = Field(alias="cooldownReduction")
    
    
    
    health: int = Field(alias="health")
    
    
    
    healthMax: int = Field(alias="healthMax")
    
    
    
    healthRegen: int = Field(alias="healthRegen")
    
    
    
    lifesteal: int = Field(alias="lifesteal")
    
    
    
    magicPen: int = Field(alias="magicPen")
    
    
    
    magicPenPercent: int = Field(alias="magicPenPercent")
    
    
    
    magicResist: int = Field(alias="magicResist")
    
    
    
    movementSpeed: int = Field(alias="movementSpeed")
    
    
    
    omnivamp: Optional[int] = Field(default=None, alias="omnivamp")
    
    
    
    physicalVamp: Optional[int] = Field(default=None, alias="physicalVamp")
    
    
    
    power: int = Field(alias="power")
    
    
    
    powerMax: int = Field(alias="powerMax")
    
    
    
    powerRegen: int = Field(alias="powerRegen")
    
    
    
    spellVamp: int = Field(alias="spellVamp")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_DamageStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    magicDamageDone: int = Field(alias="magicDamageDone")
    
    
    
    magicDamageDoneToChampions: int = Field(alias="magicDamageDoneToChampions")
    
    
    
    magicDamageTaken: int = Field(alias="magicDamageTaken")
    
    
    
    physicalDamageDone: int = Field(alias="physicalDamageDone")
    
    
    
    physicalDamageDoneToChampions: int = Field(alias="physicalDamageDoneToChampions")
    
    
    
    physicalDamageTaken: int = Field(alias="physicalDamageTaken")
    
    
    
    totalDamageDone: int = Field(alias="totalDamageDone")
    
    
    
    totalDamageDoneToChampions: int = Field(alias="totalDamageDoneToChampions")
    
    
    
    totalDamageTaken: int = Field(alias="totalDamageTaken")
    
    
    
    trueDamageDone: int = Field(alias="trueDamageDone")
    
    
    
    trueDamageDoneToChampions: int = Field(alias="trueDamageDoneToChampions")
    
    
    
    trueDamageTaken: int = Field(alias="trueDamageTaken")
    
    
    

    model_config = {"populate_by_name": True}




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
    
    
    
    timestamp: int = Field(alias="timestamp")
    
    
    
    towerType: Optional[str] = Field(default=None, alias="towerType")
    
    
    
    transformType: Optional[str] = Field(default=None, alias="transformType")
    
    
    
    type: str = Field(alias="type")
    
    
    
    victimDamageDealt: Optional[List[match_v5_MatchTimelineVictimDamage]] = Field(default=None, alias="victimDamageDealt")
    
    
    
    victimDamageReceived: Optional[List[match_v5_MatchTimelineVictimDamage]] = Field(default=None, alias="victimDamageReceived")
    
    
    
    victimId: Optional[int] = Field(default=None, alias="victimId")
    
    
    
    victimTeamfightDamageDealt: Optional[List[match_v5_MatchTimelineVictimDamage]] = Field(default=None, alias="victimTeamfightDamageDealt")
    
    
    
    victimTeamfightDamageReceived: Optional[List[match_v5_MatchTimelineVictimDamage]] = Field(default=None, alias="victimTeamfightDamageReceived")
    
    
    
    wardType: Optional[str] = Field(default=None, alias="wardType")
    
    
    
    winningTeam: Optional[int] = Field(default=None, alias="winningTeam")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_FeatDto(BaseModel):
    """
    No description provided.
    """
    
    
    featState: Optional[int] = Field(default=None, alias="featState")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_FeatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    EPIC_MONSTER_KILL: Optional[match_v5_FeatDto] = Field(default=None, alias="EPIC_MONSTER_KILL")
    
    
    
    FIRST_BLOOD: Optional[match_v5_FeatDto] = Field(default=None, alias="FIRST_BLOOD")
    
    
    
    FIRST_TURRET: Optional[match_v5_FeatDto] = Field(default=None, alias="FIRST_TURRET")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_FramesTimeLineDto(BaseModel):
    """
    No description provided.
    """
    
    
    events: List[match_v5_EventsTimeLineDto] = Field(alias="events")
    
    
    
    participantFrames: Optional[Dict[str, match_v5_ParticipantFrameDto]] = Field(default=None, alias="participantFrames")
    
    
    
    timestamp: int = Field(alias="timestamp")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_InfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    endOfGameResult: Optional[str] = Field(default=None, alias="endOfGameResult")
    
    
    
    gameCreation: int = Field(alias="gameCreation")
    
    
    
    gameDuration: int = Field(alias="gameDuration")
    
    
    
    gameEndTimestamp: Optional[int] = Field(default=None, alias="gameEndTimestamp")
    
    
    
    gameId: int = Field(alias="gameId")
    
    
    
    gameMode: str = Field(alias="gameMode")
    
    
    
    gameModeMutators: Optional[List[str]] = Field(default=None, alias="gameModeMutators")
    
    
    
    gameName: str = Field(alias="gameName")
    
    
    
    gameStartTimestamp: int = Field(alias="gameStartTimestamp")
    
    
    
    gameType: str = Field(alias="gameType")
    
    
    
    gameVersion: str = Field(alias="gameVersion")
    
    
    
    mapId: int = Field(alias="mapId")
    
    
    
    participants: List[match_v5_ParticipantDto] = Field(alias="participants")
    
    
    
    platformId: str = Field(alias="platformId")
    
    
    
    queueId: int = Field(alias="queueId")
    
    
    
    teams: List[match_v5_TeamDto] = Field(alias="teams")
    
    
    
    tournamentCode: Optional[str] = Field(default=None, alias="tournamentCode")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_InfoTimeLineDto(BaseModel):
    """
    No description provided.
    """
    
    
    endOfGameResult: Optional[str] = Field(default=None, alias="endOfGameResult")
    
    
    
    frameInterval: int = Field(alias="frameInterval")
    
    
    
    frames: List[match_v5_FramesTimeLineDto] = Field(alias="frames")
    
    
    
    gameId: Optional[int] = Field(default=None, alias="gameId")
    
    
    
    participants: Optional[List[match_v5_ParticipantTimeLineDto]] = Field(default=None, alias="participants")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    info: match_v5_InfoDto = Field(alias="info")
    
    
    
    metadata: match_v5_MetadataDto = Field(alias="metadata")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_MatchTimelineVictimDamage(BaseModel):
    """
    No description provided.
    """
    
    
    basic: bool = Field(alias="basic")
    
    
    
    magicDamage: int = Field(alias="magicDamage")
    
    
    
    name: str = Field(alias="name")
    
    
    
    participantId: int = Field(alias="participantId")
    
    
    
    physicalDamage: int = Field(alias="physicalDamage")
    
    
    
    spellName: str = Field(alias="spellName")
    
    
    
    spellSlot: int = Field(alias="spellSlot")
    
    
    
    trueDamage: int = Field(alias="trueDamage")
    
    
    
    type: str = Field(alias="type")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_MetadataDto(BaseModel):
    """
    No description provided.
    """
    
    
    dataVersion: str = Field(alias="dataVersion")
    
    
    
    matchId: str = Field(alias="matchId")
    
    
    
    participants: List[str] = Field(alias="participants")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_MetadataTimeLineDto(BaseModel):
    """
    No description provided.
    """
    
    
    dataVersion: str = Field(alias="dataVersion")
    
    
    
    matchId: str = Field(alias="matchId")
    
    
    
    participants: List[str] = Field(alias="participants")
    
    
    

    model_config = {"populate_by_name": True}




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
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_ObjectiveDto(BaseModel):
    """
    No description provided.
    """
    
    
    first: bool = Field(alias="first")
    
    
    
    kills: int = Field(alias="kills")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_ObjectivesDto(BaseModel):
    """
    No description provided.
    """
    
    
    atakhan: Optional[match_v5_ObjectiveDto] = Field(default=None, alias="atakhan")
    
    
    
    baron: match_v5_ObjectiveDto = Field(alias="baron")
    
    
    
    champion: match_v5_ObjectiveDto = Field(alias="champion")
    
    
    
    dragon: match_v5_ObjectiveDto = Field(alias="dragon")
    
    
    
    horde: Optional[match_v5_ObjectiveDto] = Field(default=None, alias="horde")
    
    
    
    inhibitor: match_v5_ObjectiveDto = Field(alias="inhibitor")
    
    
    
    riftHerald: match_v5_ObjectiveDto = Field(alias="riftHerald")
    
    
    
    tower: match_v5_ObjectiveDto = Field(alias="tower")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_ParticipantDto(BaseModel):
    """
    No description provided.
    """
    
    
    PlayerBehavior: Optional[match_v5_ParticipantPlayerBehaviorDto] = Field(default=None, alias="PlayerBehavior")
    
    
    
    allInPings: Optional[int] = Field(default=None, alias="allInPings")
    
    
    
    assistMePings: Optional[int] = Field(default=None, alias="assistMePings")
    
    
    
    assists: int = Field(alias="assists")
    
    
    
    baitPings: Optional[int] = Field(default=None, alias="baitPings")
    
    
    
    baronKills: int = Field(alias="baronKills")
    
    
    
    basicPings: Optional[int] = Field(default=None, alias="basicPings")
    
    
    
    bountyLevel: Optional[int] = Field(default=None, alias="bountyLevel")
    
    
    
    challenges: Optional[match_v5_ChallengesDto] = Field(default=None, alias="challenges")
    
    
    
    champExperience: int = Field(alias="champExperience")
    
    
    
    champLevel: int = Field(alias="champLevel")
    
    
    
    championId: int = Field(alias="championId")
    
    
    
    championName: str = Field(alias="championName")
    
    
    
    championSkinId: Optional[int] = Field(default=None, alias="championSkinId")
    
    
    
    championTransform: int = Field(alias="championTransform")
    
    
    
    commandPings: Optional[int] = Field(default=None, alias="commandPings")
    
    
    
    consumablesPurchased: int = Field(alias="consumablesPurchased")
    
    
    
    damageDealtToBuildings: Optional[int] = Field(default=None, alias="damageDealtToBuildings")
    
    
    
    damageDealtToEpicMonsters: Optional[int] = Field(default=None, alias="damageDealtToEpicMonsters")
    
    
    
    damageDealtToObjectives: int = Field(alias="damageDealtToObjectives")
    
    
    
    damageDealtToTurrets: int = Field(alias="damageDealtToTurrets")
    
    
    
    damageSelfMitigated: int = Field(alias="damageSelfMitigated")
    
    
    
    dangerPings: Optional[int] = Field(default=None, alias="dangerPings")
    
    
    
    deaths: int = Field(alias="deaths")
    
    
    
    detectorWardsPlaced: int = Field(alias="detectorWardsPlaced")
    
    
    
    doubleKills: int = Field(alias="doubleKills")
    
    
    
    dragonKills: int = Field(alias="dragonKills")
    
    
    
    eligibleForProgression: Optional[bool] = Field(default=None, alias="eligibleForProgression")
    
    
    
    enemyMissingPings: Optional[int] = Field(default=None, alias="enemyMissingPings")
    
    
    
    enemyVisionPings: Optional[int] = Field(default=None, alias="enemyVisionPings")
    
    
    
    firstBloodAssist: bool = Field(alias="firstBloodAssist")
    
    
    
    firstBloodKill: bool = Field(alias="firstBloodKill")
    
    
    
    firstTowerAssist: bool = Field(alias="firstTowerAssist")
    
    
    
    firstTowerKill: bool = Field(alias="firstTowerKill")
    
    
    
    gameEndedInEarlySurrender: bool = Field(alias="gameEndedInEarlySurrender")
    
    
    
    gameEndedInSurrender: bool = Field(alias="gameEndedInSurrender")
    
    
    
    getBackPings: Optional[int] = Field(default=None, alias="getBackPings")
    
    
    
    goldEarned: int = Field(alias="goldEarned")
    
    
    
    goldSpent: int = Field(alias="goldSpent")
    
    
    
    holdPings: Optional[int] = Field(default=None, alias="holdPings")
    
    
    
    individualPosition: str = Field(alias="individualPosition")
    
    
    
    inhibitorKills: int = Field(alias="inhibitorKills")
    
    
    
    inhibitorTakedowns: Optional[int] = Field(default=None, alias="inhibitorTakedowns")
    
    
    
    inhibitorsLost: Optional[int] = Field(default=None, alias="inhibitorsLost")
    
    
    
    item0: int = Field(alias="item0")
    
    
    
    item1: int = Field(alias="item1")
    
    
    
    item2: int = Field(alias="item2")
    
    
    
    item3: int = Field(alias="item3")
    
    
    
    item4: int = Field(alias="item4")
    
    
    
    item5: int = Field(alias="item5")
    
    
    
    item6: int = Field(alias="item6")
    
    
    
    itemsPurchased: int = Field(alias="itemsPurchased")
    
    
    
    killingSprees: int = Field(alias="killingSprees")
    
    
    
    kills: int = Field(alias="kills")
    
    
    
    lane: str = Field(alias="lane")
    
    
    
    largestCriticalStrike: int = Field(alias="largestCriticalStrike")
    
    
    
    largestKillingSpree: int = Field(alias="largestKillingSpree")
    
    
    
    largestMultiKill: int = Field(alias="largestMultiKill")
    
    
    
    longestTimeSpentLiving: int = Field(alias="longestTimeSpentLiving")
    
    
    
    magicDamageDealt: int = Field(alias="magicDamageDealt")
    
    
    
    magicDamageDealtToChampions: int = Field(alias="magicDamageDealtToChampions")
    
    
    
    magicDamageTaken: int = Field(alias="magicDamageTaken")
    
    
    
    missions: Optional[match_v5_MissionsDto] = Field(default=None, alias="missions")
    
    
    
    needVisionPings: Optional[int] = Field(default=None, alias="needVisionPings")
    
    
    
    neutralMinionsKilled: int = Field(alias="neutralMinionsKilled")
    
    
    
    nexusKills: int = Field(alias="nexusKills")
    
    
    
    nexusLost: Optional[int] = Field(default=None, alias="nexusLost")
    
    
    
    nexusTakedowns: Optional[int] = Field(default=None, alias="nexusTakedowns")
    
    
    
    objectivesStolen: int = Field(alias="objectivesStolen")
    
    
    
    objectivesStolenAssists: int = Field(alias="objectivesStolenAssists")
    
    
    
    onMyWayPings: Optional[int] = Field(default=None, alias="onMyWayPings")
    
    
    
    participantId: int = Field(alias="participantId")
    
    
    
    pentaKills: int = Field(alias="pentaKills")
    
    
    
    perks: match_v5_PerksDto = Field(alias="perks")
    
    
    
    physicalDamageDealt: int = Field(alias="physicalDamageDealt")
    
    
    
    physicalDamageDealtToChampions: int = Field(alias="physicalDamageDealtToChampions")
    
    
    
    physicalDamageTaken: int = Field(alias="physicalDamageTaken")
    
    
    
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
    
    
    
    profileIcon: int = Field(alias="profileIcon")
    
    
    
    pushPings: Optional[int] = Field(default=None, alias="pushPings")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    quadraKills: int = Field(alias="quadraKills")
    
    
    
    retreatPings: Optional[int] = Field(default=None, alias="retreatPings")
    
    
    
    riotIdGameName: Optional[str] = Field(default=None, alias="riotIdGameName")
    
    
    
    riotIdName: Optional[str] = Field(default=None, alias="riotIdName")
    
    
    
    riotIdTagline: Optional[str] = Field(default=None, alias="riotIdTagline")
    
    
    
    role: str = Field(alias="role")
    
    
    
    roleBoundItem: Optional[int] = Field(default=None, alias="roleBoundItem")
    
    
    
    sightWardsBoughtInGame: int = Field(alias="sightWardsBoughtInGame")
    
    
    
    spell1Casts: int = Field(alias="spell1Casts")
    
    
    
    spell2Casts: int = Field(alias="spell2Casts")
    
    
    
    spell3Casts: int = Field(alias="spell3Casts")
    
    
    
    spell4Casts: int = Field(alias="spell4Casts")
    
    
    
    subteamPlacement: Optional[int] = Field(default=None, alias="subteamPlacement")
    
    
    
    summoner1Casts: int = Field(alias="summoner1Casts")
    
    
    
    summoner1Id: int = Field(alias="summoner1Id")
    
    
    
    summoner2Casts: int = Field(alias="summoner2Casts")
    
    
    
    summoner2Id: int = Field(alias="summoner2Id")
    
    
    
    summonerId: str = Field(alias="summonerId")
    
    
    
    summonerLevel: int = Field(alias="summonerLevel")
    
    
    
    summonerName: str = Field(alias="summonerName")
    
    
    
    teamEarlySurrendered: bool = Field(alias="teamEarlySurrendered")
    
    
    
    teamId: int = Field(alias="teamId")
    
    
    
    teamPosition: str = Field(alias="teamPosition")
    
    
    
    timeCCingOthers: int = Field(alias="timeCCingOthers")
    
    
    
    timePlayed: int = Field(alias="timePlayed")
    
    
    
    totalAllyJungleMinionsKilled: Optional[int] = Field(default=None, alias="totalAllyJungleMinionsKilled")
    
    
    
    totalDamageDealt: int = Field(alias="totalDamageDealt")
    
    
    
    totalDamageDealtToChampions: int = Field(alias="totalDamageDealtToChampions")
    
    
    
    totalDamageShieldedOnTeammates: int = Field(alias="totalDamageShieldedOnTeammates")
    
    
    
    totalDamageTaken: int = Field(alias="totalDamageTaken")
    
    
    
    totalEnemyJungleMinionsKilled: Optional[int] = Field(default=None, alias="totalEnemyJungleMinionsKilled")
    
    
    
    totalHeal: int = Field(alias="totalHeal")
    
    
    
    totalHealsOnTeammates: int = Field(alias="totalHealsOnTeammates")
    
    
    
    totalMinionsKilled: int = Field(alias="totalMinionsKilled")
    
    
    
    totalTimeCCDealt: int = Field(alias="totalTimeCCDealt")
    
    
    
    totalTimeSpentDead: int = Field(alias="totalTimeSpentDead")
    
    
    
    totalUnitsHealed: int = Field(alias="totalUnitsHealed")
    
    
    
    tripleKills: int = Field(alias="tripleKills")
    
    
    
    trueDamageDealt: int = Field(alias="trueDamageDealt")
    
    
    
    trueDamageDealtToChampions: int = Field(alias="trueDamageDealtToChampions")
    
    
    
    trueDamageTaken: int = Field(alias="trueDamageTaken")
    
    
    
    turretKills: int = Field(alias="turretKills")
    
    
    
    turretTakedowns: Optional[int] = Field(default=None, alias="turretTakedowns")
    
    
    
    turretsLost: Optional[int] = Field(default=None, alias="turretsLost")
    
    
    
    unrealKills: int = Field(alias="unrealKills")
    
    
    
    visionClearedPings: Optional[int] = Field(default=None, alias="visionClearedPings")
    
    
    
    visionScore: int = Field(alias="visionScore")
    
    
    
    visionWardsBoughtInGame: int = Field(alias="visionWardsBoughtInGame")
    
    
    
    wardsKilled: int = Field(alias="wardsKilled")
    
    
    
    wardsPlaced: int = Field(alias="wardsPlaced")
    
    
    
    win: bool = Field(alias="win")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_ParticipantFrameDto(BaseModel):
    """
    No description provided.
    """
    
    
    championStats: match_v5_ChampionStatsDto = Field(alias="championStats")
    
    
    
    currentGold: int = Field(alias="currentGold")
    
    
    
    damageStats: match_v5_DamageStatsDto = Field(alias="damageStats")
    
    
    
    goldPerSecond: int = Field(alias="goldPerSecond")
    
    
    
    jungleMinionsKilled: int = Field(alias="jungleMinionsKilled")
    
    
    
    level: int = Field(alias="level")
    
    
    
    minionsKilled: int = Field(alias="minionsKilled")
    
    
    
    participantId: int = Field(alias="participantId")
    
    
    
    position: match_v5_PositionDto = Field(alias="position")
    
    
    
    timeEnemySpentControlled: int = Field(alias="timeEnemySpentControlled")
    
    
    
    totalGold: int = Field(alias="totalGold")
    
    
    
    xp: int = Field(alias="xp")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_ParticipantFramesDto(BaseModel):
    """
    No description provided.
    """
    
    
    param_1_9: match_v5_ParticipantFrameDto = Field(alias="1-9")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_ParticipantPlayerBehaviorDto(BaseModel):
    """
    No description provided.
    """
    
    
    PlayerBehavior_IsHeroInCombat: Optional[int] = Field(default=None, alias="PlayerBehavior_IsHeroInCombat")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_ParticipantTimeLineDto(BaseModel):
    """
    No description provided.
    """
    
    
    participantId: int = Field(alias="participantId")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_PerkStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    defense: int = Field(alias="defense")
    
    
    
    flex: int = Field(alias="flex")
    
    
    
    offense: int = Field(alias="offense")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_PerkStyleDto(BaseModel):
    """
    No description provided.
    """
    
    
    description: str = Field(alias="description")
    
    
    
    selections: List[match_v5_PerkStyleSelectionDto] = Field(alias="selections")
    
    
    
    style: int = Field(alias="style")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_PerkStyleSelectionDto(BaseModel):
    """
    No description provided.
    """
    
    
    perk: int = Field(alias="perk")
    
    
    
    var1: int = Field(alias="var1")
    
    
    
    var2: int = Field(alias="var2")
    
    
    
    var3: int = Field(alias="var3")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_PerksDto(BaseModel):
    """
    No description provided.
    """
    
    
    statPerks: match_v5_PerkStatsDto = Field(alias="statPerks")
    
    
    
    styles: List[match_v5_PerkStyleDto] = Field(alias="styles")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_PositionDto(BaseModel):
    """
    No description provided.
    """
    
    
    x: int = Field(alias="x")
    
    
    
    y: int = Field(alias="y")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_ReplayDTO(BaseModel):
    """
    No description provided.
    """
    
    
    matchFileURLs: List[str] = Field(alias="matchFileURLs")
    
    
    
    total: int = Field(alias="total")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_TeamDto(BaseModel):
    """
    No description provided.
    """
    
    
    bans: List[match_v5_BanDto] = Field(alias="bans")
    
    
    
    feats: Optional[match_v5_FeatsDto] = Field(default=None, alias="feats")
    
    
    
    objectives: match_v5_ObjectivesDto = Field(alias="objectives")
    
    
    
    teamId: int = Field(alias="teamId")
    
    
    
    win: bool = Field(alias="win")
    
    
    

    model_config = {"populate_by_name": True}




class match_v5_TimelineDto(BaseModel):
    """
    No description provided.
    """
    
    
    info: match_v5_InfoTimeLineDto = Field(alias="info")
    
    
    
    metadata: match_v5_MetadataTimeLineDto = Field(alias="metadata")
    
    
    

    model_config = {"populate_by_name": True}




class riftbound_content_v1_CardArtDTO(BaseModel):
    """
    No description provided.
    """
    
    
    artist: str = Field(alias="artist")
    
    
    
    fullURL: str = Field(alias="fullURL")
    
    
    
    thumbnailURL: str = Field(alias="thumbnailURL")
    
    
    

    model_config = {"populate_by_name": True}




class riftbound_content_v1_CardDTO(BaseModel):
    """
    No description provided.
    """
    
    
    art: riftbound_content_v1_CardArtDTO = Field(alias="art")
    
    
    
    collectorNumber: int = Field(alias="collectorNumber")
    
    
    
    description: str = Field(alias="description")
    
    
    
    faction: str = Field(alias="faction")
    
    
    
    flavorText: str = Field(alias="flavorText")
    
    
    
    id: str = Field(alias="id")
    
    
    
    keywords: List[str] = Field(alias="keywords")
    
    
    
    name: str = Field(alias="name")
    
    
    
    rarity: str = Field(alias="rarity")
    
    
    
    set: str = Field(alias="set")
    
    
    
    stats: riftbound_content_v1_CardStatsDTO = Field(alias="stats")
    
    
    
    tags: List[str] = Field(alias="tags")
    
    
    
    type: str = Field(alias="type")
    
    
    

    model_config = {"populate_by_name": True}




class riftbound_content_v1_CardStatsDTO(BaseModel):
    """
    No description provided.
    """
    
    
    cost: int = Field(alias="cost")
    
    
    
    energy: int = Field(alias="energy")
    
    
    
    might: int = Field(alias="might")
    
    
    
    power: int = Field(alias="power")
    
    
    

    model_config = {"populate_by_name": True}




class riftbound_content_v1_RiftboundContentDTO(BaseModel):
    """
    No description provided.
    """
    
    
    game: str = Field(alias="game")
    
    
    
    lastUpdated: str = Field(alias="lastUpdated")
    
    
    
    sets: List[riftbound_content_v1_SetDTO] = Field(alias="sets")
    
    
    
    version: str = Field(alias="version")
    
    
    

    model_config = {"populate_by_name": True}




class riftbound_content_v1_SetDTO(BaseModel):
    """
    No description provided.
    """
    
    
    cards: List[riftbound_content_v1_CardDTO] = Field(alias="cards")
    
    
    
    id: str = Field(alias="id")
    
    
    
    name: str = Field(alias="name")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_tft_v5_BannedChampion(BaseModel):
    """
    No description provided.
    """
    
    
    championId: int = Field(alias="championId")
    
    
    
    pickTurn: int = Field(alias="pickTurn")
    
    
    
    teamId: int = Field(alias="teamId")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_tft_v5_CurrentGameInfo(BaseModel):
    """
    No description provided.
    """
    
    
    bannedChampions: List[spectator_tft_v5_BannedChampion] = Field(alias="bannedChampions")
    
    
    
    gameId: int = Field(alias="gameId")
    
    
    
    gameLength: int = Field(alias="gameLength")
    
    
    
    gameMode: str = Field(alias="gameMode")
    
    
    
    gameQueueConfigId: Optional[int] = Field(default=None, alias="gameQueueConfigId")
    
    
    
    gameStartTime: int = Field(alias="gameStartTime")
    
    
    
    gameType: str = Field(alias="gameType")
    
    
    
    mapId: int = Field(alias="mapId")
    
    
    
    observers: spectator_tft_v5_Observer = Field(alias="observers")
    
    
    
    participants: List[spectator_tft_v5_CurrentGameParticipant] = Field(alias="participants")
    
    
    
    platformId: str = Field(alias="platformId")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_tft_v5_CurrentGameParticipant(BaseModel):
    """
    No description provided.
    """
    
    
    championId: int = Field(alias="championId")
    
    
    
    gameCustomizationObjects: List[spectator_tft_v5_GameCustomizationObject] = Field(alias="gameCustomizationObjects")
    
    
    
    perks: Optional[spectator_tft_v5_Perks] = Field(default=None, alias="perks")
    
    
    
    profileIconId: int = Field(alias="profileIconId")
    
    
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    
    
    riotId: Optional[str] = Field(default=None, alias="riotId")
    
    
    
    spell1Id: int = Field(alias="spell1Id")
    
    
    
    spell2Id: int = Field(alias="spell2Id")
    
    
    
    teamId: int = Field(alias="teamId")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_tft_v5_GameCustomizationObject(BaseModel):
    """
    No description provided.
    """
    
    
    category: str = Field(alias="category")
    
    
    
    content: str = Field(alias="content")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_tft_v5_Observer(BaseModel):
    """
    No description provided.
    """
    
    
    encryptionKey: str = Field(alias="encryptionKey")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_tft_v5_Perks(BaseModel):
    """
    No description provided.
    """
    
    
    perkIds: List[int] = Field(alias="perkIds")
    
    
    
    perkStyle: int = Field(alias="perkStyle")
    
    
    
    perkSubStyle: int = Field(alias="perkSubStyle")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_v5_BannedChampion(BaseModel):
    """
    No description provided.
    """
    
    
    championId: int = Field(alias="championId")
    
    
    
    pickTurn: int = Field(alias="pickTurn")
    
    
    
    teamId: int = Field(alias="teamId")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_v5_CurrentGameInfo(BaseModel):
    """
    No description provided.
    """
    
    
    bannedChampions: List[spectator_v5_BannedChampion] = Field(alias="bannedChampions")
    
    
    
    gameId: int = Field(alias="gameId")
    
    
    
    gameLength: int = Field(alias="gameLength")
    
    
    
    gameMode: str = Field(alias="gameMode")
    
    
    
    gameQueueConfigId: Optional[int] = Field(default=None, alias="gameQueueConfigId")
    
    
    
    gameStartTime: int = Field(alias="gameStartTime")
    
    
    
    gameType: str = Field(alias="gameType")
    
    
    
    mapId: int = Field(alias="mapId")
    
    
    
    observers: spectator_v5_Observer = Field(alias="observers")
    
    
    
    participants: List[spectator_v5_CurrentGameParticipant] = Field(alias="participants")
    
    
    
    platformId: str = Field(alias="platformId")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_v5_CurrentGameParticipant(BaseModel):
    """
    No description provided.
    """
    
    
    bot: bool = Field(alias="bot")
    
    
    
    championId: int = Field(alias="championId")
    
    
    
    gameCustomizationObjects: List[spectator_v5_GameCustomizationObject] = Field(alias="gameCustomizationObjects")
    
    
    
    perks: Optional[spectator_v5_Perks] = Field(default=None, alias="perks")
    
    
    
    profileIconId: int = Field(alias="profileIconId")
    
    
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    
    
    riotId: Optional[str] = Field(default=None, alias="riotId")
    
    
    
    spell1Id: int = Field(alias="spell1Id")
    
    
    
    spell2Id: int = Field(alias="spell2Id")
    
    
    
    teamId: int = Field(alias="teamId")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_v5_GameCustomizationObject(BaseModel):
    """
    No description provided.
    """
    
    
    category: str = Field(alias="category")
    
    
    
    content: str = Field(alias="content")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_v5_Observer(BaseModel):
    """
    No description provided.
    """
    
    
    encryptionKey: str = Field(alias="encryptionKey")
    
    
    

    model_config = {"populate_by_name": True}




class spectator_v5_Perks(BaseModel):
    """
    No description provided.
    """
    
    
    perkIds: List[int] = Field(alias="perkIds")
    
    
    
    perkStyle: int = Field(alias="perkStyle")
    
    
    
    perkSubStyle: int = Field(alias="perkSubStyle")
    
    
    

    model_config = {"populate_by_name": True}




class summoner_v4_SummonerDTO(BaseModel):
    """
    represents a summoner
    """
    
    
    id: Optional[str] = Field(default=None, alias="id")
    
    
    
    profileIconId: int = Field(alias="profileIconId")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    revisionDate: int = Field(alias="revisionDate")
    
    
    
    summonerLevel: int = Field(alias="summonerLevel")
    
    
    

    model_config = {"populate_by_name": True}




class tft_league_v1_LeagueEntryDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: Optional[bool] = Field(default=None, alias="freshBlood")
    
    
    
    hotStreak: Optional[bool] = Field(default=None, alias="hotStreak")
    
    
    
    inactive: Optional[bool] = Field(default=None, alias="inactive")
    
    
    
    leagueId: Optional[str] = Field(default=None, alias="leagueId")
    
    
    
    leaguePoints: Optional[int] = Field(default=None, alias="leaguePoints")
    
    
    
    losses: int = Field(alias="losses")
    
    
    
    miniSeries: Optional[tft_league_v1_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    
    
    queueType: str = Field(alias="queueType")
    
    
    
    rank: Optional[str] = Field(default=None, alias="rank")
    
    
    
    ratedRating: Optional[int] = Field(default=None, alias="ratedRating")
    
    
    
    ratedTier: Optional[str] = Field(default=None, alias="ratedTier")
    
    
    
    tier: Optional[str] = Field(default=None, alias="tier")
    
    
    
    veteran: Optional[bool] = Field(default=None, alias="veteran")
    
    
    
    wins: int = Field(alias="wins")
    
    
    

    model_config = {"populate_by_name": True}




class tft_league_v1_LeagueItemDTO(BaseModel):
    """
    No description provided.
    """
    
    
    freshBlood: bool = Field(alias="freshBlood")
    
    
    
    hotStreak: bool = Field(alias="hotStreak")
    
    
    
    inactive: bool = Field(alias="inactive")
    
    
    
    leaguePoints: int = Field(alias="leaguePoints")
    
    
    
    losses: int = Field(alias="losses")
    
    
    
    miniSeries: Optional[tft_league_v1_MiniSeriesDTO] = Field(default=None, alias="miniSeries")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    rank: str = Field(alias="rank")
    
    
    
    veteran: bool = Field(alias="veteran")
    
    
    
    wins: int = Field(alias="wins")
    
    
    

    model_config = {"populate_by_name": True}




class tft_league_v1_LeagueListDTO(BaseModel):
    """
    No description provided.
    """
    
    
    entries: List[tft_league_v1_LeagueItemDTO] = Field(alias="entries")
    
    
    
    leagueId: Optional[str] = Field(default=None, alias="leagueId")
    
    
    
    name: Optional[str] = Field(default=None, alias="name")
    
    
    
    queue: Optional[str] = Field(default=None, alias="queue")
    
    
    
    tier: str = Field(alias="tier")
    
    
    

    model_config = {"populate_by_name": True}




class tft_league_v1_MiniSeriesDTO(BaseModel):
    """
    No description provided.
    """
    
    
    losses: int = Field(alias="losses")
    
    
    
    progress: str = Field(alias="progress")
    
    
    
    target: int = Field(alias="target")
    
    
    
    wins: int = Field(alias="wins")
    
    
    

    model_config = {"populate_by_name": True}




class tft_league_v1_TopRatedLadderEntryDto(BaseModel):
    """
    No description provided.
    """
    
    
    previousUpdateLadderPosition: int = Field(alias="previousUpdateLadderPosition")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    ratedRating: int = Field(alias="ratedRating")
    
    
    
    ratedTier: str = Field(alias="ratedTier")
    
    
    
    wins: int = Field(alias="wins")
    
    
    

    model_config = {"populate_by_name": True}




class tft_match_v1_CompanionDto(BaseModel):
    """
    No description provided.
    """
    
    
    content_ID: str = Field(alias="content_ID")
    
    
    
    item_ID: int = Field(alias="item_ID")
    
    
    
    skin_ID: int = Field(alias="skin_ID")
    
    
    
    species: str = Field(alias="species")
    
    
    

    model_config = {"populate_by_name": True}




class tft_match_v1_InfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    endOfGameResult: Optional[str] = Field(default=None, alias="endOfGameResult")
    
    
    
    gameCreation: Optional[int] = Field(default=None, alias="gameCreation")
    
    
    
    gameId: Optional[int] = Field(default=None, alias="gameId")
    
    
    
    game_datetime: int = Field(alias="game_datetime")
    
    
    
    game_length: float = Field(alias="game_length")
    
    
    
    game_variation: Optional[str] = Field(default=None, alias="game_variation")
    
    
    
    game_version: str = Field(alias="game_version")
    
    
    
    mapId: Optional[int] = Field(default=None, alias="mapId")
    
    
    
    participants: List[tft_match_v1_ParticipantDto] = Field(alias="participants")
    
    
    
    queueId: Optional[int] = Field(default=None, alias="queueId")
    
    
    
    queue_id: int = Field(alias="queue_id")
    
    
    
    tft_game_type: Optional[str] = Field(default=None, alias="tft_game_type")
    
    
    
    tft_set_core_name: Optional[str] = Field(default=None, alias="tft_set_core_name")
    
    
    
    tft_set_number: int = Field(alias="tft_set_number")
    
    
    

    model_config = {"populate_by_name": True}




class tft_match_v1_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    info: tft_match_v1_InfoDto = Field(alias="info")
    
    
    
    metadata: tft_match_v1_MetadataDto = Field(alias="metadata")
    
    
    

    model_config = {"populate_by_name": True}




class tft_match_v1_MetadataDto(BaseModel):
    """
    No description provided.
    """
    
    
    data_version: str = Field(alias="data_version")
    
    
    
    match_id: str = Field(alias="match_id")
    
    
    
    participants: List[str] = Field(alias="participants")
    
    
    

    model_config = {"populate_by_name": True}




class tft_match_v1_ParticipantDto(BaseModel):
    """
    No description provided.
    """
    
    
    augments: Optional[List[str]] = Field(default=None, alias="augments")
    
    
    
    companion: tft_match_v1_CompanionDto = Field(alias="companion")
    
    
    
    gold_left: int = Field(alias="gold_left")
    
    
    
    last_round: int = Field(alias="last_round")
    
    
    
    level: int = Field(alias="level")
    
    
    
    missions: Optional[tft_match_v1_ParticipantMissionsDto] = Field(default=None, alias="missions")
    
    
    
    partner_group_id: Optional[int] = Field(default=None, alias="partner_group_id")
    
    
    
    placement: int = Field(alias="placement")
    
    
    
    players_eliminated: int = Field(alias="players_eliminated")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    pve_score: Optional[int] = Field(default=None, alias="pve_score")
    
    
    
    pve_wonrun: Optional[bool] = Field(default=None, alias="pve_wonrun")
    
    
    
    riotIdGameName: Optional[str] = Field(default=None, alias="riotIdGameName")
    
    
    
    riotIdTagline: Optional[str] = Field(default=None, alias="riotIdTagline")
    
    
    
    skill_tree: Optional[Dict[str, int]] = Field(default=None, alias="skill_tree")
    
    
    
    time_eliminated: float = Field(alias="time_eliminated")
    
    
    
    total_damage_to_players: int = Field(alias="total_damage_to_players")
    
    
    
    traits: List[tft_match_v1_TraitDto] = Field(alias="traits")
    
    
    
    units: List[tft_match_v1_UnitDto] = Field(alias="units")
    
    
    
    win: Optional[bool] = Field(default=None, alias="win")
    
    
    

    model_config = {"populate_by_name": True}




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
    
    
    

    model_config = {"populate_by_name": True}




class tft_match_v1_TraitDto(BaseModel):
    """
    No description provided.
    """
    
    
    name: str = Field(alias="name")
    
    
    
    num_units: int = Field(alias="num_units")
    
    
    
    style: Optional[int] = Field(default=None, alias="style")
    
    
    
    tier_current: int = Field(alias="tier_current")
    
    
    
    tier_total: Optional[int] = Field(default=None, alias="tier_total")
    
    
    

    model_config = {"populate_by_name": True}




class tft_match_v1_UnitDto(BaseModel):
    """
    No description provided.
    """
    
    
    character_id: str = Field(alias="character_id")
    
    
    
    chosen: Optional[str] = Field(default=None, alias="chosen")
    
    
    
    itemNames: Optional[List[str]] = Field(default=None, alias="itemNames")
    
    
    
    items: Optional[List[int]] = Field(default=None, alias="items")
    
    
    
    name: str = Field(alias="name")
    
    
    
    rarity: int = Field(alias="rarity")
    
    
    
    tier: int = Field(alias="tier")
    
    
    

    model_config = {"populate_by_name": True}




class tft_status_v1_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    content: str = Field(alias="content")
    
    
    
    locale: str = Field(alias="locale")
    
    
    

    model_config = {"populate_by_name": True}




class tft_status_v1_PlatformDataDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(alias="id")
    
    
    
    incidents: List[tft_status_v1_StatusDto] = Field(alias="incidents")
    
    
    
    locales: List[str] = Field(alias="locales")
    
    
    
    maintenances: List[tft_status_v1_StatusDto] = Field(alias="maintenances")
    
    
    
    name: str = Field(alias="name")
    
    
    

    model_config = {"populate_by_name": True}




class tft_status_v1_StatusDto(BaseModel):
    """
    No description provided.
    """
    
    
    archive_at: str = Field(alias="archive_at")
    
    
    
    created_at: str = Field(alias="created_at")
    
    
    
    id: int = Field(alias="id")
    
    
    
    incident_severity: str = Field(alias="incident_severity")
    
    
    
    maintenance_status: str = Field(alias="maintenance_status")
    
    
    
    platforms: List[str] = Field(alias="platforms")
    
    
    
    titles: List[tft_status_v1_ContentDto] = Field(alias="titles")
    
    
    
    updated_at: str = Field(alias="updated_at")
    
    
    
    updates: List[tft_status_v1_UpdateDto] = Field(alias="updates")
    
    
    

    model_config = {"populate_by_name": True}




class tft_status_v1_UpdateDto(BaseModel):
    """
    No description provided.
    """
    
    
    author: str = Field(alias="author")
    
    
    
    created_at: str = Field(alias="created_at")
    
    
    
    id: int = Field(alias="id")
    
    
    
    publish: bool = Field(alias="publish")
    
    
    
    publish_locations: List[str] = Field(alias="publish_locations")
    
    
    
    translations: List[tft_status_v1_ContentDto] = Field(alias="translations")
    
    
    
    updated_at: str = Field(alias="updated_at")
    
    
    

    model_config = {"populate_by_name": True}




class tft_summoner_v1_SummonerDTO(BaseModel):
    """
    represents a summoner
    """
    
    
    id: Optional[str] = Field(default=None, alias="id")
    
    
    
    profileIconId: int = Field(alias="profileIconId")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    revisionDate: int = Field(alias="revisionDate")
    
    
    
    summonerLevel: int = Field(alias="summonerLevel")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_stub_v5_LobbyEventV5DTO(BaseModel):
    """
    No description provided.
    """
    
    
    eventType: str = Field(alias="eventType")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    timestamp: str = Field(alias="timestamp")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_stub_v5_LobbyEventV5DTOWrapper(BaseModel):
    """
    No description provided.
    """
    
    
    eventList: List[tournament_stub_v5_LobbyEventV5DTO] = Field(alias="eventList")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_stub_v5_ProviderRegistrationParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    region: str = Field(alias="region")
    
    
    
    url: str = Field(alias="url")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_stub_v5_TournamentCodeParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    allowedParticipants: Optional[List[str]] = Field(default=None, alias="allowedParticipants")
    
    
    
    enoughPlayers: bool = Field(alias="enoughPlayers")
    
    
    
    mapType: str = Field(alias="mapType")
    
    
    
    metadata: Optional[str] = Field(default=None, alias="metadata")
    
    
    
    pickType: str = Field(alias="pickType")
    
    
    
    spectatorType: str = Field(alias="spectatorType")
    
    
    
    teamSize: int = Field(alias="teamSize")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_stub_v5_TournamentCodeV5DTO(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(alias="code")
    
    
    
    id: int = Field(alias="id")
    
    
    
    lobbyName: str = Field(alias="lobbyName")
    
    
    
    map: str = Field(alias="map")
    
    
    
    metaData: str = Field(alias="metaData")
    
    
    
    participants: List[str] = Field(alias="participants")
    
    
    
    password: str = Field(alias="password")
    
    
    
    pickType: str = Field(alias="pickType")
    
    
    
    providerId: int = Field(alias="providerId")
    
    
    
    region: str = Field(alias="region")
    
    
    
    teamSize: int = Field(alias="teamSize")
    
    
    
    tournamentId: int = Field(alias="tournamentId")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_stub_v5_TournamentRegistrationParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    name: Optional[str] = Field(default=None, alias="name")
    
    
    
    providerId: int = Field(alias="providerId")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_v5_LobbyEventV5DTO(BaseModel):
    """
    No description provided.
    """
    
    
    eventType: str = Field(alias="eventType")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    timestamp: str = Field(alias="timestamp")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_v5_LobbyEventV5DTOWrapper(BaseModel):
    """
    No description provided.
    """
    
    
    eventList: List[tournament_v5_LobbyEventV5DTO] = Field(alias="eventList")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_v5_ProviderRegistrationParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    region: str = Field(alias="region")
    
    
    
    url: str = Field(alias="url")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_v5_TournamentCodeParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    allowedParticipants: Optional[List[str]] = Field(default=None, alias="allowedParticipants")
    
    
    
    enoughPlayers: bool = Field(alias="enoughPlayers")
    
    
    
    mapType: str = Field(alias="mapType")
    
    
    
    metadata: Optional[str] = Field(default=None, alias="metadata")
    
    
    
    pickType: str = Field(alias="pickType")
    
    
    
    spectatorType: str = Field(alias="spectatorType")
    
    
    
    teamSize: int = Field(alias="teamSize")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_v5_TournamentCodeUpdateParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    allowedParticipants: Optional[List[str]] = Field(default=None, alias="allowedParticipants")
    
    
    
    mapType: str = Field(alias="mapType")
    
    
    
    pickType: str = Field(alias="pickType")
    
    
    
    spectatorType: str = Field(alias="spectatorType")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_v5_TournamentCodeV5DTO(BaseModel):
    """
    No description provided.
    """
    
    
    code: str = Field(alias="code")
    
    
    
    id: int = Field(alias="id")
    
    
    
    lobbyName: str = Field(alias="lobbyName")
    
    
    
    map: str = Field(alias="map")
    
    
    
    metaData: str = Field(alias="metaData")
    
    
    
    participants: List[str] = Field(alias="participants")
    
    
    
    password: str = Field(alias="password")
    
    
    
    pickType: str = Field(alias="pickType")
    
    
    
    providerId: int = Field(alias="providerId")
    
    
    
    region: str = Field(alias="region")
    
    
    
    spectators: str = Field(alias="spectators")
    
    
    
    teamSize: int = Field(alias="teamSize")
    
    
    
    tournamentId: int = Field(alias="tournamentId")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_v5_TournamentGamesV5(BaseModel):
    """
    No description provided.
    """
    
    
    gameId: int = Field(alias="gameId")
    
    
    
    gameMap: int = Field(alias="gameMap")
    
    
    
    gameMode: str = Field(alias="gameMode")
    
    
    
    gameName: str = Field(alias="gameName")
    
    
    
    gameType: str = Field(alias="gameType")
    
    
    
    losingTeam: List[tournament_v5_TournamentTeamV5] = Field(alias="losingTeam")
    
    
    
    metaData: Optional[str] = Field(default=None, alias="metaData")
    
    
    
    region: str = Field(alias="region")
    
    
    
    shortCode: str = Field(alias="shortCode")
    
    
    
    startTime: int = Field(alias="startTime")
    
    
    
    winningTeam: List[tournament_v5_TournamentTeamV5] = Field(alias="winningTeam")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_v5_TournamentRegistrationParametersV5(BaseModel):
    """
    No description provided.
    """
    
    
    name: Optional[str] = Field(default=None, alias="name")
    
    
    
    providerId: int = Field(alias="providerId")
    
    
    

    model_config = {"populate_by_name": True}




class tournament_v5_TournamentTeamV5(BaseModel):
    """
    No description provided.
    """
    
    
    puuid: str = Field(alias="puuid")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_AbilityCastsDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability1Casts: int = Field(alias="ability1Casts")
    
    
    
    ability2Casts: int = Field(alias="ability2Casts")
    
    
    
    grenadeCasts: int = Field(alias="grenadeCasts")
    
    
    
    ultimateCasts: int = Field(alias="ultimateCasts")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_AbilityDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability1Effects: Optional[str] = Field(default=None, alias="ability1Effects")
    
    
    
    ability2Effects: Optional[str] = Field(default=None, alias="ability2Effects")
    
    
    
    grenadeEffects: Optional[str] = Field(default=None, alias="grenadeEffects")
    
    
    
    ultimateEffects: Optional[str] = Field(default=None, alias="ultimateEffects")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_CoachDto(BaseModel):
    """
    No description provided.
    """
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    teamId: str = Field(alias="teamId")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_DamageDto(BaseModel):
    """
    No description provided.
    """
    
    
    bodyshots: int = Field(alias="bodyshots")
    
    
    
    damage: int = Field(alias="damage")
    
    
    
    headshots: int = Field(alias="headshots")
    
    
    
    legshots: int = Field(alias="legshots")
    
    
    
    receiver: str = Field(alias="receiver")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_EconomyDto(BaseModel):
    """
    No description provided.
    """
    
    
    armor: str = Field(alias="armor")
    
    
    
    loadoutValue: int = Field(alias="loadoutValue")
    
    
    
    remaining: int = Field(alias="remaining")
    
    
    
    spent: int = Field(alias="spent")
    
    
    
    weapon: str = Field(alias="weapon")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_FinishingDamageDto(BaseModel):
    """
    No description provided.
    """
    
    
    damageItem: str = Field(alias="damageItem")
    
    
    
    damageType: str = Field(alias="damageType")
    
    
    
    isSecondaryFireMode: bool = Field(alias="isSecondaryFireMode")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_KillDto(BaseModel):
    """
    No description provided.
    """
    
    
    assistants: List[str] = Field(alias="assistants")
    
    
    
    finishingDamage: val_console_match_v1_FinishingDamageDto = Field(alias="finishingDamage")
    
    
    
    killer: str = Field(alias="killer")
    
    
    
    playerLocations: List[val_console_match_v1_PlayerLocationsDto] = Field(alias="playerLocations")
    
    
    
    timeSinceGameStartMillis: int = Field(alias="timeSinceGameStartMillis")
    
    
    
    timeSinceRoundStartMillis: int = Field(alias="timeSinceRoundStartMillis")
    
    
    
    victim: str = Field(alias="victim")
    
    
    
    victimLocation: val_console_match_v1_LocationDto = Field(alias="victimLocation")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_LocationDto(BaseModel):
    """
    No description provided.
    """
    
    
    x: int = Field(alias="x")
    
    
    
    y: int = Field(alias="y")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    coaches: List[val_console_match_v1_CoachDto] = Field(alias="coaches")
    
    
    
    matchInfo: val_console_match_v1_MatchInfoDto = Field(alias="matchInfo")
    
    
    
    players: List[val_console_match_v1_PlayerDto] = Field(alias="players")
    
    
    
    roundResults: Optional[List[val_console_match_v1_RoundResultDto]] = Field(default=None, alias="roundResults")
    
    
    
    teams: Optional[List[val_console_match_v1_TeamDto]] = Field(default=None, alias="teams")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_MatchInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    customGameName: str = Field(alias="customGameName")
    
    
    
    gameLengthMillis: Optional[int] = Field(default=None, alias="gameLengthMillis")
    
    
    
    gameMode: str = Field(alias="gameMode")
    
    
    
    gameStartMillis: int = Field(alias="gameStartMillis")
    
    
    
    isCompleted: bool = Field(alias="isCompleted")
    
    
    
    isRanked: bool = Field(alias="isRanked")
    
    
    
    mapId: str = Field(alias="mapId")
    
    
    
    matchId: str = Field(alias="matchId")
    
    
    
    provisioningFlowId: str = Field(alias="provisioningFlowId")
    
    
    
    queueId: str = Field(alias="queueId")
    
    
    
    seasonId: str = Field(alias="seasonId")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_MatchlistDto(BaseModel):
    """
    No description provided.
    """
    
    
    history: List[val_console_match_v1_MatchlistEntryDto] = Field(alias="history")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_MatchlistEntryDto(BaseModel):
    """
    No description provided.
    """
    
    
    gameStartTimeMillis: int = Field(alias="gameStartTimeMillis")
    
    
    
    matchId: str = Field(alias="matchId")
    
    
    
    queueId: str = Field(alias="queueId")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    characterId: Optional[str] = Field(default=None, alias="characterId")
    
    
    
    competitiveTier: int = Field(alias="competitiveTier")
    
    
    
    gameName: str = Field(alias="gameName")
    
    
    
    partyId: str = Field(alias="partyId")
    
    
    
    playerCard: str = Field(alias="playerCard")
    
    
    
    playerTitle: str = Field(alias="playerTitle")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    stats: Optional[val_console_match_v1_PlayerStatsDto] = Field(default=None, alias="stats")
    
    
    
    tagLine: str = Field(alias="tagLine")
    
    
    
    teamId: str = Field(alias="teamId")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_PlayerLocationsDto(BaseModel):
    """
    No description provided.
    """
    
    
    location: val_console_match_v1_LocationDto = Field(alias="location")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    viewRadians: float = Field(alias="viewRadians")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_PlayerRoundStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability: val_console_match_v1_AbilityDto = Field(alias="ability")
    
    
    
    damage: List[val_console_match_v1_DamageDto] = Field(alias="damage")
    
    
    
    economy: val_console_match_v1_EconomyDto = Field(alias="economy")
    
    
    
    kills: List[val_console_match_v1_KillDto] = Field(alias="kills")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    score: int = Field(alias="score")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_PlayerStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    abilityCasts: Optional[val_console_match_v1_AbilityCastsDto] = Field(default=None, alias="abilityCasts")
    
    
    
    assists: int = Field(alias="assists")
    
    
    
    deaths: int = Field(alias="deaths")
    
    
    
    kills: int = Field(alias="kills")
    
    
    
    playtimeMillis: int = Field(alias="playtimeMillis")
    
    
    
    roundsPlayed: int = Field(alias="roundsPlayed")
    
    
    
    score: int = Field(alias="score")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_RecentMatchesDto(BaseModel):
    """
    No description provided.
    """
    
    
    currentTime: int = Field(alias="currentTime")
    
    
    
    matchIds: List[str] = Field(alias="matchIds")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_RoundResultDto(BaseModel):
    """
    No description provided.
    """
    
    
    bombDefuser: Optional[str] = Field(default=None, alias="bombDefuser")
    
    
    
    bombPlanter: Optional[str] = Field(default=None, alias="bombPlanter")
    
    
    
    defuseLocation: val_console_match_v1_LocationDto = Field(alias="defuseLocation")
    
    
    
    defusePlayerLocations: Optional[List[val_console_match_v1_PlayerLocationsDto]] = Field(default=None, alias="defusePlayerLocations")
    
    
    
    defuseRoundTime: int = Field(alias="defuseRoundTime")
    
    
    
    plantLocation: val_console_match_v1_LocationDto = Field(alias="plantLocation")
    
    
    
    plantPlayerLocations: Optional[List[val_console_match_v1_PlayerLocationsDto]] = Field(default=None, alias="plantPlayerLocations")
    
    
    
    plantRoundTime: int = Field(alias="plantRoundTime")
    
    
    
    plantSite: str = Field(alias="plantSite")
    
    
    
    playerStats: List[val_console_match_v1_PlayerRoundStatsDto] = Field(alias="playerStats")
    
    
    
    roundCeremony: str = Field(alias="roundCeremony")
    
    
    
    roundNum: int = Field(alias="roundNum")
    
    
    
    roundResult: str = Field(alias="roundResult")
    
    
    
    roundResultCode: str = Field(alias="roundResultCode")
    
    
    
    winningTeam: str = Field(alias="winningTeam")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_match_v1_TeamDto(BaseModel):
    """
    No description provided.
    """
    
    
    numPoints: int = Field(alias="numPoints")
    
    
    
    roundsPlayed: int = Field(alias="roundsPlayed")
    
    
    
    roundsWon: int = Field(alias="roundsWon")
    
    
    
    teamId: str = Field(alias="teamId")
    
    
    
    won: bool = Field(alias="won")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_ranked_v1_LeaderboardDto(BaseModel):
    """
    No description provided.
    """
    
    
    actId: str = Field(alias="actId")
    
    
    
    players: List[val_console_ranked_v1_PlayerDto] = Field(alias="players")
    
    
    
    query: Optional[str] = Field(default=None, alias="query")
    
    
    
    shard: str = Field(alias="shard")
    
    
    
    tierDetails: Optional[List[val_console_ranked_v1_TierDto]] = Field(default=None, alias="tierDetails")
    
    
    
    totalPlayers: int = Field(alias="totalPlayers")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_ranked_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    gameName: Optional[str] = Field(default=None, alias="gameName")
    
    
    
    leaderboardRank: int = Field(alias="leaderboardRank")
    
    
    
    numberOfWins: int = Field(alias="numberOfWins")
    
    
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    
    
    rankedRating: int = Field(alias="rankedRating")
    
    
    
    tagLine: Optional[str] = Field(default=None, alias="tagLine")
    
    
    

    model_config = {"populate_by_name": True}




class val_console_ranked_v1_TierDto(BaseModel):
    """
    UNKNOWN TYPE.
    """
    
    
    pass
    

    model_config = {"populate_by_name": True}




class val_content_v1_ActDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(alias="id")
    
    
    
    isActive: bool = Field(alias="isActive")
    
    
    
    localizedNames: Optional[val_content_v1_LocalizedNamesDto] = Field(default=None, alias="localizedNames")
    
    
    
    name: str = Field(alias="name")
    
    
    
    parentId: Optional[str] = Field(default=None, alias="parentId")
    
    
    
    type: Optional[str] = Field(default=None, alias="type")
    
    
    

    model_config = {"populate_by_name": True}




class val_content_v1_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    acts: List[val_content_v1_ActDto] = Field(alias="acts")
    
    
    
    ceremonies: Optional[List[val_content_v1_ContentItemDto]] = Field(default=None, alias="ceremonies")
    
    
    
    characters: List[val_content_v1_ContentItemDto] = Field(alias="characters")
    
    
    
    charmLevels: List[val_content_v1_ContentItemDto] = Field(alias="charmLevels")
    
    
    
    charms: List[val_content_v1_ContentItemDto] = Field(alias="charms")
    
    
    
    chromas: List[val_content_v1_ContentItemDto] = Field(alias="chromas")
    
    
    
    equips: List[val_content_v1_ContentItemDto] = Field(alias="equips")
    
    
    
    gameModes: List[val_content_v1_ContentItemDto] = Field(alias="gameModes")
    
    
    
    maps: List[val_content_v1_ContentItemDto] = Field(alias="maps")
    
    
    
    playerCards: List[val_content_v1_ContentItemDto] = Field(alias="playerCards")
    
    
    
    playerTitles: List[val_content_v1_ContentItemDto] = Field(alias="playerTitles")
    
    
    
    skinLevels: List[val_content_v1_ContentItemDto] = Field(alias="skinLevels")
    
    
    
    skins: List[val_content_v1_ContentItemDto] = Field(alias="skins")
    
    
    
    sprayLevels: List[val_content_v1_ContentItemDto] = Field(alias="sprayLevels")
    
    
    
    sprays: List[val_content_v1_ContentItemDto] = Field(alias="sprays")
    
    
    
    totems: Optional[List[val_content_v1_ContentItemDto]] = Field(default=None, alias="totems")
    
    
    
    version: str = Field(alias="version")
    
    
    

    model_config = {"populate_by_name": True}




class val_content_v1_ContentItemDto(BaseModel):
    """
    No description provided.
    """
    
    
    assetName: str = Field(alias="assetName")
    
    
    
    assetPath: Optional[str] = Field(default=None, alias="assetPath")
    
    
    
    id: str = Field(alias="id")
    
    
    
    localizedNames: Optional[val_content_v1_LocalizedNamesDto] = Field(default=None, alias="localizedNames")
    
    
    
    name: str = Field(alias="name")
    
    
    

    model_config = {"populate_by_name": True}




class val_content_v1_LocalizedNamesDto(BaseModel):
    """
    No description provided.
    """
    
    
    ar_AE: str = Field(alias="ar-AE")
    
    
    
    de_DE: str = Field(alias="de-DE")
    
    
    
    en_GB: Optional[str] = Field(default=None, alias="en-GB")
    
    
    
    en_US: str = Field(alias="en-US")
    
    
    
    es_ES: str = Field(alias="es-ES")
    
    
    
    es_MX: str = Field(alias="es-MX")
    
    
    
    fr_FR: str = Field(alias="fr-FR")
    
    
    
    id_ID: str = Field(alias="id-ID")
    
    
    
    it_IT: str = Field(alias="it-IT")
    
    
    
    ja_JP: str = Field(alias="ja-JP")
    
    
    
    ko_KR: str = Field(alias="ko-KR")
    
    
    
    pl_PL: str = Field(alias="pl-PL")
    
    
    
    pt_BR: str = Field(alias="pt-BR")
    
    
    
    ru_RU: str = Field(alias="ru-RU")
    
    
    
    th_TH: str = Field(alias="th-TH")
    
    
    
    tr_TR: str = Field(alias="tr-TR")
    
    
    
    vi_VN: str = Field(alias="vi-VN")
    
    
    
    zh_CN: str = Field(alias="zh-CN")
    
    
    
    zh_TW: str = Field(alias="zh-TW")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_AbilityCastsDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability1Casts: int = Field(alias="ability1Casts")
    
    
    
    ability2Casts: int = Field(alias="ability2Casts")
    
    
    
    grenadeCasts: int = Field(alias="grenadeCasts")
    
    
    
    ultimateCasts: int = Field(alias="ultimateCasts")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_AbilityDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability1Effects: Optional[str] = Field(default=None, alias="ability1Effects")
    
    
    
    ability2Effects: Optional[str] = Field(default=None, alias="ability2Effects")
    
    
    
    grenadeEffects: Optional[str] = Field(default=None, alias="grenadeEffects")
    
    
    
    ultimateEffects: Optional[str] = Field(default=None, alias="ultimateEffects")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_CoachDto(BaseModel):
    """
    No description provided.
    """
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    teamId: str = Field(alias="teamId")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_DamageDto(BaseModel):
    """
    No description provided.
    """
    
    
    bodyshots: int = Field(alias="bodyshots")
    
    
    
    damage: int = Field(alias="damage")
    
    
    
    headshots: int = Field(alias="headshots")
    
    
    
    legshots: int = Field(alias="legshots")
    
    
    
    receiver: str = Field(alias="receiver")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_EconomyDto(BaseModel):
    """
    No description provided.
    """
    
    
    armor: str = Field(alias="armor")
    
    
    
    loadoutValue: int = Field(alias="loadoutValue")
    
    
    
    remaining: int = Field(alias="remaining")
    
    
    
    spent: int = Field(alias="spent")
    
    
    
    weapon: str = Field(alias="weapon")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_FinishingDamageDto(BaseModel):
    """
    No description provided.
    """
    
    
    damageItem: str = Field(alias="damageItem")
    
    
    
    damageType: str = Field(alias="damageType")
    
    
    
    isSecondaryFireMode: bool = Field(alias="isSecondaryFireMode")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_KillDto(BaseModel):
    """
    No description provided.
    """
    
    
    assistants: List[str] = Field(alias="assistants")
    
    
    
    finishingDamage: val_match_v1_FinishingDamageDto = Field(alias="finishingDamage")
    
    
    
    killer: str = Field(alias="killer")
    
    
    
    playerLocations: List[val_match_v1_PlayerLocationsDto] = Field(alias="playerLocations")
    
    
    
    timeSinceGameStartMillis: int = Field(alias="timeSinceGameStartMillis")
    
    
    
    timeSinceRoundStartMillis: int = Field(alias="timeSinceRoundStartMillis")
    
    
    
    victim: str = Field(alias="victim")
    
    
    
    victimLocation: val_match_v1_LocationDto = Field(alias="victimLocation")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_LocationDto(BaseModel):
    """
    No description provided.
    """
    
    
    x: int = Field(alias="x")
    
    
    
    y: int = Field(alias="y")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_MatchDto(BaseModel):
    """
    No description provided.
    """
    
    
    coaches: List[val_match_v1_CoachDto] = Field(alias="coaches")
    
    
    
    matchInfo: val_match_v1_MatchInfoDto = Field(alias="matchInfo")
    
    
    
    players: List[val_match_v1_PlayerDto] = Field(alias="players")
    
    
    
    roundResults: Optional[List[val_match_v1_RoundResultDto]] = Field(default=None, alias="roundResults")
    
    
    
    teams: Optional[List[val_match_v1_TeamDto]] = Field(default=None, alias="teams")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_MatchInfoDto(BaseModel):
    """
    No description provided.
    """
    
    
    customGameName: str = Field(alias="customGameName")
    
    
    
    gameLengthMillis: Optional[int] = Field(default=None, alias="gameLengthMillis")
    
    
    
    gameMode: str = Field(alias="gameMode")
    
    
    
    gameStartMillis: int = Field(alias="gameStartMillis")
    
    
    
    gameVersion: str = Field(alias="gameVersion")
    
    
    
    isCompleted: bool = Field(alias="isCompleted")
    
    
    
    isRanked: bool = Field(alias="isRanked")
    
    
    
    mapId: str = Field(alias="mapId")
    
    
    
    matchId: str = Field(alias="matchId")
    
    
    
    premierMatchInfo: Dict[str, Any] = Field(alias="premierMatchInfo")
    
    
    
    provisioningFlowId: str = Field(alias="provisioningFlowId")
    
    
    
    queueId: str = Field(alias="queueId")
    
    
    
    region: str = Field(alias="region")
    
    
    
    seasonId: str = Field(alias="seasonId")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_MatchlistDto(BaseModel):
    """
    No description provided.
    """
    
    
    history: List[val_match_v1_MatchlistEntryDto] = Field(alias="history")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_MatchlistEntryDto(BaseModel):
    """
    No description provided.
    """
    
    
    gameStartTimeMillis: int = Field(alias="gameStartTimeMillis")
    
    
    
    matchId: str = Field(alias="matchId")
    
    
    
    queueId: str = Field(alias="queueId")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    accountLevel: int = Field(alias="accountLevel")
    
    
    
    characterId: Optional[str] = Field(default=None, alias="characterId")
    
    
    
    competitiveTier: int = Field(alias="competitiveTier")
    
    
    
    gameName: str = Field(alias="gameName")
    
    
    
    isObserver: bool = Field(alias="isObserver")
    
    
    
    partyId: str = Field(alias="partyId")
    
    
    
    playerCard: str = Field(alias="playerCard")
    
    
    
    playerTitle: str = Field(alias="playerTitle")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    stats: Optional[val_match_v1_PlayerStatsDto] = Field(default=None, alias="stats")
    
    
    
    tagLine: str = Field(alias="tagLine")
    
    
    
    teamId: str = Field(alias="teamId")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_PlayerLocationsDto(BaseModel):
    """
    No description provided.
    """
    
    
    location: val_match_v1_LocationDto = Field(alias="location")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    viewRadians: float = Field(alias="viewRadians")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_PlayerRoundStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    ability: val_match_v1_AbilityDto = Field(alias="ability")
    
    
    
    damage: List[val_match_v1_DamageDto] = Field(alias="damage")
    
    
    
    economy: val_match_v1_EconomyDto = Field(alias="economy")
    
    
    
    kills: List[val_match_v1_KillDto] = Field(alias="kills")
    
    
    
    puuid: str = Field(alias="puuid")
    
    
    
    score: int = Field(alias="score")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_PlayerStatsDto(BaseModel):
    """
    No description provided.
    """
    
    
    abilityCasts: Optional[val_match_v1_AbilityCastsDto] = Field(default=None, alias="abilityCasts")
    
    
    
    assists: int = Field(alias="assists")
    
    
    
    deaths: int = Field(alias="deaths")
    
    
    
    kills: int = Field(alias="kills")
    
    
    
    playtimeMillis: int = Field(alias="playtimeMillis")
    
    
    
    roundsPlayed: int = Field(alias="roundsPlayed")
    
    
    
    score: int = Field(alias="score")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_RecentMatchesDto(BaseModel):
    """
    No description provided.
    """
    
    
    currentTime: int = Field(alias="currentTime")
    
    
    
    matchIds: List[str] = Field(alias="matchIds")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_RoundResultDto(BaseModel):
    """
    No description provided.
    """
    
    
    bombDefuser: Optional[str] = Field(default=None, alias="bombDefuser")
    
    
    
    bombPlanter: Optional[str] = Field(default=None, alias="bombPlanter")
    
    
    
    defuseLocation: val_match_v1_LocationDto = Field(alias="defuseLocation")
    
    
    
    defusePlayerLocations: Optional[List[val_match_v1_PlayerLocationsDto]] = Field(default=None, alias="defusePlayerLocations")
    
    
    
    defuseRoundTime: int = Field(alias="defuseRoundTime")
    
    
    
    plantLocation: val_match_v1_LocationDto = Field(alias="plantLocation")
    
    
    
    plantPlayerLocations: Optional[List[val_match_v1_PlayerLocationsDto]] = Field(default=None, alias="plantPlayerLocations")
    
    
    
    plantRoundTime: int = Field(alias="plantRoundTime")
    
    
    
    plantSite: str = Field(alias="plantSite")
    
    
    
    playerStats: List[val_match_v1_PlayerRoundStatsDto] = Field(alias="playerStats")
    
    
    
    roundCeremony: str = Field(alias="roundCeremony")
    
    
    
    roundNum: int = Field(alias="roundNum")
    
    
    
    roundResult: str = Field(alias="roundResult")
    
    
    
    roundResultCode: str = Field(alias="roundResultCode")
    
    
    
    winningTeam: str = Field(alias="winningTeam")
    
    
    
    winningTeamRole: str = Field(alias="winningTeamRole")
    
    
    

    model_config = {"populate_by_name": True}




class val_match_v1_TeamDto(BaseModel):
    """
    No description provided.
    """
    
    
    numPoints: int = Field(alias="numPoints")
    
    
    
    roundsPlayed: int = Field(alias="roundsPlayed")
    
    
    
    roundsWon: int = Field(alias="roundsWon")
    
    
    
    teamId: str = Field(alias="teamId")
    
    
    
    won: bool = Field(alias="won")
    
    
    

    model_config = {"populate_by_name": True}




class val_ranked_v1_LeaderboardDto(BaseModel):
    """
    No description provided.
    """
    
    
    actId: str = Field(alias="actId")
    
    
    
    immortalStartingIndex: Optional[int] = Field(default=None, alias="immortalStartingIndex")
    
    
    
    immortalStartingPage: Optional[int] = Field(default=None, alias="immortalStartingPage")
    
    
    
    players: List[val_ranked_v1_PlayerDto] = Field(alias="players")
    
    
    
    query: Optional[str] = Field(default=None, alias="query")
    
    
    
    shard: str = Field(alias="shard")
    
    
    
    startIndex: Optional[int] = Field(default=None, alias="startIndex")
    
    
    
    tierDetails: Optional[Dict[str, val_ranked_v1_TierDetailDto]] = Field(default=None, alias="tierDetails")
    
    
    
    topTierRRThreshold: Optional[int] = Field(default=None, alias="topTierRRThreshold")
    
    
    
    totalPlayers: int = Field(alias="totalPlayers")
    
    
    

    model_config = {"populate_by_name": True}




class val_ranked_v1_PlayerDto(BaseModel):
    """
    No description provided.
    """
    
    
    competitiveTier: Optional[int] = Field(default=None, alias="competitiveTier")
    
    
    
    gameName: Optional[str] = Field(default=None, alias="gameName")
    
    
    
    leaderboardRank: int = Field(alias="leaderboardRank")
    
    
    
    numberOfWins: int = Field(alias="numberOfWins")
    
    
    
    prefix: Optional[str] = Field(default=None, alias="prefix")
    
    
    
    premierRosterType: str = Field(alias="premierRosterType")
    
    
    
    puuid: Optional[str] = Field(default=None, alias="puuid")
    
    
    
    rankedRating: int = Field(alias="rankedRating")
    
    
    
    tagLine: Optional[str] = Field(default=None, alias="tagLine")
    
    
    

    model_config = {"populate_by_name": True}




class val_ranked_v1_TierDetailDto(BaseModel):
    """
    No description provided.
    """
    
    
    rankedRatingThreshold: int = Field(alias="rankedRatingThreshold")
    
    
    
    startingIndex: int = Field(alias="startingIndex")
    
    
    
    startingPage: int = Field(alias="startingPage")
    
    
    

    model_config = {"populate_by_name": True}




class val_status_v1_ContentDto(BaseModel):
    """
    No description provided.
    """
    
    
    content: str = Field(alias="content")
    
    
    
    locale: str = Field(alias="locale")
    
    
    

    model_config = {"populate_by_name": True}




class val_status_v1_PlatformDataDto(BaseModel):
    """
    No description provided.
    """
    
    
    id: str = Field(alias="id")
    
    
    
    incidents: List[val_status_v1_StatusDto] = Field(alias="incidents")
    
    
    
    locales: List[str] = Field(alias="locales")
    
    
    
    maintenances: List[val_status_v1_StatusDto] = Field(alias="maintenances")
    
    
    
    name: str = Field(alias="name")
    
    
    

    model_config = {"populate_by_name": True}




class val_status_v1_StatusDto(BaseModel):
    """
    No description provided.
    """
    
    
    archive_at: str = Field(alias="archive_at")
    
    
    
    created_at: str = Field(alias="created_at")
    
    
    
    id: int = Field(alias="id")
    
    
    
    incident_severity: str = Field(alias="incident_severity")
    
    
    
    maintenance_status: str = Field(alias="maintenance_status")
    
    
    
    platforms: List[str] = Field(alias="platforms")
    
    
    
    titles: List[val_status_v1_ContentDto] = Field(alias="titles")
    
    
    
    updated_at: str = Field(alias="updated_at")
    
    
    
    updates: List[val_status_v1_UpdateDto] = Field(alias="updates")
    
    
    

    model_config = {"populate_by_name": True}




class val_status_v1_UpdateDto(BaseModel):
    """
    No description provided.
    """
    
    
    author: str = Field(alias="author")
    
    
    
    created_at: str = Field(alias="created_at")
    
    
    
    id: int = Field(alias="id")
    
    
    
    publish: bool = Field(alias="publish")
    
    
    
    publish_locations: List[str] = Field(alias="publish_locations")
    
    
    
    translations: List[val_status_v1_ContentDto] = Field(alias="translations")
    
    
    
    updated_at: str = Field(alias="updated_at")
    
    
    

    model_config = {"populate_by_name": True}




# Rebuild all models to resolve forward references
for _name, _obj in list(locals().items()):
    if isinstance(_obj, type) and issubclass(_obj, BaseModel) and _obj is not BaseModel:
        try:
            _obj.model_rebuild()
        except Exception:
            pass  # some models may not need rebuilding
del _name, _obj
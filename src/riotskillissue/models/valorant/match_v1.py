from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AbilityCasts(BaseModel):
    ability1_casts: int = Field(
        alias="ability1Casts",
    )
    ability2_casts: int = Field(
        alias="ability2Casts",
    )
    grenade_casts: int = Field(
        alias="grenadeCasts",
    )
    ultimate_casts: int = Field(
        alias="ultimateCasts",
    )

    model_config = ConfigDict(populate_by_name=True)


class Ability(BaseModel):
    ability1_effects: Optional[str] = Field(
        default=None,
        alias="ability1Effects",
    )
    ability2_effects: Optional[str] = Field(
        default=None,
        alias="ability2Effects",
    )
    grenade_effects: Optional[str] = Field(
        default=None,
        alias="grenadeEffects",
    )
    ultimate_effects: Optional[str] = Field(
        default=None,
        alias="ultimateEffects",
    )

    model_config = ConfigDict(populate_by_name=True)


class Coach(BaseModel):
    puuid: str = Field(
        alias="puuid",
    )
    team_id: str = Field(
        alias="teamId",
    )

    model_config = ConfigDict(populate_by_name=True)


class Damage(BaseModel):
    bodyshots: int = Field(
        alias="bodyshots",
    )
    damage: int = Field(
        alias="damage",
    )
    headshots: int = Field(
        alias="headshots",
    )
    legshots: int = Field(
        alias="legshots",
    )
    receiver: str = Field(
        alias="receiver",
        description="PUUID",
    )

    model_config = ConfigDict(populate_by_name=True)


class Economy(BaseModel):
    armor: str = Field(
        alias="armor",
    )
    loadout_value: int = Field(
        alias="loadoutValue",
    )
    remaining: int = Field(
        alias="remaining",
    )
    spent: int = Field(
        alias="spent",
    )
    weapon: str = Field(
        alias="weapon",
    )

    model_config = ConfigDict(populate_by_name=True)


class FinishingDamage(BaseModel):
    damage_item: str = Field(
        alias="damageItem",
    )
    damage_type: str = Field(
        alias="damageType",
    )
    is_secondary_fire_mode: bool = Field(
        alias="isSecondaryFireMode",
    )

    model_config = ConfigDict(populate_by_name=True)


class Kill(BaseModel):
    assistants: List[str] = Field(
        alias="assistants",
        description="List of PUUIDs",
    )
    finishing_damage: FinishingDamage = Field(
        alias="finishingDamage",
    )
    killer: str = Field(
        alias="killer",
        description="PUUID",
    )
    player_locations: List[PlayerLocations] = Field(
        alias="playerLocations",
    )
    time_since_game_start_millis: int = Field(
        alias="timeSinceGameStartMillis",
    )
    time_since_round_start_millis: int = Field(
        alias="timeSinceRoundStartMillis",
    )
    victim: str = Field(
        alias="victim",
        description="PUUID",
    )
    victim_location: Location = Field(
        alias="victimLocation",
    )

    model_config = ConfigDict(populate_by_name=True)


class Location(BaseModel):
    x: int = Field(
        alias="x",
    )
    y: int = Field(
        alias="y",
    )

    model_config = ConfigDict(populate_by_name=True)


class Match(BaseModel):
    coaches: List[Coach] = Field(
        alias="coaches",
    )
    match_info: MatchInfo = Field(
        alias="matchInfo",
    )
    players: List[Player] = Field(
        alias="players",
    )
    round_results: Optional[List[RoundResult]] = Field(
        default=None,
        alias="roundResults",
    )
    teams: Optional[List[Team]] = Field(
        default=None,
        alias="teams",
    )

    model_config = ConfigDict(populate_by_name=True)


class MatchInfo(BaseModel):
    custom_game_name: str = Field(
        alias="customGameName",
    )
    game_length_millis: Optional[int] = Field(
        default=None,
        alias="gameLengthMillis",
    )
    game_mode: str = Field(
        alias="gameMode",
    )
    game_start_millis: int = Field(
        alias="gameStartMillis",
    )
    game_version: str = Field(
        alias="gameVersion",
    )
    is_completed: bool = Field(
        alias="isCompleted",
    )
    is_ranked: bool = Field(
        alias="isRanked",
    )
    map_id: str = Field(
        alias="mapId",
    )
    match_id: str = Field(
        alias="matchId",
    )
    premier_match_info: Dict[str, Any] = Field(
        alias="premierMatchInfo",
    )
    provisioning_flow_id: str = Field(
        alias="provisioningFlowId",
    )
    queue_id: str = Field(
        alias="queueId",
    )
    region: str = Field(
        alias="region",
    )
    season_id: str = Field(
        alias="seasonId",
    )

    model_config = ConfigDict(populate_by_name=True)


class Matchlist(BaseModel):
    history: List[MatchlistEntry] = Field(
        alias="history",
    )
    puuid: str = Field(
        alias="puuid",
    )

    model_config = ConfigDict(populate_by_name=True)


class MatchlistEntry(BaseModel):
    game_start_time_millis: int = Field(
        alias="gameStartTimeMillis",
    )
    match_id: str = Field(
        alias="matchId",
    )
    queue_id: str = Field(
        alias="queueId",
    )

    model_config = ConfigDict(populate_by_name=True)


class Player(BaseModel):
    account_level: int = Field(
        alias="accountLevel",
    )
    character_id: Optional[str] = Field(
        default=None,
        alias="characterId",
    )
    competitive_tier: int = Field(
        alias="competitiveTier",
    )
    game_name: str = Field(
        alias="gameName",
    )
    is_observer: bool = Field(
        alias="isObserver",
    )
    party_id: str = Field(
        alias="partyId",
    )
    player_card: str = Field(
        alias="playerCard",
    )
    player_title: str = Field(
        alias="playerTitle",
    )
    puuid: str = Field(
        alias="puuid",
    )
    stats: Optional[PlayerStats] = Field(
        default=None,
        alias="stats",
    )
    tag_line: str = Field(
        alias="tagLine",
    )
    team_id: str = Field(
        alias="teamId",
    )

    model_config = ConfigDict(populate_by_name=True)


class PlayerLocations(BaseModel):
    location: Location = Field(
        alias="location",
    )
    puuid: str = Field(
        alias="puuid",
    )
    view_radians: float = Field(
        alias="viewRadians",
    )

    model_config = ConfigDict(populate_by_name=True)


class PlayerRoundStats(BaseModel):
    ability: Ability = Field(
        alias="ability",
    )
    damage: List[Damage] = Field(
        alias="damage",
    )
    economy: Economy = Field(
        alias="economy",
    )
    kills: List[Kill] = Field(
        alias="kills",
    )
    puuid: str = Field(
        alias="puuid",
    )
    score: int = Field(
        alias="score",
    )

    model_config = ConfigDict(populate_by_name=True)


class PlayerStats(BaseModel):
    ability_casts: Optional[AbilityCasts] = Field(
        default=None,
        alias="abilityCasts",
    )
    assists: int = Field(
        alias="assists",
    )
    deaths: int = Field(
        alias="deaths",
    )
    kills: int = Field(
        alias="kills",
    )
    playtime_millis: int = Field(
        alias="playtimeMillis",
    )
    rounds_played: int = Field(
        alias="roundsPlayed",
    )
    score: int = Field(
        alias="score",
    )

    model_config = ConfigDict(populate_by_name=True)


class RecentMatches(BaseModel):
    current_time: int = Field(
        alias="currentTime",
    )
    match_ids: List[str] = Field(
        alias="matchIds",
        description="A list of recent match ids.",
    )

    model_config = ConfigDict(populate_by_name=True)


class RoundResult(BaseModel):
    bomb_defuser: Optional[str] = Field(
        default=None,
        alias="bombDefuser",
        description="PUUID of player",
    )
    bomb_planter: Optional[str] = Field(
        default=None,
        alias="bombPlanter",
        description="PUUID of player",
    )
    defuse_location: Location = Field(
        alias="defuseLocation",
    )
    defuse_player_locations: Optional[List[PlayerLocations]] = Field(
        default=None,
        alias="defusePlayerLocations",
    )
    defuse_round_time: int = Field(
        alias="defuseRoundTime",
    )
    plant_location: Location = Field(
        alias="plantLocation",
    )
    plant_player_locations: Optional[List[PlayerLocations]] = Field(
        default=None,
        alias="plantPlayerLocations",
    )
    plant_round_time: int = Field(
        alias="plantRoundTime",
    )
    plant_site: str = Field(
        alias="plantSite",
    )
    player_stats: List[PlayerRoundStats] = Field(
        alias="playerStats",
    )
    round_ceremony: str = Field(
        alias="roundCeremony",
    )
    round_num: int = Field(
        alias="roundNum",
    )
    round_result: str = Field(
        alias="roundResult",
    )
    round_result_code: str = Field(
        alias="roundResultCode",
    )
    winning_team: str = Field(
        alias="winningTeam",
    )
    winning_team_role: str = Field(
        alias="winningTeamRole",
    )

    model_config = ConfigDict(populate_by_name=True)


class Team(BaseModel):
    num_points: int = Field(
        alias="numPoints",
        description="".join(("Team points scored. Number of kills in deathma", "tch.")),
    )
    rounds_played: int = Field(
        alias="roundsPlayed",
    )
    rounds_won: int = Field(
        alias="roundsWon",
    )
    team_id: str = Field(
        alias="teamId",
        description="".join(
            (
                "This is an arbitrary string. Red and Blue in b",
                "omb modes. The puuid of the player in deathmat",
                "ch.",
            )
        ),
    )
    won: bool = Field(
        alias="won",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    AbilityCasts,
    Ability,
    Coach,
    Damage,
    Economy,
    FinishingDamage,
    Kill,
    Location,
    Match,
    MatchInfo,
    Matchlist,
    MatchlistEntry,
    Player,
    PlayerLocations,
    PlayerRoundStats,
    PlayerStats,
    RecentMatches,
    RoundResult,
    Team,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Companion(BaseModel):
    content_id: str = Field(
        alias="content_ID",
    )
    item_id: int = Field(
        alias="item_ID",
    )
    skin_id: int = Field(
        alias="skin_ID",
    )
    species: str = Field(
        alias="species",
    )

    model_config = ConfigDict(populate_by_name=True)


class Info(BaseModel):
    end_of_game_result: Optional[str] = Field(
        default=None,
        alias="endOfGameResult",
    )
    game_creation: Optional[int] = Field(
        default=None,
        alias="gameCreation",
    )
    game_id: Optional[int] = Field(
        default=None,
        alias="gameId",
    )
    game_datetime: int = Field(
        alias="game_datetime",
        description="Unix timestamp.",
    )
    game_length: float = Field(
        alias="game_length",
        description="Game length in seconds.",
    )
    game_variation: Optional[str] = Field(
        default=None,
        alias="game_variation",
        description="".join(
            ("Deprecated. Game variation key. Game variation", "s documented in TFT static data.")
        ),
    )
    game_version: str = Field(
        alias="game_version",
        description="Game client version.",
    )
    map_id: Optional[int] = Field(
        default=None,
        alias="mapId",
    )
    participants: List[Participant] = Field(
        alias="participants",
    )
    queue_id_1: Optional[int] = Field(
        default=None,
        alias="queueId",
        description="".join(("Please refer to the League of Legends document", "ation.")),
    )
    queue_id: int = Field(
        alias="queue_id",
        description="".join(("Please refer to the League of Legends document", "ation.")),
    )
    tft_game_type: Optional[str] = Field(
        default=None,
        alias="tft_game_type",
    )
    tft_set_core_name: Optional[str] = Field(
        default=None,
        alias="tft_set_core_name",
    )
    tft_set_number: int = Field(
        alias="tft_set_number",
        description="Teamfight Tactics set number.",
    )

    model_config = ConfigDict(populate_by_name=True)


class Match(BaseModel):
    info: Info = Field(
        alias="info",
        description="Match info.",
    )
    metadata: Metadata = Field(
        alias="metadata",
        description="Match metadata.",
    )

    model_config = ConfigDict(populate_by_name=True)


class Metadata(BaseModel):
    data_version: str = Field(
        alias="data_version",
        description="Match data version.",
    )
    match_id: str = Field(
        alias="match_id",
        description="Match id.",
    )
    participants: List[str] = Field(
        alias="participants",
        description="A list of participant PUUIDs.",
    )

    model_config = ConfigDict(populate_by_name=True)


class Participant(BaseModel):
    augments: Optional[List[str]] = Field(
        default=None,
        alias="augments",
    )
    companion: Companion = Field(
        alias="companion",
        description="Participant's companion.",
    )
    gold_left: int = Field(
        alias="gold_left",
        description="Gold left after participant was eliminated.",
    )
    last_round: int = Field(
        alias="last_round",
        description="".join(
            (
                "The round the participant was eliminated in. N",
                "ote: If the player was eliminated in stage 2-1",
                " their last_round would be 5.",
            )
        ),
    )
    level: int = Field(
        alias="level",
        description="".join(
            ("Participant Little Legend level. Note: This is", " not the number of active units.")
        ),
    )
    missions: Optional[ParticipantMissions] = Field(
        default=None,
        alias="missions",
    )
    partner_group_id: Optional[int] = Field(
        default=None,
        alias="partner_group_id",
    )
    placement: int = Field(
        alias="placement",
        description="Participant placement upon elimination.",
    )
    players_eliminated: int = Field(
        alias="players_eliminated",
        description="Number of players the participant eliminated.",
    )
    puuid: str = Field(
        alias="puuid",
    )
    pve_score: Optional[int] = Field(
        default=None,
        alias="pve_score",
    )
    pve_wonrun: Optional[bool] = Field(
        default=None,
        alias="pve_wonrun",
    )
    riot_id_game_name: Optional[str] = Field(
        default=None,
        alias="riotIdGameName",
    )
    riot_id_tagline: Optional[str] = Field(
        default=None,
        alias="riotIdTagline",
    )
    skill_tree: Optional[Dict[str, int]] = Field(
        default=None,
        alias="skill_tree",
    )
    time_eliminated: float = Field(
        alias="time_eliminated",
        description="".join(("The number of seconds before the participant w", "as eliminated.")),
    )
    total_damage_to_players: int = Field(
        alias="total_damage_to_players",
        description="Damage the participant dealt to other players.",
    )
    traits: List[Trait] = Field(
        alias="traits",
        description="".join(("A complete list of traits for the participant'", "s active units.")),
    )
    units: List[Unit] = Field(
        alias="units",
        description="A list of active units for the participant.",
    )
    win: Optional[bool] = Field(
        default=None,
        alias="win",
    )

    model_config = ConfigDict(populate_by_name=True)


class ParticipantMissions(BaseModel):
    assists: Optional[int] = Field(
        default=None,
        alias="Assists",
    )
    damage_dealt: Optional[int] = Field(
        default=None,
        alias="DamageDealt",
    )
    damage_dealt_to_objectives: Optional[int] = Field(
        default=None,
        alias="DamageDealtToObjectives",
    )
    damage_dealt_to_turrets: Optional[int] = Field(
        default=None,
        alias="DamageDealtToTurrets",
    )
    damage_taken: Optional[int] = Field(
        default=None,
        alias="DamageTaken",
    )
    deaths: Optional[int] = Field(
        default=None,
        alias="Deaths",
    )
    double_kills: Optional[int] = Field(
        default=None,
        alias="DoubleKills",
    )
    gold_earned: Optional[int] = Field(
        default=None,
        alias="GoldEarned",
    )
    gold_spent: Optional[int] = Field(
        default=None,
        alias="GoldSpent",
    )
    inhibitors_destroyed: Optional[int] = Field(
        default=None,
        alias="InhibitorsDestroyed",
    )
    killing_sprees: Optional[int] = Field(
        default=None,
        alias="KillingSprees",
    )
    kills: Optional[int] = Field(
        default=None,
        alias="Kills",
    )
    largest_killing_spree: Optional[int] = Field(
        default=None,
        alias="LargestKillingSpree",
    )
    largest_multi_kill: Optional[int] = Field(
        default=None,
        alias="LargestMultiKill",
    )
    magic_damage_dealt: Optional[int] = Field(
        default=None,
        alias="MagicDamageDealt",
    )
    magic_damage_dealt_to_champions: Optional[int] = Field(
        default=None,
        alias="MagicDamageDealtToChampions",
    )
    magic_damage_taken: Optional[int] = Field(
        default=None,
        alias="MagicDamageTaken",
    )
    neutral_minions_killed_team_jungle: Optional[int] = Field(
        default=None,
        alias="NeutralMinionsKilledTeamJungle",
    )
    penta_kills: Optional[int] = Field(
        default=None,
        alias="PentaKills",
    )
    physical_damage_dealt: Optional[int] = Field(
        default=None,
        alias="PhysicalDamageDealt",
    )
    physical_damage_dealt_to_champions: Optional[int] = Field(
        default=None,
        alias="PhysicalDamageDealtToChampions",
    )
    physical_damage_taken: Optional[int] = Field(
        default=None,
        alias="PhysicalDamageTaken",
    )
    player_score0: Optional[int] = Field(
        default=None,
        alias="PlayerScore0",
    )
    player_score1: Optional[int] = Field(
        default=None,
        alias="PlayerScore1",
    )
    player_score10: Optional[int] = Field(
        default=None,
        alias="PlayerScore10",
    )
    player_score11: Optional[int] = Field(
        default=None,
        alias="PlayerScore11",
    )
    player_score2: Optional[int] = Field(
        default=None,
        alias="PlayerScore2",
    )
    player_score3: Optional[int] = Field(
        default=None,
        alias="PlayerScore3",
    )
    player_score4: Optional[int] = Field(
        default=None,
        alias="PlayerScore4",
    )
    player_score5: Optional[int] = Field(
        default=None,
        alias="PlayerScore5",
    )
    player_score6: Optional[int] = Field(
        default=None,
        alias="PlayerScore6",
    )
    player_score9: Optional[int] = Field(
        default=None,
        alias="PlayerScore9",
    )
    quadra_kills: Optional[int] = Field(
        default=None,
        alias="QuadraKills",
    )
    spell1_casts: Optional[int] = Field(
        default=None,
        alias="Spell1Casts",
    )
    spell2_casts: Optional[int] = Field(
        default=None,
        alias="Spell2Casts",
    )
    spell3_casts: Optional[int] = Field(
        default=None,
        alias="Spell3Casts",
    )
    spell4_casts: Optional[int] = Field(
        default=None,
        alias="Spell4Casts",
    )
    summoner_spell1_casts: Optional[int] = Field(
        default=None,
        alias="SummonerSpell1Casts",
    )
    time_cc_others: Optional[int] = Field(
        default=None,
        alias="TimeCCOthers",
    )
    total_damage_dealt_to_champions: Optional[int] = Field(
        default=None,
        alias="TotalDamageDealtToChampions",
    )
    total_minions_killed: Optional[int] = Field(
        default=None,
        alias="TotalMinionsKilled",
    )
    triple_kills: Optional[int] = Field(
        default=None,
        alias="TripleKills",
    )
    true_damage_dealt: Optional[int] = Field(
        default=None,
        alias="TrueDamageDealt",
    )
    true_damage_dealt_to_champions: Optional[int] = Field(
        default=None,
        alias="TrueDamageDealtToChampions",
    )
    true_damage_taken: Optional[int] = Field(
        default=None,
        alias="TrueDamageTaken",
    )
    unreal_kills: Optional[int] = Field(
        default=None,
        alias="UnrealKills",
    )
    vision_score: Optional[int] = Field(
        default=None,
        alias="VisionScore",
    )
    wards_killed: Optional[int] = Field(
        default=None,
        alias="WardsKilled",
    )

    model_config = ConfigDict(populate_by_name=True)


class Trait(BaseModel):
    name: str = Field(
        alias="name",
        description="Trait name.",
    )
    num_units: int = Field(
        alias="num_units",
        description="Number of units with this trait.",
    )
    style: Optional[int] = Field(
        default=None,
        alias="style",
        description="".join(
            (
                "Current style for this trait. (0 = No style, 1",
                " = Bronze, 2 = Silver, 3 = Gold, 4 = Chromatic",
                ")",
            )
        ),
    )
    tier_current: int = Field(
        alias="tier_current",
        description="Current active tier for the trait.",
    )
    tier_total: Optional[int] = Field(
        default=None,
        alias="tier_total",
        description="Total tiers for the trait.",
    )

    model_config = ConfigDict(populate_by_name=True)


class Unit(BaseModel):
    character_id: str = Field(
        alias="character_id",
        description="".join(("This field was introduced in patch 9.22 with d", "ata_version 2.")),
    )
    chosen: Optional[str] = Field(
        default=None,
        alias="chosen",
        description="".join(
            (
                "If a unit is chosen as part of the Fates set m",
                "echanic, the chosen trait will be indicated by",
                " this field. Otherwise this field is excluded ",
                "from the response.",
            )
        ),
    )
    item_names: Optional[List[str]] = Field(
        default=None,
        alias="itemNames",
    )
    items: Optional[List[int]] = Field(
        default=None,
        alias="items",
        description="".join(
            (
                "A list of the unit's items. Please refer to th",
                "e Teamfight Tactics documentation for item ids",
                ".",
            )
        ),
    )
    name: str = Field(
        alias="name",
        description="Unit name. This field is often left blank.",
    )
    rarity: int = Field(
        alias="rarity",
        description="".join(("Unit rarity. This doesn't equate to the unit c", "ost.")),
    )
    tier: int = Field(
        alias="tier",
        description="Unit tier.",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Companion,
    Info,
    Match,
    Metadata,
    Participant,
    ParticipantMissions,
    Trait,
    Unit,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

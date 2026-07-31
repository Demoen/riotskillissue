from __future__ import annotations

from typing import Dict, List, Literal, Optional, TypeAlias

from pydantic import BaseModel, ConfigDict, Field


class ApexPlayerInfo(BaseModel):
    position: int = Field(
        alias="position",
    )
    puuid: str = Field(
        alias="puuid",
    )
    value: float = Field(
        alias="value",
    )

    model_config = ConfigDict(populate_by_name=True)


class ChallengeConfigInfo(BaseModel):
    end_timestamp: Optional[int] = Field(
        default=None,
        alias="endTimestamp",
    )
    id: int = Field(
        alias="id",
    )
    leaderboard: bool = Field(
        alias="leaderboard",
    )
    localized_names: Dict[str, Dict[str, str]] = Field(
        alias="localizedNames",
    )
    start_timestamp: Optional[int] = Field(
        default=None,
        alias="startTimestamp",
    )
    state: Literal["DISABLED", "HIDDEN", "ENABLED", "ARCHIVED"] = Field(
        alias="state",
        description="".join(
            (
                "DISABLED - not visible and not calculated, HID",
                "DEN - not visible, but calculated, ENABLED - v",
                "isible and calculated, ARCHIVED - visible, but",
                " not calculated",
            )
        ),
    )
    thresholds: Dict[str, float] = Field(
        alias="thresholds",
    )
    tracking: Optional[Literal["LIFETIME", "SEASON"]] = Field(
        default=None,
        alias="tracking",
        description="".join(
            (
                "LIFETIME - stats are incremented without reset",
                ", SEASON - stats are accumulated by season and",
                " reset at the beginning of new season",
            )
        ),
    )

    model_config = ConfigDict(populate_by_name=True)


class ChallengeInfo(BaseModel):
    achieved_time: Optional[int] = Field(
        default=None,
        alias="achievedTime",
    )
    challenge_id: int = Field(
        alias="challengeId",
    )
    level: Literal[
        "NONE",
        "IRON",
        "BRONZE",
        "SILVER",
        "GOLD",
        "PLATINUM",
        "DIAMOND",
        "MASTER",
        "GRANDMASTER",
        "CHALLENGER",
        "HIGHEST_NOT_LEADERBOARD_ONLY",
        "HIGHEST",
        "LOWEST",
    ] = Field(
        alias="level",
        description="".join(
            (
                "(Legal values:  NONE,  IRON,  BRONZE,  SILVER,",
                "  GOLD,  PLATINUM,  DIAMOND,  MASTER,  GRANDMA",
                "STER,  CHALLENGER,  HIGHEST_NOT_LEADERBOARD_ON",
                "LY,  HIGHEST,  LOWEST)",
            )
        ),
    )
    percentile: float = Field(
        alias="percentile",
    )
    players_in_level: Optional[int] = Field(
        default=None,
        alias="playersInLevel",
    )
    position: Optional[int] = Field(
        default=None,
        alias="position",
    )
    value: float = Field(
        alias="value",
    )

    model_config = ConfigDict(populate_by_name=True)


class ChallengePoint(BaseModel):
    current: int = Field(
        alias="current",
    )
    level: str = Field(
        alias="level",
    )
    max: int = Field(
        alias="max",
    )
    percentile: Optional[float] = Field(
        default=None,
        alias="percentile",
    )
    position: Optional[int] = Field(
        default=None,
        alias="position",
    )

    model_config = ConfigDict(populate_by_name=True)


Level: TypeAlias = Literal[
    "NONE",
    "IRON",
    "BRONZE",
    "SILVER",
    "GOLD",
    "PLATINUM",
    "DIAMOND",
    "MASTER",
    "GRANDMASTER",
    "CHALLENGER",
]


class PlayerClientPreferences(BaseModel):
    banner_accent: Optional[str] = Field(
        default=None,
        alias="bannerAccent",
    )
    challenge_ids: Optional[List[int]] = Field(
        default=None,
        alias="challengeIds",
    )
    crest_border: Optional[str] = Field(
        default=None,
        alias="crestBorder",
    )
    prestige_crest_border_level: Optional[int] = Field(
        default=None,
        alias="prestigeCrestBorderLevel",
    )
    title: Optional[str] = Field(
        default=None,
        alias="title",
    )

    model_config = ConfigDict(populate_by_name=True)


class PlayerInfo(BaseModel):
    category_points: Dict[str, ChallengePoint] = Field(
        alias="categoryPoints",
    )
    challenges: List[ChallengeInfo] = Field(
        alias="challenges",
    )
    preferences: PlayerClientPreferences = Field(
        alias="preferences",
    )
    total_points: ChallengePoint = Field(
        alias="totalPoints",
    )

    model_config = ConfigDict(populate_by_name=True)


State: TypeAlias = Literal["DISABLED", "HIDDEN", "ENABLED", "ARCHIVED"]

Tracking: TypeAlias = Literal["LIFETIME", "SEASON"]

_MODEL_TYPES = (
    ApexPlayerInfo,
    ChallengeConfigInfo,
    ChallengeInfo,
    ChallengePoint,
    PlayerClientPreferences,
    PlayerInfo,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

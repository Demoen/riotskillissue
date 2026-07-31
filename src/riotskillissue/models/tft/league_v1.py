from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class LeagueEntry(BaseModel):
    fresh_blood: Optional[bool] = Field(
        default=None,
        alias="freshBlood",
        description="".join(("Not included for the RANKED_TFT_TURBO queueTyp", "e.")),
    )
    hot_streak: Optional[bool] = Field(
        default=None,
        alias="hotStreak",
        description="".join(("Not included for the RANKED_TFT_TURBO queueTyp", "e.")),
    )
    inactive: Optional[bool] = Field(
        default=None,
        alias="inactive",
        description="".join(("Not included for the RANKED_TFT_TURBO queueTyp", "e.")),
    )
    league_id: Optional[str] = Field(
        default=None,
        alias="leagueId",
        description="".join(("Not included for the RANKED_TFT_TURBO queueTyp", "e.")),
    )
    league_points: Optional[int] = Field(
        default=None,
        alias="leaguePoints",
        description="".join(("Not included for the RANKED_TFT_TURBO queueTyp", "e.")),
    )
    losses: int = Field(
        alias="losses",
        description="Second through eighth placement.",
    )
    mini_series: Optional[MiniSeries] = Field(
        default=None,
        alias="miniSeries",
        description="".join(("Not included for the RANKED_TFT_TURBO queueTyp", "e.")),
    )
    puuid: Optional[str] = Field(
        default=None,
        alias="puuid",
        description="".join(
            ("Player Universal Unique Identifier. Exact leng", "th of 78 characters. (Encrypted)")
        ),
    )
    queue_type: str = Field(
        alias="queueType",
    )
    rank: Optional[str] = Field(
        default=None,
        alias="rank",
        description="".join(
            (
                "The player's division within a tier. Not inclu",
                "ded for the RANKED_TFT_TURBO queueType.",
            )
        ),
    )
    rated_rating: Optional[int] = Field(
        default=None,
        alias="ratedRating",
        description="".join(("Only included for the RANKED_TFT_TURBO queueTy", "pe.")),
    )
    rated_tier: Optional[Literal["ORANGE", "PURPLE", "BLUE", "GREEN", "GRAY"]] = Field(
        default=None,
        alias="ratedTier",
        description="".join(
            (
                "Only included for the RANKED_TFT_TURBO queueTy",
                "pe.\n             (Legal values:  ORANGE,  PURP",
                "LE,  BLUE,  GREEN,  GRAY)",
            )
        ),
    )
    tier: Optional[str] = Field(
        default=None,
        alias="tier",
        description="".join(("Not included for the RANKED_TFT_TURBO queueTyp", "e.")),
    )
    veteran: Optional[bool] = Field(
        default=None,
        alias="veteran",
        description="".join(("Not included for the RANKED_TFT_TURBO queueTyp", "e.")),
    )
    wins: int = Field(
        alias="wins",
        description="First placement.",
    )

    model_config = ConfigDict(populate_by_name=True)


class LeagueItem(BaseModel):
    fresh_blood: bool = Field(
        alias="freshBlood",
    )
    hot_streak: bool = Field(
        alias="hotStreak",
    )
    inactive: bool = Field(
        alias="inactive",
    )
    league_points: int = Field(
        alias="leaguePoints",
    )
    losses: int = Field(
        alias="losses",
        description="Second through eighth placement.",
    )
    mini_series: Optional[MiniSeries] = Field(
        default=None,
        alias="miniSeries",
    )
    puuid: str = Field(
        alias="puuid",
        description="Player's encrypted puuid.",
    )
    rank: str = Field(
        alias="rank",
    )
    veteran: bool = Field(
        alias="veteran",
    )
    wins: int = Field(
        alias="wins",
        description="First placement.",
    )

    model_config = ConfigDict(populate_by_name=True)


class LeagueList(BaseModel):
    entries: List[LeagueItem] = Field(
        alias="entries",
    )
    league_id: Optional[str] = Field(
        default=None,
        alias="leagueId",
    )
    name: Optional[str] = Field(
        default=None,
        alias="name",
    )
    queue: Optional[str] = Field(
        default=None,
        alias="queue",
    )
    tier: str = Field(
        alias="tier",
    )

    model_config = ConfigDict(populate_by_name=True)


class MiniSeries(BaseModel):
    losses: int = Field(
        alias="losses",
    )
    progress: str = Field(
        alias="progress",
    )
    target: int = Field(
        alias="target",
    )
    wins: int = Field(
        alias="wins",
    )

    model_config = ConfigDict(populate_by_name=True)


class TopRatedLadderEntry(BaseModel):
    previous_update_ladder_position: int = Field(
        alias="previousUpdateLadderPosition",
    )
    puuid: str = Field(
        alias="puuid",
        description="Player's encrypted puuid.",
    )
    rated_rating: int = Field(
        alias="ratedRating",
    )
    rated_tier: Literal["ORANGE", "PURPLE", "BLUE", "GREEN", "GRAY"] = Field(
        alias="ratedTier",
        description="".join(("(Legal values:  ORANGE,  PURPLE,  BLUE,  GREEN", ",  GRAY)")),
    )
    wins: int = Field(
        alias="wins",
        description="First placement.",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    LeagueEntry,
    LeagueItem,
    LeagueList,
    MiniSeries,
    TopRatedLadderEntry,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

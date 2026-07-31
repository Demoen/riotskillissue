from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Leaderboard(BaseModel):
    act_id: str = Field(
        alias="actId",
        description="".join(
            (
                "The act id for the given leaderboard. Act ids ",
                "can be found using the val-content API.",
            )
        ),
    )
    immortal_starting_index: Optional[int] = Field(
        default=None,
        alias="immortalStartingIndex",
    )
    immortal_starting_page: Optional[int] = Field(
        default=None,
        alias="immortalStartingPage",
    )
    players: List[Player] = Field(
        alias="players",
    )
    query: Optional[str] = Field(
        default=None,
        alias="query",
    )
    shard: str = Field(
        alias="shard",
        description="The shard for the given leaderboard.",
    )
    start_index: Optional[int] = Field(
        default=None,
        alias="startIndex",
    )
    tier_details: Optional[Dict[str, TierDetail]] = Field(
        default=None,
        alias="tierDetails",
    )
    top_tier_rr_threshold: Optional[int] = Field(
        default=None,
        alias="topTierRRThreshold",
    )
    total_players: int = Field(
        alias="totalPlayers",
        description="".join(("The total number of players in the leaderboard", ".")),
    )

    model_config = ConfigDict(populate_by_name=True)


class Player(BaseModel):
    competitive_tier: Optional[int] = Field(
        default=None,
        alias="competitiveTier",
    )
    game_name: Optional[str] = Field(
        default=None,
        alias="gameName",
        description="".join(("This field may be omitted if the player has be", "en anonymized.")),
    )
    leaderboard_rank: int = Field(
        alias="leaderboardRank",
    )
    number_of_wins: int = Field(
        alias="numberOfWins",
    )
    prefix: Optional[str] = Field(
        default=None,
        alias="prefix",
    )
    premier_roster_type: str = Field(
        alias="premierRosterType",
    )
    puuid: Optional[str] = Field(
        default=None,
        alias="puuid",
        description="".join(("This field may be omitted if the player has be", "en anonymized.")),
    )
    ranked_rating: int = Field(
        alias="rankedRating",
    )
    tag_line: Optional[str] = Field(
        default=None,
        alias="tagLine",
        description="".join(("This field may be omitted if the player has be", "en anonymized.")),
    )

    model_config = ConfigDict(populate_by_name=True)


class TierDetail(BaseModel):
    ranked_rating_threshold: int = Field(
        alias="rankedRatingThreshold",
    )
    starting_index: int = Field(
        alias="startingIndex",
    )
    starting_page: int = Field(
        alias="startingPage",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Leaderboard,
    Player,
    TierDetail,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

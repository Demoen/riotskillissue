from __future__ import annotations

from typing import List, Optional

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
    tier_details: Optional[List[Tier]] = Field(
        default=None,
        alias="tierDetails",
    )
    total_players: int = Field(
        alias="totalPlayers",
        description="".join(("The total number of players in the leaderboard", ".")),
    )

    model_config = ConfigDict(populate_by_name=True)


class Player(BaseModel):
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


class Tier(BaseModel):
    "UNKNOWN TYPE."

    model_config = ConfigDict(populate_by_name=True, extra="allow")


_MODEL_TYPES = (
    Leaderboard,
    Player,
    Tier,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

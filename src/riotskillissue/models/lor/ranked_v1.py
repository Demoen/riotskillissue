from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class Leaderboard(BaseModel):
    players: List[Player] = Field(
        alias="players",
        description="A list of players in Master tier.",
    )

    model_config = ConfigDict(populate_by_name=True)


class Player(BaseModel):
    lp: int = Field(
        alias="lp",
        description="League points.",
    )
    name: str = Field(
        alias="name",
    )
    rank: int = Field(
        alias="rank",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Leaderboard,
    Player,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

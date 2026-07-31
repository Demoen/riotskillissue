from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class ChampionInfo(BaseModel):
    newplayer: List[int] = Field(
        alias="newplayer",
    )
    sr: List[int] = Field(
        alias="sr",
    )

    model_config = ConfigDict(populate_by_name=True)


class Array(BaseModel):
    "UNKNOWN TYPE."

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    ChampionInfo,
    Array,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

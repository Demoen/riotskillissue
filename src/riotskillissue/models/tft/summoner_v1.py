from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Summoner(BaseModel):
    "represents a summoner"

    id: Optional[str] = Field(
        default=None,
        alias="id",
        description="".join(
            (
                "Encrypted summoner ID. This field is deprecate",
                "d and will be removed. Use `puuid` instead.",
            )
        ),
    )
    profile_icon_id: int = Field(
        alias="profileIconId",
        description="".join(("ID of the summoner icon associated with the su", "mmoner.")),
    )
    puuid: str = Field(
        alias="puuid",
        description="".join(("Encrypted PUUID. Exact length of 78 characters", ".")),
    )
    revision_date: int = Field(
        alias="revisionDate",
        description="".join(
            (
                "Date summoner was last modified specified as e",
                "poch milliseconds. The following events will u",
                "pdate this timestamp: profile icon change, pla",
                "ying the tutorial or advanced tutorial, finish",
                "ing a game, summoner name change.",
            )
        ),
    )
    summoner_level: int = Field(
        alias="summonerLevel",
        description="Summoner level associated with the summoner.",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (Summoner,)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

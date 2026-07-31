from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Account(BaseModel):
    game_name: Optional[str] = Field(
        default=None,
        alias="gameName",
        description="".join(
            (
                "This field may be excluded from the response i",
                "f the account doesn't have a gameName.",
            )
        ),
    )
    puuid: str = Field(
        alias="puuid",
        description="".join(("Encrypted PUUID. Exact length of 78 characters", ".")),
    )
    tag_line: Optional[str] = Field(
        default=None,
        alias="tagLine",
        description="".join(
            (
                "This field may be excluded from the response i",
                "f the account doesn't have a tagLine.",
            )
        ),
    )

    model_config = ConfigDict(populate_by_name=True)


class AccountRegion(BaseModel):
    "Account region"

    game: str = Field(
        alias="game",
        description="Game to lookup active region",
    )
    puuid: str = Field(
        alias="puuid",
        description="".join(
            ("Player Universal Unique Identifier. Exact leng", "th of 78 characters. (Encrypted)")
        ),
    )
    region: str = Field(
        alias="region",
        description="Player active region",
    )

    model_config = ConfigDict(populate_by_name=True)


class ActiveShard(BaseModel):
    active_shard: str = Field(
        alias="activeShard",
    )
    game: str = Field(
        alias="game",
    )
    puuid: str = Field(
        alias="puuid",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Account,
    AccountRegion,
    ActiveShard,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

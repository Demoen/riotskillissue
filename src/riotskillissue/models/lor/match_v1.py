from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class Info(BaseModel):
    game_format: Literal["standard", "eternal"] = Field(
        alias="game_format",
        description="(Legal values:  standard,  eternal)",
    )
    game_mode: Literal["Constructed", "Expeditions", "Tutorial"] = Field(
        alias="game_mode",
        description="".join(("(Legal values:  Constructed,  Expeditions,  Tu", "torial)")),
    )
    game_start_time_utc: str = Field(
        alias="game_start_time_utc",
    )
    game_type: Literal[
        "Ranked", "Normal", "AI", "Tutorial", "VanillaTrial", "Singleton", "StandardGauntlet"
    ] = Field(
        alias="game_type",
        description="".join(
            (
                "(Legal values:  Ranked,  Normal,  AI,  Tutoria",
                "l,  VanillaTrial,  Singleton,  StandardGauntle",
                "t)",
            )
        ),
    )
    game_version: str = Field(
        alias="game_version",
    )
    players: List[Player] = Field(
        alias="players",
    )
    total_turn_count: int = Field(
        alias="total_turn_count",
        description="Total turns taken by both players.",
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


class Player(BaseModel):
    deck_code: str = Field(
        alias="deck_code",
        description="".join(
            ("Code for the deck played. Refer to LOR documen", "tation for details on deck codes.")
        ),
    )
    deck_id: str = Field(
        alias="deck_id",
    )
    factions: List[str] = Field(
        alias="factions",
    )
    game_outcome: str = Field(
        alias="game_outcome",
    )
    order_of_play: int = Field(
        alias="order_of_play",
        description="The order in which the players took turns.",
    )
    puuid: str = Field(
        alias="puuid",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Info,
    Match,
    Metadata,
    Player,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

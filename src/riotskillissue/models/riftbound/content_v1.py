from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class CardArt(BaseModel):
    artist: str = Field(
        alias="artist",
    )
    full_url: str = Field(
        alias="fullURL",
    )
    thumbnail_url: str = Field(
        alias="thumbnailURL",
    )

    model_config = ConfigDict(populate_by_name=True)


class Card(BaseModel):
    art: CardArt = Field(
        alias="art",
    )
    collector_number: int = Field(
        alias="collectorNumber",
    )
    description: str = Field(
        alias="description",
    )
    faction: str = Field(
        alias="faction",
    )
    flavor_text: str = Field(
        alias="flavorText",
    )
    id: str = Field(
        alias="id",
        description="Card ID",
    )
    keywords: List[str] = Field(
        alias="keywords",
    )
    name: str = Field(
        alias="name",
        description="Card Name",
    )
    rarity: str = Field(
        alias="rarity",
    )
    set: str = Field(
        alias="set",
    )
    stats: CardStats = Field(
        alias="stats",
    )
    tags: List[str] = Field(
        alias="tags",
    )
    type: str = Field(
        alias="type",
        description="Card Type",
    )

    model_config = ConfigDict(populate_by_name=True)


class CardStats(BaseModel):
    cost: int = Field(
        alias="cost",
    )
    energy: int = Field(
        alias="energy",
    )
    might: int = Field(
        alias="might",
    )
    power: int = Field(
        alias="power",
    )

    model_config = ConfigDict(populate_by_name=True)


class RiftboundContent(BaseModel):
    game: str = Field(
        alias="game",
        description="Game Name",
    )
    last_updated: str = Field(
        alias="lastUpdated",
        description="ISO Timestamp of content last update",
    )
    sets: List[Set] = Field(
        alias="sets",
    )
    version: str = Field(
        alias="version",
        description="Content version",
    )

    model_config = ConfigDict(populate_by_name=True)


class Set(BaseModel):
    cards: List[Card] = Field(
        alias="cards",
    )
    id: str = Field(
        alias="id",
        description="Set ID",
    )
    name: str = Field(
        alias="name",
        description="Set Name",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    CardArt,
    Card,
    CardStats,
    RiftboundContent,
    Set,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

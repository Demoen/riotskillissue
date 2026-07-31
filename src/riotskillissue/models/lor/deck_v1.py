from __future__ import annotations


from pydantic import BaseModel, ConfigDict, Field


class Deck(BaseModel):
    code: str = Field(
        alias="code",
    )
    id: str = Field(
        alias="id",
    )
    name: str = Field(
        alias="name",
    )

    model_config = ConfigDict(populate_by_name=True)


class NewDeck(BaseModel):
    code: str = Field(
        alias="code",
    )
    name: str = Field(
        alias="name",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Deck,
    NewDeck,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

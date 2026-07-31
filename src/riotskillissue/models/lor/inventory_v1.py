from __future__ import annotations


from pydantic import BaseModel, ConfigDict, Field


class Card(BaseModel):
    code: str = Field(
        alias="code",
    )
    count: str = Field(
        alias="count",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (Card,)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

from __future__ import annotations


from pydantic import BaseModel, ConfigDict


class Match(BaseModel):
    "UNKNOWN TYPE."

    model_config = ConfigDict(populate_by_name=True)


class Timeline(BaseModel):
    "UNKNOWN TYPE."

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Match,
    Timeline,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

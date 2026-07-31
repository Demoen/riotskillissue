from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class Error(BaseModel):
    status: Optional[Dict[str, Any]] = Field(
        default=None,
        alias="status",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (Error,)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

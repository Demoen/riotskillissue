from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class Content(BaseModel):
    content: str = Field(
        alias="content",
    )
    locale: str = Field(
        alias="locale",
    )

    model_config = ConfigDict(populate_by_name=True)


class PlatformData(BaseModel):
    id: str = Field(
        alias="id",
    )
    incidents: List[Status] = Field(
        alias="incidents",
    )
    locales: List[str] = Field(
        alias="locales",
    )
    maintenances: List[Status] = Field(
        alias="maintenances",
    )
    name: str = Field(
        alias="name",
    )

    model_config = ConfigDict(populate_by_name=True)


class Status(BaseModel):
    archive_at: Optional[str] = Field(
        default=None,
        alias="archive_at",
    )
    created_at: str = Field(
        alias="created_at",
    )
    id: int = Field(
        alias="id",
    )
    incident_severity: Optional[Literal["info", "warning", "critical"]] = Field(
        default=None,
        alias="incident_severity",
        description="(Legal values:  info,  warning,  critical)",
    )
    maintenance_status: Optional[Literal["scheduled", "in_progress", "complete"]] = Field(
        default=None,
        alias="maintenance_status",
        description="".join(("(Legal values:  scheduled,  in_progress,  comp", "lete)")),
    )
    platforms: List[Literal["windows", "macos", "android", "ios", "ps4", "xbone", "switch"]] = (
        Field(
            alias="platforms",
            description="".join(
                ("(Legal values: windows, macos, android, ios, p", "s4, xbone, switch)")
            ),
        )
    )
    titles: List[Content] = Field(
        alias="titles",
    )
    updated_at: Optional[str] = Field(
        default=None,
        alias="updated_at",
    )
    updates: List[Update] = Field(
        alias="updates",
    )

    model_config = ConfigDict(populate_by_name=True)


class Update(BaseModel):
    author: str = Field(
        alias="author",
    )
    created_at: str = Field(
        alias="created_at",
    )
    id: int = Field(
        alias="id",
    )
    publish: bool = Field(
        alias="publish",
    )
    publish_locations: List[Literal["riotclient", "riotstatus", "game"]] = Field(
        alias="publish_locations",
        description="(Legal values: riotclient, riotstatus, game)",
    )
    translations: List[Content] = Field(
        alias="translations",
    )
    updated_at: str = Field(
        alias="updated_at",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Content,
    PlatformData,
    Status,
    Update,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

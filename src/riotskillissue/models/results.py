from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from riotskillissue.core.types import Game


class WorkflowModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class PlayerProfile(WorkflowModel):
    game: Game
    riot_id: str
    puuid: str
    account: Any
    game_profile: Any | None = None


class MatchSummary(WorkflowModel):
    game: Game
    match_id: str
    started_at: datetime | None = None
    duration_seconds: float | None = Field(default=None, ge=0)
    queue_id: str | int | None = None
    won: bool | None = None
    player: dict[str, Any] = Field(default_factory=dict)


__all__ = ["MatchSummary", "PlayerProfile", "WorkflowModel"]

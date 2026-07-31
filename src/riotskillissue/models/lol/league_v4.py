from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LeagueEntry(BaseModel):
    fresh_blood: bool = Field(
        alias="freshBlood",
    )
    hot_streak: bool = Field(
        alias="hotStreak",
    )
    inactive: bool = Field(
        alias="inactive",
    )
    league_id: Optional[str] = Field(
        default=None,
        alias="leagueId",
    )
    league_points: int = Field(
        alias="leaguePoints",
    )
    losses: int = Field(
        alias="losses",
        description="Losing team on Summoners Rift.",
    )
    mini_series: Optional[MiniSeries] = Field(
        default=None,
        alias="miniSeries",
    )
    puuid: str = Field(
        alias="puuid",
        description="Player's encrypted puuid.",
    )
    queue_type: str = Field(
        alias="queueType",
    )
    rank: Optional[str] = Field(
        default=None,
        alias="rank",
        description="The player's division within a tier.",
    )
    summoner_id: Optional[str] = Field(
        default=None,
        alias="summonerId",
        description="".join(
            (
                "Encrypted summoner ID. This field is deprecate",
                "d and will be removed. Use `puuid` instead.",
            )
        ),
    )
    tier: Optional[str] = Field(
        default=None,
        alias="tier",
    )
    veteran: bool = Field(
        alias="veteran",
    )
    wins: int = Field(
        alias="wins",
        description="Winning team on Summoners Rift.",
    )

    model_config = ConfigDict(populate_by_name=True)


class LeagueItem(BaseModel):
    fresh_blood: bool = Field(
        alias="freshBlood",
    )
    hot_streak: bool = Field(
        alias="hotStreak",
    )
    inactive: bool = Field(
        alias="inactive",
    )
    league_points: int = Field(
        alias="leaguePoints",
    )
    losses: int = Field(
        alias="losses",
        description="Losing team on Summoners Rift.",
    )
    mini_series: Optional[MiniSeries] = Field(
        default=None,
        alias="miniSeries",
    )
    puuid: str = Field(
        alias="puuid",
        description="Player's encrypted puuid.",
    )
    rank: str = Field(
        alias="rank",
    )
    summoner_id: Optional[str] = Field(
        default=None,
        alias="summonerId",
        description="".join(
            (
                "Encrypted summoner ID. This field is deprecate",
                "d and will be removed. Use `puuid` instead.",
            )
        ),
    )
    veteran: bool = Field(
        alias="veteran",
    )
    wins: int = Field(
        alias="wins",
        description="Winning team on Summoners Rift.",
    )

    model_config = ConfigDict(populate_by_name=True)


class LeagueList(BaseModel):
    entries: List[LeagueItem] = Field(
        alias="entries",
    )
    league_id: Optional[str] = Field(
        default=None,
        alias="leagueId",
    )
    name: Optional[str] = Field(
        default=None,
        alias="name",
    )
    queue: Optional[str] = Field(
        default=None,
        alias="queue",
    )
    tier: str = Field(
        alias="tier",
    )

    model_config = ConfigDict(populate_by_name=True)


class MiniSeries(BaseModel):
    losses: int = Field(
        alias="losses",
    )
    progress: str = Field(
        alias="progress",
    )
    target: int = Field(
        alias="target",
    )
    wins: int = Field(
        alias="wins",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    LeagueEntry,
    LeagueItem,
    LeagueList,
    MiniSeries,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

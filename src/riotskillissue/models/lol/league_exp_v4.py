from __future__ import annotations

from typing import Optional

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
        description="".join(
            (
                "Losing team on Summoners Rift. Second through ",
                "eighth placement in Teamfight Tactics.",
            )
        ),
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
    rank: str = Field(
        alias="rank",
        description="The player's division within a tier.",
    )
    summoner_id: Optional[str] = Field(
        default=None,
        alias="summonerId",
        description="Player's summonerId (Encrypted)",
    )
    tier: str = Field(
        alias="tier",
    )
    veteran: bool = Field(
        alias="veteran",
    )
    wins: int = Field(
        alias="wins",
        description="".join(
            ("Winning team on Summoners Rift. First placemen", "t in Teamfight Tactics.")
        ),
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
    MiniSeries,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

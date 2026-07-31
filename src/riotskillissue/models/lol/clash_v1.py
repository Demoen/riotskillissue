from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class Player(BaseModel):
    position: Literal["UNSELECTED", "FILL", "TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"] = Field(
        alias="position",
        description="".join(
            ("(Legal values:  UNSELECTED,  FILL,  TOP,  JUNG", "LE,  MIDDLE,  BOTTOM,  UTILITY)")
        ),
    )
    puuid: str = Field(
        alias="puuid",
    )
    role: Literal["CAPTAIN", "MEMBER"] = Field(
        alias="role",
        description="(Legal values:  CAPTAIN,  MEMBER)",
    )
    team_id: Optional[str] = Field(
        default=None,
        alias="teamId",
    )

    model_config = ConfigDict(populate_by_name=True)


class Team(BaseModel):
    abbreviation: str = Field(
        alias="abbreviation",
    )
    captain: str = Field(
        alias="captain",
        description="Summoner ID of the team captain.",
    )
    icon_id: int = Field(
        alias="iconId",
    )
    id: str = Field(
        alias="id",
    )
    name: str = Field(
        alias="name",
    )
    players: List[Player] = Field(
        alias="players",
        description="Team members.",
    )
    tier: int = Field(
        alias="tier",
    )
    tournament_id: int = Field(
        alias="tournamentId",
    )

    model_config = ConfigDict(populate_by_name=True)


class Tournament(BaseModel):
    id: int = Field(
        alias="id",
    )
    name_key: str = Field(
        alias="nameKey",
    )
    name_key_secondary: str = Field(
        alias="nameKeySecondary",
    )
    schedule: List[TournamentPhase] = Field(
        alias="schedule",
        description="Tournament phase.",
    )
    theme_id: int = Field(
        alias="themeId",
    )

    model_config = ConfigDict(populate_by_name=True)


class TournamentPhase(BaseModel):
    cancelled: bool = Field(
        alias="cancelled",
    )
    id: int = Field(
        alias="id",
    )
    registration_time: int = Field(
        alias="registrationTime",
    )
    start_time: int = Field(
        alias="startTime",
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    Player,
    Team,
    Tournament,
    TournamentPhase,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

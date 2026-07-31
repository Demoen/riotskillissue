from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class LobbyEventV5(BaseModel):
    event_type: str = Field(
        alias="eventType",
        description="The type of event that was triggered",
    )
    puuid: str = Field(
        alias="puuid",
        description="The puuid that triggered the event (Encrypted)",
    )
    timestamp: str = Field(
        alias="timestamp",
        description="Timestamp from the event",
    )

    model_config = ConfigDict(populate_by_name=True)


class LobbyEventV5Wrapper(BaseModel):
    event_list: List[LobbyEventV5] = Field(
        alias="eventList",
    )

    model_config = ConfigDict(populate_by_name=True)


class ProviderRegistrationParametersV5(BaseModel):
    region: Literal[
        "BR", "EUNE", "EUW", "JP", "LAN", "LAS", "NA", "OCE", "PBE", "RU", "TR", "KR"
    ] = Field(
        alias="region",
        description="".join(
            (
                "The region in which the provider will be runni",
                "ng tournaments.\n             (Legal values:  B",
                "R,  EUNE,  EUW,  JP,  LAN,  LAS,  NA,  OCE,  P",
                "BE,  RU,  TR,  KR)",
            )
        ),
    )
    url: str = Field(
        alias="url",
        description="".join(
            (
                "The provider's callback URL to which tournamen",
                "t game results in this region should be posted",
                ". The URL must be well-formed, use the http or",
                " https protocol, and use the default port for ",
                "the protocol (http URLs must use port 80, http",
                "s URLs must use port 443).",
            )
        ),
    )

    model_config = ConfigDict(populate_by_name=True)


class TournamentCodeParametersV5(BaseModel):
    allowed_participants: Optional[List[str]] = Field(
        default=None,
        alias="allowedParticipants",
        description="".join(
            (
                "Optional list of encrypted puuids in order to ",
                "validate the players eligible to join the lobb",
                "y. NOTE: We currently do not enforce participa",
                "nts at the team level, but rather the aggregat",
                "e of teamOne and teamTwo. We may add the abili",
                "ty to enforce at the team level in the future.",
            )
        ),
    )
    enough_players: bool = Field(
        alias="enoughPlayers",
        description="".join(("Checks if allowed participants are enough to m", "ake full teams.")),
    )
    map_type: Literal["SUMMONERS_RIFT", "HOWLING_ABYSS", "LEAGUE_CLASSIC"] = Field(
        alias="mapType",
        description="".join(
            (
                "The map type of the game.\n             (Legal ",
                "values:  SUMMONERS_RIFT,  HOWLING_ABYSS,  LEAG",
                "UE_CLASSIC)",
            )
        ),
    )
    metadata: Optional[str] = Field(
        default=None,
        alias="metadata",
        description="".join(
            (
                "Optional string that may contain any data in a",
                "ny format, if specified at all. Used to denote",
                " any custom information about the game.",
            )
        ),
    )
    pick_type: Literal["BLIND_PICK", "DRAFT_MODE", "ALL_RANDOM", "TOURNAMENT_DRAFT"] = Field(
        alias="pickType",
        description="".join(
            (
                "The pick type of the game.\n             (Legal",
                " values:  BLIND_PICK,  DRAFT_MODE,  ALL_RANDOM",
                ",  TOURNAMENT_DRAFT)",
            )
        ),
    )
    spectator_type: Literal["NONE", "LOBBYONLY", "ALL"] = Field(
        alias="spectatorType",
        description="".join(
            (
                "The spectator type of the game.\n             (",
                "Legal values:  NONE,  LOBBYONLY,  ALL)",
            )
        ),
    )
    team_size: int = Field(
        alias="teamSize",
        description="".join(("The team size of the game. Valid values are 1-", "5.")),
        ge=1,
        le=5,
    )

    model_config = ConfigDict(populate_by_name=True)


class TournamentCodeV5(BaseModel):
    code: str = Field(
        alias="code",
        description="The tournament code.",
    )
    id: int = Field(
        alias="id",
        description="The tournament code's ID.",
    )
    lobby_name: str = Field(
        alias="lobbyName",
        description="The lobby name for the tournament code game.",
    )
    map: str = Field(
        alias="map",
        description="The game map for the tournament code game",
    )
    meta_data: str = Field(
        alias="metaData",
        description="The metadata for tournament code.",
    )
    participants: List[str] = Field(
        alias="participants",
        description="The puuids of the participants (Encrypted)",
    )
    password: str = Field(
        alias="password",
        description="The password for the tournament code game.",
    )
    pick_type: str = Field(
        alias="pickType",
        description="The pick mode for tournament code game.",
    )
    provider_id: int = Field(
        alias="providerId",
        description="The provider's ID.",
    )
    region: Literal[
        "BR", "EUNE", "EUW", "JP", "LAN", "LAS", "NA", "OCE", "PBE", "RU", "TR", "KR"
    ] = Field(
        alias="region",
        description="".join(
            (
                "The tournament code's region.\n             (Le",
                "gal values:  BR,  EUNE,  EUW,  JP,  LAN,  LAS,",
                "  NA,  OCE,  PBE,  RU,  TR,  KR)",
            )
        ),
    )
    team_size: int = Field(
        alias="teamSize",
        description="The team size for the tournament code game.",
    )
    tournament_id: int = Field(
        alias="tournamentId",
        description="The tournament's ID.",
    )

    model_config = ConfigDict(populate_by_name=True)


class TournamentRegistrationParametersV5(BaseModel):
    name: Optional[str] = Field(
        default=None,
        alias="name",
        description="The optional name of the tournament.",
    )
    provider_id: int = Field(
        alias="providerId",
        description="".join(
            (
                "The provider ID to specify the regional regist",
                "ered provider data to associate this tournamen",
                "t.",
            )
        ),
    )

    model_config = ConfigDict(populate_by_name=True)


_MODEL_TYPES = (
    LobbyEventV5,
    LobbyEventV5Wrapper,
    ProviderRegistrationParametersV5,
    TournamentCodeParametersV5,
    TournamentCodeV5,
    TournamentRegistrationParametersV5,
)
for _model_type in _MODEL_TYPES:
    _model_type.model_rebuild(_types_namespace=globals())
del _model_type

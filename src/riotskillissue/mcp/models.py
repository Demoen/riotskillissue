"""Schemas exposed by the RiotSkillIssue MCP tools."""

from __future__ import annotations

from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, JsonValue


class ToolModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RoutedRequest(ToolModel):
    route: str | None = Field(default=None, description="Optional Riot routing value.")


class LolPlayerRequest(RoutedRequest):
    game: Literal["lol"] = "lol"
    riot_id: str = Field(
        min_length=3,
        pattern=r"^[^#]+#[^#]+$",
        description="Riot ID in GameName#TagLine form.",
    )


class TftPlayerRequest(RoutedRequest):
    game: Literal["tft"] = "tft"
    riot_id: str = Field(
        min_length=3,
        pattern=r"^[^#]+#[^#]+$",
        description="Riot ID in GameName#TagLine form.",
    )


class ValorantPlayerRequest(RoutedRequest):
    game: Literal["valorant"] = "valorant"
    riot_id: str = Field(
        min_length=3,
        pattern=r"^[^#]+#[^#]+$",
        description="Riot ID in GameName#TagLine form.",
    )


class LorPlayerRequest(RoutedRequest):
    game: Literal["lor"] = "lor"
    riot_id: str = Field(
        min_length=3,
        pattern=r"^[^#]+#[^#]+$",
        description="Riot ID in GameName#TagLine form.",
    )


PlayerProfileRequest = Annotated[
    Union[LolPlayerRequest, TftPlayerRequest, ValorantPlayerRequest, LorPlayerRequest],
    Field(discriminator="game"),
]


class LolMatchHistoryRequest(LolPlayerRequest):
    count: int = Field(default=5, ge=1, le=20)


class TftMatchHistoryRequest(TftPlayerRequest):
    count: int = Field(default=5, ge=1, le=20)


class ValorantMatchHistoryRequest(ValorantPlayerRequest):
    count: int = Field(default=5, ge=1, le=20)


class LorMatchHistoryRequest(LorPlayerRequest):
    count: int = Field(default=5, ge=1, le=20)


MatchHistoryRequest = Annotated[
    Union[
        LolMatchHistoryRequest,
        TftMatchHistoryRequest,
        ValorantMatchHistoryRequest,
        LorMatchHistoryRequest,
    ],
    Field(discriminator="game"),
]


RankedEntriesRequest = Annotated[
    Union[LolPlayerRequest, TftPlayerRequest],
    Field(discriminator="game"),
]


class ValorantLeaderboardRequest(RoutedRequest):
    game: Literal["valorant"] = "valorant"
    act_id: str = Field(min_length=1)
    size: int = Field(default=20, ge=1, le=200)
    start_index: int = Field(default=0, ge=0)


class LorLeaderboardRequest(RoutedRequest):
    game: Literal["lor"] = "lor"


LeaderboardRequest = Annotated[
    Union[ValorantLeaderboardRequest, LorLeaderboardRequest],
    Field(discriminator="game"),
]


LiveGameRequest = Annotated[
    Union[LolPlayerRequest, TftPlayerRequest],
    Field(discriminator="game"),
]


class ChampionMasteryRequest(LolPlayerRequest):
    champion_id: int | None = Field(default=None, ge=1)
    count: int | None = Field(default=None, ge=1)


class ChallengesRequest(LolPlayerRequest):
    challenge_id: int | None = Field(default=None, ge=1)


class LolStatusRequest(RoutedRequest):
    game: Literal["lol"] = "lol"


class TftStatusRequest(RoutedRequest):
    game: Literal["tft"] = "tft"


class ValorantStatusRequest(RoutedRequest):
    game: Literal["valorant"] = "valorant"


class LorStatusRequest(RoutedRequest):
    game: Literal["lor"] = "lor"


ServiceStatusRequest = Annotated[
    Union[LolStatusRequest, TftStatusRequest, ValorantStatusRequest, LorStatusRequest],
    Field(discriminator="game"),
]


class LolContentRequest(ToolModel):
    game: Literal["lol"] = "lol"
    kind: Literal[
        "version",
        "champion",
        "champions",
        "item",
        "items",
        "runes",
        "summoner_spell",
        "summoner_spells",
        "queues",
        "maps",
        "game_modes",
    ]
    identifier: int | None = Field(default=None, ge=1)


class ValorantContentRequest(RoutedRequest):
    game: Literal["valorant"] = "valorant"
    locale: str | None = None


class RiftboundContentRequest(RoutedRequest):
    game: Literal["riftbound"] = "riftbound"
    locale: str | None = None


GameContentRequest = Annotated[
    Union[LolContentRequest, ValorantContentRequest, RiftboundContentRequest],
    Field(discriminator="game"),
]


class ToolResult(ToolModel):
    inline: bool
    size_bytes: int = Field(ge=0)
    data: JsonValue | None = None
    handle: str | None = None
    outline: dict[str, JsonValue] | None = None
    expires_in_seconds: int | None = None


class ResultPage(ToolModel):
    handle: str
    pointer: str
    size_bytes: int = Field(ge=0)
    data: JsonValue
    offset: int = Field(ge=0)
    limit: int = Field(ge=1)
    total: int | None = Field(default=None, ge=0)
    next_offset: int | None = Field(default=None, ge=0)


class OperationSummary(ToolModel):
    operation: str
    accessor_path: str
    game: str
    service: str
    method: str
    read_only: bool
    description: str | None = None


class FindOperationsResult(ToolModel):
    operations: list[OperationSummary]
    total: int = Field(ge=0)


class OperationDescription(OperationSummary):
    route_type: str | None = None
    allowed_routes: list[str] = Field(default_factory=list)
    auth_mode: str
    input_schema: dict[str, Any] = Field(default_factory=dict)


class WriteConfirmation(ToolModel):
    approved: bool = Field(description="Approve this Riot API write operation.")

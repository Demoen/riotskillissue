"""Schemas exposed by the RiotSkillIssue MCP tools."""

from __future__ import annotations

from typing import Annotated, Any, Literal, Self, Union

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator


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
        "champion_detail",
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
    patch: str | None = Field(
        default=None,
        min_length=3,
        max_length=32,
        pattern=r"^[0-9]+(?:\.[0-9]+){1,3}$",
        description="Public seasonal or Match/Data Dragon patch version.",
    )
    locale: str | None = Field(default=None, pattern=r"^[a-z]{2}_[A-Z]{2}$")


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


LolAnalysisDetail = Literal["summary", "standard", "full"]
LolKnowledgeTopic = Literal[
    "core",
    "economy",
    "minions",
    "experience",
    "item_efficiency",
    "structures",
    "wave_management",
    "objectives",
    "void_grubs",
    "roles",
    "stats",
    "items",
    "vision",
    "tempo",
    "teamfights",
    "player_data",
    "limitations",
]
LolPlatformRoute = Literal[
    "br1",
    "eun1",
    "euw1",
    "jp1",
    "kr",
    "la1",
    "la2",
    "me1",
    "na1",
    "oc1",
    "pbe1",
    "ph2",
    "ru",
    "sg2",
    "th2",
    "tr1",
    "tw2",
    "vn2",
]
LolRegionalRoute = Literal["americas", "asia", "europe", "sea"]
LolRoute = LolPlatformRoute | LolRegionalRoute


class LolAnalysisRequest(ToolModel):
    route: LolRoute | None = Field(
        default=None,
        description="Optional League platform or regional route.",
    )
    question: str | None = Field(default=None, min_length=1, max_length=2000)
    detail: LolAnalysisDetail = "standard"


class LolMatchContextRequest(LolAnalysisRequest):
    focus: str | None = Field(default=None, min_length=1, max_length=120)
    match_id: str | None = Field(
        default=None,
        min_length=3,
        max_length=64,
        pattern=r"^[A-Za-z0-9]+_[A-Za-z0-9-]+$",
    )
    riot_id: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
        pattern=r"^[^#]+#[^#]+$",
        description="Riot ID in GameName#TagLine form.",
    )
    match_index: int = Field(default=0, ge=0, le=99)
    include_timeline: bool = True

    @model_validator(mode="after")
    def validate_selector(self) -> Self:
        if (self.match_id is None) == (self.riot_id is None):
            raise ValueError("Provide exactly one of match_id or riot_id.")
        if self.match_id is not None and self.match_index != 0:
            raise ValueError("match_index can only be used with riot_id.")
        return self


class LolPlayerContextRequest(LolAnalysisRequest):
    route: LolPlatformRoute | None = Field(
        default=None,
        description="Optional League platform route.",
    )
    riot_id: str = Field(
        min_length=3,
        max_length=100,
        pattern=r"^[^#]+#[^#]+$",
        description="Riot ID in GameName#TagLine form.",
    )
    count: int = Field(default=5, ge=1, le=10)


class LolKnowledgeRequest(ToolModel):
    topic: LolKnowledgeTopic = "core"
    patch: str | None = Field(
        default=None,
        min_length=3,
        max_length=32,
        pattern=r"^[0-9]+(?:\.[0-9]+){1,3}$",
    )
    question: str | None = Field(default=None, min_length=1, max_length=2000)
    detail: LolAnalysisDetail = "standard"


class LolItemEconomyRequest(ToolModel):
    item_id: int | None = Field(default=None, ge=1)
    item_name: str | None = Field(default=None, min_length=1, max_length=120)
    patch: str | None = Field(
        default=None,
        min_length=3,
        max_length=32,
        pattern=r"^[0-9]+(?:\.[0-9]+){1,3}$",
        description="Public seasonal or Match/Data Dragon patch version.",
    )
    match_id: str | None = Field(
        default=None,
        min_length=3,
        max_length=64,
        pattern=r"^[A-Za-z0-9]+_[A-Za-z0-9-]+$",
    )
    route: LolRoute | None = Field(
        default=None,
        description="Optional League platform or regional route for match lookup.",
    )
    map_id: int | None = Field(default=11, ge=1)
    locale: str = Field(default="en_US", pattern=r"^[a-z]{2}_[A-Z]{2}$")

    @model_validator(mode="after")
    def validate_selectors(self) -> Self:
        if (self.item_id is None) == (self.item_name is None):
            raise ValueError("Provide exactly one of item_id or item_name.")
        if self.patch is not None and self.match_id is not None:
            raise ValueError("Provide at most one of patch or match_id.")
        if self.route is not None and self.match_id is None:
            raise ValueError("route can only be used with match_id.")
        return self


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

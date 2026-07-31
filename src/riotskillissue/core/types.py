from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, NewType, Optional, Type, TypeVar, Union

try:
    from enum import StrEnum
except ImportError:

    class StrEnum(str, Enum):
        pass


class Game(StrEnum):
    LOL = "lol"
    TFT = "tft"
    VALORANT = "valorant"
    LOR = "lor"
    RIFTBOUND = "riftbound"


class PlatformRoute(StrEnum):
    BR1 = "br1"
    EUN1 = "eun1"
    EUW1 = "euw1"
    JP1 = "jp1"
    KR = "kr"
    LA1 = "la1"
    LA2 = "la2"
    ME1 = "me1"
    NA1 = "na1"
    OC1 = "oc1"
    PBE1 = "pbe1"
    PH2 = "ph2"
    RU = "ru"
    SG2 = "sg2"
    TH2 = "th2"
    TR1 = "tr1"
    TW2 = "tw2"
    VN2 = "vn2"


class RegionalRoute(StrEnum):
    AMERICAS = "americas"
    APAC = "apac"
    ASIA = "asia"
    ESPORTS = "esports"
    ESPORTS_EU = "esportseu"
    EUROPE = "europe"
    SEA = "sea"


class ValorantRoute(StrEnum):
    AP = "ap"
    BR = "br"
    ESPORTS = "esports"
    EU = "eu"
    KR = "kr"
    LATAM = "latam"
    NA = "na"


class RouteKind(StrEnum):
    PLATFORM = "platform"
    REGIONAL = "regional"
    VALORANT = "valorant"
    VAL_PLATFORM = "val-platform"


Route = Union[PlatformRoute, RegionalRoute, ValorantRoute]


class RouteResolutionError(ValueError):
    def __init__(
        self,
        route_kind: Union[RouteKind, str],
        *,
        explicit: Optional[object] = None,
        default: Optional[object] = None,
        reason: Optional[str] = None,
    ) -> None:
        kind = route_kind.value if isinstance(route_kind, RouteKind) else str(route_kind)
        detail = reason or f"no {kind} route can be resolved"
        if reason is None and explicit is not None:
            detail = f"invalid explicit {kind} route: {explicit!s}"
        elif reason is None and default is not None:
            detail = f"default route {default!s} cannot resolve a {kind} route"
        super().__init__(detail)
        self.route_kind = kind
        self.explicit = explicit
        self.default = default


PLATFORM_TO_REGIONAL: Dict[PlatformRoute, RegionalRoute] = {
    PlatformRoute.BR1: RegionalRoute.AMERICAS,
    PlatformRoute.EUN1: RegionalRoute.EUROPE,
    PlatformRoute.EUW1: RegionalRoute.EUROPE,
    PlatformRoute.JP1: RegionalRoute.ASIA,
    PlatformRoute.KR: RegionalRoute.ASIA,
    PlatformRoute.LA1: RegionalRoute.AMERICAS,
    PlatformRoute.LA2: RegionalRoute.AMERICAS,
    PlatformRoute.ME1: RegionalRoute.EUROPE,
    PlatformRoute.NA1: RegionalRoute.AMERICAS,
    PlatformRoute.OC1: RegionalRoute.SEA,
    PlatformRoute.PBE1: RegionalRoute.AMERICAS,
    PlatformRoute.PH2: RegionalRoute.SEA,
    PlatformRoute.RU: RegionalRoute.EUROPE,
    PlatformRoute.SG2: RegionalRoute.SEA,
    PlatformRoute.TH2: RegionalRoute.SEA,
    PlatformRoute.TR1: RegionalRoute.EUROPE,
    PlatformRoute.TW2: RegionalRoute.SEA,
    PlatformRoute.VN2: RegionalRoute.SEA,
}

PLATFORM_TO_VALORANT: Dict[PlatformRoute, ValorantRoute] = {
    PlatformRoute.BR1: ValorantRoute.BR,
    PlatformRoute.EUN1: ValorantRoute.EU,
    PlatformRoute.EUW1: ValorantRoute.EU,
    PlatformRoute.JP1: ValorantRoute.AP,
    PlatformRoute.KR: ValorantRoute.KR,
    PlatformRoute.LA1: ValorantRoute.LATAM,
    PlatformRoute.LA2: ValorantRoute.LATAM,
    PlatformRoute.ME1: ValorantRoute.EU,
    PlatformRoute.NA1: ValorantRoute.NA,
    PlatformRoute.OC1: ValorantRoute.AP,
    PlatformRoute.PBE1: ValorantRoute.NA,
    PlatformRoute.PH2: ValorantRoute.AP,
    PlatformRoute.RU: ValorantRoute.EU,
    PlatformRoute.SG2: ValorantRoute.AP,
    PlatformRoute.TH2: ValorantRoute.AP,
    PlatformRoute.TR1: ValorantRoute.EU,
    PlatformRoute.TW2: ValorantRoute.AP,
    PlatformRoute.VN2: ValorantRoute.AP,
}

VALORANT_TO_REGIONAL: Dict[ValorantRoute, RegionalRoute] = {
    ValorantRoute.AP: RegionalRoute.APAC,
    ValorantRoute.BR: RegionalRoute.AMERICAS,
    ValorantRoute.ESPORTS: RegionalRoute.ESPORTS,
    ValorantRoute.EU: RegionalRoute.EUROPE,
    ValorantRoute.KR: RegionalRoute.ASIA,
    ValorantRoute.LATAM: RegionalRoute.AMERICAS,
    ValorantRoute.NA: RegionalRoute.AMERICAS,
}

REGIONAL_TO_VALORANT: Dict[RegionalRoute, ValorantRoute] = {
    RegionalRoute.APAC: ValorantRoute.AP,
    RegionalRoute.ESPORTS: ValorantRoute.ESPORTS,
    RegionalRoute.ESPORTS_EU: ValorantRoute.ESPORTS,
    RegionalRoute.EUROPE: ValorantRoute.EU,
    RegionalRoute.SEA: ValorantRoute.AP,
}

_RouteEnum = TypeVar("_RouteEnum", bound=StrEnum)


def _coerce_route(route: object, enum_type: Type[_RouteEnum]) -> _RouteEnum:
    if isinstance(route, enum_type):
        return route
    value = route.value if isinstance(route, Enum) else route
    if not isinstance(value, str):
        raise ValueError
    return enum_type(value.lower())


def coerce_route_kind(route_kind: Union[RouteKind, str]) -> RouteKind:
    if isinstance(route_kind, RouteKind):
        return route_kind
    value = str(route_kind).lower().replace("_", "-")
    if value in {"val", "valorant", "valorant-platform"}:
        return RouteKind.VALORANT
    return RouteKind(value)


def resolve_route(
    route_kind: Union[RouteKind, str],
    *,
    explicit: Optional[object] = None,
    default: Optional[Route] = None,
) -> Route:
    try:
        kind = coerce_route_kind(route_kind)
    except ValueError as exc:
        raise RouteResolutionError(
            route_kind, explicit=explicit, default=default, reason="unknown route kind"
        ) from exc

    if kind is RouteKind.PLATFORM:
        if explicit is not None:
            try:
                return _coerce_route(explicit, PlatformRoute)
            except ValueError as exc:
                raise RouteResolutionError(kind, explicit=explicit) from exc
        if isinstance(default, PlatformRoute):
            return default
        raise RouteResolutionError(kind, default=default)

    if kind is RouteKind.REGIONAL:
        if explicit is not None:
            try:
                return _coerce_route(explicit, RegionalRoute)
            except ValueError as exc:
                raise RouteResolutionError(kind, explicit=explicit) from exc
        if isinstance(default, RegionalRoute):
            return default
        if isinstance(default, PlatformRoute):
            return PLATFORM_TO_REGIONAL[default]
        if isinstance(default, ValorantRoute):
            return VALORANT_TO_REGIONAL[default]
        raise RouteResolutionError(kind, default=default)

    if explicit is not None:
        try:
            return _coerce_route(explicit, ValorantRoute)
        except ValueError as exc:
            raise RouteResolutionError(kind, explicit=explicit) from exc
    if isinstance(default, ValorantRoute):
        return default
    if isinstance(default, PlatformRoute):
        return PLATFORM_TO_VALORANT[default]
    if isinstance(default, RegionalRoute) and default in REGIONAL_TO_VALORANT:
        return REGIONAL_TO_VALORANT[default]
    raise RouteResolutionError(kind, default=default)


@dataclass(frozen=True)
class RiotId:
    game_name: str
    tag_line: str

    def __post_init__(self) -> None:
        game_name = self.game_name.strip()
        tag_line = self.tag_line.strip()
        if not game_name or not tag_line or "#" in game_name or "#" in tag_line:
            raise ValueError("Riot ID requires a game name and tag line")
        object.__setattr__(self, "game_name", game_name)
        object.__setattr__(self, "tag_line", tag_line)

    @classmethod
    def parse(cls, value: str) -> "RiotId":
        if not isinstance(value, str) or "#" not in value:
            raise ValueError("Riot ID must use the form game_name#tag_line")
        game_name, tag_line = value.rsplit("#", 1)
        return cls(game_name=game_name, tag_line=tag_line)

    def __str__(self) -> str:
        return f"{self.game_name}#{self.tag_line}"


Puuid = NewType("Puuid", str)
SummonerId = NewType("SummonerId", str)
AccountId = NewType("AccountId", str)

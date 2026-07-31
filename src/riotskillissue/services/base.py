from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any, Protocol

from riotskillissue.core.types import (
    Game,
    PlatformRoute,
    RegionalRoute,
    RiotId,
    RouteKind,
    RouteResolutionError,
    ValorantRoute,
    resolve_route,
)
from riotskillissue.services.models import MatchSummary, PlayerProfile


class RawOperations(Protocol):
    async def call_operation(
        self,
        operation: str,
        arguments: Mapping[str, Any],
    ) -> Any: ...


class WorkflowService:
    def __init__(self, raw: RawOperations) -> None:
        self._raw = raw

    async def _call(self, operation: str, **arguments: Any) -> Any:
        return await self._raw.call_operation(
            operation,
            {key: value for key, value in arguments.items() if value is not None},
        )

    async def _account(
        self,
        riot_id: RiotId,
        *,
        route: RegionalRoute | None,
    ) -> Any:
        return await self._call(
            "account-v1.getByRiotId",
            game_name=riot_id.game_name,
            tag_line=riot_id.tag_line,
            route=route,
        )

    async def _profile(
        self,
        game: Game,
        riot_id: str,
        *,
        account_route: RegionalRoute | None,
        profile_operation: str | None,
        profile_arguments: Mapping[str, Any] | None = None,
        profile_identity_argument: str = "puuid",
    ) -> PlayerProfile:
        parsed = RiotId.parse(riot_id)
        account = await self._account(parsed, route=account_route)
        puuid = str(_field(account, "puuid"))
        game_profile = None
        if profile_operation is not None:
            arguments = dict(profile_arguments or {})
            arguments[profile_identity_argument] = puuid
            game_profile = await self._call(profile_operation, **arguments)
        return PlayerProfile(
            game=game,
            riot_id=str(parsed),
            puuid=puuid,
            account=account,
            game_profile=game_profile,
        )


def platform_route(value: PlatformRoute | str | None) -> PlatformRoute | None:
    if value is None:
        return None
    if isinstance(value, PlatformRoute):
        return value
    try:
        return PlatformRoute(value.lower())
    except ValueError as exc:
        raise RouteResolutionError(RouteKind.PLATFORM, explicit=value) from exc


def regional_route(value: RegionalRoute | str | None) -> RegionalRoute | None:
    if value is None:
        return None
    if isinstance(value, RegionalRoute):
        return value
    try:
        return RegionalRoute(value.lower())
    except ValueError as exc:
        raise RouteResolutionError(RouteKind.REGIONAL, explicit=value) from exc


def valorant_route(value: ValorantRoute | str | None) -> ValorantRoute | None:
    if value is None:
        return None
    if isinstance(value, ValorantRoute):
        return value
    try:
        return ValorantRoute(value.lower())
    except ValueError as exc:
        raise RouteResolutionError(RouteKind.VALORANT, explicit=value) from exc


def regional_from_platform(
    value: PlatformRoute | None,
) -> RegionalRoute | None:
    if value is None:
        return None
    resolved = resolve_route(RouteKind.REGIONAL, default=value)
    if not isinstance(resolved, RegionalRoute):
        raise TypeError("Resolved route is not regional")
    return resolved


def regional_from_valorant(
    value: ValorantRoute | None,
) -> RegionalRoute | None:
    if value is None:
        return None
    resolved = resolve_route(RouteKind.REGIONAL, default=value)
    if not isinstance(resolved, RegionalRoute):
        raise TypeError("Resolved route is not regional")
    return resolved


async def account_puuid(
    service: WorkflowService,
    riot_id: str,
    *,
    route: RegionalRoute | None,
) -> tuple[RiotId, str]:
    parsed = RiotId.parse(riot_id)
    account = await service._account(parsed, route=route)
    return parsed, str(_field(account, "puuid"))


def summary_from_match(game: Game, match: Any, puuid: str) -> MatchSummary:
    metadata = _field(match, "metadata", default={})
    info = _field(match, "info", "match_info", "matchInfo", default={})
    match_id = str(
        _field(metadata, "match_id", "matchId", default="")
        or _field(info, "match_id", "matchId", default="")
        or _field(match, "match_id", "matchId", default="")
    )
    participants = (
        _field(info, "participants", "players", default=None)
        or _field(match, "players", default=[])
        or []
    )
    player: dict[str, Any] = {}
    for participant in participants:
        if str(_field(participant, "puuid", default="")) == puuid:
            player = _mapping(participant)
            break

    won = _field(player, "win", default=None)
    if won is None:
        placement = _field(player, "placement", default=None)
        won = placement == 1 if isinstance(placement, int) else None
    if won is None:
        outcome = _field(player, "game_outcome", default=None)
        if isinstance(outcome, str):
            won = outcome.casefold() in {"win", "won", "victory"}
    if won is None:
        team_id = _field(player, "team_id", "teamId", default=None)
        for team in _field(match, "teams", default=[]) or []:
            if team_id is not None and _field(team, "team_id", "teamId") == team_id:
                team_won = _field(team, "won", default=None)
                won = team_won if isinstance(team_won, bool) else None
                break

    started = _field(
        info,
        "game_start_timestamp",
        "game_start_millis",
        "game_datetime",
        "gameStartTimestamp",
        "gameStartMillis",
        default=None,
    )
    started_at = _timestamp(started)
    if started_at is None:
        started_at = _iso_timestamp(
            _field(info, "game_start_time_utc", "game_start_time", default=None)
        )

    duration = _field(
        info,
        "game_duration",
        "game_length",
        "gameDuration",
        "gameLength",
        default=None,
    )
    duration_millis = _field(
        info,
        "game_length_millis",
        "gameLengthMillis",
        default=None,
    )
    if duration is None and isinstance(duration_millis, (int, float)):
        duration = duration_millis / 1000

    queue_id = _field(
        info,
        "queue_id",
        "queueId",
        "queue",
        default=None,
    )
    return MatchSummary(
        game=game,
        match_id=match_id,
        started_at=started_at,
        duration_seconds=float(duration) if isinstance(duration, (int, float)) else None,
        queue_id=queue_id if isinstance(queue_id, (str, int)) else None,
        won=bool(won) if isinstance(won, bool) else None,
        player=player,
    )


def history_match_ids(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    history = _field(value, "history", default=[]) or []
    result: list[str] = []
    for item in history:
        match_id = _field(item, "match_id", "matchId", default=None)
        if match_id:
            result.append(str(match_id))
    return result


def _mapping(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    dump = getattr(value, "model_dump", None)
    if callable(dump):
        result = dump()
        return dict(result) if isinstance(result, dict) else {}
    return {}


def _field(value: Any, *names: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        for name in names:
            if name in value:
                return value[name]
        return default
    for name in names:
        if hasattr(value, name):
            return getattr(value, name)
    return default


def _timestamp(value: Any) -> datetime | None:
    if not isinstance(value, (int, float)):
        return None
    seconds = value / 1000 if value > 10_000_000_000 else value
    try:
        return datetime.fromtimestamp(seconds, tz=timezone.utc)
    except (OSError, OverflowError, ValueError):
        return None


def _iso_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

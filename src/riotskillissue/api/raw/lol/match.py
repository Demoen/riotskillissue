from __future__ import annotations

from typing import Any, Awaitable, Callable, List, Literal, Optional, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RegionalRoute, RouteKind
from riotskillissue.models.lol.match_v5 import Match, Replay, Timeline

_GET_MATCH_IDS_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(List[str]).validate_python
_GET_REPLAY_RESPONSE_ADAPTER = TypeAdapter(Replay).validate_python
_GET_MATCH_RESPONSE_ADAPTER = TypeAdapter(Match).validate_python
_GET_TIMELINE_RESPONSE_ADAPTER = TypeAdapter(Timeline).validate_python


class LolMatchApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_match_ids_by_puuid(
        self,
        *,
        puuid: str,
        count: Optional[int] = None,
        end_time: Optional[int] = None,
        queue: Optional[int] = None,
        start: Optional[int] = None,
        start_time: Optional[int] = None,
        type: Optional[Literal["ranked", "normal", "tourney", "tutorial"]] = None,
        route: RegionalRoute | str | None = None,
    ) -> List[str]:
        "Get a list of match ids by puuid"
        path = "/lol/match/v5/matches/by-puuid/{puuid}/ids"
        path = path.replace(
            "{puuid}",
            quote(str(puuid), safe=""),
        )
        params: dict[str, Any] = {
            "count": count,
            "endTime": end_time,
            "queue": queue,
            "start": start,
            "startTime": start_time,
            "type": type,
        }
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe", "sea"),
        )
        return cast(
            List[str],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="match-v5.getMatchIdsByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_MATCH_IDS_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_replay(
        self,
        *,
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> Replay:
        "Get player replays"
        path = "/lol/match/v5/matches/by-puuid/{puuid}/replays"
        path = path.replace(
            "{puuid}",
            quote(str(puuid), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe", "sea"),
        )
        return cast(
            Replay,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="match-v5.getReplay",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_REPLAY_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_match(
        self,
        *,
        match_id: str,
        route: RegionalRoute | str | None = None,
    ) -> Match:
        "Get a match by match id"
        path = "/lol/match/v5/matches/{matchId}"
        path = path.replace(
            "{matchId}",
            quote(str(match_id), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe", "sea"),
        )
        return cast(
            Match,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="match-v5.getMatch",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_MATCH_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_timeline(
        self,
        *,
        match_id: str,
        route: RegionalRoute | str | None = None,
    ) -> Timeline:
        "Get a match timeline by match id"
        path = "/lol/match/v5/matches/{matchId}/timeline"
        path = path.replace(
            "{matchId}",
            quote(str(match_id), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe", "sea"),
        )
        return cast(
            Timeline,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="match-v5.getTimeline",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_TIMELINE_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolMatchApi:
    def __init__(
        self,
        async_api: LolMatchApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_match_ids_by_puuid(
        self,
        *,
        puuid: str,
        count: Optional[int] = None,
        end_time: Optional[int] = None,
        queue: Optional[int] = None,
        start: Optional[int] = None,
        start_time: Optional[int] = None,
        type: Optional[Literal["ranked", "normal", "tourney", "tutorial"]] = None,
        route: RegionalRoute | str | None = None,
    ) -> List[str]:
        return cast(
            List[str],
            self._run(
                self._async_api.get_match_ids_by_puuid(
                    puuid=puuid,
                    count=count,
                    end_time=end_time,
                    queue=queue,
                    start=start,
                    start_time=start_time,
                    type=type,
                    route=route,
                )
            ),
        )

    def get_replay(
        self,
        *,
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> Replay:
        return cast(
            Replay,
            self._run(
                self._async_api.get_replay(
                    puuid=puuid,
                    route=route,
                )
            ),
        )

    def get_match(
        self,
        *,
        match_id: str,
        route: RegionalRoute | str | None = None,
    ) -> Match:
        return cast(
            Match,
            self._run(
                self._async_api.get_match(
                    match_id=match_id,
                    route=route,
                )
            ),
        )

    def get_timeline(
        self,
        *,
        match_id: str,
        route: RegionalRoute | str | None = None,
    ) -> Timeline:
        return cast(
            Timeline,
            self._run(
                self._async_api.get_timeline(
                    match_id=match_id,
                    route=route,
                )
            ),
        )

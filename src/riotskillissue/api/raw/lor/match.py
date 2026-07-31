from __future__ import annotations

from typing import Any, Awaitable, Callable, List, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RegionalRoute, RouteKind
from riotskillissue.models.lor.match_v1 import Match

_GET_MATCH_IDS_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(List[str]).validate_python
_GET_MATCH_RESPONSE_ADAPTER = TypeAdapter(Match).validate_python


class LorMatchApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_match_ids_by_puuid(
        self,
        *,
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> List[str]:
        "Get a list of match ids by PUUID"
        path = "/lor/match/v1/matches/by-puuid/{puuid}/ids"
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
            allowed_routes=("americas", "apac", "europe", "sea"),
        )
        return cast(
            List[str],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lor-match-v1.getMatchIdsByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_MATCH_IDS_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_match(
        self,
        *,
        match_id: str,
        route: RegionalRoute | str | None = None,
    ) -> Match:
        "Get match by id"
        path = "/lor/match/v1/matches/{matchId}"
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
            allowed_routes=("americas", "apac", "europe", "sea"),
        )
        return cast(
            Match,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lor-match-v1.getMatch",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_MATCH_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLorMatchApi:
    def __init__(
        self,
        async_api: LorMatchApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_match_ids_by_puuid(
        self,
        *,
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> List[str]:
        return cast(
            List[str],
            self._run(
                self._async_api.get_match_ids_by_puuid(
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

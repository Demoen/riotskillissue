from __future__ import annotations

from typing import Any, Awaitable, Callable, cast

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.lol.champion_v3 import ChampionInfo

_GET_CHAMPION_INFO_RESPONSE_ADAPTER = TypeAdapter(ChampionInfo).validate_python


class LolChampionApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_champion_info(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> ChampionInfo:
        "Returns champion rotations, including free-to-play and low-level free-to-play…"
        path = "/lol/platform/v3/champion-rotations"
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("platform"),
            route,
            allowed_routes=(
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
                "ru",
                "sg2",
                "tr1",
                "tw2",
                "vn2",
            ),
        )
        return cast(
            ChampionInfo,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="champion-v3.getChampionInfo",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CHAMPION_INFO_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolChampionApi:
    def __init__(
        self,
        async_api: LolChampionApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_champion_info(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> ChampionInfo:
        return cast(
            ChampionInfo,
            self._run(
                self._async_api.get_champion_info(
                    route=route,
                )
            ),
        )

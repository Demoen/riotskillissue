from __future__ import annotations

from typing import Any, Awaitable, Callable, cast

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.lol.status_v4 import PlatformData

_GET_PLATFORM_DATA_RESPONSE_ADAPTER = TypeAdapter(PlatformData).validate_python


class LolStatusApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_platform_data(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> PlatformData:
        "Get League of Legends status for the given platform."
        path = "/lol/status/v4/platform-data"
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
                "pbe1",
                "ru",
                "sg2",
                "tr1",
                "vn2",
            ),
        )
        return cast(
            PlatformData,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lol-status-v4.getPlatformData",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_PLATFORM_DATA_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolStatusApi:
    def __init__(
        self,
        async_api: LolStatusApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_platform_data(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> PlatformData:
        return cast(
            PlatformData,
            self._run(
                self._async_api.get_platform_data(
                    route=route,
                )
            ),
        )

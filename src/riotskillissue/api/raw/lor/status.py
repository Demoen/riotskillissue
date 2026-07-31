from __future__ import annotations

from typing import Any, Awaitable, Callable, cast

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RegionalRoute, RouteKind
from riotskillissue.models.lor.status_v1 import PlatformData

_GET_PLATFORM_DATA_RESPONSE_ADAPTER = TypeAdapter(PlatformData).validate_python


class LorStatusApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_platform_data(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> PlatformData:
        "Get Legends of Runeterra status for the given platform."
        path = "/lor/status/v1/platform-data"
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "europe", "sea"),
        )
        return cast(
            PlatformData,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lor-status-v1.getPlatformData",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_PLATFORM_DATA_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLorStatusApi:
    def __init__(
        self,
        async_api: LorStatusApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_platform_data(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> PlatformData:
        return cast(
            PlatformData,
            self._run(
                self._async_api.get_platform_data(
                    route=route,
                )
            ),
        )

from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional, cast

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RegionalRoute, RouteKind
from riotskillissue.models.riftbound.content_v1 import RiftboundContent

_GET_CONTENT_RESPONSE_ADAPTER = TypeAdapter(RiftboundContent).validate_python


class RiftboundContentApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_content(
        self,
        *,
        locale: Optional[str] = None,
        route: RegionalRoute | str | None = None,
    ) -> RiftboundContent:
        "Get riftbound content"
        path = "/riftbound/content/v1/contents"
        params: dict[str, Any] = {
            "locale": locale,
        }
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe"),
        )
        return cast(
            RiftboundContent,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="riftbound-content-v1.getContent",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CONTENT_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncRiftboundContentApi:
    def __init__(
        self,
        async_api: RiftboundContentApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_content(
        self,
        *,
        locale: Optional[str] = None,
        route: RegionalRoute | str | None = None,
    ) -> RiftboundContent:
        return cast(
            RiftboundContent,
            self._run(
                self._async_api.get_content(
                    locale=locale,
                    route=route,
                )
            ),
        )

from __future__ import annotations

from typing import Any, Awaitable, Callable, Optional, cast

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RouteKind, ValorantRoute
from riotskillissue.models.valorant.content_v1 import Content

_GET_CONTENT_RESPONSE_ADAPTER = TypeAdapter(Content).validate_python


class ValorantContentApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_content(
        self,
        *,
        locale: Optional[str] = None,
        route: ValorantRoute | str | None = None,
    ) -> Content:
        "Get content optionally filtered by locale"
        path = "/val/content/v1/contents"
        params: dict[str, Any] = {
            "locale": locale,
        }
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("val-platform"),
            route,
            allowed_routes=("ap", "br", "esports", "eu", "kr", "latam", "na"),
        )
        return cast(
            Content,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="val-content-v1.getContent",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CONTENT_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncValorantContentApi:
    def __init__(
        self,
        async_api: ValorantContentApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_content(
        self,
        *,
        locale: Optional[str] = None,
        route: ValorantRoute | str | None = None,
    ) -> Content:
        return cast(
            Content,
            self._run(
                self._async_api.get_content(
                    locale=locale,
                    route=route,
                )
            ),
        )

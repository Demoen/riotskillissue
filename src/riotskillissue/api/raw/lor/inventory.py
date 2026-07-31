from __future__ import annotations

from typing import Any, Awaitable, Callable, List, cast

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RegionalRoute, RouteKind
from riotskillissue.models.lor.inventory_v1 import Card

_GET_CARDS_RESPONSE_ADAPTER = TypeAdapter(List[Card]).validate_python


class LorInventoryApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_cards(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> List[Card]:
        "Return a list of cards owned by the calling user."
        path = "/lor/inventory/v1/cards/me"
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
            List[Card],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lor-inventory-v1.getCards",
                auth_mode="rso",
                cache_user_scoped=True,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CARDS_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLorInventoryApi:
    def __init__(
        self,
        async_api: LorInventoryApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_cards(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> List[Card]:
        return cast(
            List[Card],
            self._run(
                self._async_api.get_cards(
                    route=route,
                )
            ),
        )

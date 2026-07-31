from __future__ import annotations

from typing import Any, Awaitable, Callable, cast

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RegionalRoute, RouteKind
from riotskillissue.models.lor.ranked_v1 import Leaderboard

_GET_LEADERBOARDS_RESPONSE_ADAPTER = TypeAdapter(Leaderboard).validate_python


class LorRankedApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_leaderboards(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> Leaderboard:
        "Get the players in Master tier."
        path = "/lor/ranked/v1/leaderboards"
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
            Leaderboard,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lor-ranked-v1.getLeaderboards",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_LEADERBOARDS_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLorRankedApi:
    def __init__(
        self,
        async_api: LorRankedApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_leaderboards(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> Leaderboard:
        return cast(
            Leaderboard,
            self._run(
                self._async_api.get_leaderboards(
                    route=route,
                )
            ),
        )

from __future__ import annotations

from typing import Any, Awaitable, Callable, Literal, Optional, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RouteKind, ValorantRoute
from riotskillissue.models.valorant.console_ranked_v1 import Leaderboard

_GET_LEADERBOARD_RESPONSE_ADAPTER = TypeAdapter(Leaderboard).validate_python


class ValorantConsoleRankedApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_leaderboard(
        self,
        *,
        act_id: str,
        platform_type: Literal["playstation", "xbox"],
        size: Optional[int] = None,
        start_index: Optional[int] = None,
        route: ValorantRoute | str | None = None,
    ) -> Leaderboard:
        "Get leaderboard for the competitive queue"
        path = "".join(("/val/console/ranked/v1/leaderboards/by-act/{ac", "tId}"))
        path = path.replace(
            "{actId}",
            quote(str(act_id), safe=""),
        )
        params: dict[str, Any] = {
            "platformType": platform_type,
            "size": size,
            "startIndex": start_index,
        }
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("val-platform"),
            route,
            allowed_routes=("ap", "eu", "na"),
        )
        return cast(
            Leaderboard,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="val-console-ranked-v1.getLeaderboard",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_LEADERBOARD_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncValorantConsoleRankedApi:
    def __init__(
        self,
        async_api: ValorantConsoleRankedApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_leaderboard(
        self,
        *,
        act_id: str,
        platform_type: Literal["playstation", "xbox"],
        size: Optional[int] = None,
        start_index: Optional[int] = None,
        route: ValorantRoute | str | None = None,
    ) -> Leaderboard:
        return cast(
            Leaderboard,
            self._run(
                self._async_api.get_leaderboard(
                    act_id=act_id,
                    platform_type=platform_type,
                    size=size,
                    start_index=start_index,
                    route=route,
                )
            ),
        )

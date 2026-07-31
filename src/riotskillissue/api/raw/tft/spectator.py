from __future__ import annotations

from typing import Any, Awaitable, Callable, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.tft.spectator_v5 import CurrentGameInfo

_GET_CURRENT_GAME_INFO_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(CurrentGameInfo).validate_python


class TftSpectatorApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_current_game_info_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> CurrentGameInfo:
        "Get current game information for the given puuid."
        path = "".join(("/lol/spectator/tft/v5/active-games/by-puuid/{e", "ncryptedPUUID}"))
        path = path.replace(
            "{encryptedPUUID}",
            quote(str(encrypted_puuid), safe=""),
        )
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
            CurrentGameInfo,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="spectator-tft-v5.getCurrentGameInfoByPuuid",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CURRENT_GAME_INFO_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncTftSpectatorApi:
    def __init__(
        self,
        async_api: TftSpectatorApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_current_game_info_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> CurrentGameInfo:
        return cast(
            CurrentGameInfo,
            self._run(
                self._async_api.get_current_game_info_by_puuid(
                    encrypted_puuid=encrypted_puuid,
                    route=route,
                )
            ),
        )

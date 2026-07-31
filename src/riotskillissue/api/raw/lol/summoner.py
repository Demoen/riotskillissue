from __future__ import annotations

from typing import Any, Awaitable, Callable, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.lol.summoner_v4 import Summoner

_GET_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(Summoner).validate_python
_GET_BY_ACCESS_TOKEN_RESPONSE_ADAPTER = TypeAdapter(Summoner).validate_python


class LolSummonerApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> Summoner:
        "Get a summoner by PUUID."
        path = "".join(("/lol/summoner/v4/summoners/by-puuid/{encrypted", "PUUID}"))
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
            Summoner,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="summoner-v4.getByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_by_access_token(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Summoner:
        "Get a summoner by access token."
        path = "/lol/summoner/v4/summoners/me"
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
            Summoner,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="summoner-v4.getByAccessToken",
                auth_mode="rso",
                cache_user_scoped=True,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_BY_ACCESS_TOKEN_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolSummonerApi:
    def __init__(
        self,
        async_api: LolSummonerApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> Summoner:
        return cast(
            Summoner,
            self._run(
                self._async_api.get_by_puuid(
                    encrypted_puuid=encrypted_puuid,
                    route=route,
                )
            ),
        )

    def get_by_access_token(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Summoner:
        return cast(
            Summoner,
            self._run(
                self._async_api.get_by_access_token(
                    route=route,
                )
            ),
        )

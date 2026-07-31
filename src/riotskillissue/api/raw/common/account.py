from __future__ import annotations

from typing import Any, Awaitable, Callable, Literal, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RegionalRoute, RouteKind
from riotskillissue.models.common.account_v1 import Account, AccountRegion, ActiveShard

_GET_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(Account).validate_python
_GET_BY_RIOT_ID_RESPONSE_ADAPTER = TypeAdapter(Account).validate_python
_GET_BY_ACCESS_TOKEN_RESPONSE_ADAPTER = TypeAdapter(Account).validate_python
_GET_ACTIVE_SHARD_RESPONSE_ADAPTER = TypeAdapter(ActiveShard).validate_python
_GET_ACTIVE_REGION_RESPONSE_ADAPTER = TypeAdapter(AccountRegion).validate_python


class CommonAccountApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_by_puuid(
        self,
        *,
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> Account:
        "Get account by puuid"
        path = "/riot/account/v1/accounts/by-puuid/{puuid}"
        path = path.replace(
            "{puuid}",
            quote(str(puuid), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe"),
        )
        return cast(
            Account,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="account-v1.getByPuuid",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_by_riot_id(
        self,
        *,
        game_name: str,
        tag_line: str,
        route: RegionalRoute | str | None = None,
    ) -> Account:
        "Get account by riot id"
        path = "".join(("/riot/account/v1/accounts/by-riot-id/{gameName", "}/{tagLine}"))
        path = path.replace(
            "{gameName}",
            quote(str(game_name), safe=""),
        )
        path = path.replace(
            "{tagLine}",
            quote(str(tag_line), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe"),
        )
        return cast(
            Account,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="account-v1.getByRiotId",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_BY_RIOT_ID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_by_access_token(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> Account:
        "Get account by access token"
        path = "/riot/account/v1/accounts/me"
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe"),
        )
        return cast(
            Account,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="account-v1.getByAccessToken",
                auth_mode="rso",
                cache_user_scoped=True,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_BY_ACCESS_TOKEN_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_active_shard(
        self,
        *,
        game: Literal["val", "lor", "2xko"],
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> ActiveShard:
        "Get active shard for a player"
        path = "".join(("/riot/account/v1/active-shards/by-game/{game}/", "by-puuid/{puuid}"))
        path = path.replace(
            "{game}",
            quote(str(game), safe=""),
        )
        path = path.replace(
            "{puuid}",
            quote(str(puuid), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe"),
        )
        return cast(
            ActiveShard,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="account-v1.getActiveShard",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_ACTIVE_SHARD_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_active_region(
        self,
        *,
        game: Literal["lol", "tft"],
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> AccountRegion:
        "Get active region (lol and tft)"
        path = "".join(("/riot/account/v1/region/by-game/{game}/by-puui", "d/{puuid}"))
        path = path.replace(
            "{game}",
            quote(str(game), safe=""),
        )
        path = path.replace(
            "{puuid}",
            quote(str(puuid), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas", "asia", "europe"),
        )
        return cast(
            AccountRegion,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="account-v1.getActiveRegion",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_ACTIVE_REGION_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncCommonAccountApi:
    def __init__(
        self,
        async_api: CommonAccountApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_by_puuid(
        self,
        *,
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> Account:
        return cast(
            Account,
            self._run(
                self._async_api.get_by_puuid(
                    puuid=puuid,
                    route=route,
                )
            ),
        )

    def get_by_riot_id(
        self,
        *,
        game_name: str,
        tag_line: str,
        route: RegionalRoute | str | None = None,
    ) -> Account:
        return cast(
            Account,
            self._run(
                self._async_api.get_by_riot_id(
                    game_name=game_name,
                    tag_line=tag_line,
                    route=route,
                )
            ),
        )

    def get_by_access_token(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> Account:
        return cast(
            Account,
            self._run(
                self._async_api.get_by_access_token(
                    route=route,
                )
            ),
        )

    def get_active_shard(
        self,
        *,
        game: Literal["val", "lor", "2xko"],
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> ActiveShard:
        return cast(
            ActiveShard,
            self._run(
                self._async_api.get_active_shard(
                    game=game,
                    puuid=puuid,
                    route=route,
                )
            ),
        )

    def get_active_region(
        self,
        *,
        game: Literal["lol", "tft"],
        puuid: str,
        route: RegionalRoute | str | None = None,
    ) -> AccountRegion:
        return cast(
            AccountRegion,
            self._run(
                self._async_api.get_active_region(
                    game=game,
                    puuid=puuid,
                    route=route,
                )
            ),
        )

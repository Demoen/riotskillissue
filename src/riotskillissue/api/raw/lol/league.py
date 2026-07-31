from __future__ import annotations

from typing import Any, Awaitable, Callable, List, Literal, Optional, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.lol.league_v4 import LeagueEntry, LeagueList

_GET_CHALLENGER_LEAGUE_RESPONSE_ADAPTER = TypeAdapter(LeagueList).validate_python
_GET_LEAGUE_ENTRIES_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(List[LeagueEntry]).validate_python
_GET_LEAGUE_ENTRIES_RESPONSE_ADAPTER = TypeAdapter(List[LeagueEntry]).validate_python
_GET_GRANDMASTER_LEAGUE_RESPONSE_ADAPTER = TypeAdapter(LeagueList).validate_python
_GET_MASTER_LEAGUE_RESPONSE_ADAPTER = TypeAdapter(LeagueList).validate_python


class LolLeagueApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_challenger_league(
        self,
        *,
        queue: Literal["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        route: PlatformRoute | str | None = None,
    ) -> LeagueList:
        "Get the challenger league for given queue."
        path = "".join(("/lol/league/v4/challengerleagues/by-queue/{que", "ue}"))
        path = path.replace(
            "{queue}",
            quote(str(queue), safe=""),
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
            LeagueList,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="league-v4.getChallengerLeague",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CHALLENGER_LEAGUE_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_league_entries_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> List[LeagueEntry]:
        "Get league entries in all queues for a given puuid"
        path = "".join(("/lol/league/v4/entries/by-puuid/{encryptedPUUI", "D}"))
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
            List[LeagueEntry],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="league-v4.getLeagueEntriesByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_LEAGUE_ENTRIES_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_league_entries(
        self,
        *,
        division: Literal["I", "II", "III", "IV"],
        queue: Literal["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        tier: Literal["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"],
        page: Optional[int] = None,
        route: PlatformRoute | str | None = None,
    ) -> List[LeagueEntry]:
        "Get all the league entries."
        path = "".join(("/lol/league/v4/entries/{queue}/{tier}/{divisio", "n}"))
        path = path.replace(
            "{division}",
            quote(str(division), safe=""),
        )
        path = path.replace(
            "{queue}",
            quote(str(queue), safe=""),
        )
        path = path.replace(
            "{tier}",
            quote(str(tier), safe=""),
        )
        params: dict[str, Any] = {
            "page": page,
        }
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
            List[LeagueEntry],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="league-v4.getLeagueEntries",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_LEAGUE_ENTRIES_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_grandmaster_league(
        self,
        *,
        queue: Literal["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        route: PlatformRoute | str | None = None,
    ) -> LeagueList:
        "Get the grandmaster league of a specific queue."
        path = "".join(("/lol/league/v4/grandmasterleagues/by-queue/{qu", "eue}"))
        path = path.replace(
            "{queue}",
            quote(str(queue), safe=""),
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
            LeagueList,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="league-v4.getGrandmasterLeague",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_GRANDMASTER_LEAGUE_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_master_league(
        self,
        *,
        queue: Literal["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        route: PlatformRoute | str | None = None,
    ) -> LeagueList:
        "Get the master league for given queue."
        path = "/lol/league/v4/masterleagues/by-queue/{queue}"
        path = path.replace(
            "{queue}",
            quote(str(queue), safe=""),
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
            LeagueList,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="league-v4.getMasterLeague",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_MASTER_LEAGUE_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolLeagueApi:
    def __init__(
        self,
        async_api: LolLeagueApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_challenger_league(
        self,
        *,
        queue: Literal["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        route: PlatformRoute | str | None = None,
    ) -> LeagueList:
        return cast(
            LeagueList,
            self._run(
                self._async_api.get_challenger_league(
                    queue=queue,
                    route=route,
                )
            ),
        )

    def get_league_entries_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> List[LeagueEntry]:
        return cast(
            List[LeagueEntry],
            self._run(
                self._async_api.get_league_entries_by_puuid(
                    encrypted_puuid=encrypted_puuid,
                    route=route,
                )
            ),
        )

    def get_league_entries(
        self,
        *,
        division: Literal["I", "II", "III", "IV"],
        queue: Literal["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        tier: Literal["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"],
        page: Optional[int] = None,
        route: PlatformRoute | str | None = None,
    ) -> List[LeagueEntry]:
        return cast(
            List[LeagueEntry],
            self._run(
                self._async_api.get_league_entries(
                    division=division,
                    queue=queue,
                    tier=tier,
                    page=page,
                    route=route,
                )
            ),
        )

    def get_grandmaster_league(
        self,
        *,
        queue: Literal["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        route: PlatformRoute | str | None = None,
    ) -> LeagueList:
        return cast(
            LeagueList,
            self._run(
                self._async_api.get_grandmaster_league(
                    queue=queue,
                    route=route,
                )
            ),
        )

    def get_master_league(
        self,
        *,
        queue: Literal["RANKED_SOLO_5x5", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        route: PlatformRoute | str | None = None,
    ) -> LeagueList:
        return cast(
            LeagueList,
            self._run(
                self._async_api.get_master_league(
                    queue=queue,
                    route=route,
                )
            ),
        )

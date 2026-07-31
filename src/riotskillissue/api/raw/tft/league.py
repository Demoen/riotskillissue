from __future__ import annotations

from typing import Any, Awaitable, Callable, List, Literal, Optional, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.tft.league_v1 import LeagueEntry, LeagueList, TopRatedLadderEntry

_GET_LEAGUE_ENTRIES_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(List[LeagueEntry]).validate_python
_GET_CHALLENGER_LEAGUE_RESPONSE_ADAPTER = TypeAdapter(LeagueList).validate_python
_GET_LEAGUE_ENTRIES_RESPONSE_ADAPTER = TypeAdapter(List[LeagueEntry]).validate_python
_GET_GRANDMASTER_LEAGUE_RESPONSE_ADAPTER = TypeAdapter(LeagueList).validate_python
_GET_MASTER_LEAGUE_RESPONSE_ADAPTER = TypeAdapter(LeagueList).validate_python
_GET_TOP_RATED_LADDER_RESPONSE_ADAPTER = TypeAdapter(List[TopRatedLadderEntry]).validate_python


class TftLeagueApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_league_entries_by_puuid(
        self,
        *,
        puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> List[LeagueEntry]:
        "Get league entries in all queues for a given puuid"
        path = "/tft/league/v1/by-puuid/{puuid}"
        path = path.replace(
            "{puuid}",
            quote(str(puuid), safe=""),
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
                operation_id="tft-league-v1.getLeagueEntriesByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_LEAGUE_ENTRIES_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_challenger_league(
        self,
        *,
        queue: Optional[Literal["RANKED_TFT", "RANKED_TFT_DOUBLE_UP"]] = None,
        route: PlatformRoute | str | None = None,
    ) -> LeagueList:
        "Get the challenger league."
        path = "/tft/league/v1/challenger"
        params: dict[str, Any] = {
            "queue": queue,
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
            LeagueList,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="tft-league-v1.getChallengerLeague",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CHALLENGER_LEAGUE_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_league_entries(
        self,
        *,
        division: Literal["I", "II", "III", "IV"],
        tier: Literal["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"],
        page: Optional[int] = None,
        queue: Optional[Literal["RANKED_TFT", "RANKED_TFT_DOUBLE_UP"]] = None,
        route: PlatformRoute | str | None = None,
    ) -> List[LeagueEntry]:
        "Get all the league entries."
        path = "/tft/league/v1/entries/{tier}/{division}"
        path = path.replace(
            "{division}",
            quote(str(division), safe=""),
        )
        path = path.replace(
            "{tier}",
            quote(str(tier), safe=""),
        )
        params: dict[str, Any] = {
            "page": page,
            "queue": queue,
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
                operation_id="tft-league-v1.getLeagueEntries",
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
        queue: Optional[Literal["RANKED_TFT", "RANKED_TFT_DOUBLE_UP"]] = None,
        route: PlatformRoute | str | None = None,
    ) -> LeagueList:
        "Get the grandmaster league."
        path = "/tft/league/v1/grandmaster"
        params: dict[str, Any] = {
            "queue": queue,
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
            LeagueList,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="tft-league-v1.getGrandmasterLeague",
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
        queue: Optional[Literal["RANKED_TFT", "RANKED_TFT_DOUBLE_UP"]] = None,
        route: PlatformRoute | str | None = None,
    ) -> LeagueList:
        "Get the master league."
        path = "/tft/league/v1/master"
        params: dict[str, Any] = {
            "queue": queue,
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
            LeagueList,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="tft-league-v1.getMasterLeague",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_MASTER_LEAGUE_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_top_rated_ladder(
        self,
        *,
        queue: Literal["RANKED_TFT_TURBO"],
        route: PlatformRoute | str | None = None,
    ) -> List[TopRatedLadderEntry]:
        "Get the top rated ladder for given queue"
        path = "/tft/league/v1/rated-ladders/{queue}/top"
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
            List[TopRatedLadderEntry],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="tft-league-v1.getTopRatedLadder",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_TOP_RATED_LADDER_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncTftLeagueApi:
    def __init__(
        self,
        async_api: TftLeagueApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_league_entries_by_puuid(
        self,
        *,
        puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> List[LeagueEntry]:
        return cast(
            List[LeagueEntry],
            self._run(
                self._async_api.get_league_entries_by_puuid(
                    puuid=puuid,
                    route=route,
                )
            ),
        )

    def get_challenger_league(
        self,
        *,
        queue: Optional[Literal["RANKED_TFT", "RANKED_TFT_DOUBLE_UP"]] = None,
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

    def get_league_entries(
        self,
        *,
        division: Literal["I", "II", "III", "IV"],
        tier: Literal["DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON"],
        page: Optional[int] = None,
        queue: Optional[Literal["RANKED_TFT", "RANKED_TFT_DOUBLE_UP"]] = None,
        route: PlatformRoute | str | None = None,
    ) -> List[LeagueEntry]:
        return cast(
            List[LeagueEntry],
            self._run(
                self._async_api.get_league_entries(
                    division=division,
                    tier=tier,
                    page=page,
                    queue=queue,
                    route=route,
                )
            ),
        )

    def get_grandmaster_league(
        self,
        *,
        queue: Optional[Literal["RANKED_TFT", "RANKED_TFT_DOUBLE_UP"]] = None,
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
        queue: Optional[Literal["RANKED_TFT", "RANKED_TFT_DOUBLE_UP"]] = None,
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

    def get_top_rated_ladder(
        self,
        *,
        queue: Literal["RANKED_TFT_TURBO"],
        route: PlatformRoute | str | None = None,
    ) -> List[TopRatedLadderEntry]:
        return cast(
            List[TopRatedLadderEntry],
            self._run(
                self._async_api.get_top_rated_ladder(
                    queue=queue,
                    route=route,
                )
            ),
        )

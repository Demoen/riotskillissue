from __future__ import annotations

from typing import Any, Awaitable, Callable, Literal, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RouteKind, ValorantRoute
from riotskillissue.models.valorant.match_v1 import Match, Matchlist, RecentMatches

_GET_MATCH_RESPONSE_ADAPTER = TypeAdapter(Match).validate_python
_GET_MATCHLIST_RESPONSE_ADAPTER = TypeAdapter(Matchlist).validate_python
_GET_RECENT_RESPONSE_ADAPTER = TypeAdapter(RecentMatches).validate_python


class ValorantMatchApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_match(
        self,
        *,
        match_id: str,
        route: ValorantRoute | str | None = None,
    ) -> Match:
        "Get match by id"
        path = "/val/match/v1/matches/{matchId}"
        path = path.replace(
            "{matchId}",
            quote(str(match_id), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("val-platform"),
            route,
            allowed_routes=("ap", "br", "esports", "eu", "kr", "latam", "na"),
        )
        return cast(
            Match,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="val-match-v1.getMatch",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_MATCH_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_matchlist(
        self,
        *,
        puuid: str,
        route: ValorantRoute | str | None = None,
    ) -> Matchlist:
        "Get matchlist for games played by puuid"
        path = "/val/match/v1/matchlists/by-puuid/{puuid}"
        path = path.replace(
            "{puuid}",
            quote(str(puuid), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("val-platform"),
            route,
            allowed_routes=("ap", "br", "esports", "eu", "kr", "latam", "na"),
        )
        return cast(
            Matchlist,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="val-match-v1.getMatchlist",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_MATCHLIST_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_recent(
        self,
        *,
        queue: Literal[
            "competitive",
            "unrated",
            "spikerush",
            "tournamentmode",
            "deathmatch",
            "onefa",
            "ggteam",
            "hurm",
            "swiftplay",
            "skirmish2v2",
            "skirmishascension1v1",
            "skirmishascension2v2",
        ],
        route: ValorantRoute | str | None = None,
    ) -> RecentMatches:
        "Get recent matches"
        path = "/val/match/v1/recent-matches/by-queue/{queue}"
        path = path.replace(
            "{queue}",
            quote(str(queue), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("val-platform"),
            route,
            allowed_routes=("ap", "br", "esports", "eu", "kr", "latam", "na"),
        )
        return cast(
            RecentMatches,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="val-match-v1.getRecent",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_RECENT_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncValorantMatchApi:
    def __init__(
        self,
        async_api: ValorantMatchApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_match(
        self,
        *,
        match_id: str,
        route: ValorantRoute | str | None = None,
    ) -> Match:
        return cast(
            Match,
            self._run(
                self._async_api.get_match(
                    match_id=match_id,
                    route=route,
                )
            ),
        )

    def get_matchlist(
        self,
        *,
        puuid: str,
        route: ValorantRoute | str | None = None,
    ) -> Matchlist:
        return cast(
            Matchlist,
            self._run(
                self._async_api.get_matchlist(
                    puuid=puuid,
                    route=route,
                )
            ),
        )

    def get_recent(
        self,
        *,
        queue: Literal[
            "competitive",
            "unrated",
            "spikerush",
            "tournamentmode",
            "deathmatch",
            "onefa",
            "ggteam",
            "hurm",
            "swiftplay",
            "skirmish2v2",
            "skirmishascension1v1",
            "skirmishascension2v2",
        ],
        route: ValorantRoute | str | None = None,
    ) -> RecentMatches:
        return cast(
            RecentMatches,
            self._run(
                self._async_api.get_recent(
                    queue=queue,
                    route=route,
                )
            ),
        )

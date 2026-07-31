from __future__ import annotations

from typing import Any, Awaitable, Callable, List, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.lol.clash_v1 import Player, Team, Tournament

_GET_PLAYERS_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(List[Player]).validate_python
_GET_TEAM_BY_ID_RESPONSE_ADAPTER = TypeAdapter(Team).validate_python
_GET_TOURNAMENTS_RESPONSE_ADAPTER = TypeAdapter(List[Tournament]).validate_python
_GET_TOURNAMENT_BY_TEAM_RESPONSE_ADAPTER = TypeAdapter(Tournament).validate_python
_GET_TOURNAMENT_BY_ID_RESPONSE_ADAPTER = TypeAdapter(Tournament).validate_python


class LolClashApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_players_by_puuid(
        self,
        *,
        puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> List[Player]:
        "Get players by puuid"
        path = "/lol/clash/v1/players/by-puuid/{puuid}"
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
            List[Player],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="clash-v1.getPlayersByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_PLAYERS_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_team_by_id(
        self,
        *,
        team_id: str,
        route: PlatformRoute | str | None = None,
    ) -> Team:
        "Get team by ID."
        path = "/lol/clash/v1/teams/{teamId}"
        path = path.replace(
            "{teamId}",
            quote(str(team_id), safe=""),
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
            Team,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="clash-v1.getTeamById",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_TEAM_BY_ID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_tournaments(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> List[Tournament]:
        "Get all active or upcoming tournaments."
        path = "/lol/clash/v1/tournaments"
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
            List[Tournament],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="clash-v1.getTournaments",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_TOURNAMENTS_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_tournament_by_team(
        self,
        *,
        team_id: str,
        route: PlatformRoute | str | None = None,
    ) -> Tournament:
        "Get tournament by team ID."
        path = "/lol/clash/v1/tournaments/by-team/{teamId}"
        path = path.replace(
            "{teamId}",
            quote(str(team_id), safe=""),
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
            Tournament,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="clash-v1.getTournamentByTeam",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_TOURNAMENT_BY_TEAM_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_tournament_by_id(
        self,
        *,
        tournament_id: int,
        route: PlatformRoute | str | None = None,
    ) -> Tournament:
        "Get tournament by ID."
        path = "/lol/clash/v1/tournaments/{tournamentId}"
        path = path.replace(
            "{tournamentId}",
            quote(str(tournament_id), safe=""),
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
            Tournament,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="clash-v1.getTournamentById",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_TOURNAMENT_BY_ID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolClashApi:
    def __init__(
        self,
        async_api: LolClashApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_players_by_puuid(
        self,
        *,
        puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> List[Player]:
        return cast(
            List[Player],
            self._run(
                self._async_api.get_players_by_puuid(
                    puuid=puuid,
                    route=route,
                )
            ),
        )

    def get_team_by_id(
        self,
        *,
        team_id: str,
        route: PlatformRoute | str | None = None,
    ) -> Team:
        return cast(
            Team,
            self._run(
                self._async_api.get_team_by_id(
                    team_id=team_id,
                    route=route,
                )
            ),
        )

    def get_tournaments(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> List[Tournament]:
        return cast(
            List[Tournament],
            self._run(
                self._async_api.get_tournaments(
                    route=route,
                )
            ),
        )

    def get_tournament_by_team(
        self,
        *,
        team_id: str,
        route: PlatformRoute | str | None = None,
    ) -> Tournament:
        return cast(
            Tournament,
            self._run(
                self._async_api.get_tournament_by_team(
                    team_id=team_id,
                    route=route,
                )
            ),
        )

    def get_tournament_by_id(
        self,
        *,
        tournament_id: int,
        route: PlatformRoute | str | None = None,
    ) -> Tournament:
        return cast(
            Tournament,
            self._run(
                self._async_api.get_tournament_by_id(
                    tournament_id=tournament_id,
                    route=route,
                )
            ),
        )

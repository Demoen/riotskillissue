from __future__ import annotations

from typing import Any, Awaitable, Callable, List, Optional, cast
from urllib.parse import quote

from pydantic import BaseModel, TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RegionalRoute, RouteKind
from riotskillissue.models.lol.tournament_stub_v5 import (
    LobbyEventV5Wrapper,
    ProviderRegistrationParametersV5,
    TournamentCodeParametersV5,
    TournamentCodeV5,
    TournamentRegistrationParametersV5,
)

_CREATE_TOURNAMENT_CODE_RESPONSE_ADAPTER = TypeAdapter(List[str]).validate_python
_GET_TOURNAMENT_CODE_RESPONSE_ADAPTER = TypeAdapter(TournamentCodeV5).validate_python
_GET_LOBBY_EVENTS_BY_CODE_RESPONSE_ADAPTER = TypeAdapter(LobbyEventV5Wrapper).validate_python
_REGISTER_PROVIDER_DATA_RESPONSE_ADAPTER = TypeAdapter(int).validate_python
_REGISTER_TOURNAMENT_RESPONSE_ADAPTER = TypeAdapter(int).validate_python


class LolTournamentStubApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def create_tournament_code(
        self,
        *,
        tournament_id: int,
        count: Optional[int] = None,
        body: TournamentCodeParametersV5,
        route: RegionalRoute | str | None = None,
    ) -> List[str]:
        "Create a tournament code for the given tournament - Stub method"
        path = "/lol/tournament-stub/v5/codes"
        params: dict[str, Any] = {
            "tournamentId": tournament_id,
            "count": count,
        }
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        request_kwargs["json"] = (
            body.model_dump(by_alias=True, exclude_none=True)
            if isinstance(body, BaseModel)
            else body
        )
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas",),
        )
        return cast(
            List[str],
            await self.http.request(
                method="POST",
                url=path,
                region_or_platform=resolved_route,
                operation_id="tournament-stub-v5.createTournamentCode",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_CREATE_TOURNAMENT_CODE_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_tournament_code(
        self,
        *,
        tournament_code: str,
        route: RegionalRoute | str | None = None,
    ) -> TournamentCodeV5:
        "Returns the tournament code DTO associated with a tournament code string - Stub…"
        path = "/lol/tournament-stub/v5/codes/{tournamentCode}"
        path = path.replace(
            "{tournamentCode}",
            quote(str(tournament_code), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas",),
        )
        return cast(
            TournamentCodeV5,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="tournament-stub-v5.getTournamentCode",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_TOURNAMENT_CODE_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_lobby_events_by_code(
        self,
        *,
        tournament_code: str,
        route: RegionalRoute | str | None = None,
    ) -> LobbyEventV5Wrapper:
        "Gets a list of lobby events by tournament code - Stub method"
        path = "".join(("/lol/tournament-stub/v5/lobby-events/by-code/{", "tournamentCode}"))
        path = path.replace(
            "{tournamentCode}",
            quote(str(tournament_code), safe=""),
        )
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas",),
        )
        return cast(
            LobbyEventV5Wrapper,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="tournament-stub-v5.getLobbyEventsByCode",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_LOBBY_EVENTS_BY_CODE_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def register_provider_data(
        self,
        *,
        body: ProviderRegistrationParametersV5,
        route: RegionalRoute | str | None = None,
    ) -> int:
        "Creates a tournament provider and returns its ID - Stub method"
        path = "/lol/tournament-stub/v5/providers"
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        request_kwargs["json"] = (
            body.model_dump(by_alias=True, exclude_none=True)
            if isinstance(body, BaseModel)
            else body
        )
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas",),
        )
        return cast(
            int,
            await self.http.request(
                method="POST",
                url=path,
                region_or_platform=resolved_route,
                operation_id="tournament-stub-v5.registerProviderData",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_REGISTER_PROVIDER_DATA_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def register_tournament(
        self,
        *,
        body: TournamentRegistrationParametersV5,
        route: RegionalRoute | str | None = None,
    ) -> int:
        "Creates a tournament and returns its ID - Stub method"
        path = "/lol/tournament-stub/v5/tournaments"
        params: dict[str, Any] = {}
        request_kwargs: dict[str, Any] = {
            "params": {key: value for key, value in params.items() if value is not None}
        }
        request_kwargs["json"] = (
            body.model_dump(by_alias=True, exclude_none=True)
            if isinstance(body, BaseModel)
            else body
        )
        resolved_route = self.http.resolve_route(
            RouteKind("regional"),
            route,
            allowed_routes=("americas",),
        )
        return cast(
            int,
            await self.http.request(
                method="POST",
                url=path,
                region_or_platform=resolved_route,
                operation_id="tournament-stub-v5.registerTournament",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_REGISTER_TOURNAMENT_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolTournamentStubApi:
    def __init__(
        self,
        async_api: LolTournamentStubApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def create_tournament_code(
        self,
        *,
        tournament_id: int,
        count: Optional[int] = None,
        body: TournamentCodeParametersV5,
        route: RegionalRoute | str | None = None,
    ) -> List[str]:
        return cast(
            List[str],
            self._run(
                self._async_api.create_tournament_code(
                    tournament_id=tournament_id,
                    count=count,
                    body=body,
                    route=route,
                )
            ),
        )

    def get_tournament_code(
        self,
        *,
        tournament_code: str,
        route: RegionalRoute | str | None = None,
    ) -> TournamentCodeV5:
        return cast(
            TournamentCodeV5,
            self._run(
                self._async_api.get_tournament_code(
                    tournament_code=tournament_code,
                    route=route,
                )
            ),
        )

    def get_lobby_events_by_code(
        self,
        *,
        tournament_code: str,
        route: RegionalRoute | str | None = None,
    ) -> LobbyEventV5Wrapper:
        return cast(
            LobbyEventV5Wrapper,
            self._run(
                self._async_api.get_lobby_events_by_code(
                    tournament_code=tournament_code,
                    route=route,
                )
            ),
        )

    def register_provider_data(
        self,
        *,
        body: ProviderRegistrationParametersV5,
        route: RegionalRoute | str | None = None,
    ) -> int:
        return cast(
            int,
            self._run(
                self._async_api.register_provider_data(
                    body=body,
                    route=route,
                )
            ),
        )

    def register_tournament(
        self,
        *,
        body: TournamentRegistrationParametersV5,
        route: RegionalRoute | str | None = None,
    ) -> int:
        return cast(
            int,
            self._run(
                self._async_api.register_tournament(
                    body=body,
                    route=route,
                )
            ),
        )

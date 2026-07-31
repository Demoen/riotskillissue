from __future__ import annotations

from typing import Any, Awaitable, Callable, List, cast

from pydantic import BaseModel, TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import RegionalRoute, RouteKind
from riotskillissue.models.lor.deck_v1 import Deck, NewDeck

_GET_DECKS_RESPONSE_ADAPTER = TypeAdapter(List[Deck]).validate_python
_CREATE_DECK_RESPONSE_ADAPTER = TypeAdapter(str).validate_python


class LorDeckApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_decks(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> List[Deck]:
        "Get a list of the calling user's decks."
        path = "/lor/deck/v1/decks/me"
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
            List[Deck],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lor-deck-v1.getDecks",
                auth_mode="rso",
                cache_user_scoped=True,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_DECKS_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def create_deck(
        self,
        *,
        body: NewDeck,
        route: RegionalRoute | str | None = None,
    ) -> str:
        "Create a new deck for the calling user."
        path = "/lor/deck/v1/decks/me"
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
            allowed_routes=("americas", "europe", "sea"),
        )
        return cast(
            str,
            await self.http.request(
                method="POST",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lor-deck-v1.createDeck",
                auth_mode="rso",
                cache_user_scoped=True,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_CREATE_DECK_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLorDeckApi:
    def __init__(
        self,
        async_api: LorDeckApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_decks(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> List[Deck]:
        return cast(
            List[Deck],
            self._run(
                self._async_api.get_decks(
                    route=route,
                )
            ),
        )

    def create_deck(
        self,
        *,
        body: NewDeck,
        route: RegionalRoute | str | None = None,
    ) -> str:
        return cast(
            str,
            self._run(
                self._async_api.create_deck(
                    body=body,
                    route=route,
                )
            ),
        )

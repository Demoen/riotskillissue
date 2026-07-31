from __future__ import annotations

from typing import Any, Awaitable, Callable, List, Literal, Optional, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.lol.league_exp_v4 import LeagueEntry

_GET_LEAGUE_ENTRIES_RESPONSE_ADAPTER = TypeAdapter(List[LeagueEntry]).validate_python


class LolLeagueExpApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_league_entries(
        self,
        *,
        division: Literal["I", "II", "III", "IV"],
        queue: Literal["RANKED_SOLO_5x5", "RANKED_TFT", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        tier: Literal[
            "CHALLENGER",
            "GRANDMASTER",
            "MASTER",
            "DIAMOND",
            "EMERALD",
            "PLATINUM",
            "GOLD",
            "SILVER",
            "BRONZE",
            "IRON",
        ],
        page: Optional[int] = None,
        route: PlatformRoute | str | None = None,
    ) -> List[LeagueEntry]:
        "Get all the league entries."
        path = "".join(("/lol/league-exp/v4/entries/{queue}/{tier}/{div", "ision}"))
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
                operation_id="league-exp-v4.getLeagueEntries",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_LEAGUE_ENTRIES_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolLeagueExpApi:
    def __init__(
        self,
        async_api: LolLeagueExpApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_league_entries(
        self,
        *,
        division: Literal["I", "II", "III", "IV"],
        queue: Literal["RANKED_SOLO_5x5", "RANKED_TFT", "RANKED_FLEX_SR", "RANKED_FLEX_TT"],
        tier: Literal[
            "CHALLENGER",
            "GRANDMASTER",
            "MASTER",
            "DIAMOND",
            "EMERALD",
            "PLATINUM",
            "GOLD",
            "SILVER",
            "BRONZE",
            "IRON",
        ],
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

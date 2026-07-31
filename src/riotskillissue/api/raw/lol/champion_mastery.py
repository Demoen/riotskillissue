from __future__ import annotations

from typing import Any, Awaitable, Callable, List, Optional, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.lol.champion_mastery_v4 import ChampionMastery

_GET_ALL_CHAMPION_MASTERIES_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(
    List[ChampionMastery]
).validate_python
_GET_CHAMPION_MASTERY_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(ChampionMastery).validate_python
_GET_TOP_CHAMPION_MASTERIES_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(
    List[ChampionMastery]
).validate_python
_GET_CHAMPION_MASTERY_SCORE_BY_PUUID_RESPONSE_ADAPTER = TypeAdapter(int).validate_python


class LolChampionMasteryApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_all_champion_masteries_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> List[ChampionMastery]:
        "Get all champion mastery entries sorted by number of champion points descending."
        path = "".join(
            ("/lol/champion-mastery/v4/champion-masteries/by", "-puuid/{encryptedPUUID}")
        )
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
            List[ChampionMastery],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="champion-mastery-v4.getAllChampionMasteriesByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_ALL_CHAMPION_MASTERIES_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_champion_mastery_by_puuid(
        self,
        *,
        champion_id: int,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> ChampionMastery:
        "Get a champion mastery by puuid and champion ID."
        path = "".join(
            (
                "/lol/champion-mastery/v4/champion-masteries/by",
                "-puuid/{encryptedPUUID}/by-champion/{championI",
                "d}",
            )
        )
        path = path.replace(
            "{championId}",
            quote(str(champion_id), safe=""),
        )
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
            ChampionMastery,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="champion-mastery-v4.getChampionMasteryByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CHAMPION_MASTERY_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_top_champion_masteries_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        count: Optional[int] = None,
        route: PlatformRoute | str | None = None,
    ) -> List[ChampionMastery]:
        "Get specified number of top champion mastery entries sorted by number of champion…"
        path = "".join(
            ("/lol/champion-mastery/v4/champion-masteries/by", "-puuid/{encryptedPUUID}/top")
        )
        path = path.replace(
            "{encryptedPUUID}",
            quote(str(encrypted_puuid), safe=""),
        )
        params: dict[str, Any] = {
            "count": count,
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
            List[ChampionMastery],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="champion-mastery-v4.getTopChampionMasteriesByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_TOP_CHAMPION_MASTERIES_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_champion_mastery_score_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> int:
        "Get a player's total champion mastery score, which is the sum of individual…"
        path = "".join(("/lol/champion-mastery/v4/scores/by-puuid/{encr", "yptedPUUID}"))
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
            int,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="champion-mastery-v4.getChampionMasteryScoreByPUUID",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CHAMPION_MASTERY_SCORE_BY_PUUID_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolChampionMasteryApi:
    def __init__(
        self,
        async_api: LolChampionMasteryApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_all_champion_masteries_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> List[ChampionMastery]:
        return cast(
            List[ChampionMastery],
            self._run(
                self._async_api.get_all_champion_masteries_by_puuid(
                    encrypted_puuid=encrypted_puuid,
                    route=route,
                )
            ),
        )

    def get_champion_mastery_by_puuid(
        self,
        *,
        champion_id: int,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> ChampionMastery:
        return cast(
            ChampionMastery,
            self._run(
                self._async_api.get_champion_mastery_by_puuid(
                    champion_id=champion_id,
                    encrypted_puuid=encrypted_puuid,
                    route=route,
                )
            ),
        )

    def get_top_champion_masteries_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        count: Optional[int] = None,
        route: PlatformRoute | str | None = None,
    ) -> List[ChampionMastery]:
        return cast(
            List[ChampionMastery],
            self._run(
                self._async_api.get_top_champion_masteries_by_puuid(
                    encrypted_puuid=encrypted_puuid,
                    count=count,
                    route=route,
                )
            ),
        )

    def get_champion_mastery_score_by_puuid(
        self,
        *,
        encrypted_puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> int:
        return cast(
            int,
            self._run(
                self._async_api.get_champion_mastery_score_by_puuid(
                    encrypted_puuid=encrypted_puuid,
                    route=route,
                )
            ),
        )

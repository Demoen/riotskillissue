from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, List, Literal, Optional, cast
from urllib.parse import quote

from pydantic import TypeAdapter
from riotskillissue.core.http import HttpClient
from riotskillissue.core.types import PlatformRoute, RouteKind
from riotskillissue.models.lol.challenges_v1 import ApexPlayerInfo, ChallengeConfigInfo, PlayerInfo

_GET_ALL_CHALLENGE_CONFIGS_RESPONSE_ADAPTER = TypeAdapter(List[ChallengeConfigInfo]).validate_python
_GET_ALL_CHALLENGE_PERCENTILES_RESPONSE_ADAPTER = TypeAdapter(
    Dict[str, Dict[str, float]]
).validate_python
_GET_CHALLENGE_CONFIGS_RESPONSE_ADAPTER = TypeAdapter(ChallengeConfigInfo).validate_python
_GET_CHALLENGE_LEADERBOARDS_RESPONSE_ADAPTER = TypeAdapter(List[ApexPlayerInfo]).validate_python
_GET_CHALLENGE_PERCENTILES_RESPONSE_ADAPTER = TypeAdapter(Dict[str, float]).validate_python
_GET_PLAYER_DATA_RESPONSE_ADAPTER = TypeAdapter(PlayerInfo).validate_python


class LolChallengesApi:
    def __init__(self, http: HttpClient) -> None:
        self.http = http

    async def get_all_challenge_configs(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> List[ChallengeConfigInfo]:
        "List of all basic challenge configuration information (includes all translations…"
        path = "/lol/challenges/v1/challenges/config"
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
                "pbe1",
                "ru",
                "sg2",
                "tr1",
                "tw2",
                "vn2",
            ),
        )
        return cast(
            List[ChallengeConfigInfo],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lol-challenges-v1.getAllChallengeConfigs",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_ALL_CHALLENGE_CONFIGS_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_all_challenge_percentiles(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Dict[str, Dict[str, float]]:
        "Map of level to percentile of players who have achieved it - keys: ChallengeId ->…"
        path = "/lol/challenges/v1/challenges/percentiles"
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
                "pbe1",
                "ru",
                "sg2",
                "tr1",
                "tw2",
                "vn2",
            ),
        )
        return cast(
            Dict[str, Dict[str, float]],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lol-challenges-v1.getAllChallengePercentiles",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_ALL_CHALLENGE_PERCENTILES_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_challenge_configs(
        self,
        *,
        challenge_id: int,
        route: PlatformRoute | str | None = None,
    ) -> ChallengeConfigInfo:
        "Get challenge configuration (REST)"
        path = "".join(("/lol/challenges/v1/challenges/{challengeId}/co", "nfig"))
        path = path.replace(
            "{challengeId}",
            quote(str(challenge_id), safe=""),
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
                "pbe1",
                "ru",
                "sg2",
                "tr1",
                "tw2",
                "vn2",
            ),
        )
        return cast(
            ChallengeConfigInfo,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lol-challenges-v1.getChallengeConfigs",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CHALLENGE_CONFIGS_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_challenge_leaderboards(
        self,
        *,
        challenge_id: int,
        level: Literal[
            "NONE",
            "IRON",
            "BRONZE",
            "SILVER",
            "GOLD",
            "PLATINUM",
            "DIAMOND",
            "MASTER",
            "GRANDMASTER",
            "CHALLENGER",
            "HIGHEST_NOT_LEADERBOARD_ONLY",
            "HIGHEST",
            "LOWEST",
        ],
        limit: Optional[int] = None,
        route: PlatformRoute | str | None = None,
    ) -> List[ApexPlayerInfo]:
        "Return top players for each level. Level must be MASTER, GRANDMASTER or CHALLENGER."
        path = "".join(
            ("/lol/challenges/v1/challenges/{challengeId}/le", "aderboards/by-level/{level}")
        )
        path = path.replace(
            "{challengeId}",
            quote(str(challenge_id), safe=""),
        )
        path = path.replace(
            "{level}",
            quote(str(level), safe=""),
        )
        params: dict[str, Any] = {
            "limit": limit,
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
                "pbe1",
                "ru",
                "sg2",
                "tr1",
                "tw2",
                "vn2",
            ),
        )
        return cast(
            List[ApexPlayerInfo],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lol-challenges-v1.getChallengeLeaderboards",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CHALLENGE_LEADERBOARDS_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_challenge_percentiles(
        self,
        *,
        challenge_id: int,
        route: PlatformRoute | str | None = None,
    ) -> Dict[str, float]:
        "Map of level to percentile of players who have achieved it"
        path = "".join(("/lol/challenges/v1/challenges/{challengeId}/pe", "rcentiles"))
        path = path.replace(
            "{challengeId}",
            quote(str(challenge_id), safe=""),
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
                "pbe1",
                "ru",
                "sg2",
                "tr1",
                "tw2",
                "vn2",
            ),
        )
        return cast(
            Dict[str, float],
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lol-challenges-v1.getChallengePercentiles",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_CHALLENGE_PERCENTILES_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )

    async def get_player_data(
        self,
        *,
        puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> PlayerInfo:
        "Returns player information with list of all progressed challenges (REST)"
        path = "/lol/challenges/v1/player-data/{puuid}"
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
                "pbe1",
                "ru",
                "sg2",
                "tr1",
                "tw2",
                "vn2",
            ),
        )
        return cast(
            PlayerInfo,
            await self.http.request(
                method="GET",
                url=path,
                region_or_platform=resolved_route,
                operation_id="lol-challenges-v1.getPlayerData",
                auth_mode="api_key",
                cache_user_scoped=False,
                successful_statuses=(200,),
                no_content_statuses=(),
                response_adapter=_GET_PLAYER_DATA_RESPONSE_ADAPTER,
                **request_kwargs,
            ),
        )


class SyncLolChallengesApi:
    def __init__(
        self,
        async_api: LolChallengesApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_api = async_api
        self._run = runner

    def get_all_challenge_configs(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> List[ChallengeConfigInfo]:
        return cast(
            List[ChallengeConfigInfo],
            self._run(
                self._async_api.get_all_challenge_configs(
                    route=route,
                )
            ),
        )

    def get_all_challenge_percentiles(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Dict[str, Dict[str, float]]:
        return cast(
            Dict[str, Dict[str, float]],
            self._run(
                self._async_api.get_all_challenge_percentiles(
                    route=route,
                )
            ),
        )

    def get_challenge_configs(
        self,
        *,
        challenge_id: int,
        route: PlatformRoute | str | None = None,
    ) -> ChallengeConfigInfo:
        return cast(
            ChallengeConfigInfo,
            self._run(
                self._async_api.get_challenge_configs(
                    challenge_id=challenge_id,
                    route=route,
                )
            ),
        )

    def get_challenge_leaderboards(
        self,
        *,
        challenge_id: int,
        level: Literal[
            "NONE",
            "IRON",
            "BRONZE",
            "SILVER",
            "GOLD",
            "PLATINUM",
            "DIAMOND",
            "MASTER",
            "GRANDMASTER",
            "CHALLENGER",
            "HIGHEST_NOT_LEADERBOARD_ONLY",
            "HIGHEST",
            "LOWEST",
        ],
        limit: Optional[int] = None,
        route: PlatformRoute | str | None = None,
    ) -> List[ApexPlayerInfo]:
        return cast(
            List[ApexPlayerInfo],
            self._run(
                self._async_api.get_challenge_leaderboards(
                    challenge_id=challenge_id,
                    level=level,
                    limit=limit,
                    route=route,
                )
            ),
        )

    def get_challenge_percentiles(
        self,
        *,
        challenge_id: int,
        route: PlatformRoute | str | None = None,
    ) -> Dict[str, float]:
        return cast(
            Dict[str, float],
            self._run(
                self._async_api.get_challenge_percentiles(
                    challenge_id=challenge_id,
                    route=route,
                )
            ),
        )

    def get_player_data(
        self,
        *,
        puuid: str,
        route: PlatformRoute | str | None = None,
    ) -> PlayerInfo:
        return cast(
            PlayerInfo,
            self._run(
                self._async_api.get_player_data(
                    puuid=puuid,
                    route=route,
                )
            ),
        )

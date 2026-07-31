from __future__ import annotations

import asyncio
from typing import Any, Literal

from riotskillissue.core.types import (
    Game,
    PlatformRoute,
    RegionalRoute,
    ValorantRoute,
)
from riotskillissue.services.base import (
    RawOperations,
    WorkflowService,
    _field,
    account_puuid,
    history_match_ids,
    platform_route,
    regional_from_platform,
    regional_from_valorant,
    regional_route,
    summary_from_match,
    valorant_route,
)
from riotskillissue.services.models import MatchSummary, PlayerProfile
from riotskillissue.static import DataDragonClient


def _history_count(count: int) -> int:
    if count < 1 or count > 20:
        raise ValueError("count must be between 1 and 20")
    return count


async def _match_summaries(
    game: Game,
    match_ids: list[str],
    puuid: str,
    fetch: Any,
    *,
    concurrency: int,
) -> list[MatchSummary]:
    semaphore = asyncio.Semaphore(concurrency)

    async def load(match_id: str) -> MatchSummary:
        async with semaphore:
            match = await fetch(match_id)
        return summary_from_match(game, match, puuid)

    results = await asyncio.gather(
        *(load(match_id) for match_id in match_ids),
        return_exceptions=True,
    )
    return [item for item in results if isinstance(item, MatchSummary)]


class LolService(WorkflowService):
    def __init__(self, raw: RawOperations, static: DataDragonClient) -> None:
        super().__init__(raw)
        self.static = static

    async def player_profile(
        self,
        riot_id: str,
        *,
        route: PlatformRoute | str | None = None,
    ) -> PlayerProfile:
        platform = platform_route(route)
        return await self._profile(
            Game.LOL,
            riot_id,
            account_route=regional_from_platform(platform),
            profile_operation="summoner-v4.getByPUUID",
            profile_arguments={"route": platform},
            profile_identity_argument="encrypted_puuid",
        )

    async def match_ids(
        self,
        riot_id: str,
        *,
        count: int = 20,
        start: int = 0,
        start_time: int | None = None,
        end_time: int | None = None,
        queue: int | None = None,
        match_type: Literal["ranked", "normal", "tourney", "tutorial"] | None = None,
        route: PlatformRoute | str | None = None,
    ) -> list[str]:
        if count < 1 or count > 100:
            raise ValueError("count must be between 1 and 100")
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        result = await self._call(
            "match-v5.getMatchIdsByPUUID",
            puuid=puuid,
            count=count,
            start=start,
            start_time=start_time,
            end_time=end_time,
            queue=queue,
            type=match_type,
            route=regional_from_platform(platform),
        )
        return history_match_ids(result)

    async def match_history(
        self,
        riot_id: str,
        *,
        count: int = 5,
        start_time: int | None = None,
        end_time: int | None = None,
        queue: int | None = None,
        match_type: Literal["ranked", "normal", "tourney", "tutorial"] | None = None,
        route: PlatformRoute | str | None = None,
        concurrency: int = 5,
    ) -> list[MatchSummary]:
        count = _history_count(count)
        if concurrency < 1:
            raise ValueError("concurrency must be positive")
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        result = await self._call(
            "match-v5.getMatchIdsByPUUID",
            puuid=puuid,
            count=count,
            start=0,
            start_time=start_time,
            end_time=end_time,
            queue=queue,
            type=match_type,
            route=regional_from_platform(platform),
        )
        ids = history_match_ids(result)[:count]

        async def fetch(match_id: str) -> Any:
            return await self._call(
                "match-v5.getMatch",
                match_id=match_id,
                route=regional_from_platform(platform),
            )

        return await _match_summaries(
            Game.LOL,
            ids,
            puuid,
            fetch,
            concurrency=concurrency,
        )

    async def ranked_entries(
        self,
        riot_id: str,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        return await self._call(
            "league-v4.getLeagueEntriesByPUUID",
            encrypted_puuid=puuid,
            route=platform,
        )

    async def live_game(
        self,
        riot_id: str,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        return await self._call(
            "spectator-v5.getCurrentGameInfoByPuuid",
            encrypted_puuid=puuid,
            route=platform,
        )

    async def champion_mastery(
        self,
        riot_id: str,
        *,
        champion_id: int | None = None,
        count: int | None = None,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        if count is not None and count < 1:
            raise ValueError("count must be positive")
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        if champion_id is not None:
            return await self._call(
                "champion-mastery-v4.getChampionMasteryByPUUID",
                encrypted_puuid=puuid,
                champion_id=champion_id,
                route=platform,
            )
        if count is not None:
            return await self._call(
                "champion-mastery-v4.getTopChampionMasteriesByPUUID",
                encrypted_puuid=puuid,
                count=count,
                route=platform,
            )
        return await self._call(
            "champion-mastery-v4.getAllChampionMasteriesByPUUID",
            encrypted_puuid=puuid,
            route=platform,
        )

    async def challenges(
        self,
        riot_id: str,
        *,
        challenge_id: int | None = None,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        data = await self._call(
            "lol-challenges-v1.getPlayerData",
            puuid=puuid,
            route=platform,
        )
        if challenge_id is None:
            return data
        for challenge in _field(data, "challenges", default=[]) or []:
            if _field(challenge, "challenge_id", "challengeId") == challenge_id:
                return challenge
        return None

    async def status(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        return await self._call(
            "lol-status-v4.getPlatformData",
            route=platform_route(route),
        )


class TftService(WorkflowService):
    async def profile(
        self,
        riot_id: str,
        *,
        route: PlatformRoute | str | None = None,
    ) -> PlayerProfile:
        platform = platform_route(route)
        return await self._profile(
            Game.TFT,
            riot_id,
            account_route=regional_from_platform(platform),
            profile_operation="tft-summoner-v1.getByPUUID",
            profile_arguments={"route": platform},
            profile_identity_argument="encrypted_puuid",
        )

    async def match_ids(
        self,
        riot_id: str,
        *,
        count: int = 20,
        start: int = 0,
        start_time: int | None = None,
        end_time: int | None = None,
        route: PlatformRoute | str | None = None,
    ) -> list[str]:
        if count < 1 or count > 100:
            raise ValueError("count must be between 1 and 100")
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        result = await self._call(
            "tft-match-v1.getMatchIdsByPUUID",
            puuid=puuid,
            count=count,
            start=start,
            start_time=start_time,
            end_time=end_time,
            route=regional_from_platform(platform),
        )
        return history_match_ids(result)

    async def match_history(
        self,
        riot_id: str,
        *,
        count: int = 5,
        start_time: int | None = None,
        end_time: int | None = None,
        route: PlatformRoute | str | None = None,
        concurrency: int = 5,
    ) -> list[MatchSummary]:
        count = _history_count(count)
        if concurrency < 1:
            raise ValueError("concurrency must be positive")
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        result = await self._call(
            "tft-match-v1.getMatchIdsByPUUID",
            puuid=puuid,
            count=count,
            start=0,
            start_time=start_time,
            end_time=end_time,
            route=regional_from_platform(platform),
        )
        ids = history_match_ids(result)[:count]

        async def fetch(match_id: str) -> Any:
            return await self._call(
                "tft-match-v1.getMatch",
                match_id=match_id,
                route=regional_from_platform(platform),
            )

        return await _match_summaries(
            Game.TFT,
            ids,
            puuid,
            fetch,
            concurrency=concurrency,
        )

    async def ranked_entries(
        self,
        riot_id: str,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        return await self._call(
            "tft-league-v1.getLeagueEntriesByPUUID",
            puuid=puuid,
            route=platform,
        )

    async def live_game(
        self,
        riot_id: str,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        platform = platform_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_platform(platform),
        )
        return await self._call(
            "spectator-tft-v5.getCurrentGameInfoByPuuid",
            encrypted_puuid=puuid,
            route=platform,
        )

    async def status(
        self,
        *,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        return await self._call(
            "tft-status-v1.getPlatformData",
            route=platform_route(route),
        )


class ValorantService(WorkflowService):
    async def profile(
        self,
        riot_id: str,
        *,
        route: ValorantRoute | str | None = None,
    ) -> PlayerProfile:
        cluster = valorant_route(route)
        return await self._profile(
            Game.VALORANT,
            riot_id,
            account_route=regional_from_valorant(cluster),
            profile_operation="account-v1.getActiveShard",
            profile_arguments={
                "game": "val",
                "route": regional_from_valorant(cluster),
            },
        )

    async def active_shard(
        self,
        riot_id: str,
        *,
        route: ValorantRoute | str | None = None,
    ) -> Any:
        return (
            await self.profile(riot_id, route=route)
        ).game_profile

    async def match_ids(
        self,
        riot_id: str,
        *,
        count: int = 20,
        route: ValorantRoute | str | None = None,
    ) -> list[str]:
        if count < 1 or count > 100:
            raise ValueError("count must be between 1 and 100")
        cluster = valorant_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_valorant(cluster),
        )
        history = await self._call(
            "val-match-v1.getMatchlist",
            puuid=puuid,
            route=cluster,
        )
        return history_match_ids(history)[:count]

    async def match_history(
        self,
        riot_id: str,
        *,
        count: int = 5,
        route: ValorantRoute | str | None = None,
        concurrency: int = 5,
    ) -> list[MatchSummary]:
        count = _history_count(count)
        if concurrency < 1:
            raise ValueError("concurrency must be positive")
        cluster = valorant_route(route)
        _, puuid = await account_puuid(
            self,
            riot_id,
            route=regional_from_valorant(cluster),
        )
        history = await self._call(
            "val-match-v1.getMatchlist",
            puuid=puuid,
            route=cluster,
        )
        ids = history_match_ids(history)[:count]

        async def fetch(match_id: str) -> Any:
            return await self._call(
                "val-match-v1.getMatch",
                match_id=match_id,
                route=cluster,
            )

        return await _match_summaries(
            Game.VALORANT,
            ids,
            puuid,
            fetch,
            concurrency=concurrency,
        )

    async def recent_matches(
        self,
        queue: str,
        *,
        route: ValorantRoute | str | None = None,
    ) -> Any:
        return await self._call(
            "val-match-v1.getRecent",
            queue=queue,
            route=valorant_route(route),
        )

    async def leaderboard(
        self,
        *,
        act_id: str,
        size: int = 20,
        start_index: int = 0,
        route: ValorantRoute | str | None = None,
    ) -> Any:
        if size < 1 or size > 200:
            raise ValueError("size must be between 1 and 200")
        if start_index < 0:
            raise ValueError("start_index cannot be negative")
        return await self._call(
            "val-ranked-v1.getLeaderboard",
            act_id=act_id,
            size=size,
            start_index=start_index,
            route=valorant_route(route),
        )

    async def content(
        self,
        *,
        locale: str | None = None,
        route: ValorantRoute | str | None = None,
    ) -> Any:
        return await self._call(
            "val-content-v1.getContent",
            locale=locale,
            route=valorant_route(route),
        )

    async def status(
        self,
        *,
        route: ValorantRoute | str | None = None,
    ) -> Any:
        return await self._call(
            "val-status-v1.getPlatformData",
            route=valorant_route(route),
        )


class LorService(WorkflowService):
    async def profile(
        self,
        riot_id: str,
        *,
        route: RegionalRoute | str | None = None,
    ) -> PlayerProfile:
        regional = regional_route(route)
        return await self._profile(
            Game.LOR,
            riot_id,
            account_route=regional,
            profile_operation="account-v1.getActiveShard",
            profile_arguments={"game": "lor", "route": regional},
        )

    async def active_region(
        self,
        riot_id: str,
        *,
        route: RegionalRoute | str | None = None,
    ) -> Any:
        return (
            await self.profile(riot_id, route=route)
        ).game_profile

    async def match_ids(
        self,
        riot_id: str,
        *,
        count: int = 20,
        route: RegionalRoute | str | None = None,
    ) -> list[str]:
        if count < 1 or count > 100:
            raise ValueError("count must be between 1 and 100")
        regional = regional_route(route)
        _, puuid = await account_puuid(self, riot_id, route=regional)
        result = await self._call(
            "lor-match-v1.getMatchIdsByPUUID",
            puuid=puuid,
            route=regional,
        )
        return history_match_ids(result)[:count]

    async def match_history(
        self,
        riot_id: str,
        *,
        count: int = 5,
        route: RegionalRoute | str | None = None,
        concurrency: int = 5,
    ) -> list[MatchSummary]:
        count = _history_count(count)
        if concurrency < 1:
            raise ValueError("concurrency must be positive")
        regional = regional_route(route)
        _, puuid = await account_puuid(self, riot_id, route=regional)
        result = await self._call(
            "lor-match-v1.getMatchIdsByPUUID",
            puuid=puuid,
            route=regional,
        )
        ids = history_match_ids(result)[:count]

        async def fetch(match_id: str) -> Any:
            return await self._call(
                "lor-match-v1.getMatch",
                match_id=match_id,
                route=regional,
            )

        return await _match_summaries(
            Game.LOR,
            ids,
            puuid,
            fetch,
            concurrency=concurrency,
        )

    async def leaderboard(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> Any:
        return await self._call(
            "lor-ranked-v1.getLeaderboards",
            route=regional_route(route),
        )

    async def status(
        self,
        *,
        route: RegionalRoute | str | None = None,
    ) -> Any:
        return await self._call(
            "lor-status-v1.getPlatformData",
            route=regional_route(route),
        )


class RiftboundService(WorkflowService):
    async def content(
        self,
        *,
        locale: str | None = None,
        route: RegionalRoute | str | None = None,
    ) -> Any:
        return await self._call(
            "riftbound-content-v1.getContent",
            locale=locale,
            route=regional_route(route),
        )

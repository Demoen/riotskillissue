from __future__ import annotations

from typing import Any, Awaitable, Callable, Mapping

from riotskillissue.api.registry import OPERATION_REGISTRY
from riotskillissue.core.http import HttpClient
from riotskillissue.api.raw.common.account import (
    CommonAccountApi,
    SyncCommonAccountApi,
)
from riotskillissue.api.raw.lol.challenges import (
    LolChallengesApi,
    SyncLolChallengesApi,
)
from riotskillissue.api.raw.lol.champion import (
    LolChampionApi,
    SyncLolChampionApi,
)
from riotskillissue.api.raw.lol.champion_mastery import (
    LolChampionMasteryApi,
    SyncLolChampionMasteryApi,
)
from riotskillissue.api.raw.lol.clash import (
    LolClashApi,
    SyncLolClashApi,
)
from riotskillissue.api.raw.lol.league import (
    LolLeagueApi,
    SyncLolLeagueApi,
)
from riotskillissue.api.raw.lol.league_exp import (
    LolLeagueExpApi,
    SyncLolLeagueExpApi,
)
from riotskillissue.api.raw.lol.match import (
    LolMatchApi,
    SyncLolMatchApi,
)
from riotskillissue.api.raw.lol.rso_match import (
    LolRsoMatchApi,
    SyncLolRsoMatchApi,
)
from riotskillissue.api.raw.lol.spectator import (
    LolSpectatorApi,
    SyncLolSpectatorApi,
)
from riotskillissue.api.raw.lol.status import (
    LolStatusApi,
    SyncLolStatusApi,
)
from riotskillissue.api.raw.lol.summoner import (
    LolSummonerApi,
    SyncLolSummonerApi,
)
from riotskillissue.api.raw.lol.tournament import (
    LolTournamentApi,
    SyncLolTournamentApi,
)
from riotskillissue.api.raw.lol.tournament_stub import (
    LolTournamentStubApi,
    SyncLolTournamentStubApi,
)
from riotskillissue.api.raw.tft.league import (
    TftLeagueApi,
    SyncTftLeagueApi,
)
from riotskillissue.api.raw.tft.match import (
    TftMatchApi,
    SyncTftMatchApi,
)
from riotskillissue.api.raw.tft.spectator import (
    TftSpectatorApi,
    SyncTftSpectatorApi,
)
from riotskillissue.api.raw.tft.status import (
    TftStatusApi,
    SyncTftStatusApi,
)
from riotskillissue.api.raw.tft.summoner import (
    TftSummonerApi,
    SyncTftSummonerApi,
)
from riotskillissue.api.raw.valorant.console_match import (
    ValorantConsoleMatchApi,
    SyncValorantConsoleMatchApi,
)
from riotskillissue.api.raw.valorant.console_ranked import (
    ValorantConsoleRankedApi,
    SyncValorantConsoleRankedApi,
)
from riotskillissue.api.raw.valorant.content import (
    ValorantContentApi,
    SyncValorantContentApi,
)
from riotskillissue.api.raw.valorant.match import (
    ValorantMatchApi,
    SyncValorantMatchApi,
)
from riotskillissue.api.raw.valorant.ranked import (
    ValorantRankedApi,
    SyncValorantRankedApi,
)
from riotskillissue.api.raw.valorant.status import (
    ValorantStatusApi,
    SyncValorantStatusApi,
)
from riotskillissue.api.raw.lor.deck import (
    LorDeckApi,
    SyncLorDeckApi,
)
from riotskillissue.api.raw.lor.inventory import (
    LorInventoryApi,
    SyncLorInventoryApi,
)
from riotskillissue.api.raw.lor.match import (
    LorMatchApi,
    SyncLorMatchApi,
)
from riotskillissue.api.raw.lor.ranked import (
    LorRankedApi,
    SyncLorRankedApi,
)
from riotskillissue.api.raw.lor.status import (
    LorStatusApi,
    SyncLorStatusApi,
)
from riotskillissue.api.raw.riftbound.content import (
    RiftboundContentApi,
    SyncRiftboundContentApi,
)


class CommonRawApi:
    def __init__(self, http: HttpClient) -> None:
        self.account = CommonAccountApi(http)


class SyncCommonRawApi:
    def __init__(
        self,
        async_api: CommonRawApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self.account = SyncCommonAccountApi(
            async_api.account,
            runner,
        )


class LolRawApi:
    def __init__(self, http: HttpClient) -> None:
        self.challenges = LolChallengesApi(http)
        self.champion = LolChampionApi(http)
        self.champion_mastery = LolChampionMasteryApi(http)
        self.clash = LolClashApi(http)
        self.league = LolLeagueApi(http)
        self.league_exp = LolLeagueExpApi(http)
        self.match = LolMatchApi(http)
        self.rso_match = LolRsoMatchApi(http)
        self.spectator = LolSpectatorApi(http)
        self.status = LolStatusApi(http)
        self.summoner = LolSummonerApi(http)
        self.tournament = LolTournamentApi(http)
        self.tournament_stub = LolTournamentStubApi(http)


class SyncLolRawApi:
    def __init__(
        self,
        async_api: LolRawApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self.challenges = SyncLolChallengesApi(
            async_api.challenges,
            runner,
        )
        self.champion = SyncLolChampionApi(
            async_api.champion,
            runner,
        )
        self.champion_mastery = SyncLolChampionMasteryApi(
            async_api.champion_mastery,
            runner,
        )
        self.clash = SyncLolClashApi(
            async_api.clash,
            runner,
        )
        self.league = SyncLolLeagueApi(
            async_api.league,
            runner,
        )
        self.league_exp = SyncLolLeagueExpApi(
            async_api.league_exp,
            runner,
        )
        self.match = SyncLolMatchApi(
            async_api.match,
            runner,
        )
        self.rso_match = SyncLolRsoMatchApi(
            async_api.rso_match,
            runner,
        )
        self.spectator = SyncLolSpectatorApi(
            async_api.spectator,
            runner,
        )
        self.status = SyncLolStatusApi(
            async_api.status,
            runner,
        )
        self.summoner = SyncLolSummonerApi(
            async_api.summoner,
            runner,
        )
        self.tournament = SyncLolTournamentApi(
            async_api.tournament,
            runner,
        )
        self.tournament_stub = SyncLolTournamentStubApi(
            async_api.tournament_stub,
            runner,
        )


class TftRawApi:
    def __init__(self, http: HttpClient) -> None:
        self.league = TftLeagueApi(http)
        self.match = TftMatchApi(http)
        self.spectator = TftSpectatorApi(http)
        self.status = TftStatusApi(http)
        self.summoner = TftSummonerApi(http)


class SyncTftRawApi:
    def __init__(
        self,
        async_api: TftRawApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self.league = SyncTftLeagueApi(
            async_api.league,
            runner,
        )
        self.match = SyncTftMatchApi(
            async_api.match,
            runner,
        )
        self.spectator = SyncTftSpectatorApi(
            async_api.spectator,
            runner,
        )
        self.status = SyncTftStatusApi(
            async_api.status,
            runner,
        )
        self.summoner = SyncTftSummonerApi(
            async_api.summoner,
            runner,
        )


class ValorantRawApi:
    def __init__(self, http: HttpClient) -> None:
        self.console_match = ValorantConsoleMatchApi(http)
        self.console_ranked = ValorantConsoleRankedApi(http)
        self.content = ValorantContentApi(http)
        self.match = ValorantMatchApi(http)
        self.ranked = ValorantRankedApi(http)
        self.status = ValorantStatusApi(http)


class SyncValorantRawApi:
    def __init__(
        self,
        async_api: ValorantRawApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self.console_match = SyncValorantConsoleMatchApi(
            async_api.console_match,
            runner,
        )
        self.console_ranked = SyncValorantConsoleRankedApi(
            async_api.console_ranked,
            runner,
        )
        self.content = SyncValorantContentApi(
            async_api.content,
            runner,
        )
        self.match = SyncValorantMatchApi(
            async_api.match,
            runner,
        )
        self.ranked = SyncValorantRankedApi(
            async_api.ranked,
            runner,
        )
        self.status = SyncValorantStatusApi(
            async_api.status,
            runner,
        )


class LorRawApi:
    def __init__(self, http: HttpClient) -> None:
        self.deck = LorDeckApi(http)
        self.inventory = LorInventoryApi(http)
        self.match = LorMatchApi(http)
        self.ranked = LorRankedApi(http)
        self.status = LorStatusApi(http)


class SyncLorRawApi:
    def __init__(
        self,
        async_api: LorRawApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self.deck = SyncLorDeckApi(
            async_api.deck,
            runner,
        )
        self.inventory = SyncLorInventoryApi(
            async_api.inventory,
            runner,
        )
        self.match = SyncLorMatchApi(
            async_api.match,
            runner,
        )
        self.ranked = SyncLorRankedApi(
            async_api.ranked,
            runner,
        )
        self.status = SyncLorStatusApi(
            async_api.status,
            runner,
        )


class RiftboundRawApi:
    def __init__(self, http: HttpClient) -> None:
        self.content = RiftboundContentApi(http)


class SyncRiftboundRawApi:
    def __init__(
        self,
        async_api: RiftboundRawApi,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self.content = SyncRiftboundContentApi(
            async_api.content,
            runner,
        )


class GeneratedRawClient:
    def __init__(self, http: HttpClient) -> None:
        self.common = CommonRawApi(http)
        self.lol = LolRawApi(http)
        self.tft = TftRawApi(http)
        self.valorant = ValorantRawApi(http)
        self.lor = LorRawApi(http)
        self.riftbound = RiftboundRawApi(http)

    async def call_operation(
        self,
        operation: str,
        arguments: Mapping[str, Any],
    ) -> Any:
        spec = OPERATION_REGISTRY[operation]
        if spec.source != "riot_api":
            raise ValueError(f"{operation!r} is not a raw Riot API operation")
        target: Any = self
        for segment in spec.accessor_path.split("."):
            target = getattr(target, segment)
        return await target(**dict(arguments))


class SyncGeneratedRawClient:
    def __init__(
        self,
        async_raw: GeneratedRawClient,
        runner: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._async_raw = async_raw
        self._run = runner
        self.common = SyncCommonRawApi(
            async_raw.common,
            runner,
        )
        self.lol = SyncLolRawApi(
            async_raw.lol,
            runner,
        )
        self.tft = SyncTftRawApi(
            async_raw.tft,
            runner,
        )
        self.valorant = SyncValorantRawApi(
            async_raw.valorant,
            runner,
        )
        self.lor = SyncLorRawApi(
            async_raw.lor,
            runner,
        )
        self.riftbound = SyncRiftboundRawApi(
            async_raw.riftbound,
            runner,
        )

    def call_operation(
        self,
        operation: str,
        arguments: Mapping[str, Any],
    ) -> Any:
        return self._run(self._async_raw.call_operation(operation, arguments))

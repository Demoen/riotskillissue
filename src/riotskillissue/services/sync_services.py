from __future__ import annotations

from collections.abc import Awaitable
from typing import Any, Literal, Protocol, TypeVar

from riotskillissue.core.types import PlatformRoute, RegionalRoute, ValorantRoute
from riotskillissue.services.async_services import (
    LolService,
    LorService,
    RiftboundService,
    TftService,
    ValorantService,
)
from riotskillissue.services.models import MatchSummary, PlayerProfile
from riotskillissue.static import SyncDataDragonClient

T = TypeVar("T")


class Runner(Protocol):
    def __call__(self, awaitable: Awaitable[T]) -> T: ...


class SyncLolService:
    def __init__(
        self,
        service: LolService,
        run: Runner,
        static: SyncDataDragonClient,
    ) -> None:
        self._service = service
        self._run = run
        self.static = static

    def player_profile(
        self, riot_id: str, *, route: PlatformRoute | str | None = None
    ) -> PlayerProfile:
        return self._run(self._service.player_profile(riot_id, route=route))

    def match_ids(
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
        return self._run(
            self._service.match_ids(
                riot_id,
                count=count,
                start=start,
                start_time=start_time,
                end_time=end_time,
                queue=queue,
                match_type=match_type,
                route=route,
            )
        )

    def match_history(
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
        return self._run(
            self._service.match_history(
                riot_id,
                count=count,
                start_time=start_time,
                end_time=end_time,
                queue=queue,
                match_type=match_type,
                route=route,
                concurrency=concurrency,
            )
        )

    def ranked_entries(
        self, riot_id: str, *, route: PlatformRoute | str | None = None
    ) -> Any:
        return self._run(self._service.ranked_entries(riot_id, route=route))

    def live_game(
        self, riot_id: str, *, route: PlatformRoute | str | None = None
    ) -> Any:
        return self._run(self._service.live_game(riot_id, route=route))

    def champion_mastery(
        self,
        riot_id: str,
        *,
        champion_id: int | None = None,
        count: int | None = None,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        return self._run(
            self._service.champion_mastery(
                riot_id,
                champion_id=champion_id,
                count=count,
                route=route,
            )
        )

    def challenges(
        self,
        riot_id: str,
        *,
        challenge_id: int | None = None,
        route: PlatformRoute | str | None = None,
    ) -> Any:
        return self._run(
            self._service.challenges(
                riot_id,
                challenge_id=challenge_id,
                route=route,
            )
        )

    def status(self, *, route: PlatformRoute | str | None = None) -> Any:
        return self._run(self._service.status(route=route))


class SyncTftService:
    def __init__(self, service: TftService, run: Runner) -> None:
        self._service = service
        self._run = run

    def profile(
        self, riot_id: str, *, route: PlatformRoute | str | None = None
    ) -> PlayerProfile:
        return self._run(self._service.profile(riot_id, route=route))

    def match_ids(
        self,
        riot_id: str,
        *,
        count: int = 20,
        start: int = 0,
        start_time: int | None = None,
        end_time: int | None = None,
        route: PlatformRoute | str | None = None,
    ) -> list[str]:
        return self._run(
            self._service.match_ids(
                riot_id,
                count=count,
                start=start,
                start_time=start_time,
                end_time=end_time,
                route=route,
            )
        )

    def match_history(
        self,
        riot_id: str,
        *,
        count: int = 5,
        start_time: int | None = None,
        end_time: int | None = None,
        route: PlatformRoute | str | None = None,
        concurrency: int = 5,
    ) -> list[MatchSummary]:
        return self._run(
            self._service.match_history(
                riot_id,
                count=count,
                start_time=start_time,
                end_time=end_time,
                route=route,
                concurrency=concurrency,
            )
        )

    def ranked_entries(
        self, riot_id: str, *, route: PlatformRoute | str | None = None
    ) -> Any:
        return self._run(self._service.ranked_entries(riot_id, route=route))

    def live_game(
        self, riot_id: str, *, route: PlatformRoute | str | None = None
    ) -> Any:
        return self._run(self._service.live_game(riot_id, route=route))

    def status(self, *, route: PlatformRoute | str | None = None) -> Any:
        return self._run(self._service.status(route=route))


class SyncValorantService:
    def __init__(
        self,
        service: ValorantService,
        run: Runner,
    ) -> None:
        self._service = service
        self._run = run

    def profile(
        self, riot_id: str, *, route: ValorantRoute | str | None = None
    ) -> PlayerProfile:
        return self._run(self._service.profile(riot_id, route=route))

    def active_shard(
        self,
        riot_id: str,
        *,
        route: ValorantRoute | str | None = None,
    ) -> Any:
        return self._run(self._service.active_shard(riot_id, route=route))

    def match_ids(
        self,
        riot_id: str,
        *,
        count: int = 20,
        route: ValorantRoute | str | None = None,
    ) -> list[str]:
        return self._run(
            self._service.match_ids(riot_id, count=count, route=route)
        )

    def match_history(
        self,
        riot_id: str,
        *,
        count: int = 5,
        route: ValorantRoute | str | None = None,
        concurrency: int = 5,
    ) -> list[MatchSummary]:
        return self._run(
            self._service.match_history(
                riot_id,
                count=count,
                route=route,
                concurrency=concurrency,
            )
        )

    def recent_matches(
        self,
        queue: str,
        *,
        route: ValorantRoute | str | None = None,
    ) -> Any:
        return self._run(self._service.recent_matches(queue, route=route))

    def leaderboard(
        self,
        *,
        act_id: str,
        size: int = 20,
        start_index: int = 0,
        route: ValorantRoute | str | None = None,
    ) -> Any:
        return self._run(
            self._service.leaderboard(
                act_id=act_id,
                size=size,
                start_index=start_index,
                route=route,
            )
        )

    def content(
        self,
        *,
        locale: str | None = None,
        route: ValorantRoute | str | None = None,
    ) -> Any:
        return self._run(self._service.content(locale=locale, route=route))

    def status(self, *, route: ValorantRoute | str | None = None) -> Any:
        return self._run(self._service.status(route=route))


class SyncLorService:
    def __init__(self, service: LorService, run: Runner) -> None:
        self._service = service
        self._run = run

    def profile(
        self, riot_id: str, *, route: RegionalRoute | str | None = None
    ) -> PlayerProfile:
        return self._run(self._service.profile(riot_id, route=route))

    def active_region(
        self,
        riot_id: str,
        *,
        route: RegionalRoute | str | None = None,
    ) -> Any:
        return self._run(self._service.active_region(riot_id, route=route))

    def match_ids(
        self,
        riot_id: str,
        *,
        count: int = 20,
        route: RegionalRoute | str | None = None,
    ) -> list[str]:
        return self._run(
            self._service.match_ids(riot_id, count=count, route=route)
        )

    def match_history(
        self,
        riot_id: str,
        *,
        count: int = 5,
        route: RegionalRoute | str | None = None,
        concurrency: int = 5,
    ) -> list[MatchSummary]:
        return self._run(
            self._service.match_history(
                riot_id,
                count=count,
                route=route,
                concurrency=concurrency,
            )
        )

    def leaderboard(self, *, route: RegionalRoute | str | None = None) -> Any:
        return self._run(self._service.leaderboard(route=route))

    def status(self, *, route: RegionalRoute | str | None = None) -> Any:
        return self._run(self._service.status(route=route))


class SyncRiftboundService:
    def __init__(
        self,
        service: RiftboundService,
        run: Runner,
    ) -> None:
        self._service = service
        self._run = run

    def content(
        self,
        *,
        locale: str | None = None,
        route: RegionalRoute | str | None = None,
    ) -> Any:
        return self._run(self._service.content(locale=locale, route=route))

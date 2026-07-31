from __future__ import annotations

import asyncio
from collections.abc import Mapping
from typing import Any

import pytest

from riotskillissue import (
    Game,
    PlatformRoute,
    RegionalRoute,
    RouteResolutionError,
    ValorantRoute,
)
from riotskillissue.services import (
    LolService,
    LorService,
    RiftboundService,
    TftService,
    ValorantService,
)
from riotskillissue.services.base import summary_from_match


class FakeRaw:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.active = 0
        self.max_active = 0

    async def call_operation(
        self,
        operation: str,
        arguments: Mapping[str, Any],
    ) -> Any:
        values = dict(arguments)
        self.calls.append((operation, values))
        if operation == "account-v1.getByRiotId":
            return {
                "puuid": "player-puuid",
                "gameName": values["game_name"],
                "tagLine": values["tag_line"],
            }
        if operation.endswith("getMatchIdsByPUUID"):
            return [f"MATCH_{index}" for index in range(values.get("count", 8))]
        if operation == "val-match-v1.getMatchlist":
            return {
                "history": [
                    {"matchId": f"VAL_{index}"}
                    for index in range(8)
                ]
            }
        if operation.endswith(".getMatch"):
            match_id = values["match_id"]
            self.active += 1
            self.max_active = max(self.max_active, self.active)
            await asyncio.sleep(0)
            self.active -= 1
            if match_id.endswith("_2"):
                raise RuntimeError("partial upstream failure")
            return {
                "metadata": {"matchId": match_id},
                "info": {
                    "game_start_timestamp": 1_700_000_000_000,
                    "game_duration": 1200,
                    "queue_id": 420,
                    "participants": [
                        {"puuid": "player-puuid", "win": True}
                    ],
                },
            }
        return {"operation": operation, "arguments": values}


@pytest.mark.asyncio
async def test_lol_profile_uses_account_and_platform_profile() -> None:
    raw = FakeRaw()
    service = LolService(raw, object())  # type: ignore[arg-type]

    profile = await service.player_profile(
        "Player#EUW",
        route=PlatformRoute.EUW1,
    )

    assert profile.puuid == "player-puuid"
    assert profile.riot_id == "Player#EUW"
    assert raw.calls == [
        (
            "account-v1.getByRiotId",
            {
                "game_name": "Player",
                "tag_line": "EUW",
                "route": RegionalRoute.EUROPE,
            },
        ),
        (
            "summoner-v4.getByPUUID",
            {
                "route": PlatformRoute.EUW1,
                "encrypted_puuid": "player-puuid",
            },
        ),
    ]


@pytest.mark.asyncio
async def test_lol_history_is_bounded_and_tolerates_partial_failure() -> None:
    raw = FakeRaw()
    service = LolService(raw, object())  # type: ignore[arg-type]

    history = await service.match_history(
        "Player#EUW",
        count=5,
        concurrency=2,
        route=PlatformRoute.EUW1,
    )

    assert [item.match_id for item in history] == [
        "MATCH_0",
        "MATCH_1",
        "MATCH_3",
        "MATCH_4",
    ]
    assert raw.max_active <= 2
    assert all(item.player["puuid"] == "player-puuid" for item in history)


@pytest.mark.asyncio
async def test_match_history_rejects_out_of_range_count() -> None:
    raw = FakeRaw()
    service = TftService(raw)

    with pytest.raises(ValueError, match="between 1 and 20"):
        await service.match_history("Player#EUW", count=21)


@pytest.mark.asyncio
async def test_workflow_rejects_wrong_route_family() -> None:
    service = TftService(FakeRaw())

    with pytest.raises(RouteResolutionError):
        await service.status(route="europe")


@pytest.mark.asyncio
async def test_tft_workflows_use_tft_operations() -> None:
    raw = FakeRaw()
    service = TftService(raw)

    profile = await service.profile("Player#EUW", route=PlatformRoute.EUW1)
    ranked = await service.ranked_entries(
        "Player#EUW",
        route=PlatformRoute.EUW1,
    )
    live = await service.live_game("Player#EUW", route=PlatformRoute.EUW1)
    status = await service.status(route=PlatformRoute.EUW1)

    assert profile.game.value == "tft"
    assert ranked["operation"] == "tft-league-v1.getLeagueEntriesByPUUID"
    assert live["operation"] == "spectator-tft-v5.getCurrentGameInfoByPuuid"
    assert status["operation"] == "tft-status-v1.getPlatformData"


@pytest.mark.asyncio
async def test_valorant_workflows_use_valorant_routing() -> None:
    raw = FakeRaw()
    service = ValorantService(raw)

    profile = await service.profile("Player#EUW", route=ValorantRoute.EU)
    history = await service.match_history(
        "Player#EUW",
        route=ValorantRoute.EU,
        count=3,
    )
    leaderboard = await service.leaderboard(
        act_id="act",
        route=ValorantRoute.EU,
    )
    recent = await service.recent_matches("competitive", route=ValorantRoute.EU)
    content = await service.content(locale="en-US", route=ValorantRoute.EU)
    status = await service.status(route=ValorantRoute.EU)

    assert profile.game.value == "valorant"
    assert [item.match_id for item in history] == ["VAL_0", "VAL_1"]
    assert leaderboard["operation"] == "val-ranked-v1.getLeaderboard"
    assert recent["operation"] == "val-match-v1.getRecent"
    assert content["operation"] == "val-content-v1.getContent"
    assert status["operation"] == "val-status-v1.getPlatformData"


@pytest.mark.asyncio
async def test_lor_and_riftbound_workflows() -> None:
    raw = FakeRaw()
    lor = LorService(raw)
    riftbound = RiftboundService(raw)

    profile = await lor.profile("Player#EUW", route=RegionalRoute.EUROPE)
    history = await lor.match_history(
        "Player#EUW",
        route=RegionalRoute.EUROPE,
        count=3,
    )
    leaderboard = await lor.leaderboard(route=RegionalRoute.EUROPE)
    status = await lor.status(route=RegionalRoute.EUROPE)
    content = await riftbound.content(
        locale="en_US",
        route=RegionalRoute.EUROPE,
    )

    assert profile.game.value == "lor"
    assert [item.match_id for item in history] == ["MATCH_0", "MATCH_1"]
    assert leaderboard["operation"] == "lor-ranked-v1.getLeaderboards"
    assert status["operation"] == "lor-status-v1.getPlatformData"
    assert content["operation"] == "riftbound-content-v1.getContent"


def test_player_summaries_cover_valorant_and_lor_shapes() -> None:
    valorant = summary_from_match(
        Game.VALORANT,
        {
            "matchInfo": {
                "matchId": "VAL_1",
                "gameStartMillis": 1_700_000_000_000,
                "gameLengthMillis": 900_000,
                "queueId": "competitive",
            },
            "players": [{"puuid": "p", "teamId": "Blue"}],
            "teams": [{"teamId": "Blue", "won": True}],
        },
        "p",
    )
    lor = summary_from_match(
        Game.LOR,
        {
            "metadata": {"match_id": "LOR_1"},
            "info": {
                "game_start_time_utc": "2026-07-31T08:00:00Z",
                "players": [{"puuid": "p", "game_outcome": "win"}],
            },
        },
        "p",
    )

    assert valorant.match_id == "VAL_1"
    assert valorant.duration_seconds == 900
    assert valorant.won is True
    assert lor.match_id == "LOR_1"
    assert lor.won is True
    assert lor.started_at is not None

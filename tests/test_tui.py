from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

pytest.importorskip("textual")

from rich.console import Console
from textual.widgets import Static

from riotskillissue import tui
from riotskillissue.core.http import NotFoundError


def participant(**values):
    return SimpleNamespace(
        **{
            "champion_id": 1,
            "puuid": "player-puuid",
            "riot_id": "Player#EUW",
            "team_id": 100,
            "spell1_id": 4,
            "spell2_id": 14,
            "bot": False,
            **values,
        }
    )


def mock_client(monkeypatch, *, players=None, bans=None, error=None):
    client = AsyncMock()
    client.__aenter__.return_value = client

    async def exit_client(*args):
        await client.close()

    client.__aexit__.side_effect = exit_client
    client.lol.live_game.return_value = SimpleNamespace(
        participants=players or [],
        banned_champions=bans or [],
    )
    client.lol.live_game.side_effect = error
    client.lol.static.get_champion.return_value = {"name": "Annie"}
    client.raw.lol.league.get_league_entries_by_puuid.return_value = []
    monkeypatch.setattr(tui, "RiotClient", Mock(return_value=client))
    return client


def snapshot(**values):
    return {
        "error": None,
        "player": "Player#EUW",
        "queue": "Ranked Solo/Duo",
        "blue_team": [],
        "red_team": [],
        "bans": [],
        **values,
    }


def rendered(widget):
    console = Console(width=160, color_system=None)
    with console.capture() as capture:
        console.print(widget.render())
    return capture.get()


async def test_optional_enrichment_failures_keep_players_and_report_unavailable(monkeypatch):
    client = mock_client(
        monkeypatch,
        players=[participant(), participant(team_id=200, puuid="red-puuid")],
        bans=[SimpleNamespace(champion_id=2)],
    )
    client.lol.static.get_champion.side_effect = RuntimeError("Static service down")
    client.raw.lol.league.get_league_entries_by_puuid.side_effect = RuntimeError("Rank service down")

    data = await tui.fetch_live_game_data("RGAPI-test", "Player", "EUW", "euw1")

    assert len(data["blue_team"]) == len(data["red_team"]) == 1
    assert data["blue_team"][0]["champion"] == "Champion 1"
    assert data["blue_team"][0]["rank_available"] is False
    assert data["bans"] == ["#2"]
    assert any("Champion data unavailable" in warning for warning in data["warnings"])
    assert any("Rank unavailable" in warning for warning in data["warnings"])
    assert any("Ban data unavailable" in warning for warning in data["warnings"])
    table = tui.TeamTable().build_table("Blue", data["blue_team"], "blue")
    console = Console(width=160)
    with console.capture() as capture:
        console.print(table)
    assert "Unavailable" in capture.get()


async def test_anonymous_players_and_bots_do_not_request_rank(monkeypatch):
    client = mock_client(
        monkeypatch,
        players=[participant(puuid=None), participant(bot=True, team_id=200)],
    )

    data = await tui.fetch_live_game_data("RGAPI-test", "Player", "EUW", "euw1")

    client.raw.lol.league.get_league_entries_by_puuid.assert_not_awaited()
    assert len(data["blue_team"]) == len(data["red_team"]) == 1
    assert data["blue_team"][0]["rank_available"] is False
    assert data["warnings"] == []


@pytest.mark.parametrize(
    ("path", "not_in_game"),
    [
        ("/lol/spectator/v5/active-games/by-summoner/puuid", True),
        ("/riot/account/v1/accounts/by-riot-id/Player/EUW", False),
    ],
)
async def test_only_spectator_not_found_enters_waiting_mode(monkeypatch, path, not_in_game):
    error = NotFoundError(httpx.Response(404, request=httpx.Request("GET", f"https://example.com{path}")))
    mock_client(monkeypatch, error=error)

    if not_in_game:
        data = await tui.fetch_live_game_data("RGAPI-test", "Player", "EUW", "euw1")
        assert data["error"] == "not_in_game"
    else:
        with pytest.raises(NotFoundError):
            await tui.fetch_live_game_data("RGAPI-test", "Player", "EUW", "euw1")


async def test_keyboard_remains_responsive_and_refreshes_do_not_overlap(monkeypatch):
    started = asyncio.Event()
    cancelled = asyncio.Event()
    client = mock_client(monkeypatch)

    async def close_client():
        assert cancelled.is_set()

    client.close.side_effect = close_client

    async def blocked_fetch(**kwargs):
        started.set()
        try:
            await asyncio.Event().wait()
        finally:
            cancelled.set()

    fetch = AsyncMock(side_effect=blocked_fetch)
    monkeypatch.setattr(tui, "fetch_live_game_data", fetch)
    app = tui.LiveGameApp("RGAPI-test", "Player", "EUW")

    async with asyncio.timeout(10), app.run_test() as pilot:
        await asyncio.wait_for(started.wait(), timeout=2)
        await pilot.press("r", "r")
        assert fetch.await_count == 1
        await pilot.press("q")

    await asyncio.wait_for(cancelled.wait(), timeout=2)
    client.close.assert_awaited_once()


@pytest.mark.parametrize("borrowed", [False, True])
@pytest.mark.parametrize("outcome", ["success", "error", "cancel"])
async def test_fetch_closes_only_owned_clients(monkeypatch, borrowed, outcome):
    client = mock_client(monkeypatch)
    started = asyncio.Event()

    async def blocked_game(*args, **kwargs):
        started.set()
        await asyncio.Event().wait()

    if outcome == "error":
        client.lol.live_game.side_effect = RuntimeError("Network unavailable")
    elif outcome == "cancel":
        client.lol.live_game.side_effect = blocked_game

    async with asyncio.timeout(10):
        task = asyncio.create_task(
            tui.fetch_live_game_data(
                "RGAPI-test", "Player", "EUW", "euw1",
                client=client if borrowed else None,
            )
        )
        if outcome == "cancel":
            await started.wait()
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
        elif outcome == "error":
            with pytest.raises(RuntimeError, match="Network unavailable"):
                await task
        else:
            await task

    if borrowed:
        tui.RiotClient.assert_not_called()
        client.__aenter__.assert_not_awaited()
        client.__aexit__.assert_not_awaited()
        client.close.assert_not_awaited()
    else:
        tui.RiotClient.assert_called_once()
        client.__aenter__.assert_awaited_once()
        client.__aexit__.assert_awaited_once()
        client.close.assert_awaited_once()


async def test_app_reuses_client_across_successful_and_failed_refreshes(monkeypatch):
    client = mock_client(monkeypatch)
    fetch = AsyncMock(side_effect=[snapshot(), RuntimeError("Network unavailable"), snapshot()])
    monkeypatch.setattr(tui, "fetch_live_game_data", fetch)
    app = tui.LiveGameApp("RGAPI-test", "Player", "EUW")

    async with app.run_test() as pilot:
        await app.workers.wait_for_complete()
        for _ in range(2):
            await pilot.press("r")
            await app.workers.wait_for_complete()
        assert fetch.await_count == 3
        assert all(call.kwargs["client"] is client for call in fetch.await_args_list)
        tui.RiotClient.assert_called_once()
        client.close.assert_not_awaited()

    client.close.assert_awaited_once()


async def test_failed_refresh_preserves_snapshot_and_recovers(monkeypatch):
    fetch = AsyncMock(
        side_effect=[
            snapshot(game_id=1),
            RuntimeError("Network failed with RGAPI-test"),
            snapshot(game_id=2),
        ]
    )
    monkeypatch.setattr(tui, "fetch_live_game_data", fetch)
    app = tui.LiveGameApp("RGAPI-test", "Player", "EUW")

    async with app.run_test() as pilot:
        await app.workers.wait_for_complete()
        await pilot.press("r")
        await app.workers.wait_for_complete()

        assert app.game_data["game_id"] == 1
        assert app.query("#game-header")
        status = rendered(app.query_one("#status-bar", Static))
        assert "Showing previous data" in status
        assert "RGAPI-test" not in status

        await pilot.press("r")
        await app.workers.wait_for_complete()
        assert app.game_data["game_id"] == 2
        assert app.last_error is None
        assert "Showing previous data" not in rendered(app.query_one("#status-bar", Static))


async def test_countdown_updates_status_and_refreshes_when_due(monkeypatch):
    fetch = AsyncMock(return_value=snapshot(warnings=["Rank unavailable for Player#EUW."]))
    monkeypatch.setattr(tui, "fetch_live_game_data", fetch)
    app = tui.LiveGameApp("RGAPI-test", "Player", "EUW", auto_refresh=5)

    async with app.run_test() as pilot:
        await app.workers.wait_for_complete()
        app._countdown_timer.pause()
        assert "Rank unavailable" in rendered(app.query_one("#warnings-widget", Static))
        app._tick_countdown()
        await pilot.pause()
        assert "Next refresh in 4s" in rendered(app.query_one("#status-bar", Static))

        for _ in range(4):
            app._tick_countdown()
        await app.workers.wait_for_complete()
        assert fetch.await_count == 2
        assert app.refresh_countdown == 5


@pytest.mark.parametrize("interval", [0, -1, 4])
def test_programmatic_refresh_interval_is_validated(interval):
    with pytest.raises(ValueError, match="at least 5 seconds"):
        tui.LiveGameApp("RGAPI-test", "Player", "EUW", auto_refresh=interval)

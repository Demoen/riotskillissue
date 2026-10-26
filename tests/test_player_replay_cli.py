from __future__ import annotations

import os
from pathlib import Path

import pytest
import respx
from typer.testing import CliRunner

from riotskillissue import cli
from riotskillissue.league_client import ClientReplay, LeagueClientError

runner = CliRunner()


@pytest.fixture
def local_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    for name in list(os.environ):
        if name.startswith("RIOT_"):
            monkeypatch.delenv(name)

    class LocalClient:
        instances = []
        error = None
        matches = [
            ClientReplay(index, game_id, "EUW1", "16.21.1", "MATCHED_GAME", 420, 1792000000000)
            for index, game_id in enumerate([123, 456], start=1)
        ]

        def __init__(self, lockfile=None):
            self.lockfile = lockfile
            self.list_calls = []
            self.download_calls = []
            self.closed = False
            self.instances.append(self)

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            self.closed = True

        async def player_replays(self, riot_id, *, count):
            self.list_calls.append((riot_id, count))
            return self.matches

        async def download_replay(self, replay, destination, *, overwrite, timeout):
            self.download_calls.append((replay, destination, overwrite, timeout))
            if self.error:
                raise self.error
            return destination or tmp_path / "League Replays" / replay.filename

    def unexpected_public_client(*args, **kwargs):
        raise AssertionError("Player mode must not use the public Riot API client")

    monkeypatch.setattr(cli, "LeagueReplayClient", LocalClient)
    monkeypatch.setattr(cli, "RiotClient", unexpected_public_client)
    return LocalClient


def test_player_list_needs_no_api_key_or_rso_token(local_client) -> None:
    result = runner.invoke(cli.app, ["replays", "list", "--player", "Another Player#EUW"])
    assert result.exit_code == 0, result.output
    assert "EUW1_123" in result.output
    assert "EUW1_456" in result.output
    assert "Recent matches" in result.output
    assert local_client.instances[0].list_calls == [("Another Player#EUW", 20)]
    assert local_client.instances[0].closed


def test_player_mode_ignores_public_api_environment(local_client, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RIOT_API_KEY", "unused-api-secret")
    monkeypatch.setenv("RIOT_RSO_ACCESS_TOKEN", "unused-rso-secret")
    monkeypatch.setenv("RIOT_MAX_RETRIES", "invalid")
    monkeypatch.setenv("RIOT_BASE_URL", "https://unused.example")
    result = runner.invoke(cli.app, ["replays", "list", "--player", "Player#TAG"])
    assert result.exit_code == 0, result.output
    assert "unused" not in result.output


def test_player_interactive_download_uses_displayed_matches(local_client) -> None:
    result = runner.invoke(
        cli.app, ["replays", "download", "--player", "Player#TAG"], input="2\n"
    )
    assert result.exit_code == 0, result.output
    instance = local_client.instances[0]
    assert instance.list_calls == [("Player#TAG", 20)]
    assert instance.download_calls == [(local_client.matches[1], None, False, 120)]
    assert "EUW1_456" in result.output
    assert "EUW1-456.rofl" in result.output
    assert "League Replays" in result.output
    assert instance.closed


def test_player_download_passes_copy_and_client_options(local_client, tmp_path: Path) -> None:
    output = tmp_path / "chosen.rofl"
    lockfile = tmp_path / "custom-install" / "lockfile"
    result = runner.invoke(cli.app, [
        "replays", "download", "1", "--player", "Player#TAG",
        "--output", str(output), "--overwrite", "--lockfile", str(lockfile),
        "--count", "5", "--timeout", "60",
    ])
    assert result.exit_code == 0, result.output
    instance = local_client.instances[0]
    assert instance.lockfile == lockfile
    assert instance.list_calls == [("Player#TAG", 5)]
    assert instance.download_calls == [(local_client.matches[0], output, True, 60)]


def test_player_lockfile_environment_is_used(local_client, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    lockfile = tmp_path / "League" / "lockfile"
    monkeypatch.setenv("RIOT_LCU_LOCKFILE", str(lockfile))
    result = runner.invoke(cli.app, ["replays", "list", "--player", "Player#TAG"])
    assert result.exit_code == 0, result.output
    assert local_client.instances[0].lockfile == lockfile


@pytest.mark.parametrize("riot_id", ["Player", "Player#", "#TAG", "Player#TAG#EXTRA", ""])
def test_player_id_is_validated_before_connecting(local_client, riot_id: str) -> None:
    result = runner.invoke(cli.app, ["replays", "download", "--player", riot_id])
    assert result.exit_code == 2
    assert "full Riot ID" in result.output
    assert not local_client.instances


def test_player_mode_rejects_regional_route(local_client) -> None:
    result = runner.invoke(cli.app, [
        "replays", "list", "--player", "Player#TAG", "--route", "europe",
    ])
    assert result.exit_code == 2
    assert "Omit --route" in result.output
    assert not local_client.instances


@pytest.mark.parametrize("arguments", [
    ["--count", "0"], ["--count", "21"], ["--timeout", "0"], ["--timeout", "nan"],
])
def test_player_invalid_limits_do_not_connect(local_client, arguments: list[str]) -> None:
    result = runner.invoke(cli.app, ["replays", "download", "--player", "Player#TAG", *arguments])
    assert result.exit_code == 2
    assert not local_client.instances


@pytest.mark.parametrize("option", ["--count", "--timeout"])
def test_local_options_require_player(local_client, option: str) -> None:
    result = runner.invoke(cli.app, ["replays", "download", "1", option, "5"])
    assert result.exit_code == 2
    assert "require --player" in result.output
    assert not local_client.instances


def test_invalid_player_match_selection_never_downloads(local_client) -> None:
    result = runner.invoke(cli.app, ["replays", "download", "3", "--player", "Player#TAG"])
    assert result.exit_code == 2
    assert not local_client.instances[0].download_calls
    assert local_client.instances[0].closed


@pytest.mark.parametrize(("command", "exit_code"), [("list", 0), ("download", 1)])
def test_empty_player_history_does_not_prompt_or_download(local_client, command: str, exit_code: int) -> None:
    local_client.matches = []
    result = runner.invoke(cli.app, ["replays", command, "--player", "Player#TAG"])
    assert result.exit_code == exit_code
    assert "No recent matches" in result.output
    assert not local_client.instances[0].download_calls


def test_client_rate_limit_is_reported_without_another_download(local_client) -> None:
    local_client.error = LeagueClientError(
        "Replay download limit reached: 10 downloads per hour. Retry after 1800 seconds.",
        status=429,
        retry_after=1800,
    )
    result = runner.invoke(cli.app, ["replays", "download", "1", "--player", "Player#TAG"])
    assert result.exit_code == 1
    assert "10 downloads per hour" in result.output
    assert "1800 seconds" in result.output
    assert "Traceback" not in result.output
    assert len(local_client.instances[0].download_calls) == 1


def test_aborted_player_selection_never_downloads(local_client) -> None:
    result = runner.invoke(cli.app, ["replays", "download", "--player", "Player#TAG"], input="")
    assert result.exit_code == 1
    assert not local_client.instances[0].download_calls
    assert local_client.instances[0].closed


def test_real_client_download_limit_shows_retry_after(tmp_path: Path) -> None:
    lockfile = tmp_path / "lockfile"
    lockfile.write_text("LeagueClient:1234:54321:local-secret:https", encoding="utf-8")
    with respx.mock(base_url="https://127.0.0.1:54321") as mock:
        mock.post("/lol-summoner/v1/summoners/aliases").respond(
            200, json=[{"gameName": "Player", "tagLine": "TAG", "puuid": "player-puuid"}]
        )
        mock.get("/lol-match-history/v1/products/lol/player-puuid/matches").respond(
            200, json={"games": {"games": [{
                "gameId": 123, "platformId": "EUW1", "gameVersion": "16.21.1",
                "gameType": "MATCHED_GAME", "queueId": 420,
                "gameCreation": 1790000000000, "gameDuration": 1800,
            }]}},
        )
        mock.get("/lol-rso-auth/v1/authorization").respond(
            200, json={"currentPlatformId": "EUW1"}
        )
        mock.get("/lol-replays/v1/rofls/path").respond(200, json=str(tmp_path))
        mock.get("/lol-replays/v1/metadata/123").respond(
            200, json={"gameId": 123, "state": "download", "downloadProgress": 0}
        )
        download = mock.post("/lol-replays/v1/rofls/123/download").respond(
            429, text="private upstream details", headers={"Retry-After": "1800"}
        )
        result = runner.invoke(cli.app, [
            "replays", "download", "1", "--player", "Player#TAG", "--lockfile", str(lockfile),
        ])
    assert result.exit_code == 1
    assert "10 downloads per hour" in result.output
    assert "1800" in result.output
    assert "private upstream details" not in result.output
    assert "local-secret" not in result.output
    assert "Traceback" not in result.output
    assert download.call_count == 1
    assert not (tmp_path / "EUW1-123.rofl").exists()

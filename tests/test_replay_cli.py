from __future__ import annotations

import os
from pathlib import Path

import httpx
import pytest
import respx
from typer.testing import CliRunner

from riotskillissue.cli import app

runner = CliRunner()
TOKEN = "test-rso-player-token"
API_URL = "https://europe.api.riotgames.com/lol/match/v5/matches/replays"
REPLAY_URL = "https://replays.example.test/euw1_123/0.replay?X-Amz-Signature=secret-signature"
REPLAY_BYTES = b"RIOT\x00replay payload"


@pytest.fixture(autouse=True)
def replay_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in list(os.environ):
        if name.startswith("RIOT_"):
            monkeypatch.delenv(name)
    monkeypatch.setenv("RIOT_RSO_ACCESS_TOKEN", TOKEN)
    monkeypatch.setenv("RIOT_MAX_RETRIES", "0")


def test_replay_help_is_available_without_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("RIOT_RSO_ACCESS_TOKEN")
    result = runner.invoke(app, ["replays", "--help"])
    assert result.exit_code == 0
    assert "download" in result.output
    assert "list" in result.output


def test_invalid_configuration_does_not_expose_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RIOT_MAX_RETRIES", "invalid")
    result = runner.invoke(app, ["replays", "list"])
    assert result.exit_code == 2
    assert "environment configuration" in result.output
    assert TOKEN not in result.output
    assert "Traceback" not in result.output


def test_replays_require_rso_even_when_an_api_key_is_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("RIOT_RSO_ACCESS_TOKEN")
    monkeypatch.setenv("RIOT_API_KEY", "RGAPI-not-an-rso-token")
    with respx.mock(assert_all_called=False) as router:
        result = runner.invoke(app, ["replays", "list"])
    assert result.exit_code == 2
    assert "RIOT_RSO_ACCESS_TOKEN" in result.output
    assert "RGAPI-not-an-rso-token" not in result.output
    assert not router.calls


@pytest.mark.parametrize("route", ["euw1", "apac", "not-a-route"])
def test_replay_route_is_validated_before_request(route: str) -> None:
    with respx.mock(assert_all_called=False) as router:
        result = runner.invoke(app, ["replays", "list", "--route", route])
    assert result.exit_code == 2
    assert "americas, asia, europe, or sea" in result.output
    assert not router.calls


def test_list_uses_rso_and_does_not_print_signed_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RIOT_API_KEY", "RGAPI-another-credential")
    with respx.mock() as router:
        listing = router.get(API_URL).respond(
            200, json={"total": 1, "matchFileURLs": [REPLAY_URL]}
        )
        result = runner.invoke(app, ["replays", "list"])
    assert result.exit_code == 0, result.output
    assert "EUW1_123.rofl" in result.output
    assert "secret-signature" not in result.output
    assert TOKEN not in result.output
    assert listing.calls[0].request.headers["Authorization"] == f"Bearer {TOKEN}"
    assert "X-Riot-Token" not in listing.calls[0].request.headers


def test_access_token_option_overrides_environment() -> None:
    with respx.mock() as router:
        listing = router.get(API_URL).respond(200, json={"total": 0, "matchFileURLs": []})
        result = runner.invoke(app, ["replays", "list", "--access-token", "explicit-token"])
    assert result.exit_code == 0, result.output
    assert listing.calls[0].request.headers["Authorization"] == "Bearer explicit-token"
    assert "explicit-token" not in result.output


@pytest.mark.parametrize("route", ["americas", "asia", "sea"])
def test_replay_route_selects_regional_endpoint(route: str) -> None:
    with respx.mock() as router:
        router.get(f"https://{route}.api.riotgames.com/lol/match/v5/matches/replays").respond(
            200, json={"total": 0, "matchFileURLs": []}
        )
        result = runner.invoke(app, ["replays", "list", "--route", route.upper()])
    assert result.exit_code == 0, result.output
    assert "No replays are available" in result.output


def test_download_saves_selected_replay_without_sending_credentials(tmp_path: Path) -> None:
    destination = tmp_path / "new-directory" / "game.rofl"
    with respx.mock() as router:
        router.get(API_URL).respond(200, json={"total": 1, "matchFileURLs": [REPLAY_URL]})
        download = router.get(REPLAY_URL).respond(200, content=REPLAY_BYTES)
        result = runner.invoke(app, ["replays", "download", "1", "--output", str(destination)])
    assert result.exit_code == 0, result.output
    assert destination.read_bytes() == REPLAY_BYTES
    assert "Saved replay" in result.output
    assert "Authorization" not in download.calls[0].request.headers
    assert "X-Riot-Token" not in download.calls[0].request.headers
    assert "secret-signature" not in result.output
    assert TOKEN not in result.output


def test_interactive_download_uses_the_displayed_list(tmp_path: Path) -> None:
    other_url = "https://replays.example.test/EUW1_456.replay?signature=other-secret"
    destination = tmp_path / "chosen.rofl"
    with respx.mock() as router:
        listing = router.get(API_URL).respond(
            200, json={"total": 2, "matchFileURLs": [REPLAY_URL, other_url]}
        )
        router.get(other_url).respond(200, content=REPLAY_BYTES)
        result = runner.invoke(
            app, ["replays", "download", "--output", str(destination)], input="2\n"
        )
    assert result.exit_code == 0, result.output
    assert "EUW1_123.rofl" in result.output
    assert "EUW1_456.rofl" in result.output
    assert "Replay number" in result.output
    assert listing.call_count == 1
    assert destination.read_bytes() == REPLAY_BYTES


def test_default_output_uses_replay_filename(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    with respx.mock() as router:
        router.get(API_URL).respond(200, json={"total": 1, "matchFileURLs": [REPLAY_URL]})
        router.get(REPLAY_URL).respond(200, content=REPLAY_BYTES)
        result = runner.invoke(app, ["replays", "download", "1"])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "EUW1_123.rofl").read_bytes() == REPLAY_BYTES


@pytest.mark.parametrize("index", ["0", "2"])
def test_invalid_replay_number_never_downloads(index: str) -> None:
    with respx.mock(assert_all_called=False) as router:
        router.get(API_URL).respond(200, json={"total": 1, "matchFileURLs": [REPLAY_URL]})
        download = router.get(REPLAY_URL).respond(200, content=REPLAY_BYTES)
        result = runner.invoke(app, ["replays", "download", index])
    assert result.exit_code == 2
    assert not download.called


def test_download_with_empty_list_fails_without_writing(tmp_path: Path) -> None:
    destination = tmp_path / "unavailable.rofl"
    with respx.mock() as router:
        router.get(API_URL).respond(200, json={"total": 0, "matchFileURLs": []})
        result = runner.invoke(app, ["replays", "download", "1", "--output", str(destination)])
    assert result.exit_code == 1
    assert "No replays are available" in result.output
    assert not destination.exists()


def test_existing_file_needs_explicit_overwrite(tmp_path: Path) -> None:
    destination = tmp_path / "existing.rofl"
    destination.write_bytes(b"previous replay")
    with respx.mock(assert_all_called=False) as router:
        router.get(API_URL).respond(200, json={"total": 1, "matchFileURLs": [REPLAY_URL]})
        download = router.get(REPLAY_URL).respond(200, content=REPLAY_BYTES)
        result = runner.invoke(app, ["replays", "download", "1", "--output", str(destination)])
        assert result.exit_code == 1
        assert "--overwrite" in result.output
        assert destination.read_bytes() == b"previous replay"
        assert not download.called
        replaced = runner.invoke(
            app, ["replays", "download", "1", "--output", str(destination), "--overwrite"]
        )
    assert replaced.exit_code == 0, replaced.output
    assert destination.read_bytes() == REPLAY_BYTES


@pytest.mark.parametrize(
    ("status", "message"),
    [(401, "invalid or expired"), (403, "RSO approval"), (404, "regional route")],
)
def test_api_errors_are_actionable_and_secret_safe(status: int, message: str) -> None:
    with respx.mock() as router:
        router.get(API_URL).respond(status, text=f"upstream echoed {TOKEN} {REPLAY_URL}")
        result = runner.invoke(app, ["replays", "list"])
    assert result.exit_code == 1
    assert message in result.output
    assert TOKEN not in result.output
    assert "secret-signature" not in result.output
    assert "Traceback" not in result.output


def test_api_rate_limit_reports_full_retry_after_without_retry() -> None:
    with respx.mock() as router:
        listing = router.get(API_URL).respond(429, headers={"Retry-After": "3600"})
        result = runner.invoke(app, ["replays", "list"])
    assert result.exit_code == 1
    assert "3600 seconds" in result.output
    assert listing.call_count == 1


@pytest.mark.parametrize("failure", ["expired", "network"])
def test_file_download_errors_do_not_expose_signed_url(tmp_path: Path, failure: str) -> None:
    destination = tmp_path / "game.rofl"
    with respx.mock() as router:
        router.get(API_URL).respond(200, json={"total": 1, "matchFileURLs": [REPLAY_URL]})
        download = router.get(REPLAY_URL)
        if failure == "expired":
            download.respond(403, text=f"Expired {REPLAY_URL}")
        else:
            download.mock(side_effect=httpx.ConnectError(f"Could not reach {REPLAY_URL}"))
        result = runner.invoke(app, ["replays", "download", "1", "--output", str(destination)])
    assert result.exit_code == 1
    assert "Error:" in result.output
    assert "secret-signature" not in result.output
    assert TOKEN not in result.output
    assert "Traceback" not in result.output
    assert not destination.exists()

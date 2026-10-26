from __future__ import annotations

import base64
import json
from pathlib import Path

import httpx
import pytest
import respx

from riotskillissue import ClientReplay, LeagueClientError, LeagueReplayClient
from riotskillissue import league_client as module

BASE = "https://127.0.0.1:54321"
METADATA = "/lol-replays/v1/metadata/123"
DOWNLOAD = "/lol-replays/v1/rofls/123/download"
GAME = {
    "gameId": 123,
    "platformId": "EUW1",
    "gameVersion": "16.21.1",
    "gameType": "MATCHED_GAME",
    "queueId": 420,
    "gameCreation": 1_790_000_000_000,
    "gameDuration": 1800,
    "gameMode": "CLASSIC",
}


@pytest.fixture
def lockfile(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "lockfile"
    path.write_text("LeagueClient:1234:54321:local-secret:https", encoding="utf-8")
    monkeypatch.setattr(module, "_POLL_INTERVAL", 0)
    return path


@pytest.fixture
def replay() -> ClientReplay:
    return ClientReplay(1, 123, "EUW1", "16.21.1", "MATCHED_GAME", 420, 1_790_001_800_000)


def mock_context(mock: respx.MockRouter, folder: Path, *, platform: str = "EUW1") -> None:
    mock.get("/lol-rso-auth/v1/authorization").respond(
        200, json={"currentPlatformId": platform}
    )
    mock.get("/lol-replays/v1/rofls/path").respond(200, json=str(folder))


def metadata(state: str, **extra: object) -> httpx.Response:
    return httpx.Response(200, json={"gameId": 123, "state": state, **extra})


@pytest.mark.asyncio
async def test_lookup_uses_full_riot_id_and_bounded_client_history(
    lockfile: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("RIOT_API_KEY", "private-api-key")
    monkeypatch.setenv("RIOT_RSO_ACCESS_TOKEN", "private-rso-token")
    monkeypatch.setenv("RIOT_BASE_URL", "https://external.example")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.example:8080")
    with respx.mock(base_url=BASE) as mock:
        alias = mock.post("/lol-summoner/v1/summoners/aliases").respond(
            200, json=[{"gameName": "Player Name", "tagLine": "EUW", "puuid": "player-puuid"}]
        )
        history = mock.get("/lol-match-history/v1/products/lol/player-puuid/matches").respond(
            200, json={"games": {"games": [GAME]}}
        )
        async with LeagueReplayClient(lockfile) as client:
            assert not client._http.trust_env
            assert not client._http.follow_redirects
            replays = await client.player_replays("Player Name#EUW", count=10)
        assert client._http.is_closed
    assert json.loads(alias.calls.last.request.content) == [
        {"gameName": "Player Name", "tagLine": "EUW"}
    ]
    assert dict(history.calls.last.request.url.params) == {"begIndex": "0", "endIndex": "9"}
    assert replays[0].game_end == GAME["gameCreation"] + GAME["gameDuration"] * 1000
    assert replays[0].filename == "EUW1-123.rofl"
    for call in (alias.calls.last, history.calls.last):
        assert call.request.headers["Authorization"] == (
            "Basic " + base64.b64encode(b"riot:local-secret").decode()
        )
        assert "X-Riot-Token" not in call.request.headers
        assert call.request.url.host == "127.0.0.1"
    assert "local-secret" not in repr(client)


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid", [
    {"gameId": True}, {"gameId": 1.9}, {"gameId": "123"},
    {"gameVersion": None}, {"gameCreation": float("inf")}, {"platformId": "../EUW1"},
])
async def test_malformed_match_fields_are_not_coerced_into_download_targets(
    lockfile: Path, invalid: dict[str, object]
) -> None:
    with respx.mock(base_url=BASE) as mock:
        mock.post("/lol-summoner/v1/summoners/aliases").respond(
            200, json=[{"gameName": "Name", "tagLine": "TAG", "puuid": "puuid"}]
        )
        # A raw body permits the non-standard Infinity value for parser robustness.
        mock.get("/lol-match-history/v1/products/lol/puuid/matches").respond(
            200, text=json.dumps({"games": {"games": [{**GAME, **invalid}]}})
        )
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError, match="unexpected match history"):
                await client.player_replays("Name#TAG")
        assert all("/lol-replays/" not in call.request.url.path for call in mock.calls)


@pytest.mark.asyncio
async def test_create_metadata_download_once_and_copy_completed_file(
    lockfile: Path, replay: ClientReplay, tmp_path: Path
) -> None:
    folder = tmp_path / "client-replays"
    folder.mkdir()
    source = folder / replay.filename
    destination = tmp_path / "exports" / "selected.rofl"
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, folder)
        mock.get(METADATA).mock(side_effect=[
            httpx.Response(404), metadata("download"), metadata("downloading"),
            metadata("watch", downloadProgress=0),
        ])
        create = mock.post("/lol-replays/v2/metadata/123/create").respond(204)

        def download(request: httpx.Request) -> httpx.Response:
            source.write_bytes(b"RIOT\x00replay data")
            return httpx.Response(204)

        start = mock.post(DOWNLOAD).mock(side_effect=download)
        async with LeagueReplayClient(lockfile) as client:
            saved = await client.download_replay(replay, destination)
    assert saved == destination
    assert source.read_bytes() == destination.read_bytes() == b"RIOT\x00replay data"
    assert list(destination.parent.iterdir()) == [destination]
    assert start.call_count == 1
    assert json.loads(start.calls.last.request.content) == {
        "componentType": "replay-button_match-history"
    }
    assert json.loads(create.calls.last.request.content) == {
        "gameVersion": replay.game_version,
        "gameType": replay.game_type,
        "queueId": replay.queue_id,
        "gameEnd": replay.game_end,
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("initial_state", ["found", "downloading", "watch"])
async def test_existing_or_in_progress_download_never_posts_again(
    lockfile: Path, replay: ClientReplay, tmp_path: Path, initial_state: str
) -> None:
    source = tmp_path / replay.filename
    source.write_bytes(b"already downloaded")
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        mock.get(METADATA).mock(side_effect=[metadata(initial_state), metadata("watch")])
        async with LeagueReplayClient(lockfile) as client:
            saved = await client.download_replay(replay)
        assert all(call.request.method == "GET" for call in mock.calls)
    assert saved == source
    assert source.read_bytes() == b"already downloaded"


@pytest.mark.asyncio
async def test_existing_output_is_rejected_before_metadata_or_download(
    lockfile: Path, replay: ClientReplay, tmp_path: Path
) -> None:
    destination = tmp_path / "existing.rofl"
    destination.write_bytes(b"keep me")
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError, match="--overwrite"):
                await client.download_replay(replay, destination)
        assert all(call.request.method == "GET" for call in mock.calls)
        assert not any("metadata" in call.request.url.path for call in mock.calls)
    assert destination.read_bytes() == b"keep me"


@pytest.mark.asyncio
async def test_same_output_as_client_file_is_reused_without_overwrite(
    lockfile: Path, replay: ClientReplay, tmp_path: Path
) -> None:
    source = tmp_path / replay.filename
    source.write_bytes(b"original")
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        mock.get(METADATA).mock(return_value=metadata("watch"))
        async with LeagueReplayClient(lockfile) as client:
            saved = await client.download_replay(replay, source, overwrite=True)
    assert saved == source
    assert source.read_bytes() == b"original"


@pytest.mark.asyncio
async def test_region_mismatch_prevents_numeric_game_id_requests(
    lockfile: Path, replay: ClientReplay
) -> None:
    with respx.mock(base_url=BASE) as mock:
        mock.get("/lol-rso-auth/v1/authorization").respond(
            200, json={"currentPlatformId": "NA1"}
        )
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError, match="different region"):
                await client.download_replay(replay)
        assert len(mock.calls) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "state", ["incompatible", "missingOrExpired", "unsupported", "error", "retryDownload", "lost"]
)
async def test_unavailable_state_does_not_start_download(
    lockfile: Path, replay: ClientReplay, tmp_path: Path, state: str
) -> None:
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        mock.get(METADATA).mock(return_value=metadata(state))
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError):
                await client.download_replay(replay)
        assert all(call.request.method == "GET" for call in mock.calls)


@pytest.mark.asyncio
@pytest.mark.parametrize("result", [{"state": {}}, {"gameId": 456, "state": "download"}])
async def test_bad_metadata_does_not_start_download(
    lockfile: Path, replay: ClientReplay, tmp_path: Path, result: dict[str, object]
) -> None:
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        mock.get(METADATA).respond(200, json=result)
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError):
                await client.download_replay(replay)
        assert all(call.request.method == "GET" for call in mock.calls)


@pytest.mark.asyncio
async def test_download_quota_is_reported_without_retry(
    lockfile: Path, replay: ClientReplay, tmp_path: Path
) -> None:
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        mock.get(METADATA).mock(return_value=metadata("download"))
        start = mock.post(DOWNLOAD).respond(
            429, headers={"Retry-After": "3600"}, text="private body local-secret"
        )
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError, match="10 downloads per hour") as caught:
                await client.download_replay(replay)
        assert start.call_count == 1
    assert caught.value.status == 429
    assert caught.value.retry_after == 3600
    assert "3600" in str(caught.value)
    assert "local-secret" not in str(caught.value)


@pytest.mark.asyncio
async def test_lookup_rate_limit_does_not_claim_download_quota(lockfile: Path) -> None:
    with respx.mock(base_url=BASE) as mock:
        mock.post("/lol-summoner/v1/summoners/aliases").respond(429)
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError) as caught:
                await client.player_replays("Name#TAG")
    assert "10 downloads" not in str(caught.value)


@pytest.mark.asyncio
async def test_new_metadata_quota_error_stops_without_retry(
    lockfile: Path, replay: ClientReplay, tmp_path: Path
) -> None:
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        mock.get(METADATA).mock(
            return_value=metadata("error", errorCode="REPLAY_RATE_LIMIT_EXCEEDED")
        )
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError, match="10 downloads per hour"):
                await client.download_replay(replay)
        assert all(call.request.method == "GET" for call in mock.calls)


@pytest.mark.asyncio
async def test_ambiguous_download_failure_is_not_replayed(
    lockfile: Path, replay: ClientReplay, tmp_path: Path
) -> None:
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        mock.get(METADATA).mock(return_value=metadata("download"))
        start = mock.post(DOWNLOAD).mock(side_effect=httpx.ReadTimeout("private local-secret"))
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError) as caught:
                await client.download_replay(replay)
        assert start.call_count == 1
    assert "local-secret" not in str(caught.value)
    assert "may still finish" in str(caught.value)


@pytest.mark.asyncio
async def test_poll_timeout_does_not_retry_or_delete_clients_file(
    lockfile: Path, replay: ClientReplay, tmp_path: Path
) -> None:
    source = tmp_path / replay.filename
    source.write_bytes(b"client-managed partial download")
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        mock.get(METADATA).mock(return_value=metadata("downloading"))
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError, match="background"):
                await client.download_replay(replay, timeout=0.01)
        assert all(call.request.method == "GET" for call in mock.calls)
    assert source.read_bytes() == b"client-managed partial download"


@pytest.mark.asyncio
async def test_redirect_cannot_forward_local_credentials(lockfile: Path) -> None:
    with respx.mock(base_url=BASE) as mock:
        mock.post("/lol-summoner/v1/summoners/aliases").respond(
            302, headers={"Location": "https://external.example/collect"}
        )
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError, match="redirect"):
                await client.player_replays("Name#TAG")
        assert len(mock.calls) == 1


@pytest.mark.parametrize("contents", [
    "RiotClient:1:54321:secret:https", "LeagueClient:0:54321:secret:https",
    "LeagueClient:1:65536:secret:https", "LeagueClient:1:54321::https",
    "LeagueClient:1:54321:secret:http", "invalid-secret",
])
def test_bad_lockfiles_do_not_expose_contents(tmp_path: Path, contents: str) -> None:
    path = tmp_path / "lockfile"
    path.write_text(contents, encoding="utf-8")
    with pytest.raises(LeagueClientError) as caught:
        LeagueReplayClient(path)
    assert "secret" not in str(caught.value)


@pytest.mark.asyncio
async def test_lockfile_environment_override_and_discovery(
    lockfile: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("RIOT_LCU_LOCKFILE", str(lockfile))
    async with LeagueReplayClient():
        pass
    monkeypatch.delenv("RIOT_LCU_LOCKFILE")
    monkeypatch.setattr(module, "_default_lockfiles", lambda: [lockfile])
    async with LeagueReplayClient():
        pass
    assert "local-secret" not in repr(module._read_credentials(lockfile))


def test_missing_lockfile_explains_how_to_connect(tmp_path: Path) -> None:
    with pytest.raises(LeagueClientError, match="--lockfile"):
        LeagueReplayClient(tmp_path / "missing")


@pytest.mark.asyncio
async def test_failed_copy_preserves_both_client_file_and_existing_destination(
    lockfile: Path, replay: ClientReplay, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / replay.filename
    source.write_bytes(b"downloaded replay")
    target = tmp_path / "export.rofl"
    target.write_bytes(b"previous export")

    def fail_copy(*args: object, **kwargs: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(module.shutil, "copyfileobj", fail_copy)
    with respx.mock(base_url=BASE) as mock:
        mock_context(mock, tmp_path)
        mock.get(METADATA).mock(return_value=metadata("watch"))
        async with LeagueReplayClient(lockfile) as client:
            with pytest.raises(LeagueClientError, match="copy"):
                await client.download_replay(replay, target, overwrite=True)
    assert source.read_bytes() == b"downloaded replay"
    assert target.read_bytes() == b"previous export"
    assert not list(tmp_path.glob("*.part"))

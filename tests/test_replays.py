from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
import pytest
import respx

from riotskillissue import (
    ReplayDownloadError,
    ReplayFile,
    RiotClient,
    StaticRsoTokenProvider,
    SyncRiotClient,
)
from riotskillissue.replays import download_replay, replay_files

API_URL = "https://europe.api.riotgames.com/lol/match/v5/matches/replays"
FILE_URL = "https://replays.example/euw1_123/0.replay?signature=secret%2Fvalue&part=0"
REPLAY_BYTES = b"RIOT\x00\x00\xffbinary replay contents"


@pytest.mark.asyncio
async def test_replays_use_rso_and_stream_files_without_credentials(tmp_path: Path) -> None:
    with respx.mock as mock:
        listing = mock.get(API_URL).respond(
            200, json={"matchFileURLs": [FILE_URL], "total": 1}
        )
        download = mock.get(FILE_URL).respond(200, content=REPLAY_BYTES)
        async with RiotClient(
            api_key="RGAPI-unrelated",
            rso_token_provider=StaticRsoTokenProvider("player-token"),
        ) as client:
            files = await client.lol.replays(route="europe")
            assert files == [ReplayFile(1, "EUW1_123.rofl", FILE_URL)]
            path = await client.lol.download_replay(
                files[0], tmp_path / "new-directory" / files[0].filename
            )

    assert path.read_bytes() == REPLAY_BYTES
    assert "signature" not in repr(files[0])
    assert listing.calls.last.request.headers["Authorization"] == "Bearer player-token"
    assert "X-Riot-Token" not in listing.calls.last.request.headers
    assert not listing.calls.last.request.url.query
    request = download.calls.last.request
    assert request.url.query == b"signature=secret%2Fvalue&part=0"
    assert not {"authorization", "x-riot-token", "cookie"} & set(request.headers)
    assert list(path.parent.iterdir()) == [path]


def test_replay_names_are_safe_unique_and_handle_both_path_shapes() -> None:
    urls = [
        "https://replays.example/NA1_123.replay?signature=hidden",
        "https://replays.example/na1_456/0.replay?signature=hidden",
        "https://replays.example/custom.rofl",
        "https://replays.example/other/custom.rofl",
        "https://replays.example/..%2F..%2Foutside.replay",
        "https://replays.example/CON.replay",
        "https://replays.example/con.txt.replay",
        "https://replays.example/COM1.replay",
        "https://replays.example/",
        "https://replays.example/%5Cwindows%5Cfile.replay",
    ]
    files = replay_files(urls)
    assert [file.filename for file in files] == [
        "NA1_123.rofl",
        "NA1_456.rofl",
        "custom.rofl",
        "custom-4.rofl",
        "replay-5.rofl",
        "replay-6.rofl",
        "replay-7.rofl",
        "replay-8.rofl",
        "replay-9.rofl",
        "replay-10.rofl",
    ]
    assert [file.url for file in files] == urls


@pytest.mark.parametrize("filename", ["../outside.rofl", "CON.rofl", "file.txt", "x\\y.rofl"])
def test_replay_file_rejects_unsafe_names(filename: str) -> None:
    with pytest.raises(ValueError, match="safe .rofl"):
        ReplayFile(1, filename, FILE_URL)


@pytest.mark.asyncio
async def test_replay_rejects_non_https_url_before_writing(tmp_path: Path) -> None:
    replay = ReplayFile(1, "replay.rofl", "http://replays.example/file?secret=token")
    with respx.mock as mock:
        with pytest.raises(ReplayDownloadError) as caught:
            await download_replay(replay, tmp_path / "new" / "replay.rofl")
        assert not mock.calls
    assert "secret" not in str(caught.value)
    assert not list(tmp_path.iterdir())


@pytest.mark.asyncio
async def test_replay_redirect_drops_cookies(tmp_path: Path) -> None:
    target = "https://replays.example/final?signature=other-secret"
    with respx.mock as mock:
        mock.get(FILE_URL).respond(
            302, headers={"Location": target, "Set-Cookie": "session=private; Path=/"}
        )
        redirected = mock.get(target).respond(200, content=REPLAY_BYTES)
        path = await download_replay(replay_files([FILE_URL])[0], tmp_path / "replay.rofl")

    assert path.read_bytes() == REPLAY_BYTES
    assert not {"authorization", "x-riot-token", "cookie"} & set(
        redirected.calls.last.request.headers
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "target",
    ["http://replays.example/insecure", "https://user:secret@replays.example/private"],
)
async def test_replay_rejects_unsafe_redirects(tmp_path: Path, target: str) -> None:
    with respx.mock as mock:
        mock.get(FILE_URL).respond(302, headers={"Location": target})
        with pytest.raises(ReplayDownloadError) as caught:
            await download_replay(replay_files([FILE_URL])[0], tmp_path / "replay.rofl")
        assert len(mock.calls) == 1
    assert "secret" not in str(caught.value)
    assert not list(tmp_path.iterdir())


@pytest.mark.asyncio
async def test_replay_redirects_are_bounded(tmp_path: Path) -> None:
    with respx.mock as mock:
        route = mock.get(FILE_URL).respond(302, headers={"Location": FILE_URL})
        with pytest.raises(ReplayDownloadError, match="redirect limit"):
            await download_replay(replay_files([FILE_URL])[0], tmp_path / "replay.rofl")
        assert route.call_count == 6
    assert not list(tmp_path.iterdir())


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [403, 404, 429, 500])
async def test_replay_http_errors_are_sanitized_and_not_retried(
    tmp_path: Path, status: int
) -> None:
    with respx.mock as mock:
        route = mock.get(FILE_URL).respond(
            status, text=f"Failed to read {FILE_URL}", headers={"Retry-After": "3600"}
        )
        with pytest.raises(ReplayDownloadError) as caught:
            await download_replay(replay_files([FILE_URL])[0], tmp_path / "replay.rofl")
        assert route.call_count == 1
    assert caught.value.status == status
    assert caught.value.retry_after == 3600
    assert "signature" not in str(caught.value)
    assert "secret" not in repr(caught.value)
    assert not list(tmp_path.iterdir())


class InterruptedStream(httpx.AsyncByteStream):
    def __init__(self, *, cancelled: bool = False) -> None:
        self.cancelled = cancelled

    async def __aiter__(self):
        yield b"partial" * 10000
        if self.cancelled:
            raise asyncio.CancelledError
        raise httpx.ReadError(f"Connection interrupted for {FILE_URL}")


@pytest.mark.asyncio
@pytest.mark.parametrize("cancelled", [False, True])
async def test_interrupted_download_keeps_existing_file_and_cleans_up(
    tmp_path: Path, cancelled: bool
) -> None:
    path = tmp_path / "replay.rofl"
    path.write_bytes(b"existing replay")
    expected_error = asyncio.CancelledError if cancelled else ReplayDownloadError
    with respx.mock as mock:
        mock.get(FILE_URL).mock(
            return_value=httpx.Response(200, stream=InterruptedStream(cancelled=cancelled))
        )
        with pytest.raises(expected_error) as caught:
            await download_replay(replay_files([FILE_URL])[0], path, overwrite=True)
    assert "secret" not in str(caught.value)
    assert path.read_bytes() == b"existing replay"
    assert list(tmp_path.iterdir()) == [path]


@pytest.mark.asyncio
@pytest.mark.parametrize("body,length", [(b"", "0"), (b"partial", "100")])
async def test_empty_or_incomplete_download_is_not_published(
    tmp_path: Path, body: bytes, length: str
) -> None:
    with respx.mock as mock:
        mock.get(FILE_URL).respond(200, content=body, headers={"Content-Length": length})
        with pytest.raises(ReplayDownloadError, match="empty|incomplete"):
            await download_replay(replay_files([FILE_URL])[0], tmp_path / "replay.rofl")
    assert not list(tmp_path.iterdir())


@pytest.mark.asyncio
async def test_existing_file_requires_explicit_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "replay.rofl"
    path.write_bytes(b"existing")
    with respx.mock as mock:
        route = mock.get(FILE_URL).respond(200, content=REPLAY_BYTES)
        with pytest.raises(ReplayDownloadError, match="already exists"):
            await download_replay(replay_files([FILE_URL])[0], path)
        assert not route.called
        await download_replay(replay_files([FILE_URL])[0], path, overwrite=True)
    assert path.read_bytes() == REPLAY_BYTES
    assert list(tmp_path.iterdir()) == [path]


@pytest.mark.asyncio
async def test_file_created_during_download_is_preserved(tmp_path: Path) -> None:
    path = tmp_path / "replay.rofl"

    def concurrent_writer(request: httpx.Request) -> httpx.Response:
        path.write_bytes(b"created by another process")
        return httpx.Response(200, content=REPLAY_BYTES)

    with respx.mock as mock:
        mock.get(FILE_URL).mock(side_effect=concurrent_writer)
        with pytest.raises(ReplayDownloadError, match="already exists"):
            await download_replay(replay_files([FILE_URL])[0], path)
    assert path.read_bytes() == b"created by another process"
    assert list(tmp_path.iterdir()) == [path]


def test_sync_replay_listing_and_download(tmp_path: Path) -> None:
    with respx.mock as mock:
        mock.get(API_URL).respond(200, json={"matchFileURLs": [FILE_URL], "total": 1})
        mock.get(FILE_URL).respond(200, content=REPLAY_BYTES)
        with SyncRiotClient(
            rso_token_provider=StaticRsoTokenProvider("player-token")
        ) as client:
            files = client.lol.replays(route="europe")
            path = client.lol.download_replay(files[0], tmp_path / files[0].filename)
    assert path.read_bytes() == REPLAY_BYTES

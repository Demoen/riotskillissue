from __future__ import annotations

import fnmatch
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
import respx

from riotskillissue.core import cache as cache_module
from riotskillissue.core import ratelimit as ratelimit_module
from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.http import HttpClient, RiotNetworkError, RiotTimeoutError, ServerError
from riotskillissue.static import DataDragonClient


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["POST", "PATCH"])
@pytest.mark.parametrize(
    ("failure", "error_type"),
    [
        (httpx.ReadTimeout("response lost"), RiotTimeoutError),
        (httpx.WriteTimeout("write interrupted"), RiotTimeoutError),
        (httpx.ReadError("response lost"), RiotNetworkError),
        (httpx.WriteError("write interrupted"), RiotNetworkError),
        (httpx.RemoteProtocolError("response interrupted"), RiotNetworkError),
        (httpx.DecodingError("invalid response encoding"), RiotNetworkError),
        (httpx.Response(503), ServerError),
    ],
)
async def test_non_idempotent_requests_are_not_replayed_after_ambiguous_failures(
    method: str,
    failure: Exception | httpx.Response,
    error_type: type[Exception],
) -> None:
    client = HttpClient(
        RiotClientConfig(api_key="RGAPI-test", retry_backoff_base=0.001)
    )
    try:
        with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
            route = mock.route(method=method, path="/mutation").mock(
                side_effect=[failure, httpx.Response(200, json={"created": True})]
            )
            with pytest.raises(error_type):
                await client.request(method, "/mutation", "na1", json={"name": "event"})
            assert route.call_count == 1
    finally:
        await client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["POST", "PATCH"])
@pytest.mark.parametrize("error_type", [httpx.ConnectError, httpx.ConnectTimeout, httpx.PoolTimeout])
async def test_non_idempotent_requests_retry_failures_before_sending(
    method: str, error_type: type[Exception]
) -> None:
    client = HttpClient(
        RiotClientConfig(api_key="RGAPI-test", retry_backoff_base=0.001)
    )
    try:
        with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
            route = mock.route(method=method, path="/mutation").mock(
                side_effect=[error_type("not connected"), httpx.Response(201, json={"id": 1})]
            )
            response = await client.request(method, "/mutation", "na1", json={"name": "event"})
            assert response.json() == {"id": 1}
            assert route.call_count == 2
    finally:
        await client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE"])
@pytest.mark.parametrize("failure", [httpx.ReadTimeout("response lost"), httpx.Response(503)])
async def test_idempotent_requests_still_retry_transient_failures(
    method: str, failure: Exception | httpx.Response
) -> None:
    client = HttpClient(
        RiotClientConfig(api_key="RGAPI-test", retry_backoff_base=0.001)
    )
    try:
        with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
            route = mock.route(method=method, path="/resource").mock(
                side_effect=[failure, httpx.Response(200, json={"ok": True})]
            )
            response = await client.request(method, "/resource", "na1")
            assert response.json() == {"ok": True}
            assert route.call_count == 2
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_rate_limited_mutations_still_retry() -> None:
    client = HttpClient(RiotClientConfig(api_key="RGAPI-test"))
    try:
        with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
            route = mock.post("/mutation").mock(
                side_effect=[
                    httpx.Response(429, headers={"Retry-After": "0"}),
                    httpx.Response(201, json={"id": 1}),
                ]
            )
            response = await client.request("POST", "/mutation", "na1", json={"name": "event"})
            assert response.json() == {"id": 1}
            assert route.call_count == 2
    finally:
        await client.close()


class _RedisStore:
    def __init__(self) -> None:
        self.data: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        return self.data.get(key)

    async def set(self, key: str, value: str, *, ex: int | None = None) -> None:
        self.data[key] = value

    async def delete(self, *keys: str) -> None:
        for key in keys:
            self.data.pop(key, None)

    async def flushdb(self) -> None:
        self.data.clear()

    async def scan_iter(self, *, match: str, count: int):
        for key in list(self.data):
            if fnmatch.fnmatchcase(key, match):
                yield key


@pytest.fixture
def redis_cache(monkeypatch: pytest.MonkeyPatch):
    pytest.importorskip("redis")
    store = _RedisStore()
    monkeypatch.setattr(cache_module.Redis, "from_url", lambda _: store)
    return cache_module.RedisCache("redis://unused"), store


@pytest.mark.asyncio
async def test_redis_cache_operations_preserve_unrelated_data(redis_cache) -> None:
    cache, store = redis_cache
    await store.set("application:session", "user-session")
    await store.set("riot:rl:app:na1:key:120", "rate-limit-window")
    await cache.set("application:session", "cached-response", ttl=60)
    assert await store.get("application:session") == "user-session"
    assert await cache.get("application:session") == "cached-response"
    await cache.delete("application:session")
    assert await cache.get("application:session") is None
    assert await store.get("application:session") == "user-session"

    for index in range(105):
        await cache.set(str(index), {"value": index}, ttl=60)
    await cache.clear()

    assert store.data == {
        "application:session": "user-session",
        "riot:rl:app:na1:key:120": "rate-limit-window",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value",
    [
        {1: {"name": "Annie"}, "1": {"name": "string key"}},
        (200, {"Content-Type": "application/json"}, b'{"value": 1}'),
        {"__bytes__": "literal", "__tuple__": [1, 2], "__dict__": [["a", "b"]]},
        [{2: (b"nested", {"value": [1, 2]})}],
    ],
)
async def test_redis_cache_round_trips_supported_values(redis_cache, value: Any) -> None:
    cache, _ = redis_cache
    await cache.set("value", value, ttl=60)
    assert await cache.get("value") == value


@pytest.mark.asyncio
async def test_data_dragon_lookup_survives_redis_cache_round_trip(redis_cache) -> None:
    cache, _ = redis_cache
    async with DataDragonClient(cache=cache) as client:
        with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
            route = mock.get("/cdn/16.1.1/data/en_US/champion.json").respond(
                200, json={"data": {"Annie": {"key": "1", "id": "Annie", "name": "Annie"}}}
            )
            first = await client.get_champion(1, version="16.1.1")
            second = await client.get_champion(1, version="16.1.1")
            assert first == second == {"key": "1", "id": "Annie", "name": "Annie"}
            assert route.call_count == 1


@pytest.fixture
def redis_connection(monkeypatch: pytest.MonkeyPatch):
    connection = MagicMock()
    connection.aclose = AsyncMock()
    connection.register_script.return_value = AsyncMock(return_value=b"0")
    redis_module = MagicMock()
    redis_module.from_url.return_value = connection
    monkeypatch.setattr(ratelimit_module, "redis", redis_module)
    return connection


@pytest.mark.asyncio
async def test_http_client_closes_its_redis_limiter(redis_connection) -> None:
    client = HttpClient(RiotClientConfig(api_key="RGAPI-test", redis_url="redis://unused"))

    await client.close()

    assert client._client.is_closed
    redis_connection.aclose.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_shared_redis_limiter_remains_open_until_owner_closes_it(redis_connection) -> None:
    limiter = ratelimit_module.RedisRateLimiter("redis://unused")
    config = RiotClientConfig(api_key="RGAPI-test", redis_url="redis://unused")
    first_client = HttpClient(config, rate_limiter=limiter)
    second_client = HttpClient(config, rate_limiter=limiter)
    try:
        await first_client.close()
        redis_connection.aclose.assert_not_awaited()

        with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
            mock.get("/resource").respond(200, json={"ok": True})
            response = await second_client.request("GET", "/resource", "na1")
            assert response.json() == {"ok": True}
    finally:
        await first_client.close()
        await second_client.close()

    redis_connection.aclose.assert_not_awaited()
    await limiter.close()
    redis_connection.aclose.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_owned_redis_limiter_closes_when_http_shutdown_fails(
    redis_connection, monkeypatch: pytest.MonkeyPatch
) -> None:
    client = HttpClient(RiotClientConfig(api_key="RGAPI-test", redis_url="redis://unused"))
    http_close = client._client.aclose
    monkeypatch.setattr(client._client, "aclose", AsyncMock(side_effect=RuntimeError("close failed")))
    try:
        with pytest.raises(RuntimeError, match="close failed"):
            await client.close()
        redis_connection.aclose.assert_awaited_once_with()
    finally:
        await http_close()

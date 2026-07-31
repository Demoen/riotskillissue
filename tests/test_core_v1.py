from __future__ import annotations

from typing import List, Optional, Tuple

import httpx
import pytest
import respx
from pydantic import BaseModel

from riotskillissue.auth import (
    RefreshingRsoTokenProvider,
    StaticRsoTokenProvider,
    TokenResponse,
)
from riotskillissue.core.cache import MemoryCache
from riotskillissue.core.config import RiotClientConfig
from riotskillissue.core.http import (
    HttpClient,
    MalformedResponseError,
    MissingCredentialError,
    RateLimitError,
    ResponseValidationError,
    RiotNetworkError,
    RiotTimeoutError,
)
from riotskillissue.core.ratelimit import AbstractRateLimiter, RateLimitBucket
from riotskillissue.core.types import (
    PlatformRoute,
    RegionalRoute,
    RiotId,
    RouteKind,
    RouteResolutionError,
    ValorantRoute,
)


class _RecordingLimiter(AbstractRateLimiter):
    def __init__(self) -> None:
        self.acquires: List[Tuple[str, List[RateLimitBucket]]] = []
        self.updates: List[Tuple[str, str, Optional[str]]] = []

    async def acquire(self, key: str, limits: List[RateLimitBucket]) -> None:
        self.acquires.append((key, limits))

    async def update(
        self, key: str, counts: str, limits: Optional[str] = None
    ) -> None:
        self.updates.append((key, counts, limits))


class _Result(BaseModel):
    value: int


@pytest.mark.asyncio
async def test_route_resolution_and_allowed_routes() -> None:
    config = RiotClientConfig(
        api_key="RGAPI-test",
        default_route=PlatformRoute.EUW1,
    )
    client = HttpClient(config)

    assert client.resolve_route(RouteKind.PLATFORM) is PlatformRoute.EUW1
    assert client.resolve_route(RouteKind.REGIONAL) is RegionalRoute.EUROPE
    assert client.resolve_route(RouteKind.VALORANT) is ValorantRoute.EU
    assert (
        client.resolve_route(
            RouteKind.REGIONAL,
            allowed_routes=("europe",),
        )
        is RegionalRoute.EUROPE
    )

    with pytest.raises(RouteResolutionError):
        client.resolve_route(
            RouteKind.REGIONAL,
            allowed_routes=("americas",),
        )

    apac_client = HttpClient(
        RiotClientConfig(
            api_key="RGAPI-test",
            default_route=PlatformRoute.KR,
        )
    )
    assert (
        apac_client.resolve_route(
            RouteKind.REGIONAL,
            allowed_routes=("americas", "apac", "europe", "sea"),
        )
        is RegionalRoute.APAC
    )

    regional_client = HttpClient(
        RiotClientConfig(
            api_key="RGAPI-test",
            default_route=RegionalRoute.EUROPE,
        )
    )
    assert regional_client.resolve_route(RouteKind.VALORANT) is ValorantRoute.EU
    await client.close()
    await apac_client.close()
    await regional_client.close()


def test_riot_id_parsing() -> None:
    riot_id = RiotId.parse(" Player Name #EUW ")

    assert riot_id.game_name == "Player Name"
    assert riot_id.tag_line == "EUW"
    assert str(riot_id) == "Player Name#EUW"

    with pytest.raises(ValueError):
        RiotId.parse("missing-tag")


def test_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RIOT_API_KEY", "  RGAPI-test  ")
    monkeypatch.setenv("RIOT_DEFAULT_ROUTE", "euw1")
    monkeypatch.setenv("RIOT_MAX_RETRIES", "0")
    monkeypatch.setenv("RIOT_MAX_RATE_LIMIT_RETRIES", "7")
    monkeypatch.setenv("RIOT_CONNECT_TIMEOUT", "1")
    monkeypatch.setenv("RIOT_READ_TIMEOUT", "2")
    monkeypatch.setenv("RIOT_WRITE_TIMEOUT", "3")
    monkeypatch.setenv("RIOT_POOL_TIMEOUT", "4")

    config = RiotClientConfig.from_env()

    assert config.api_key == "RGAPI-test"
    assert config.default_route is PlatformRoute.EUW1
    assert config.max_retries == 0
    assert config.max_rate_limit_retries == 7
    assert (
        config.connect_timeout,
        config.read_timeout,
        config.write_timeout,
        config.pool_timeout,
    ) == (1.0, 2.0, 3.0, 4.0)


@pytest.mark.asyncio
async def test_auth_selection_and_missing_credentials() -> None:
    api_config = RiotClientConfig(api_key="RGAPI-test")
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        api_route = mock.get("/api").respond(200, json={"value": 1})
        client = HttpClient(api_config)
        result = await client.request(
            "GET",
            "/api",
            PlatformRoute.NA1,
            response_adapter=_Result.model_validate,
        )
        await client.close()

    assert result == _Result(value=1)
    assert api_route.calls.last.request.headers["X-Riot-Token"] == "RGAPI-test"
    assert "Authorization" not in api_route.calls.last.request.headers

    rso_config = RiotClientConfig(
        rso_token_provider=StaticRsoTokenProvider("access-token")
    )
    async with respx.mock(base_url="https://americas.api.riotgames.com") as mock:
        rso_route = mock.get("/rso").respond(200, json={"value": 2})
        client = HttpClient(rso_config)
        result = await client.request(
            "GET",
            "/rso",
            RegionalRoute.AMERICAS,
            auth_mode="rso",
            response_adapter=_Result.model_validate,
        )
        await client.close()

    assert result == _Result(value=2)
    assert rso_route.calls.last.request.headers["Authorization"] == (
        "Bearer access-token"
    )
    assert "X-Riot-Token" not in rso_route.calls.last.request.headers

    client = HttpClient(RiotClientConfig())
    with pytest.raises(MissingCredentialError):
        await client.request("GET", "/missing", PlatformRoute.NA1)
    await client.close()


@pytest.mark.asyncio
async def test_rso_cache_default_and_api_key_isolation() -> None:
    shared_cache = MemoryCache()
    rso_config = RiotClientConfig(
        rso_token_provider=StaticRsoTokenProvider("access-token")
    )
    async with respx.mock(base_url="https://americas.api.riotgames.com") as mock:
        route = mock.get("/rso").mock(
            side_effect=[
                httpx.Response(200, json={"value": 1}),
                httpx.Response(200, json={"value": 2}),
            ]
        )
        client = HttpClient(rso_config, cache=shared_cache)
        first = await client.request(
            "GET",
            "/rso",
            RegionalRoute.AMERICAS,
            auth_mode="rso",
            response_adapter=None,
        )
        second = await client.request(
            "GET",
            "/rso",
            RegionalRoute.AMERICAS,
            auth_mode="rso",
            response_adapter=None,
        )
        await client.close()

    assert first["value"] == 1
    assert second["value"] == 2
    assert route.call_count == 2
    assert not shared_cache._store

    shared_cache = MemoryCache()
    async with respx.mock(base_url="https://americas.api.riotgames.com") as mock:
        route = mock.get("/rso-scoped").mock(
            side_effect=[
                httpx.Response(200, json={"value": 1}),
                httpx.Response(200, json={"value": 2}),
            ]
        )
        first_client = HttpClient(
            RiotClientConfig(
                rso_token_provider=StaticRsoTokenProvider("first-token"),
                cache_rso_responses=True,
            ),
            cache=shared_cache,
        )
        second_client = HttpClient(
            RiotClientConfig(
                rso_token_provider=StaticRsoTokenProvider("second-token"),
                cache_rso_responses=True,
            ),
            cache=shared_cache,
        )
        first = await first_client.request(
            "GET",
            "/rso-scoped",
            RegionalRoute.AMERICAS,
            auth_mode="rso",
            response_adapter=None,
        )
        second = await second_client.request(
            "GET",
            "/rso-scoped",
            RegionalRoute.AMERICAS,
            auth_mode="rso",
            response_adapter=None,
        )
        await first_client.close()
        await second_client.close()

    assert first["value"] == 1
    assert second["value"] == 2
    assert route.call_count == 2
    assert all("token" not in key for key in shared_cache._store)

    shared_cache = MemoryCache()
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        route = mock.get("/scoped").mock(
            side_effect=[
                httpx.Response(200, json={"value": 1}),
                httpx.Response(200, json={"value": 2}),
            ]
        )
        first_client = HttpClient(
            RiotClientConfig(api_key="RGAPI-one"),
            cache=shared_cache,
        )
        second_client = HttpClient(
            RiotClientConfig(api_key="RGAPI-two"),
            cache=shared_cache,
        )
        first = await first_client.request(
            "GET",
            "/scoped",
            PlatformRoute.NA1,
            response_adapter=None,
        )
        second = await second_client.request(
            "GET",
            "/scoped",
            PlatformRoute.NA1,
            response_adapter=None,
        )
        await first_client.close()
        await second_client.close()

    assert first["value"] == 1
    assert second["value"] == 2
    assert route.call_count == 2
    assert all("RGAPI" not in key for key in shared_cache._store)


@pytest.mark.asyncio
async def test_bounded_rate_limit_and_response_handling() -> None:
    config = RiotClientConfig(
        api_key="RGAPI-test",
        max_retries=0,
        max_rate_limit_retries=1,
    )
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        route = mock.get("/limited").mock(
            side_effect=[
                httpx.Response(429, headers={"Retry-After": "0"}),
                httpx.Response(429, headers={"Retry-After": "0"}),
            ]
        )
        client = HttpClient(config)
        with pytest.raises(RateLimitError) as exc_info:
            await client.request("GET", "/limited", PlatformRoute.NA1)
        await client.close()

    assert exc_info.value.retries == 1
    assert route.call_count == 2

    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        mock.delete("/empty").respond(204)
        client = HttpClient(config)
        result = await client.request(
            "DELETE",
            "/empty",
            PlatformRoute.NA1,
            response_adapter=None,
            successful_statuses=("204",),
            no_content_statuses=("204",),
        )
        await client.close()

    assert result is None


@pytest.mark.asyncio
async def test_typed_transport_and_response_errors() -> None:
    config = RiotClientConfig(api_key="RGAPI-test", max_retries=0)
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        mock.get("/network").mock(side_effect=httpx.ConnectError("offline"))
        client = HttpClient(config)
        with pytest.raises(RiotNetworkError):
            await client.request("GET", "/network", PlatformRoute.NA1)
        await client.close()

    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        mock.get("/timeout").mock(side_effect=httpx.ReadTimeout("slow"))
        client = HttpClient(config)
        with pytest.raises(RiotTimeoutError):
            await client.request("GET", "/timeout", PlatformRoute.NA1)
        await client.close()

    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        mock.get("/malformed").respond(200, content=b"{")
        client = HttpClient(config)
        with pytest.raises(MalformedResponseError):
            await client.request(
                "GET",
                "/malformed",
                PlatformRoute.NA1,
                response_adapter=None,
            )
        await client.close()

    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        mock.get("/invalid").respond(200, json={"value": "not-an-int"})
        client = HttpClient(config)
        with pytest.raises(ResponseValidationError):
            await client.request(
                "GET",
                "/invalid",
                PlatformRoute.NA1,
                response_adapter=_Result.model_validate,
            )
        await client.close()


@pytest.mark.asyncio
async def test_application_and_method_buckets_are_separate() -> None:
    limiter = _RecordingLimiter()
    config = RiotClientConfig(api_key="RGAPI-test")
    headers = {
        "X-App-Rate-Limit": "10:1",
        "X-App-Rate-Limit-Count": "1:1",
        "X-Method-Rate-Limit": "5:1",
        "X-Method-Rate-Limit-Count": "1:1",
    }
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        mock.get("/buckets").mock(
            side_effect=[
                httpx.Response(200, json={}, headers=headers),
                httpx.Response(200, json={}, headers=headers),
            ]
        )
        client = HttpClient(config, rate_limiter=limiter)
        for _ in range(2):
            await client.request(
                "GET",
                "/buckets",
                PlatformRoute.NA1,
                operation_id="test.getBuckets",
                cache=False,
            )
        await client.close()

    acquired_keys = [key for key, _ in limiter.acquires]
    assert sum(key.startswith("app:") for key in acquired_keys) == 2
    assert sum(key.startswith("method:") for key in acquired_keys) == 1
    updated_keys = [key for key, _, _ in limiter.updates]
    assert any(key.startswith("app:") for key in updated_keys)
    assert any(key.startswith("method:") for key in updated_keys)


@pytest.mark.asyncio
async def test_refreshing_rso_provider() -> None:
    now = 0.0
    refreshes: List[str] = []

    def clock() -> float:
        return now

    async def refresh(refresh_token: str) -> TokenResponse:
        refreshes.append(refresh_token)
        return TokenResponse(
            access_token="new-token",
            refresh_token="new-refresh",
            expires_in=20,
        )

    provider = RefreshingRsoTokenProvider(
        TokenResponse(
            access_token="old-token",
            refresh_token="old-refresh",
            expires_in=10,
        ),
        refresh,
        refresh_leeway=1,
        clock=clock,
    )

    assert await provider.get_token() == "old-token"
    now = 10
    assert await provider.get_token() == "new-token"
    assert refreshes == ["old-refresh"]

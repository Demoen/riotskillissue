import pytest
import respx
from httpx import Response
from riotskillissue.core.http import HttpClient, RateLimitError
from riotskillissue.core.types import Region

@pytest.mark.asyncio
async def test_http_retry_on_500(config):
    """Verify that the client retries on 500 errors."""
    
    # We rely on tenacity decorators on _execute_with_retry
    # To test this, we should mock the underlying httpx client
    
    async with respx.mock(base_url="https://na1.api.riotgames.com") as respx_mock:
        # Fail twice, then succeed
        route = respx_mock.get("/test").mock(side_effect=[
            Response(500),
            Response(500),
            Response(200, json={"ok": True})
        ])
        
        http_client = HttpClient(config)
        resp = await http_client.request("GET", "/test", Region.NA1)
        
        assert resp.status_code == 200
        assert resp.json() == {"ok": True}
        assert route.call_count == 3

@pytest.mark.asyncio
async def test_http_429_handling(config):
    """Verify that 429s are retried automatically with Retry-After."""
    
    async with respx.mock(base_url="https://na1.api.riotgames.com") as respx_mock:
        # 429 once, then succeed on retry
        route = respx_mock.get("/test").mock(side_effect=[
            Response(429, headers={"Retry-After": "0"}),
            Response(200, json={"ok": True})
        ])
        
        http_client = HttpClient(config)
        resp = await http_client.request("GET", "/test", Region.NA1)
        
        assert resp.status_code == 200
        assert resp.json() == {"ok": True}
        assert route.call_count == 2  # first 429, then success

@pytest.mark.asyncio
async def test_redis_limiter_init():
    """Verify RedisRateLimiter initializes and registers script."""
    # We can't easily test the script execution without real Redis or fakeredis,
    # but we can verify it attempts to connect.
    
    try:
        from riotskillissue.core.ratelimit import RedisRateLimiter
        # Stub the redis module
        import sys
        from unittest.mock import MagicMock
        
        mock_redis = MagicMock()
        mock_redis_client = MagicMock()
        mock_redis.from_url.return_value = mock_redis_client
        
        # Inject stub
        import riotskillissue.core.ratelimit as rl
        old_redis = rl.redis
        rl.redis = mock_redis
        
        limiter = RedisRateLimiter("redis://localhost")
        
        # Should have registered script
        assert mock_redis_client.register_script.called
        
        # Cleanup
        rl.redis = old_redis
        
    except ImportError:
        pytest.skip("redis not installed")

@pytest.mark.asyncio
async def test_malformed_response(config):
    """Verify behavior when riot sends garbage."""
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        mock.get("/garbage").respond(200, content=b"Not JSON")
        
        client = HttpClient(config)
        resp = await client.request("GET", "/garbage", "na1")
        
        with pytest.raises(Exception):
            resp.json()

@pytest.mark.asyncio
async def test_auth_header(config):
    """Verify API Key header is injected."""
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        route = mock.get("/auth-check").respond(200)
        
        client = HttpClient(config)
        await client.request("GET", "/auth-check", "na1")
        
        assert route.calls.last.request.headers["X-Riot-Token"] == config.api_key


@pytest.mark.asyncio
async def test_hooks_request_and_response(config):
    """Verify that request and response hooks are called."""
    request_calls = []
    response_calls = []

    async def on_request(method, url, kwargs):
        request_calls.append((method, url))

    async def on_response(resp):
        response_calls.append(resp.status_code)

    hooks = {"request": on_request, "response": on_response}

    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        mock.get("/hook-test").respond(200, json={"ok": True})

        client = HttpClient(config, hooks=hooks)
        await client.request("GET", "/hook-test", "na1")

        assert len(request_calls) == 1
        assert request_calls[0] == ("GET", "/hook-test")
        assert len(response_calls) == 1
        assert response_calls[0] == 200


@pytest.mark.asyncio
async def test_base_url_override(config):
    """Verify that base_url config overrides the default host."""
    from riotskillissue import RiotClientConfig

    custom_config = RiotClientConfig(
        api_key="RGAPI-TEST", base_url="https://custom.api.test"
    )

    async with respx.mock(base_url="https://custom.api.test") as mock:
        route = mock.get("/lol/test").respond(200, json={"ok": True})

        client = HttpClient(custom_config)
        resp = await client.request("GET", "/lol/test", "na1")

        assert resp.status_code == 200
        assert route.called


@pytest.mark.asyncio
async def test_client_repr(config):
    """Verify RiotClient repr masks the API key."""
    from riotskillissue import RiotClient

    async with RiotClient(config=config) as client:
        r = repr(client)
        assert "RGAPI-TE..." in r
        assert "RGAPI-TEST" not in r

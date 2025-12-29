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
    """Verify that 429s raise RateLimitError (or are handled)."""
    
    # By default implementation raises RateLimitError
    async with respx.mock(base_url="https://na1.api.riotgames.com") as respx_mock:
        respx_mock.get("/test").mock(return_value=Response(429, headers={"Retry-After": "1"}))
        
        http_client = HttpClient(config)
        
        # We expect a RateLimitError to be raised eventually or immediately
        # Our implementation raises it immediately inside _execute_with_retry if not retried by tenacity
        # Tenacity config in http.py: retry_if_exception_type((NetworkError, Timeout...))
        # It does NOT verify 429 status code for retry automatically unless we added it.
        # In http.py logic: "raise RateLimitError"
        
        with pytest.raises(RateLimitError) as exc:
            await http_client.request("GET", "/test", Region.NA1)
        
        assert exc.value.retry_after == 1.0

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

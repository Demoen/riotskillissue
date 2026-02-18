import pytest
import respx
import asyncio
import time
from httpx import Response, TimeoutException, NetworkError
from riotskillissue.core.http import HttpClient, ServerError, RateLimitError
from riotskillissue.core.ratelimit import MemoryRateLimiter, RateLimitBucket

@pytest.mark.asyncio
async def test_chaos_network(config):
    """Verify system survives packet loss / transient errors."""
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        # 1. Timeout, then Network Error, then Success
        mock.get("/chaos").mock(side_effect=[
            TimeoutException("Simulated Timeout"),
            NetworkError("Connection Reset"),
            Response(200, json={"survived": True})
        ])
        
        client = HttpClient(config)
        resp = await client.request("GET", "/chaos", "na1")
        assert resp.json()["survived"] is True

@pytest.mark.asyncio
async def test_rate_limit_thrashing(config):
    """Verify behavior under 429 pressure — retries until success."""
    
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        # Return 429 three times, then success.
        # Our new implementation sleeps Retry-After and retries automatically.
        mock.get("/thrash").mock(side_effect=[
            Response(429, headers={"Retry-After": "0"}),
            Response(429, headers={"Retry-After": "0"}),
            Response(429, headers={"Retry-After": "0"}),
            Response(200, json={"ok": True}),
        ])
        
        client = HttpClient(config)
        resp = await client.request("GET", "/thrash", "na1")
        assert resp.status_code == 200
        assert resp.json() == {"ok": True}

@pytest.mark.asyncio
async def test_memory_limiter_concurrency():
    """Verify MemoryRateLimiter handles concurrent acquire."""
    limiter = MemoryRateLimiter()
    bucket = [RateLimitBucket(limit=5, window=1)] # 5 req / 1 sec
    
    # Launch 10 tasks. First 5 should pass immediately. 6-10 should wait.
    start = time.time()
    
    async def task():
        await limiter.acquire("key", bucket)
        
    tasks = [task() for _ in range(10)]
    await asyncio.gather(*tasks)
    
    duration = time.time() - start
    # Should be slightly more than 1s because 6th request waits for window reset
    # This proves the limiter actually limited flow.
    # Note: sleep precision can be flaky, but > 0.5 is safe bet.
    assert duration > 0.5 

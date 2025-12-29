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
    """Verify behavior under massive 429 pressure."""
    # We want to ensure we don't spiral into infinite recursion or crash.
    
    async with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        # Return 429 ten times, then success.
        # Tenacity default config stops after 3.
        # So we expect a RateLimitError or generic retry error effectively.
        # Wait, our retry policy for httpx errors is stop_after_attempt(3).
        # We manually raise RateLimitError inside logic.
        # Does tenacity catch RateLimitError? NO. 
        # In http.py: retry_if_exception_type((Network... ServerError))
        # So 429 is propagated immediately.
        
        mock.get("/thrash").respond(429, headers={"Retry-After": "0.1"})
        
        client = HttpClient(config)
        with pytest.raises(RateLimitError):
            await client.request("GET", "/thrash", "na1")

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

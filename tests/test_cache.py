import pytest
import respx
import time
import asyncio
from httpx import Response
from riotskillissue.core.cache import MemoryCache, AbstractCache
from riotskillissue.core.types import Region
from riotskillissue import RiotClient, RiotClientConfig

@pytest.mark.asyncio
async def test_memory_cache(config):
    """Verify that requests are cached."""
    
    cache = MemoryCache()
    
    async with respx.mock(base_url="https://na1.api.riotgames.com") as respx_mock:
        # Mock returns different values to prove we didn't call it twice
        route = respx_mock.get("/test").mock(side_effect=[
            Response(200, json={"count": 1}),
            Response(200, json={"count": 2})
        ])
        
        async with RiotClient(config=config, cache=cache) as client:
            # First call: hits network
            resp1 = await client.http.request("GET", "/test", Region.NA1)
            assert resp1.json()["count"] == 1
            assert route.call_count == 1
            
            # Second call: hits cache
            resp2 = await client.http.request("GET", "/test", Region.NA1)
            assert resp2.json()["count"] == 1  # Still 1 because cached!
            assert route.call_count == 1       # Still 1 call!
            
            # Force verify cache stored it
            # params is empty dict, so key uses ""
            stored = await cache.get(f"GET:/test:{Region.NA1}:")
            assert stored is not None


@pytest.mark.asyncio
async def test_memory_cache_ttl_expiry():
    """Verify that cache entries expire after TTL."""
    cache = MemoryCache()

    await cache.set("key", "value", ttl=1)
    assert await cache.get("key") == "value"

    # Wait for TTL to expire
    await asyncio.sleep(1.1)
    assert await cache.get("key") is None


@pytest.mark.asyncio
async def test_memory_cache_lru_eviction():
    """Verify LRU eviction when cache exceeds max_size."""
    cache = MemoryCache(max_size=2)

    await cache.set("a", 1, ttl=60)
    await cache.set("b", 2, ttl=60)
    await cache.set("c", 3, ttl=60)  # Should evict "a"

    assert await cache.get("a") is None
    assert await cache.get("b") == 2
    assert await cache.get("c") == 3


@pytest.mark.asyncio
async def test_memory_cache_delete():
    """Verify explicit delete."""
    cache = MemoryCache()

    await cache.set("key", "value", ttl=60)
    await cache.delete("key")
    assert await cache.get("key") is None


@pytest.mark.asyncio
async def test_memory_cache_clear():
    """Verify clear removes all entries."""
    cache = MemoryCache()

    await cache.set("a", 1, ttl=60)
    await cache.set("b", 2, ttl=60)
    await cache.clear()

    assert await cache.get("a") is None
    assert await cache.get("b") is None

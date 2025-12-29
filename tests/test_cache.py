import pytest
import respx
import time
from httpx import Response
from riotskillissue.core.cache import MemoryCache, RedisCache, AbstractCache
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


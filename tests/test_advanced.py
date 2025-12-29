import pytest
import respx
from riotskillissue.core.pagination import paginate
from riotskillissue.static import DataDragonClient
from riotskillissue.auth import RsoClient, RsoConfig
from httpx import Response

@pytest.mark.asyncio
async def test_pagination():
    """Verify pagination helper yields all items."""
    
    # Mock function that mimics paginated API
    # Arg names must match what paginate uses (start, count)
    async def mock_api(start: int, count: int):
        # Return items [start, start+1, ...] up to count
        # Total limit 250 items available
        total_items = 250
        if start >= total_items:
            return []
        
        end = min(start + count, total_items)
        return list(range(start, end))

    items = []
    async for item in paginate(mock_api, count=100, max_results=250):
        items.append(item)
        
    assert len(items) == 250
    assert items[0] == 0
    assert items[-1] == 249

@pytest.mark.asyncio
async def test_datadragon():
    """Verify Data Dragon works with mocks."""
    client = DataDragonClient()
    
    async with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
        # Mock versions
        mock.get("/api/versions.json").respond(200, json=["14.1.1", "13.24.1"])
        
        # Mock champions
        mock.get("/cdn/14.1.1/data/en_US/champion.json").respond(200, json={
            "data": {
                "Annie": {"key": "1", "name": "Annie"}
            }
        })
        
        version = await client.get_latest_version()
        assert version == "14.1.1"
        
        annie = await client.get_champion(1)
        assert annie["name"] == "Annie"
        
        # Verify caching (mock shouldn't be called again if cached)
        # But we rely on AbstractCache default which is NoOpCache unless injected.
        # Here we used default so it WILL call again unless we inject MemoryCache.
        
@pytest.mark.asyncio
async def test_rso_flow():
    """Verify RSO URL generation and token exchange."""
    config = RsoConfig(
        client_id="id",
        client_secret="secret",
        redirect_uri="http://localhost/callback"
    )
    client = RsoClient(config)
    
    # 1. Auth URL
    url = client.get_auth_url()
    assert "client_id=id" in url
    assert "response_type=code" in url
    
    # 2. Token Exchange
    async with respx.mock(base_url="https://auth.riotgames.com") as mock:
        mock.post("/token").respond(200, json={
            "access_token": "at",
            "refresh_token": "rt",
            "id_token": "id",
            "expires_in": 3600,
            "scope": "openid"
        })
        
        tokens = await client.exchange_code("auth_code")
        assert tokens.access_token == "at"
        assert tokens.expires_in == 3600

@pytest.mark.asyncio
async def test_pagination_edge_cases():
    """Verify pagination robustly handles empty results, exact fits, etc."""
    
    # 1. Empty Result Loop
    async def empty_api(**kwargs): return []
    items = [x async for x in paginate(empty_api)]
    assert len(items) == 0

    # 2. Exact fit (count=10, Total=10)
    async def exact_api(start, count):
        if start >= 10: return []
        return list(range(start, min(start+count, 10)))

    items = [x async for x in paginate(exact_api, count=5)] # 2 pages of 5
    assert len(items) == 10
    
    # 3. Partial page (count=10, Total=5)
    async def partial_api(start, count):
        if start > 0: return []
        return [1, 2, 3, 4, 5]
        
    items = [x async for x in paginate(partial_api, count=10)]
    assert len(items) == 5

    # 4. Error Mid-stream
    call_count = 0
    async def error_api(start, count):
        nonlocal call_count
        call_count += 1
        if call_count == 2:
            raise ValueError("Boom")
        return [1]
        
    with pytest.raises(ValueError):
        async for x in paginate(error_api, count=1):
            pass

@pytest.mark.asyncio
async def test_datadragon_failures():
    """Verify Data Dragon reliability."""
    client = DataDragonClient() # No cache injected = NoOpCache
    
    async with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
        # Network Error on Version
        mock.get("/api/versions.json").mock(side_effect=Response(500))
        
        with pytest.raises(Exception):
             await client.get_latest_version()

        # Malformed JSON
        mock.get("/api/versions.json").respond(200, content=b"{") # Bad JSON
        
        with pytest.raises(Exception): # JSONDecodeError wrapped or propagated
             await client.get_latest_version()

@pytest.mark.asyncio
async def test_rso_failures():
    """Verify RSO error propagation."""
    config = RsoConfig(client_id="id", client_secret="s", redirect_uri="u")
    client = RsoClient(config)
    
    async with respx.mock(base_url="https://auth.riotgames.com") as mock:
        # 400 Bad Request (Invalid Code)
        mock.post("/token").respond(400, json={"error": "invalid_grant"})
        
        from riotskillissue.core.http import RiotAPIError
        with pytest.raises(RiotAPIError) as exc:
            await client.exchange_code("bad_code")
        assert exc.value.status == 400
        assert "invalid_grant" in exc.value.message

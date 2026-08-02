import pytest
import respx
from riotskillissue.core.cache import MemoryCache
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
        mock.get("/cdn/14.1.1/data/en_US/champion.json").respond(
            200, json={"data": {"Annie": {"key": "1", "name": "Annie"}}}
        )

        version = await client.get_latest_version()
        assert version == "14.1.1"

        annie = await client.get_champion(1)
        assert annie["name"] == "Annie"


@pytest.mark.asyncio
async def test_datadragon_resolves_historical_match_version():
    client = DataDragonClient()

    async with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
        mock.get("/api/versions.json").respond(
            200,
            json=["16.15.1", "16.14.2", "15.24.1", "14.1.1"],
        )
        mock.get("/cdn/15.24.1/data/en_US/item.json").respond(
            200,
            json={"data": {"1001": {"name": "Boots"}}},
        )

        version = await client.resolve_version("15.24.650.1234")
        items = await client.get_all_items(version=version)

    assert version == "15.24.1"
    assert items[1001]["name"] == "Boots"
    await client.close()


@pytest.mark.asyncio
async def test_datadragon_version_resolution_falls_back_to_latest():
    client = DataDragonClient()

    async with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
        route = mock.get("/api/versions.json").respond(
            200,
            json=["16.15.1", "16.14.2"],
        )

        resolved = await client.resolve_version("9.99.1")
        malformed = await client.resolve_version("not-a-version")

    assert resolved == "16.15.1"
    assert malformed == "16.15.1"
    assert route.call_count == 1
    await client.close()


@pytest.mark.asyncio
async def test_datadragon_version_cache_refreshes_after_ttl(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [1000.0]
    monkeypatch.setattr("riotskillissue.core.cache.time.time", lambda: clock[0])
    client = DataDragonClient(cache=MemoryCache())

    async with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
        route = mock.get("/api/versions.json").mock(
            side_effect=[
                Response(200, json=["16.15.1", "16.14.2"]),
                Response(200, json=["16.16.1", "16.15.1"]),
            ]
        )

        assert await client.get_versions() == ["16.15.1", "16.14.2"]
        assert await client.get_latest_version() == "16.15.1"
        assert await client.resolve_version("16.14.100.1") == "16.14.2"
        clock[0] += 3599
        assert await client.get_latest_version() == "16.15.1"
        assert route.call_count == 1

        clock[0] += 2
        assert await client.get_latest_version() == "16.16.1"
        assert await client.resolve_version("16.15.100.1") == "16.15.1"
        assert route.call_count == 2

    await client.close()


@pytest.mark.asyncio
async def test_datadragon_champion_detail_includes_abilities():
    client = DataDragonClient()

    async with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
        mock.get("/api/versions.json").respond(200, json=["16.15.1"])
        mock.get("/cdn/16.15.1/data/en_US/champion.json").respond(
            200,
            json={"data": {"Annie": {"id": "Annie", "key": "1"}}},
        )
        mock.get("/cdn/16.15.1/data/en_US/champion/Annie.json").respond(
            200,
            json={
                "data": {
                    "Annie": {
                        "id": "Annie",
                        "passive": {"name": "Pyromania"},
                        "spells": [{"name": "Disintegrate"}],
                    }
                }
            },
        )

        detail = await client.get_champion_detail(1)

    assert detail is not None
    assert detail["passive"]["name"] == "Pyromania"
    assert detail["spells"][0]["name"] == "Disintegrate"
    await client.close()


@pytest.mark.asyncio
async def test_datadragon_strict_version_resolution_normalizes_public_patch():
    client = DataDragonClient()

    async with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
        route = mock.get("/api/versions.json").respond(
            200,
            json=["16.15.1", "16.14.2"],
        )

        assert await client.resolve_version("26.15", strict=True) == "16.15.1"
        with pytest.raises(LookupError):
            await client.resolve_version("26.13", strict=True)
        with pytest.raises(ValueError):
            await client.resolve_version("not-a-version", strict=True)

    assert route.call_count == 1
    await client.close()


@pytest.mark.asyncio
async def test_datadragon_item_efficiency_uses_patch_component_baselines():
    client = DataDragonClient()
    items = {
        "1028": {
            "name": "Ruby Crystal",
            "gold": {"total": 400, "purchasable": True},
            "stats": {"FlatHPPoolMod": 150},
        },
        "1036": {
            "name": "Long Sword",
            "gold": {"total": 350, "purchasable": True},
            "stats": {"FlatPhysicalDamageMod": 10},
        },
        "1042": {
            "name": "Dagger",
            "gold": {"total": 250, "purchasable": True},
            "stats": {"PercentAttackSpeedMod": 0.1},
        },
        "2022": {
            "name": "Glowing Mote",
            "description": "Grants ability haste outside structured stats.",
            "gold": {"total": 250, "purchasable": True},
            "maps": {"11": True},
            "stats": {},
        },
        "9000": {
            "name": "Synthetic Blade",
            "description": "A passive that is deliberately not priced.",
            "gold": {"base": 900, "total": 3000, "sell": 2100, "purchasable": True},
            "maps": {"11": True},
            "stats": {
                "FlatPhysicalDamageMod": 50,
                "FlatHPPoolMod": 400,
                "PercentAttackSpeedMod": 0.2,
                "UnrepresentedStat": 5,
            },
        },
    }

    async with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
        mock.get("/api/versions.json").respond(200, json=["16.15.1"])
        item_route = mock.get("/cdn/16.15.1/data/en_US/item.json").respond(
            200,
            json={"data": items},
        )

        result = await client.get_item_efficiency(
            item_name="Synthetic Blade",
            game_version="26.15",
        )
        unrepresented = await client.get_item_efficiency(
            2022,
            game_version="26.15",
        )

    assert item_route.call_count == 1
    assert result["patch"] == {
        "requested": "26.15",
        "resolved_data_dragon_version": "16.15.1",
        "basis": "explicit_patch",
        "cross_patch_fallback": False,
    }
    assert result["item"]["id"] == 9000
    assert result["item"]["purchase_cost"] == 3000
    assert result["item"]["combine_cost"] == 900
    assert result["priced_base_stat_value"] == pytest.approx(3316.6667)
    assert result["raw_stat_efficiency_percent"] == pytest.approx(110.5556)
    assert {entry["stat"] for entry in result["priced_stats"]} == {
        "attack_damage",
        "health",
        "attack_speed",
    }
    assert result["unpriced_stats"] == [{"data_dragon_key": "UnrepresentedStat", "raw_amount": 5.0}]
    assert result["coverage"]["complete_for_all_item_effects"] is False
    assert unrepresented["priced_base_stat_value"] is None
    assert unrepresented["raw_stat_efficiency_percent"] is None
    assert unrepresented["coverage"]["calculation_status"] == ("no_priceable_structured_stats")
    await client.close()


@pytest.mark.asyncio
async def test_datadragon_item_efficiency_never_cross_patch_falls_back():
    client = DataDragonClient()

    async with respx.mock(
        base_url="https://ddragon.leagueoflegends.com",
        assert_all_called=False,
    ) as mock:
        mock.get("/api/versions.json").respond(200, json=["16.15.1"])
        item_route = mock.get("/cdn/16.15.1/data/en_US/item.json").respond(
            200,
            json={"data": {}},
        )

        with pytest.raises(LookupError):
            await client.get_item_efficiency(1036, game_version="15.24")

    assert item_route.call_count == 0
    await client.close()


@pytest.mark.asyncio
async def test_rso_flow():
    """Verify RSO URL generation and token exchange."""
    config = RsoConfig(
        client_id="id", client_secret="secret", redirect_uri="http://localhost/callback"
    )
    client = RsoClient(config)

    # 1. Auth URL (now returns a dict with url, state, code_verifier)
    auth_data = client.get_auth_url()
    assert isinstance(auth_data, dict)
    assert "url" in auth_data
    assert "state" in auth_data
    assert "code_verifier" in auth_data
    assert "client_id=id" in auth_data["url"]
    assert "response_type=code" in auth_data["url"]
    assert "state=" in auth_data["url"]
    assert "code_challenge=" in auth_data["url"]
    assert "code_challenge_method=S256" in auth_data["url"]

    # 2. Token Exchange
    async with respx.mock(base_url="https://auth.riotgames.com") as mock:
        mock.post("/token").respond(
            200,
            json={
                "access_token": "at",
                "refresh_token": "rt",
                "id_token": "id",
                "expires_in": 3600,
                "scope": "openid",
            },
        )

        tokens = await client.exchange_code("auth_code", code_verifier=auth_data["code_verifier"])
        assert tokens.access_token == "at"
        assert tokens.expires_in == 3600

    await client.close()


@pytest.mark.asyncio
async def test_pagination_edge_cases():
    """Verify pagination robustly handles empty results, exact fits, etc."""

    # 1. Empty Result Loop
    async def empty_api(**kwargs):
        return []

    items = [x async for x in paginate(empty_api)]
    assert len(items) == 0

    # 2. Exact fit (count=10, Total=10)
    async def exact_api(start, count):
        if start >= 10:
            return []
        return list(range(start, min(start + count, 10)))

    items = [x async for x in paginate(exact_api, count=5)]  # 2 pages of 5
    assert len(items) == 10

    # 3. Partial page (count=10, Total=5)
    async def partial_api(start, count):
        if start > 0:
            return []
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
    client = DataDragonClient()  # No cache injected = NoOpCache

    async with respx.mock(base_url="https://ddragon.leagueoflegends.com") as mock:
        # Network Error on Version
        mock.get("/api/versions.json").mock(side_effect=Response(500))

        with pytest.raises(Exception):
            await client.get_latest_version()

        # Malformed JSON
        mock.get("/api/versions.json").respond(200, content=b"{")  # Bad JSON

        with pytest.raises(Exception):  # JSONDecodeError wrapped or propagated
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

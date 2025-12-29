import pytest
import respx
from httpx import Response
from riotskillissue import RiotClient, RiotClientConfig
from riotskillissue.core.types import Region, Platform

@pytest.mark.asyncio
async def test_summoner_by_puuid(client):
    """Test the generated summoner.get_by_puuid binding."""
    
    # We use get_by_puuid because get_by_name is gone in v4
    async with respx.mock(base_url="https://na1.api.riotgames.com") as respx_mock:
        route = respx_mock.get("/lol/summoner/v4/summoners/by-puuid/12345").mock(
            return_value=Response(200, json={
                "id": "123", 
                "accountId": "456", 
                "puuid": "12345", 
                "name": "Faker", 
                "profileIconId": 1, 
                "revisionDate": 123456, 
                "summonerLevel": 100
            })
        )
        
        # Generated method should now be get_by_puuid (snake_case of getByPUUID)
        summoner = await client.summoner.get_by_puuid(
            region=Region.NA1,
            encryptedPUUID="12345"
        )
        
        assert route.called
        # assert summoner.name == "Faker" # 'name' field removed in latest spec
        assert summoner.summonerLevel == 100

@pytest.mark.asyncio
async def test_match_ids_by_puuid(client):
    """Test match list binding."""
    
    async with respx.mock(base_url="https://americas.api.riotgames.com") as respx_mock:
        route = respx_mock.get("/lol/match/v5/matches/by-puuid/12345/ids").mock(
            return_value=Response(200, json=["NA1_1", "NA1_2"])
        )
        
        # Matches v5 uses platform explicitly in URL
        matches = await client.match.get_match_ids_by_puuid(
            region=Platform.AMERICAS, # Correct platform
            puuid="12345",
            start=0,
            count=20
        )
        
        assert route.called
        assert len(matches) == 2
        assert matches[0] == "NA1_1"

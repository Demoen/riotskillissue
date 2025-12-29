from contextlib import asynccontextmanager
import respx
from httpx import Response
from typing import Dict, Any, Union, Optional
from .core.client import RiotClient

class RiotMock:
    """
    Mock server utility for testing Riot API integrations.
    Wraps respx for easier Riot-specific mocking.
    """
    def __init__(self):
        self.mocker = respx.mock
        
    @asynccontextmanager
    async def configure(self, base_url: str = "https://na1.api.riotgames.com"):
        """
        Context manager to mock API calls.
        
        Usage:
            mock = RiotMock()
            async with mock.configure() as m:
                m.get("/lol/summoner/v4/summoners/by-name/Faker").respond(200, json={...})
                # run client code
        """
        async with self.mocker(base_url=base_url) as mock:
            yield mock
            
    # Helpers for common mocks
    @staticmethod
    def mock_summoner(mock: respx.MockRouter, puuid: str, region: str = "na1", level: int = 30):
        """Helper to mock a summoner response."""
        return mock.get(f"/lol/summoner/v4/summoners/by-puuid/{puuid}").respond(
            200, 
            json={
                "id": "summ_id",
                "accountId": "acc_id",
                "puuid": puuid,
                "name": "MockSummoner",
                "profileIconId": 1,
                "revisionDate": 1600000000000,
                "summonerLevel": level
            }
        )

__all__ = ["RiotMock"]

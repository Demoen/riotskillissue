import pytest
import respx
from httpx import Response
from riotskillissue import SyncRiotClient, RiotClientConfig
from riotskillissue.core.types import PlatformRoute


@pytest.fixture
def sync_config():
    return RiotClientConfig(api_key="RGAPI-TEST-SYNC")


def test_sync_client_context_manager(sync_config):
    """Verify SyncRiotClient works as a context manager."""
    with SyncRiotClient(config=sync_config) as client:
        assert client.config.api_key == "RGAPI-TEST-SYNC"


def test_sync_client_repr(sync_config):
    """Verify SyncRiotClient.__repr__ wraps the async client repr."""
    with SyncRiotClient(config=sync_config) as client:
        r = repr(client)
        assert "SyncRiotClient" in r
        assert "default_route=" in r


def test_sync_client_api_call(sync_config):
    """Verify a synchronous API call through the proxy."""
    with respx.mock(base_url="https://na1.api.riotgames.com") as mock:
        mock.get("/lol/summoner/v4/summoners/by-puuid/test-puuid").respond(
            200,
            json={
                "id": "123",
                "accountId": "456",
                "puuid": "test-puuid",
                "profileIconId": 1,
                "revisionDate": 123456,
                "summonerLevel": 42,
            },
        )

        with SyncRiotClient(config=sync_config) as client:
            summoner = client.raw.lol.summoner.get_by_puuid(
                route=PlatformRoute.NA1,
                encrypted_puuid="test-puuid",
            )
            assert summoner.summoner_level == 42
            assert summoner.puuid == "test-puuid"


def test_sync_client_close(sync_config):
    """Verify explicit close() works."""
    client = SyncRiotClient(config=sync_config)
    client.close()
    # Should not raise after close

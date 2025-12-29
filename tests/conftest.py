import pytest
from riotskillissue import RiotClient, RiotClientConfig

@pytest.fixture
def config():
    return RiotClientConfig(api_key="RGAPI-TEST")

@pytest.fixture
async def client(config):
    async with RiotClient(config=config) as c:
        yield c

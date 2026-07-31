from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import respx


class RiotMock:
    def __init__(self) -> None:
        self.mocker = respx.mock

    @asynccontextmanager
    async def configure(
        self,
        base_url: str = "https://na1.api.riotgames.com",
    ) -> AsyncIterator[respx.MockRouter]:
        async with self.mocker(base_url=base_url) as mock:
            yield mock

    @staticmethod
    def mock_summoner(
        mock: respx.MockRouter,
        puuid: str,
        *,
        level: int = 30,
    ) -> respx.Route:
        return mock.get(f"/lol/summoner/v4/summoners/by-puuid/{puuid}").respond(
            200,
            json={
                "id": "summ_id",
                "puuid": puuid,
                "profileIconId": 1,
                "revisionDate": 1600000000000,
                "summonerLevel": level,
            },
        )


__all__ = ["RiotMock"]

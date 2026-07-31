import asyncio

from riotskillissue import PlatformRoute, RiotClient


async def main() -> None:
    async with RiotClient(
        api_key="RGAPI-MOCK",
        default_route=PlatformRoute.EUW1,
    ) as riot:
        print(riot.lol)
        print(riot.raw.lol.match)
        print(riot.raw.valorant.content)


if __name__ == "__main__":
    asyncio.run(main())

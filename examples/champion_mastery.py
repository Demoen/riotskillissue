import asyncio

from riotskillissue import PlatformRoute, RiotClient


async def main() -> None:
    async with RiotClient(default_route=PlatformRoute.EUW1) as riot:
        masteries = await riot.lol.champion_mastery("Player#EUW", count=10)
        for mastery in masteries:
            print(mastery)


if __name__ == "__main__":
    asyncio.run(main())

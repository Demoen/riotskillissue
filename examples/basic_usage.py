import asyncio

from riotskillissue import PlatformRoute, RiotClient


async def main() -> None:
    async with RiotClient(default_route=PlatformRoute.EUW1) as riot:
        profile = await riot.lol.player_profile("Player#EUW")
        print(profile.model_dump())


if __name__ == "__main__":
    asyncio.run(main())

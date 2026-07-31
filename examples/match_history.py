import asyncio

from riotskillissue import PlatformRoute, RiotClient


async def main() -> None:
    async with RiotClient(default_route=PlatformRoute.EUW1) as riot:
        history = await riot.lol.match_history("Player#EUW", count=5)
        for match in history:
            print(match.match_id, match.won, match.duration_seconds)


if __name__ == "__main__":
    asyncio.run(main())

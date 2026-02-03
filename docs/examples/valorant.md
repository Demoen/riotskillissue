# VALORANT Examples

Working examples for the VALORANT API endpoints.

!!! note "API Access"
    VALORANT match data requires special API access. Content and status endpoints are publicly available.

## Content Data

Get VALORANT content (agents, maps, game modes):

```python
import asyncio
from riotskillissue import RiotClient, Region

async def main():
    async with RiotClient() as client:
        content = await client.val_content.get_content(
            region=Region.EUW1
        )
        
        print(f"VALORANT Version: {content.version}")
        
        # List agents
        print("\nAgents:")
        for agent in content.characters[:5]:
            print(f"  - {agent.name}")
        
        # List maps
        print("\nMaps:")
        for m in content.maps:
            print(f"  - {m.name}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Platform Status

Check VALORANT server status:

```python
import asyncio
from riotskillissue import RiotClient, Region

async def main():
    async with RiotClient() as client:
        status = await client.val_status.get_platform_data(
            region=Region.EUW1
        )
        
        print(f"Platform: {status.name}")
        print(f"Locales: {', '.join(status.locales)}")
        
        if status.maintenances:
            print("\nActive Maintenances:")
            for m in status.maintenances:
                print(f"  - {m.titles[0].content if m.titles else 'Unknown'}")
        
        if status.incidents:
            print("\nActive Incidents:")
            for i in status.incidents:
                print(f"  - {i.titles[0].content if i.titles else 'Unknown'}")
        
        if not status.maintenances and not status.incidents:
            print("\nAll systems operational.")

if __name__ == "__main__":
    asyncio.run(main())
```

## Ranked Leaderboard

Get VALORANT ranked leaderboard (requires special API access):

```python
import asyncio
from riotskillissue import RiotClient, Region

async def main():
    async with RiotClient() as client:
        try:
            leaderboard = await client.val_ranked.get_leaderboard(
                region=Region.EUW1,
                actId="current"  # Replace with actual act ID
            )
            
            print(f"Leaderboard entries: {len(leaderboard.players)}")
            
            for player in leaderboard.players[:10]:
                print(f"{player.leaderboardRank}. {player.gameName}#{player.tagLine}")
                print(f"   Rating: {player.rankedRating}")
                
        except Exception as e:
            print(f"Note: Ranked API requires special access - {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Account Lookup

Look up a VALORANT player by Riot ID:

```python
import asyncio
from riotskillissue import RiotClient, Platform

async def main():
    async with RiotClient() as client:
        # VALORANT uses the same account API
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Player",
            tagLine="EUW"
        )
        
        print(f"Account: {account.gameName}#{account.tagLine}")
        print(f"PUUID: {account.puuid}")

if __name__ == "__main__":
    asyncio.run(main())
```

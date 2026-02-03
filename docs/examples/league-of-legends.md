# League of Legends Examples

Working examples for the League of Legends API endpoints.

## Account Lookup

Look up a player by their Riot ID:

```python
import asyncio
from riotskillissue import RiotClient, Platform

async def main():
    async with RiotClient() as client:
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Agurin",
            tagLine="EUW"
        )
        print(f"Account: {account.gameName}#{account.tagLine}")
        print(f"PUUID: {account.puuid}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Summoner Data

Get summoner profile information:

```python
import asyncio
from riotskillissue import RiotClient, Platform, Region

async def main():
    async with RiotClient() as client:
        # First get the account
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Agurin",
            tagLine="EUW"
        )
        
        # Then get summoner data
        summoner = await client.summoner.get_by_puuid(
            region=Region.EUW1,
            encryptedPUUID=account.puuid
        )
        
        print(f"Summoner Level: {summoner.summonerLevel}")
        print(f"Profile Icon ID: {summoner.profileIconId}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Match History

Fetch recent matches for a player:

```python
import asyncio
from riotskillissue import RiotClient, Platform

async def main():
    async with RiotClient() as client:
        # Get account
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Agurin",
            tagLine="EUW"
        )
        
        # Get last 5 match IDs
        match_ids = await client.match.get_match_ids_by_puuid(
            region=Platform.EUROPE,
            puuid=account.puuid,
            count=5
        )
        
        print(f"Recent matches: {len(match_ids)}")
        for match_id in match_ids:
            print(f"  - {match_id}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Match Details

Get detailed information about a specific match:

```python
import asyncio
from riotskillissue import RiotClient, Platform

async def main():
    async with RiotClient() as client:
        # Get match by ID
        match = await client.match.get_match(
            region=Platform.EUROPE,
            matchId="EUW1_7654321098"  # Replace with real match ID
        )
        
        print(f"Game Mode: {match.info.gameMode}")
        print(f"Duration: {match.info.gameDuration // 60} minutes")
        print(f"Queue ID: {match.info.queueId}")
        
        # Print participants
        print("\nParticipants:")
        for p in match.info.participants:
            kda = f"{p.kills}/{p.deaths}/{p.assists}"
            print(f"  {p.championName}: {p.summonerName} - {kda}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Paginated Match History

Use the pagination helper for large match history fetches:

```python
import asyncio
from riotskillissue import RiotClient, Platform, paginate

async def main():
    async with RiotClient() as client:
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Agurin",
            tagLine="EUW"
        )
        
        # Fetch up to 50 matches using pagination
        count = 0
        async for match_id in paginate(
            client.match.get_match_ids_by_puuid,
            region=Platform.EUROPE,
            puuid=account.puuid,
            count=20,
            max_results=50
        ):
            count += 1
            print(f"{count}. {match_id}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Champion Mastery

Get a player's champion mastery data:

```python
import asyncio
from riotskillissue import RiotClient, Platform, Region

async def main():
    async with RiotClient() as client:
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Agurin",
            tagLine="EUW"
        )
        
        summoner = await client.summoner.get_by_puuid(
            region=Region.EUW1,
            encryptedPUUID=account.puuid
        )
        
        # Get top champion masteries
        masteries = await client.champion_mastery.get_all_masteries(
            region=Region.EUW1,
            encryptedPUUID=account.puuid
        )
        
        print("Top 5 Champions:")
        for m in masteries[:5]:
            print(f"  Champion {m.championId}: Level {m.championLevel} ({m.championPoints:,} pts)")

if __name__ == "__main__":
    asyncio.run(main())
```

## Live Game (Spectator)

Check if a player is currently in game:

```python
import asyncio
from riotskillissue import RiotClient, Platform, Region

async def main():
    async with RiotClient() as client:
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Agurin",
            tagLine="EUW"
        )
        
        try:
            game = await client.spectator.get_current_game_info(
                region=Region.EUW1,
                encryptedPUUID=account.puuid
            )
            print(f"Currently in game!")
            print(f"Game Mode: {game.gameMode}")
            print(f"Game Length: {game.gameLength // 60} minutes")
        except Exception as e:
            print("Player is not currently in a game.")

if __name__ == "__main__":
    asyncio.run(main())
```

## League Standings

Get ranked league entries:

```python
import asyncio
from riotskillissue import RiotClient, Platform, Region

async def main():
    async with RiotClient() as client:
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Agurin",
            tagLine="EUW"
        )
        
        summoner = await client.summoner.get_by_puuid(
            region=Region.EUW1,
            encryptedPUUID=account.puuid
        )
        
        entries = await client.league.get_entries_by_summoner(
            region=Region.EUW1,
            encryptedSummonerId=summoner.id
        )
        
        for entry in entries:
            print(f"{entry.queueType}:")
            print(f"  Rank: {entry.tier} {entry.rank} ({entry.leaguePoints} LP)")
            print(f"  Record: {entry.wins}W / {entry.losses}L")

if __name__ == "__main__":
    asyncio.run(main())
```

## Static Data (Data Dragon)

Get champion and item static data:

```python
import asyncio
from riotskillissue import RiotClient

async def main():
    async with RiotClient() as client:
        # Get champion data by ID
        annie = await client.static.get_champion(1)
        print(f"Champion: {annie['name']}")
        print(f"Title: {annie['title']}")
        
        # Get item data by ID  
        dorans_blade = await client.static.get_item(1055)
        print(f"\nItem: {dorans_blade['name']}")
        print(f"Cost: {dorans_blade['gold']['total']} gold")

if __name__ == "__main__":
    asyncio.run(main())
```

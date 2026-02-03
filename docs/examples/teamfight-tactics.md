# Teamfight Tactics Examples

Working examples for the TFT API endpoints.

## TFT Summoner Data

Get TFT-specific summoner information:

```python
import asyncio
from riotskillissue import RiotClient, Platform, Region

async def main():
    async with RiotClient() as client:
        # Get account
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Player",
            tagLine="EUW"
        )
        
        # Get TFT summoner data
        summoner = await client.tft_summoner.get_by_puuid(
            region=Region.EUW1,
            encryptedPUUID=account.puuid
        )
        
        print(f"Summoner Level: {summoner.summonerLevel}")

if __name__ == "__main__":
    asyncio.run(main())
```

## TFT Match History

Fetch recent TFT matches:

```python
import asyncio
from riotskillissue import RiotClient, Platform

async def main():
    async with RiotClient() as client:
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Player",
            tagLine="EUW"
        )
        
        # Get recent TFT match IDs
        match_ids = await client.tft_match.get_match_ids_by_puuid(
            region=Platform.EUROPE,
            puuid=account.puuid,
            count=10
        )
        
        print(f"Recent TFT matches: {len(match_ids)}")
        for match_id in match_ids:
            print(f"  - {match_id}")

if __name__ == "__main__":
    asyncio.run(main())
```

## TFT Match Details

Get detailed information about a TFT match:

```python
import asyncio
from riotskillissue import RiotClient, Platform

async def main():
    async with RiotClient() as client:
        account = await client.account.get_by_riot_id(
            region=Platform.EUROPE,
            gameName="Player",
            tagLine="EUW"
        )
        
        # Get most recent match
        match_ids = await client.tft_match.get_match_ids_by_puuid(
            region=Platform.EUROPE,
            puuid=account.puuid,
            count=1
        )
        
        if match_ids:
            match = await client.tft_match.get_match(
                region=Platform.EUROPE,
                matchId=match_ids[0]
            )
            
            print(f"Game Version: {match.info.game_version}")
            print(f"Queue ID: {match.info.queue_id}")
            
            # Find our player in the match
            for participant in match.info.participants:
                if participant.puuid == account.puuid:
                    print(f"\nYour placement: {participant.placement}")
                    print(f"Level: {participant.level}")
                    print(f"Gold left: {participant.gold_left}")

if __name__ == "__main__":
    asyncio.run(main())
```

## TFT Ranked Leaderboard

Get challenger league entries:

```python
import asyncio
from riotskillissue import RiotClient, Region

async def main():
    async with RiotClient() as client:
        # Get TFT Challenger league
        league = await client.tft_league.get_challenger_league(
            region=Region.EUW1
        )
        
        print(f"TFT Challenger League - {league.tier}")
        print(f"Total players: {len(league.entries)}")
        
        # Sort by LP and print top 10
        sorted_entries = sorted(
            league.entries, 
            key=lambda e: e.leaguePoints, 
            reverse=True
        )
        
        print("\nTop 10 Players:")
        for i, entry in enumerate(sorted_entries[:10], 1):
            print(f"{i}. {entry.summonerName}: {entry.leaguePoints} LP")

if __name__ == "__main__":
    asyncio.run(main())
```

## TFT Platform Status

Check TFT server status:

```python
import asyncio
from riotskillissue import RiotClient, Region

async def main():
    async with RiotClient() as client:
        status = await client.tft_status.get_platform_data(
            region=Region.EUW1
        )
        
        print(f"Platform: {status.name}")
        print(f"Locales: {', '.join(status.locales)}")
        
        if status.maintenances:
            print("\nActive Maintenances:")
            for m in status.maintenances:
                print(f"  - {m.titles[0].content if m.titles else 'Unknown'}")
        else:
            print("\nNo active maintenances.")

if __name__ == "__main__":
    asyncio.run(main())
```

"""
RiotSkillIssue - Match History Example

Demonstrates fetching and processing match history with pagination.

Usage:
    1. Set RIOT_API_KEY environment variable
    2. Run: python match_history.py
"""

import asyncio
import os
from riotskillissue import RiotClient, Platform, paginate


async def main():
    if not os.getenv("RIOT_API_KEY"):
        print("Error: RIOT_API_KEY environment variable not set")
        return

    async with RiotClient() as client:
        print("Looking up account...")
        
        try:
            account = await client.account.get_by_riot_id(
                region=Platform.EUROPE,
                gameName="Agurin",
                tagLine="EUW"
            )
            
            print(f"Found: {account.gameName}#{account.tagLine}")
            print("\nFetching match history...")
            
            # Get last 5 matches
            match_ids = await client.match.get_match_ids_by_puuid(
                region=Platform.EUROPE,
                puuid=account.puuid,
                count=5
            )
            
            print(f"\nLast {len(match_ids)} matches:")
            
            for match_id in match_ids:
                match = await client.match.get_match(
                    region=Platform.EUROPE,
                    matchId=match_id
                )
                
                # Find the player in the match
                for p in match.info.participants:
                    if p.puuid == account.puuid:
                        kda = f"{p.kills}/{p.deaths}/{p.assists}"
                        result = "WIN" if p.win else "LOSS"
                        print(f"  {match_id}")
                        print(f"    {p.championName} - {kda} - {result}")
                        break
                        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

"""
RiotSkillIssue - Champion Mastery Example

Demonstrates fetching champion mastery data with static data integration.

Usage:
    1. Set RIOT_API_KEY environment variable
    2. Run: python champion_mastery.py
"""

import asyncio
import os
from riotskillissue import RiotClient, Platform, Region


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
            print("\nFetching champion mastery...")
            
            # Get all masteries
            masteries = await client.champion_mastery.get_all_masteries(
                region=Region.EUW1,
                encryptedPUUID=account.puuid
            )
            
            print(f"\nTop 10 Champions (out of {len(masteries)}):")
            print("-" * 50)
            
            for i, m in enumerate(masteries[:10], 1):
                # Get champion name from static data
                champion = await client.static.get_champion(m.championId)
                name = champion["name"] if champion else f"Champion {m.championId}"
                
                # Format mastery points
                points = f"{m.championPoints:,}"
                
                print(f"{i:2}. {name:15} | Level {m.championLevel} | {points:>10} pts")
                
            # Calculate total mastery score
            total_points = sum(m.championPoints for m in masteries)
            print("-" * 50)
            print(f"Total Mastery Points: {total_points:,}")
                
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

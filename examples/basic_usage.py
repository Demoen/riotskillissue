"""
RiotSkillIssue - Basic Usage Example

Demonstrates account lookup and summoner data retrieval.

Usage:
    1. Set RIOT_API_KEY environment variable
    2. Run: python basic_usage.py
"""

import asyncio
import os
from riotskillissue import RiotClient, Platform, Region


async def main():
    # Check for API key
    if not os.getenv("RIOT_API_KEY"):
        print("Error: RIOT_API_KEY environment variable not set")
        print("Get your key at: https://developer.riotgames.com/")
        return

    async with RiotClient() as client:
        # Example: Look up a known player
        print("Looking up account...")
        
        try:
            account = await client.account.get_by_riot_id(
                region=Platform.EUROPE,
                gameName="Agurin",
                tagLine="EUW"
            )
            
            print(f"Account: {account.gameName}#{account.tagLine}")
            print(f"PUUID: {account.puuid[:20]}...")
            
            # Get summoner data
            print("\nFetching summoner data...")
            summoner = await client.summoner.get_by_puuid(
                region=Region.EUW1,
                encryptedPUUID=account.puuid
            )
            
            print(f"Summoner Level: {summoner.summonerLevel}")
            print(f"Profile Icon ID: {summoner.profileIconId}")
            
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

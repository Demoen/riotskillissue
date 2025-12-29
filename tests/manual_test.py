import asyncio
import logging
from riotskillissue import RiotClient, RiotClientConfig

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    print("Initializing RiotClient...")
    # Mock config
    config = RiotClientConfig(api_key="RGAPI-MOCK")
    
    async with RiotClient(config=config) as client:
        print("Client initialized.")
        
        # Check if attributes exist
        if hasattr(client, "summoner"):
            print("✅ client.summoner exists")
        else:
            print("❌ client.summoner MISSING")
            
        if hasattr(client, "match"):
            print("✅ client.match exists")
        else:
            print("❌ client.match MISSING")

        print("Verification complete.")

if __name__ == "__main__":
    asyncio.run(main())

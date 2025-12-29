from typing import Optional, Dict, Any, List
import httpx
from .core.cache import AbstractCache, NoOpCache

class DataDragonClient:
    """
    Client for Riot's Data Dragon static data service.
    Automatically handles versioning and caching.
    """
    params = {} # No auth needed

    def __init__(self, cache: Optional[AbstractCache] = None):
        self.base_url = "https://ddragon.leagueoflegends.com"
        self.http = httpx.AsyncClient()
        self.cache = cache or NoOpCache()
        self.version: Optional[str] = None
    
    async def get_latest_version(self) -> str:
        """Fetch the latest version of Data Dragon."""
        if self.version:
            return self.version
            
        cache_key = "ddragon:version"
        cached = await self.cache.get(cache_key)
        if cached:
            self.version = cached
            return cached
            
        resp = await self.http.get(f"{self.base_url}/api/versions.json")
        versions = resp.json()
        latest = versions[0]
        
        await self.cache.set(cache_key, latest, ttl=3600) # Cache for 1 hour
        self.version = latest
        return latest

    async def get_champion(self, champion_key: int) -> Optional[Dict[str, Any]]:
        """
        Get champion data by ID (key).
        e.g. 1 -> Annie
        """
        version = await self.get_latest_version()
        
        # We need to fetch the full champion list to map ID -> Data
        # Ideally we cache this heavy object
        cache_key = f"ddragon:{version}:champions"
        
        champions_map = await self.cache.get(cache_key)
        if not champions_map:
            resp = await self.http.get(f"{self.base_url}/cdn/{version}/data/en_US/champion.json")
            data = resp.json()["data"]
            
            # Map by "key" (ID) which is string in JSON but usually treated as int
            champions_map = {int(c["key"]): c for c in data.values()}
            await self.cache.set(cache_key, champions_map, ttl=86400) # Cache for 24h
            
        return champions_map.get(champion_key)
    
    async def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get item data by ID."""
        version = await self.get_latest_version()
        cache_key = f"ddragon:{version}:items"
        
        items_map = await self.cache.get(cache_key)
        if not items_map:
            resp = await self.http.get(f"{self.base_url}/cdn/{version}/data/en_US/item.json")
            data = resp.json()["data"]
            items_map = {int(k): v for k, v in data.items()}
            await self.cache.set(cache_key, items_map, ttl=86400)
            
        return items_map.get(item_id)

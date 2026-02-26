from typing import Optional, Dict, Any, List, Type
from types import TracebackType
import logging
import httpx
from .core.cache import AbstractCache, NoOpCache

logger = logging.getLogger(__name__)


class DataDragonClient:
    """Client for Riot's Data Dragon static data service.

    Automatically resolves the latest patch version and caches
    heavy responses (champions, items, runes, summoner spells, etc.).
    """

    COMMUNITY_DRAGON = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default"

    def __init__(self, cache: Optional[AbstractCache] = None):
        self.base_url = "https://ddragon.leagueoflegends.com"
        self.http = httpx.AsyncClient()
        self.cache = cache or NoOpCache()
        self.version: Optional[str] = None

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self.http.aclose()

    async def __aenter__(self) -> "DataDragonClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    # -- Version -------------------------------------------------------------

    async def get_latest_version(self) -> str:
        """Fetch the latest Data Dragon patch version."""
        if self.version:
            return self.version

        cache_key = "ddragon:version"
        cached = await self.cache.get(cache_key)
        if cached:
            self.version = cached
            return cached

        resp = await self.http.get(f"{self.base_url}/api/versions.json")
        resp.raise_for_status()
        versions = resp.json()
        latest = versions[0]

        await self.cache.set(cache_key, latest, ttl=3600)  # 1 hour
        self.version = latest
        return latest

    # -- Generic fetch helper ------------------------------------------------

    async def _fetch_map(
        self, cache_suffix: str, url_path: str, key_fn: Any = None
    ) -> Dict:
        """Fetch a JSON resource, cache it, and return the map."""
        version = await self.get_latest_version()
        cache_key = f"ddragon:{version}:{cache_suffix}"

        data_map = await self.cache.get(cache_key)
        if data_map is not None:
            return data_map

        url = f"{self.base_url}/cdn/{version}/data/en_US/{url_path}"
        resp = await self.http.get(url)
        resp.raise_for_status()
        data = resp.json()["data"]

        if key_fn:
            data_map = key_fn(data)
        else:
            data_map = data

        await self.cache.set(cache_key, data_map, ttl=86400)  # 24 hours
        return data_map

    # -- Champions -----------------------------------------------------------

    async def get_champion(self, champion_key: int) -> Optional[Dict[str, Any]]:
        """Get champion data by numeric key (e.g. 1 -> Annie)."""
        champions = await self._fetch_map(
            "champions",
            "champion.json",
            key_fn=lambda d: {int(c["key"]): c for c in d.values()},
        )
        return champions.get(champion_key)

    async def get_all_champions(self) -> Dict[int, Dict[str, Any]]:
        """Return all champions keyed by numeric ID."""
        return await self._fetch_map(
            "champions",
            "champion.json",
            key_fn=lambda d: {int(c["key"]): c for c in d.values()},
        )

    # -- Items ---------------------------------------------------------------

    async def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Get item data by ID."""
        items = await self._fetch_map(
            "items",
            "item.json",
            key_fn=lambda d: {int(k): v for k, v in d.items()},
        )
        return items.get(item_id)

    async def get_all_items(self) -> Dict[int, Dict[str, Any]]:
        """Return all items keyed by numeric ID."""
        return await self._fetch_map(
            "items",
            "item.json",
            key_fn=lambda d: {int(k): v for k, v in d.items()},
        )

    # -- Summoner Spells -----------------------------------------------------

    async def get_summoner_spells(self) -> Dict[int, Dict[str, Any]]:
        """Return all summoner spells keyed by numeric key."""
        return await self._fetch_map(
            "summoner_spells",
            "summoner.json",
            key_fn=lambda d: {int(s["key"]): s for s in d.values()},
        )

    async def get_summoner_spell(self, spell_key: int) -> Optional[Dict[str, Any]]:
        """Get a single summoner spell by numeric key."""
        spells = await self.get_summoner_spells()
        return spells.get(spell_key)

    # -- Runes ---------------------------------------------------------------

    async def get_runes(self) -> List[Dict[str, Any]]:
        """Return the full rune tree list."""
        version = await self.get_latest_version()
        cache_key = f"ddragon:{version}:runes"

        cached = await self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{self.base_url}/cdn/{version}/data/en_US/runesReforged.json"
        resp = await self.http.get(url)
        resp.raise_for_status()
        runes = resp.json()

        await self.cache.set(cache_key, runes, ttl=86400)
        return runes

    # -- Queues / Maps / Game Modes ------------------------------------------

    async def get_queues(self) -> List[Dict[str, Any]]:
        """Return queue metadata (id, map, description, notes)."""
        cache_key = "ddragon:queues"
        cached = await self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = "https://static.developer.riotgames.com/docs/lol/queues.json"
        resp = await self.http.get(url)
        resp.raise_for_status()
        queues = resp.json()

        await self.cache.set(cache_key, queues, ttl=86400)
        return queues

    async def get_maps(self) -> List[Dict[str, Any]]:
        """Return map metadata."""
        cache_key = "ddragon:maps"
        cached = await self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = "https://static.developer.riotgames.com/docs/lol/maps.json"
        resp = await self.http.get(url)
        resp.raise_for_status()
        maps = resp.json()

        await self.cache.set(cache_key, maps, ttl=86400)
        return maps

    async def get_game_modes(self) -> List[Dict[str, Any]]:
        """Return game mode metadata."""
        cache_key = "ddragon:gamemodes"
        cached = await self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = "https://static.developer.riotgames.com/docs/lol/gameModes.json"
        resp = await self.http.get(url)
        resp.raise_for_status()
        modes = resp.json()

        await self.cache.set(cache_key, modes, ttl=86400)
        return modes

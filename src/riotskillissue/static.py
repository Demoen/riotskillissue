from collections.abc import Awaitable, Callable
from typing import Optional, Dict, Any, List, Type
from types import TracebackType
import logging
import re
import httpx
from .core.cache import AbstractCache, MemoryCache

logger = logging.getLogger(__name__)

_VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
_LOCALE_PATTERN = re.compile(r"^[a-z]{2}_[A-Z]{2}$")
_CHAMPION_ID_PATTERN = re.compile(r"^[A-Za-z0-9]+$")
_ITEM_STAT_BASELINES = {
    "FlatPhysicalDamageMod": (1036, "attack_damage", 1.0, "points"),
    "FlatMagicDamageMod": (1052, "ability_power", 1.0, "points"),
    "FlatHPPoolMod": (1028, "health", 1.0, "points"),
    "FlatMPPoolMod": (1027, "mana", 1.0, "points"),
    "FlatArmorMod": (1029, "armor", 1.0, "points"),
    "FlatSpellBlockMod": (1033, "magic_resistance", 1.0, "points"),
    "PercentAttackSpeedMod": (1042, "attack_speed", 100.0, "percent"),
    "FlatMovementSpeedMod": (1001, "movement_speed", 1.0, "points"),
    "FlatCritChanceMod": (1018, "critical_strike_chance", 100.0, "percent"),
}


class DataDragonClient:
    """Client for Riot's Data Dragon static data service.

    Automatically resolves the latest patch version and caches
    heavy responses (champions, items, runes, summoner spells, etc.).
    """

    def __init__(self, cache: Optional[AbstractCache] = None):
        self.base_url = "https://ddragon.leagueoflegends.com"
        self.http = httpx.AsyncClient()
        self.cache = cache or MemoryCache(max_size=256)
        self.version: Optional[str] = None
        self.versions: Optional[List[str]] = None

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
        versions = await self.get_versions()
        self.version = versions[0]
        return self.version

    async def get_versions(self) -> List[str]:
        """Return Data Dragon versions in Riot's preferred order."""
        cache_key = "ddragon:versions"
        cached = await self.cache.get(cache_key)
        if cached:
            versions = [str(item) for item in cached]
            if versions:
                self.versions = versions
                return list(versions)

        resp = await self.http.get(f"{self.base_url}/api/versions.json")
        resp.raise_for_status()
        payload = resp.json()
        versions = [str(item) for item in payload if _VERSION_PATTERN.fullmatch(str(item))]
        if not versions:
            raise ValueError("Data Dragon returned no valid versions")

        await self.cache.set(cache_key, versions, ttl=3600)
        self.versions = versions
        return list(versions)

    async def resolve_version(
        self,
        game_version: str | None = None,
        *,
        strict: bool = False,
    ) -> str:
        """Resolve a Match V5 game version to the matching Data Dragon release."""
        if not game_version:
            return await self.get_latest_version()
        fields = str(game_version).split(".")
        if len(fields) < 2 or not all(field.isdigit() for field in fields[:2]):
            if strict:
                raise ValueError("invalid League patch version")
            return await self.get_latest_version()
        major = int(fields[0])
        if major >= 25:
            major -= 10
        prefix = f"{major}.{int(fields[1])}."
        versions = await self.get_versions()
        resolved = next((version for version in versions if version.startswith(prefix)), None)
        if resolved is not None:
            return resolved
        if strict:
            raise LookupError(f"no Data Dragon release exists for patch {prefix[:-1]}")
        return versions[0]

    # -- Generic fetch helper ------------------------------------------------

    async def _fetch_map(
        self,
        cache_suffix: str,
        url_path: str,
        key_fn: Any = None,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Dict:
        """Fetch a JSON resource, cache it, and return the map."""
        resolved_version = version or await self.get_latest_version()
        if _VERSION_PATTERN.fullmatch(resolved_version) is None:
            raise ValueError("invalid Data Dragon version")
        if _LOCALE_PATTERN.fullmatch(locale) is None:
            raise ValueError("invalid Data Dragon locale")
        cache_key = f"ddragon:{resolved_version}:{locale}:{cache_suffix}"

        data_map = await self.cache.get(cache_key)
        if data_map is not None:
            return data_map

        url = f"{self.base_url}/cdn/{resolved_version}/data/{locale}/{url_path}"
        resp = await self.http.get(url)
        resp.raise_for_status()
        data = resp.json()["data"]

        if key_fn:
            data_map = key_fn(data)
        else:
            data_map = data

        await self.cache.set(cache_key, data_map, ttl=86400)
        return data_map

    # -- Champions -----------------------------------------------------------

    async def get_champion(
        self,
        champion_key: int,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Optional[Dict[str, Any]]:
        """Get champion data by numeric key (e.g. 1 -> Annie)."""
        champions = await self._fetch_map(
            "champions",
            "champion.json",
            key_fn=lambda d: {int(c["key"]): c for c in d.values()},
            version=version,
            locale=locale,
        )
        return champions.get(champion_key)

    async def get_all_champions(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Dict[int, Dict[str, Any]]:
        """Return all champions keyed by numeric ID."""
        return await self._fetch_map(
            "champions",
            "champion.json",
            key_fn=lambda d: {int(c["key"]): c for c in d.values()},
            version=version,
            locale=locale,
        )

    async def get_champion_detail(
        self,
        champion_key: int,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Optional[Dict[str, Any]]:
        """Get full champion data, including abilities, by numeric key."""
        resolved_version = version or await self.get_latest_version()
        champion = await self.get_champion(
            champion_key,
            version=resolved_version,
            locale=locale,
        )
        if champion is None:
            return None
        champion_id = str(champion.get("id", ""))
        if _CHAMPION_ID_PATTERN.fullmatch(champion_id) is None:
            raise ValueError("invalid Data Dragon champion identifier")
        data = await self._fetch_map(
            f"champion:{champion_id}",
            f"champion/{champion_id}.json",
            version=resolved_version,
            locale=locale,
        )
        detail = data.get(champion_id)
        return dict(detail) if isinstance(detail, dict) else None

    # -- Items ---------------------------------------------------------------

    async def get_item(
        self,
        item_id: int,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Optional[Dict[str, Any]]:
        """Get item data by ID."""
        items = await self._fetch_map(
            "items",
            "item.json",
            key_fn=lambda d: {int(k): v for k, v in d.items()},
            version=version,
            locale=locale,
        )
        return items.get(item_id)

    async def get_all_items(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Dict[int, Dict[str, Any]]:
        """Return all items keyed by numeric ID."""
        return await self._fetch_map(
            "items",
            "item.json",
            key_fn=lambda d: {int(k): v for k, v in d.items()},
            version=version,
            locale=locale,
        )

    async def get_item_efficiency(
        self,
        item_id: int | None = None,
        *,
        item_name: str | None = None,
        game_version: str | None = None,
        version: str | None = None,
        locale: str = "en_US",
        map_id: int | None = 11,
    ) -> Dict[str, Any]:
        """Calculate patch-matched component-baseline raw-stat efficiency."""
        if (item_id is None) == (item_name is None):
            raise ValueError("provide exactly one item ID or item name")
        if version is not None and game_version is not None:
            raise ValueError("provide at most one version selector")
        if version is not None:
            if _VERSION_PATTERN.fullmatch(version) is None:
                raise ValueError("invalid Data Dragon version")
            versions = await self.get_versions()
            if version not in versions:
                raise LookupError(f"Data Dragon release {version} is unavailable")
            resolved_version = version
            patch_basis = "explicit_data_dragon_version"
        elif game_version is not None:
            resolved_version = await self.resolve_version(game_version, strict=True)
            patch_basis = "explicit_patch"
        else:
            resolved_version = await self.get_latest_version()
            patch_basis = "latest_at_request"

        items = await self.get_all_items(version=resolved_version, locale=locale)
        selected_id, item = _select_item(
            items,
            item_id=item_id,
            item_name=item_name,
            map_id=map_id,
        )
        gold = _mapping(item.get("gold"))
        total_cost = _positive_number(gold.get("total"))
        stats = _mapping(item.get("stats"))
        priced_stats: List[Dict[str, Any]] = []
        unpriced_stats: List[Dict[str, Any]] = []

        for stat_key, raw_value in stats.items():
            amount = _finite_number(raw_value)
            if amount is None or amount == 0:
                continue
            baseline = _ITEM_STAT_BASELINES.get(str(stat_key))
            if baseline is None:
                unpriced_stats.append({"data_dragon_key": str(stat_key), "raw_amount": amount})
                continue
            baseline_id, stat_name, display_multiplier, unit = baseline
            baseline_item = items.get(baseline_id)
            if not isinstance(baseline_item, dict):
                unpriced_stats.append(
                    {
                        "data_dragon_key": str(stat_key),
                        "raw_amount": amount,
                        "reason": "patch baseline unavailable",
                    }
                )
                continue
            baseline_stats = _mapping(baseline_item.get("stats"))
            baseline_gold = _mapping(baseline_item.get("gold"))
            baseline_amount = _positive_number(baseline_stats.get(stat_key))
            baseline_cost = _positive_number(baseline_gold.get("total"))
            if baseline_amount is None or baseline_cost is None:
                unpriced_stats.append(
                    {
                        "data_dragon_key": str(stat_key),
                        "raw_amount": amount,
                        "reason": "patch baseline unavailable",
                    }
                )
                continue
            displayed_amount = amount * display_multiplier
            displayed_baseline_amount = baseline_amount * display_multiplier
            gold_per_display_unit = baseline_cost / displayed_baseline_amount
            gold_value = amount * (baseline_cost / baseline_amount)
            priced_stats.append(
                {
                    "stat": stat_name,
                    "data_dragon_key": str(stat_key),
                    "amount": round(displayed_amount, 4),
                    "unit": unit,
                    "baseline": {
                        "item_id": baseline_id,
                        "item_name": baseline_item.get("name"),
                        "cost": round(baseline_cost, 4),
                        "amount": round(displayed_baseline_amount, 4),
                        "gold_per_unit": round(gold_per_display_unit, 4),
                    },
                    "gold_value": round(gold_value, 4),
                    "formula": (
                        f"{displayed_amount:g} {unit} × {gold_per_display_unit:.4f} gold/{unit}"
                    ),
                }
            )

        priced_value = sum(float(entry["gold_value"]) for entry in priced_stats)
        efficiency = (
            priced_value / total_cost * 100
            if priced_stats and total_cost is not None and total_cost > 0
            else None
        )
        maps = _mapping(item.get("maps"))
        map_available = None if map_id is None else bool(maps.get(str(map_id), False))
        return {
            "status": "available",
            "patch": {
                "requested": game_version or version,
                "resolved_data_dragon_version": resolved_version,
                "basis": patch_basis,
                "cross_patch_fallback": False,
            },
            "locale": locale,
            "methodology": "patch_component_baseline_raw_stats",
            "item": {
                "id": selected_id,
                "name": item.get("name"),
                "description": item.get("description"),
                "plaintext": item.get("plaintext"),
                "purchase_cost": total_cost,
                "combine_cost": _finite_number(gold.get("base")),
                "sell_value": _finite_number(gold.get("sell")),
                "purchasable": gold.get("purchasable"),
                "builds_from": item.get("from", []),
                "builds_into": item.get("into", []),
                "requested_map_id": map_id,
                "available_on_requested_map": map_available,
            },
            "priced_stats": priced_stats,
            "unpriced_stats": unpriced_stats,
            "priced_base_stat_value": round(priced_value, 4) if priced_stats else None,
            "raw_stat_efficiency_percent": (
                round(efficiency, 4) if efficiency is not None else None
            ),
            "coverage": {
                "structured_stats_found": len(priced_stats) + len(unpriced_stats),
                "priced_stats": len(priced_stats),
                "unpriced_stats": len(unpriced_stats),
                "complete_for_data_dragon_stats": not unpriced_stats,
                "complete_for_all_item_effects": False,
                "calculation_status": (
                    "no_priceable_structured_stats"
                    if not priced_stats
                    else "partial"
                    if unpriced_stats
                    else "complete_for_structured_stats_only"
                ),
            },
            "limitations": [
                "Gold efficiency is a derived comparison, not a Riot-authored item metric.",
                "Only structured stats with a pure component baseline in this patch are priced.",
                "Passives, actives, conditional effects, transformations, and omitted "
                "tooltip stats are excluded.",
                "The percentage is raw-stat efficiency, not total item value or a build "
                "recommendation.",
            ],
            "sources": [
                "https://developer.riotgames.com/docs/lol#data-dragon",
            ],
        }

    # -- Summoner Spells -----------------------------------------------------

    async def get_summoner_spells(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Dict[int, Dict[str, Any]]:
        """Return all summoner spells keyed by numeric key."""
        return await self._fetch_map(
            "summoner_spells",
            "summoner.json",
            key_fn=lambda d: {int(s["key"]): s for s in d.values()},
            version=version,
            locale=locale,
        )

    async def get_summoner_spell(
        self,
        spell_key: int,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Optional[Dict[str, Any]]:
        """Get a single summoner spell by numeric key."""
        spells = await self.get_summoner_spells(version=version, locale=locale)
        return spells.get(spell_key)

    # -- Runes ---------------------------------------------------------------

    async def get_runes(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> List[Dict[str, Any]]:
        """Return the full rune tree list."""
        resolved_version = version or await self.get_latest_version()
        if _VERSION_PATTERN.fullmatch(resolved_version) is None:
            raise ValueError("invalid Data Dragon version")
        if _LOCALE_PATTERN.fullmatch(locale) is None:
            raise ValueError("invalid Data Dragon locale")
        cache_key = f"ddragon:{resolved_version}:{locale}:runes"

        cached = await self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{self.base_url}/cdn/{resolved_version}/data/{locale}/runesReforged.json"
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


def _select_item(
    items: Dict[int, Dict[str, Any]],
    *,
    item_id: int | None,
    item_name: str | None,
    map_id: int | None,
) -> tuple[int, Dict[str, Any]]:
    if item_id is not None:
        item = items.get(item_id)
        if item is None:
            raise LookupError(f"item {item_id} is unavailable in this patch")
        return item_id, item

    normalized = str(item_name).strip().casefold()
    candidates = [
        (candidate_id, item)
        for candidate_id, item in items.items()
        if str(item.get("name", "")).strip().casefold() == normalized
    ]
    if map_id is not None:
        map_candidates = [
            (candidate_id, item)
            for candidate_id, item in candidates
            if bool(_mapping(item.get("maps")).get(str(map_id), False))
        ]
        if map_candidates:
            candidates = map_candidates
    purchasable = [
        (candidate_id, item)
        for candidate_id, item in candidates
        if _mapping(item.get("gold")).get("purchasable") is True
    ]
    if purchasable:
        candidates = purchasable
    if not candidates:
        raise LookupError(f"item {item_name!r} is unavailable in this patch")
    if len(candidates) > 1:
        identifiers = ", ".join(str(candidate_id) for candidate_id, _ in candidates)
        raise ValueError(f"item name is ambiguous in this patch; matching IDs: {identifiers}")
    return candidates[0]


def _mapping(value: Any) -> Dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _finite_number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    return number if number == number and abs(number) != float("inf") else None


def _positive_number(value: Any) -> float | None:
    number = _finite_number(value)
    return number if number is not None and number > 0 else None


class SyncDataDragonClient:
    def __init__(
        self,
        client: DataDragonClient,
        run: Callable[[Awaitable[Any]], Any],
    ) -> None:
        self._client = client
        self._run = run

    def get_latest_version(self) -> str:
        return self._run(self._client.get_latest_version())

    def get_versions(self) -> List[str]:
        return self._run(self._client.get_versions())

    def resolve_version(
        self,
        game_version: str | None = None,
        *,
        strict: bool = False,
    ) -> str:
        return self._run(self._client.resolve_version(game_version, strict=strict))

    def get_champion(
        self,
        champion_key: int,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Optional[Dict[str, Any]]:
        return self._run(
            self._client.get_champion(
                champion_key,
                version=version,
                locale=locale,
            )
        )

    def get_all_champions(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Dict[int, Dict[str, Any]]:
        return self._run(self._client.get_all_champions(version=version, locale=locale))

    def get_champion_detail(
        self,
        champion_key: int,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Optional[Dict[str, Any]]:
        return self._run(
            self._client.get_champion_detail(
                champion_key,
                version=version,
                locale=locale,
            )
        )

    def get_item(
        self,
        item_id: int,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Optional[Dict[str, Any]]:
        return self._run(self._client.get_item(item_id, version=version, locale=locale))

    def get_all_items(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Dict[int, Dict[str, Any]]:
        return self._run(self._client.get_all_items(version=version, locale=locale))

    def get_item_efficiency(
        self,
        item_id: int | None = None,
        *,
        item_name: str | None = None,
        game_version: str | None = None,
        version: str | None = None,
        locale: str = "en_US",
        map_id: int | None = 11,
    ) -> Dict[str, Any]:
        return self._run(
            self._client.get_item_efficiency(
                item_id,
                item_name=item_name,
                game_version=game_version,
                version=version,
                locale=locale,
                map_id=map_id,
            )
        )

    def get_summoner_spells(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Dict[int, Dict[str, Any]]:
        return self._run(self._client.get_summoner_spells(version=version, locale=locale))

    def get_summoner_spell(
        self,
        spell_key: int,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> Optional[Dict[str, Any]]:
        return self._run(
            self._client.get_summoner_spell(
                spell_key,
                version=version,
                locale=locale,
            )
        )

    def get_runes(
        self,
        *,
        version: str | None = None,
        locale: str = "en_US",
    ) -> List[Dict[str, Any]]:
        return self._run(self._client.get_runes(version=version, locale=locale))

    def get_queues(self) -> List[Dict[str, Any]]:
        return self._run(self._client.get_queues())

    def get_maps(self) -> List[Dict[str, Any]]:
        return self._run(self._client.get_maps())

    def get_game_modes(self) -> List[Dict[str, Any]]:
        return self._run(self._client.get_game_modes())

"""League match and player context assembly for MCP."""

from __future__ import annotations

import asyncio
import inspect
import math
import re
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime, time
from enum import Enum
from typing import Any

from pydantic import BaseModel

from riotskillissue.core.types import PLATFORM_TO_REGIONAL, PlatformRoute, RiotId

from .errors import IntegrationContractError, InvalidArgumentsError

_TEAM_IDS = (100, 200)
_GRUB_MARKERS = ("HORDE", "GRUB")
_MAJOR_EVENT_TYPES = {
    "BUILDING_KILL",
    "CHAMPION_KILL",
    "ELITE_MONSTER_KILL",
    "FEAT_UPDATE",
    "GAME_END",
    "TURRET_PLATE_DESTROYED",
}
_ITEM_EVENT_TYPES = {
    "ITEM_DESTROYED",
    "ITEM_PURCHASED",
    "ITEM_SOLD",
    "ITEM_UNDO",
}
_MATCH_PREFIX = re.compile(r"^([A-Za-z0-9]+)_")
_QUERY_TOPICS = {
    "void_grubs": ("void grub", "voidgrub", "grub", "horde", "hunger of the void"),
    "objectives": (
        "objective",
        "dragon",
        "drake",
        "baron",
        "herald",
        "atakhan",
        "turret",
        "tower",
        "inhibitor",
    ),
    "combat": ("fight", "teamfight", "kill", "death", "damage", "kda", "carry"),
    "economy": (
        "gold",
        "farm",
        "cs",
        "economy",
        "lead",
        "tempo",
        "xp",
        "experience",
        "minion",
        "wave",
        "last hit",
        "efficiency",
    ),
    "lanes": ("lane", "top", "jungle", "mid", "middle", "bot", "adc", "support"),
    "builds": ("item", "build", "rune", "spell", "power spike", "powerspike"),
    "vision": ("vision", "ward", "sight", "control ward"),
    "player": ("player", "rank", "mastery", "champion pool", "recent", "form"),
}
_OFFICIAL_SOURCES = {
    "riot_api": "https://developer.riotgames.com/apis#match-v5",
    "league_api": "https://developer.riotgames.com/docs/lol",
    "data_dragon": "https://developer.riotgames.com/docs/lol#data-dragon",
    "void_grubs_14_1": (
        "https://www.leagueoflegends.com/en-us/news/game-updates/patch-14-1-notes/"
    ),
    "void_grubs_25_9": (
        "https://www.leagueoflegends.com/en-us/news/game-updates/patch-25-09-notes/"
    ),
    "void_grubs_26_1": (
        "https://www.leagueoflegends.com/en-us/news/game-updates/patch-26-1-notes/"
    ),
    "economy_26_1": ("https://www.leagueoflegends.com/en-us/news/game-updates/patch-26-1-notes/"),
    "caster_gold_11_19": (
        "https://www.leagueoflegends.com/en-us/news/game-updates/patch-11-19-notes/"
    ),
}
_KNOWLEDGE: dict[str, dict[str, Any]] = {
    "core": {
        "principles": [
            "Two teams normally compete to destroy the opposing Nexus.",
            "Gold buys item power; experience grants levels and ability ranks.",
            "Kills matter through the gold, experience, time, space, and objectives they create.",
            "Turrets and inhibitors open durable map access; objectives create team-wide leverage.",
            "Impact is multidimensional: combat, economy, pressure, vision, utility, and conversion.",
        ],
        "analysis": [
            "Compare players within role and game state instead of ranking one raw statistic.",
            "Separate an observed result from a plausible explanation and from proven causality.",
            "Use the timeline to test whether a lead was converted into structures or major objectives.",
        ],
    },
    "objectives": {
        "principles": [
            "Turrets create gold and map access; inhibitors create lane pressure toward the Nexus.",
            "Elemental dragons provide persistent team power and can progress toward Dragon Soul.",
            "Baron primarily enables siege and map control through its team buff.",
            "Void Grubs reward early top-side control and improve later structure pressure.",
            "An objective's opportunity cost includes waves, camps, plates, vision, deaths, and cross-map trades.",
        ],
        "analysis": [
            "Measure setup state, capture cost, immediate trades, and later conversion separately.",
            "Objective count alone does not establish value if the opponent gained more elsewhere.",
        ],
    },
    "wave_management": {
        "principles": [
            "A wave can be pushed, held, slow-pushed, frozen, or allowed to bounce depending on relative minion counts and reinforcement timing.",
            "Wave value includes last-hit gold, proximity experience, lane priority, recall timing, structure pressure, and the opponent's denied access.",
            "A roam or objective trade should price the waves and experience put at risk, not only the kills or objective reward gained.",
            "Crashes create time to recall, move, ward, invade, or pressure a structure while the opponent collects under pressure.",
        ],
        "analysis": [
            "Use exact timeline gold, XP, and CS deltas as observations; Match V5 does not identify every minion type, last hit, or nearby XP recipient.",
            "Treat estimated missed-wave value as a model with explicit patch, composition, sharing, and collection assumptions.",
            "Champion wave-clear, threat, teleport access, death timers, and the next objective change whether a nominal wave loss is strategically acceptable.",
        ],
    },
    "roles": {
        "principles": [
            "Top commonly manages a long solo lane, side pressure, and frontline or carry duties.",
            "Jungle converts pathing and lane priority into ganks, vision, and neutral objectives.",
            "Mid combines lane economy with central access to both sides of the map.",
            "Bottom carry usually supplies sustained damage while support supplies setup, protection, and vision.",
        ],
        "analysis": [
            "Role expectations depend on champion, composition, matchup, resources, and game phase.",
            "TeamPosition is Riot's preferred inferred role field for standard team compositions.",
        ],
    },
    "stats": {
        "principles": [
            "KDA describes takedown efficiency but not target value, timing, or conversion.",
            "Kill participation estimates involvement in team kills and is role- and strategy-dependent.",
            "Damage requires context: target durability, uptime, range, resources, and whether it enabled objectives.",
            "CS, gold, and experience describe resources; efficiency asks what the player produced with them.",
        ],
        "analysis": [
            "Normalize volume statistics per minute and include team shares when comparing one game.",
            "Avoid treating a high damage or vision number as automatically good without event context.",
        ],
    },
    "items": {
        "principles": [
            "Items turn gold into stats and effects; completed-item timing can change fight outcomes.",
            "A build should be evaluated against champion scaling, opponents, damage profile, and game state.",
            "Runes and summoner spells affect trading, survivability, access, and strategic options.",
        ],
        "analysis": [
            "Use patch-matched Data Dragon because item identities, costs, and effects change over time.",
            "Match V5 exposes final inventory and the timeline exposes transactions, not player intent.",
        ],
    },
    "vision": {
        "principles": [
            "Vision changes the information available for pathing, picks, objectives, and safe pressure.",
            "Vision denial can matter as much as wards placed, particularly around an upcoming objective.",
        ],
        "analysis": [
            "Vision score is a broad contribution signal, not a complete map-control measurement.",
            "Match telemetry cannot reconstruct everything each player could see at every moment.",
        ],
    },
    "tempo": {
        "principles": [
            "Tempo is the ability to act first or spend time while the opponent cannot answer efficiently.",
            "Recall timing, wave state, death timers, travel, and objective spawn windows shape tempo.",
        ],
        "analysis": [
            "Use gold and event checkpoints as proxies; Match V5 does not expose every wave state or decision.",
            "A nominal gold loss can still buy valuable map position, but that conclusion needs evidence.",
        ],
    },
    "teamfights": {
        "principles": [
            "Teamfights depend on composition, cooldowns, positioning, target access, and resource state.",
            "Engage, peel, zoning, and threat can have impact that damage totals only partially capture.",
        ],
        "analysis": [
            "Timeline kill clusters identify likely fights but are not a complete replay.",
            "Victim damage records on kill events are partial and should not be treated as full fight damage.",
        ],
    },
    "player_data": {
        "principles": [
            "Riot IDs resolve to stable PUUIDs; PUUID endpoints are preferred when available.",
            "Ranked entries, mastery, challenges, and bounded recent matches describe different aspects of a player.",
        ],
        "analysis": [
            "A short recent-match sample is descriptive, not a durable skill rating.",
            "Public APIs do not provide hidden MMR, unrestricted name search, biographies, or esports rosters.",
        ],
    },
    "limitations": {
        "principles": [
            "Post-game telemetry is a record of selected facts, not a replay or a causal model.",
            "Missing timeline or static data reduces detail but does not invalidate available match facts.",
        ],
        "analysis": [
            "Do not infer exact buff damage, unseen information, intent, comms, or cooldown state when absent.",
            "Label estimates and associations and cite the fields that support them.",
        ],
    },
}


class LolAnalysisService:
    """Assemble bounded League evidence from Riot APIs and static content."""

    def __init__(self, client: Any) -> None:
        self._client = client

    async def match_context(self, request: Any) -> dict[str, Any]:
        values = _request_values(request)
        warnings: list[str] = []
        sources: list[dict[str, str]] = []
        match_id = _optional_text(values.get("match_id"))
        riot_id = _optional_text(values.get("riot_id"))
        route = _optional_text(values.get("route"))
        focus_puuid: str | None = None

        if riot_id is not None:
            match_id, focus_puuid = await self._resolve_player_match(
                riot_id,
                route=route,
                match_index=int(values.get("match_index", 0)),
            )
            sources.extend(
                [
                    _source("account-v1.getByRiotId"),
                    _source("match-v5.getMatchIdsByPUUID"),
                ]
            )
        if match_id is None:
            raise InvalidArgumentsError("A match ID or Riot ID is required.")

        regional = _match_route(match_id, route)
        match_task = self._call(
            "match-v5.getMatch",
            match_id=match_id,
            route=regional,
        )
        include_timeline = bool(values.get("include_timeline", True))
        if include_timeline:
            match_result, timeline_result = await asyncio.gather(
                match_task,
                self._call(
                    "match-v5.getTimeline",
                    match_id=match_id,
                    route=regional,
                ),
                return_exceptions=True,
            )
        else:
            match_result = await match_task
            timeline_result = None
        if isinstance(match_result, BaseException):
            raise match_result
        sources.append(_source("match-v5.getMatch"))
        timeline: Any | None = None
        if isinstance(timeline_result, BaseException):
            warnings.append(_unavailable("Match timeline", timeline_result))
        elif timeline_result is not None:
            timeline = timeline_result

        match = _validate_match_payload(_to_data(match_result), match_id)
        timeline_data: Mapping[str, Any] | None = None
        if timeline is not None:
            timeline_data, timeline_warnings = _validate_timeline_payload(
                _to_data(timeline),
                match_id,
                expected_participants=len(
                    _as_list(_field(_as_mapping(match.get("info")), "participants", default=[]))
                ),
            )
            warnings.extend(timeline_warnings)
            if timeline_data is not None:
                sources.append(_source("match-v5.getTimeline"))
        static, static_warnings = await self._load_match_static(match)
        warnings.extend(static_warnings)
        if static.get("version") is not None:
            sources.append(_source("Data Dragon", str(static["version"])))
        return _build_match_context(
            match,
            timeline_data,
            static,
            question=_optional_text(values.get("question")),
            focus=_optional_text(values.get("focus")),
            focus_puuid=focus_puuid,
            detail=str(values.get("detail", "standard")),
            route=regional,
            warnings=warnings,
            sources=sources,
        )

    async def player_context(self, request: Any) -> dict[str, Any]:
        values = _request_values(request)
        riot_id = _optional_text(values.get("riot_id"))
        if riot_id is None:
            raise InvalidArgumentsError("A Riot ID is required.")
        route = _optional_text(values.get("route"))
        count = int(values.get("count", values.get("match_count", 5)))
        if count < 1 or count > 10:
            raise InvalidArgumentsError("Player context match count must be between 1 and 10.")
        return await self._build_player_context(
            riot_id,
            route=route,
            count=count,
            question=_optional_text(values.get("question")),
            detail=str(values.get("detail", "standard")),
        )

    def knowledge(self, request: Any) -> dict[str, Any]:
        values = _request_values(request)
        topic = str(values.get("topic", "core"))
        content: dict[str, Any]
        if topic == "void_grubs":
            content = _void_grub_knowledge(_optional_text(values.get("patch")))
        elif topic in {
            "economy",
            "minions",
            "experience",
            "item_efficiency",
            "structures",
        }:
            content = _economy_knowledge(
                topic,
                _optional_text(values.get("patch")),
            )
        else:
            known_content = _KNOWLEDGE.get(topic)
            if known_content is None:
                raise InvalidArgumentsError("Unknown League knowledge topic.")
            content = _to_data(known_content)
        content = _knowledge_detail(content, str(values.get("detail", "standard")))
        question = _optional_text(values.get("question"))
        return {
            "topic": topic,
            "scope": "League of Legends, primarily standard Summoner's Rift",
            "patch_requested": _optional_text(values.get("patch")),
            "knowledge": content,
            "question_relevance": _question_relevance(question, scope="knowledge"),
            "sources": [
                _OFFICIAL_SOURCES["league_api"],
                _OFFICIAL_SOURCES["data_dragon"],
                *(content.get("sources", []) if isinstance(content, dict) else []),
            ],
        }

    async def item_economy(self, request: Any) -> dict[str, Any]:
        values = _request_values(request)
        item_id = values.get("item_id")
        item_name = _optional_text(values.get("item_name"))
        patch = _optional_text(values.get("patch"))
        match_id = _optional_text(values.get("match_id"))
        route = _optional_text(values.get("route"))
        map_id = _int(values.get("map_id")) or None
        match_basis: dict[str, Any] | None = None
        sources: list[dict[str, str]] = []

        if match_id is not None:
            regional = _match_route(match_id, route)
            match_result = await self._call(
                "match-v5.getMatch",
                match_id=match_id,
                route=regional,
            )
            match = _validate_match_payload(_to_data(match_result), match_id)
            info = _as_mapping(_field(match, "info", default={}))
            patch = _optional_text(_field(info, "gameVersion", "game_version"))
            map_id = _int(_field(info, "mapId", "map_id")) or map_id
            match_basis = {
                "match_id": match_id,
                "route": regional,
                "game_version": patch,
                "queue_id": _int(_field(info, "queueId", "queue_id")),
                "map_id": map_id,
                "game_mode": _field(info, "gameMode", "game_mode"),
            }
            sources.append(_source("match-v5.getMatch"))

        static_client = getattr(self._client, "static", None)
        method = getattr(static_client, "get_item_efficiency", None)
        if not callable(method):
            raise IntegrationContractError(
                "The installed RiotSkillIssue client lacks item economy support."
            )
        try:
            economy = await _invoke(
                method,
                item_id=item_id,
                item_name=item_name,
                game_version=patch,
                locale=str(values.get("locale", "en_US")),
                map_id=map_id,
            )
        except (LookupError, ValueError) as exc:
            raise InvalidArgumentsError(str(exc)) from exc
        economy_data = _as_mapping(economy)
        resolved = _optional_text(
            _field(
                _as_mapping(economy_data.get("patch")),
                "resolved_data_dragon_version",
            )
        )
        if resolved is not None:
            sources.append(_source("Data Dragon items", resolved))
        if match_basis is None:
            applicability = {
                "status": "standard_summoners_rift_assumed",
                "map_id": map_id,
                "warning": "No queue was supplied; alternate-mode price or effect rules are not modelled.",
            }
        else:
            is_standard = (
                _int(match_basis.get("map_id")) == 11
                and _int(match_basis.get("queue_id")) != 480
                and str(match_basis.get("game_mode", "")).upper() == "CLASSIC"
            )
            applicability = {
                "status": "standard_summoners_rift" if is_standard else "unverified_mode",
                "map_id": match_basis.get("map_id"),
                "queue_id": match_basis.get("queue_id"),
                "warning": (
                    None
                    if is_standard
                    else "Alternate queue modifiers are not included in the efficiency calculation."
                ),
            }
        return {
            "item_query": {"item_id": item_id, "item_name": item_name},
            "match_basis": match_basis,
            "economy": economy_data,
            "applicability": applicability,
            "evidence_classes": {
                "observed": "Match identity, patch, queue, and map when match_id was supplied.",
                "derived": "Component-baseline rates and raw-stat arithmetic.",
                "excluded": "Unstructured item effects and unrepresented stats.",
            },
            "sources": sources,
        }

    async def _resolve_player_match(
        self,
        riot_id: str,
        *,
        route: str | None,
        match_index: int,
    ) -> tuple[str, str]:
        if match_index < 0 or match_index > 99:
            raise InvalidArgumentsError("match_index must be between 0 and 99.")
        route = self._effective_route(route)
        parsed = RiotId.parse(riot_id)
        regional = _regional_from_route(route)
        account = await self._call(
            "account-v1.getByRiotId",
            game_name=parsed.game_name,
            tag_line=parsed.tag_line,
            route=_account_route(route),
        )
        account_data = _to_data(account)
        puuid = _required_text(_field(account_data, "puuid"), "Riot account PUUID")
        ids = await self._call(
            "match-v5.getMatchIdsByPUUID",
            puuid=puuid,
            start=0,
            count=match_index + 1,
            route=regional,
        )
        match_ids = [str(item) for item in _as_list(_to_data(ids))]
        if match_index >= len(match_ids):
            raise InvalidArgumentsError("The requested recent match does not exist.")
        return match_ids[match_index], puuid

    async def _build_player_context(
        self,
        riot_id: str,
        *,
        route: str | None,
        count: int,
        question: str | None,
        detail: str,
    ) -> dict[str, Any]:
        route = self._effective_route(route)
        parsed = RiotId.parse(riot_id)
        platform = _platform_route(route)
        regional = _regional_from_route(platform)
        account = _to_data(
            await self._call(
                "account-v1.getByRiotId",
                game_name=parsed.game_name,
                tag_line=parsed.tag_line,
                route=_account_route(platform),
            )
        )
        puuid = _required_text(_field(account, "puuid"), "Riot account PUUID")
        optional_calls = {
            "summoner": self._call(
                "summoner-v4.getByPUUID",
                encrypted_puuid=puuid,
                route=platform,
            ),
            "ranked": self._call(
                "league-v4.getLeagueEntriesByPUUID",
                encrypted_puuid=puuid,
                route=platform,
            ),
            "mastery": self._call(
                "champion-mastery-v4.getTopChampionMasteriesByPUUID",
                encrypted_puuid=puuid,
                count=10,
                route=platform,
            ),
            "challenges": self._call(
                "lol-challenges-v1.getPlayerData",
                puuid=puuid,
                route=platform,
            ),
            "match_ids": self._call(
                "match-v5.getMatchIdsByPUUID",
                puuid=puuid,
                start=0,
                count=count,
                route=regional,
            ),
        }
        settled, warnings = await _settle(optional_calls)
        match_ids = [str(item) for item in _as_list(settled.get("match_ids"))][:count]
        match_calls = {
            match_id: self._call(
                "match-v5.getMatch",
                match_id=match_id,
                route=_match_route(match_id, regional),
            )
            for match_id in match_ids
        }
        matches, match_warnings = await _settle(match_calls)
        warnings.extend(match_warnings)

        champions: dict[int, dict[str, Any]] = {}
        champion_static_loaded = False
        static_client = getattr(self._client, "static", None)
        if static_client is not None:
            method = getattr(static_client, "get_all_champions", None)
            if callable(method):
                try:
                    champions = _int_key_map(_to_data(await _invoke(method)))
                    champion_static_loaded = True
                except Exception as exc:
                    warnings.append(_unavailable("Champion static data", exc))

        loaded_matches: list[Mapping[str, Any]] = []
        for match_id in match_ids:
            if match_id not in matches:
                continue
            try:
                loaded_matches.append(
                    _validate_match_payload(_to_data(matches[match_id]), match_id)
                )
            except IntegrationContractError:
                warnings.append(f"Match {match_id} returned a malformed payload and was ignored.")
        operation_by_section = {
            "summoner": "summoner-v4.getByPUUID",
            "ranked": "league-v4.getLeagueEntriesByPUUID",
            "mastery": "champion-mastery-v4.getTopChampionMasteriesByPUUID",
            "challenges": "lol-challenges-v1.getPlayerData",
            "match_ids": "match-v5.getMatchIdsByPUUID",
        }
        provenance_sources = [_source("account-v1.getByRiotId")]
        provenance_sources.extend(
            _source(operation)
            for section, operation in operation_by_section.items()
            if section in settled
        )
        if loaded_matches:
            provenance_sources.append(_source("match-v5.getMatch"))
        if champion_static_loaded:
            provenance_sources.append(_source("Data Dragon champions"))
        return _player_context_payload(
            riot_id=riot_id,
            account=account,
            puuid=puuid,
            summoner=_to_data(settled.get("summoner")),
            ranked=_to_data(settled.get("ranked")),
            mastery=_to_data(settled.get("mastery")),
            challenges=_to_data(settled.get("challenges")),
            matches=loaded_matches,
            requested_count=count,
            match_ids=match_ids,
            champions=champions,
            route=platform,
            question=question,
            detail=detail,
            warnings=warnings,
            sources=provenance_sources,
            unavailable_sections=[section for section in optional_calls if section not in settled],
        )

    def _effective_route(self, route: str | None) -> str | None:
        if route is not None:
            return route
        config = getattr(self._client, "config", None)
        configured = getattr(config, "default_route", None)
        if isinstance(configured, Enum):
            configured = configured.value
        return _optional_text(configured)

    async def _load_match_static(
        self,
        match: Mapping[str, Any],
    ) -> tuple[dict[str, Any], list[str]]:
        static_client = getattr(self._client, "static", None)
        if static_client is None:
            return {}, ["Data Dragon enrichment is unavailable on this client."]
        info = _as_mapping(_field(match, "info", default={}))
        game_version = _optional_text(_field(info, "gameVersion", "game_version"))
        resolved_version: str | None = None
        warnings: list[str] = []
        resolver = getattr(static_client, "resolve_version", None)
        if callable(resolver):
            try:
                resolved_version = str(
                    await _invoke(
                        resolver,
                        game_version=game_version,
                        strict=True,
                    )
                )
            except Exception as exc:
                warnings.append(_unavailable("Data Dragon version resolution", exc))
        static_patch_match = _same_patch(game_version, resolved_version)
        rejected_version: str | None = None
        if game_version is not None and static_patch_match is not True:
            rejected_version = resolved_version
            resolved_version = None
            warnings.append(
                "Patch-matched Data Dragon content was unavailable; versioned enrichment was omitted."
            )
        calls: dict[str, Any] = {}
        for key, method_name in (
            ("items", "get_all_items"),
            ("spells", "get_summoner_spells"),
            ("runes", "get_runes"),
            ("queues", "get_queues"),
            ("maps", "get_maps"),
        ):
            method = getattr(static_client, method_name, None)
            if not callable(method):
                continue
            if (
                key in {"items", "spells", "runes"}
                and game_version is not None
                and resolved_version is None
            ):
                continue
            kwargs = (
                {"version": resolved_version}
                if resolved_version is not None and key in {"items", "spells", "runes"}
                else {}
            )
            calls[key] = _invoke(method, **kwargs)
        settled, static_warnings = await _settle(calls, label_suffix=" static data")
        warnings.extend(static_warnings)
        return {
            "version": resolved_version,
            "rejected_version": rejected_version,
            "patch_match": static_patch_match,
            "match_game_version": game_version,
            "items": _int_key_map(_to_data(settled.get("items"))),
            "spells": _int_key_map(_to_data(settled.get("spells"))),
            "runes": _rune_map(_to_data(settled.get("runes"))),
            "queues": _as_list(_to_data(settled.get("queues"))),
            "maps": _as_list(_to_data(settled.get("maps"))),
        }, warnings

    async def _call(self, operation: str, **arguments: Any) -> Any:
        dispatch = getattr(self._client, "call_operation", None)
        if not callable(dispatch):
            raw = getattr(self._client, "raw", None)
            dispatch = getattr(raw, "call_operation", None)
        if not callable(dispatch):
            raise IntegrationContractError(
                "The installed RiotSkillIssue client lacks operation dispatch support."
            )
        cleaned = {key: value for key, value in arguments.items() if value is not None}
        result = dispatch(operation, cleaned)
        return await result if inspect.isawaitable(result) else result


def _validate_match_payload(value: Any, expected_match_id: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise IntegrationContractError("Match V5 returned a malformed match payload.")
    metadata = _as_mapping(_field(value, "metadata", default={}))
    info = _as_mapping(_field(value, "info", default={}))
    actual_match_id = _optional_text(_field(metadata, "matchId", "match_id"))
    participants = _as_list(_field(info, "participants", default=[]))
    teams = _as_list(_field(info, "teams", default=[]))
    if actual_match_id != expected_match_id or not participants or len(teams) < 2:
        raise IntegrationContractError(
            "Match V5 returned an incomplete or mismatched match payload."
        )
    return value


def _validate_timeline_payload(
    value: Any,
    expected_match_id: str,
    *,
    expected_participants: int,
) -> tuple[Mapping[str, Any] | None, list[str]]:
    if not isinstance(value, Mapping):
        return None, ["Match timeline was malformed and was ignored."]
    metadata = _as_mapping(_field(value, "metadata", default={}))
    actual_match_id = _optional_text(_field(metadata, "matchId", "match_id"))
    if actual_match_id is not None and actual_match_id != expected_match_id:
        return None, ["Match timeline identified a different match and was ignored."]
    info = _as_mapping(_field(value, "info", default={}))
    frames = [_as_mapping(item) for item in _as_list(_field(info, "frames", default=[]))]
    if not frames:
        return None, ["Match timeline contained no frames and was ignored."]
    warnings: list[str] = []
    maximum_participants = max(
        (
            len(_as_mapping(_field(frame, "participantFrames", "participant_frames", default={})))
            for frame in frames
        ),
        default=0,
    )
    if expected_participants and maximum_participants < expected_participants:
        warnings.append(
            "Match timeline participant frames were incomplete; frame-derived metrics are partial."
        )
    return value, warnings


def _build_match_context(
    match: Mapping[str, Any],
    timeline: Mapping[str, Any] | None,
    static: Mapping[str, Any],
    *,
    question: str | None,
    focus: str | None,
    focus_puuid: str | None,
    detail: str,
    route: str,
    warnings: list[str],
    sources: list[dict[str, str]],
) -> dict[str, Any]:
    metadata = _as_mapping(_field(match, "metadata", default={}))
    info = _as_mapping(_field(match, "info", default={}))
    participants = [
        _as_mapping(value) for value in _as_list(_field(info, "participants", default=[]))
    ]
    teams = [_as_mapping(value) for value in _as_list(_field(info, "teams", default=[]))]
    duration = _duration_seconds(_field(info, "gameDuration", "game_duration", default=0))
    participant_by_id = {
        _int(_field(participant, "participantId", "participant_id")): participant
        for participant in participants
        if _int(_field(participant, "participantId", "participant_id")) > 0
    }
    team_participants = {
        team_id: [
            participant
            for participant in participants
            if _int(_field(participant, "teamId", "team_id")) == team_id
        ]
        for team_id in _TEAM_IDS
    }
    team_kills = {
        team_id: sum(_int(_field(item, "kills")) for item in members)
        for team_id, members in team_participants.items()
    }
    items = _int_key_map(static.get("items"))
    spells = _int_key_map(static.get("spells"))
    runes = _int_key_map(static.get("runes"))
    frames = _timeline_frames(timeline)
    events = _timeline_events(frames)
    timeline_quality = _timeline_quality(frames, expected_participants=len(participants))
    compact_participants = [
        _participant_summary(
            participant,
            duration=duration,
            team_kills=team_kills.get(_int(_field(participant, "teamId", "team_id")), 0),
            items=items,
            spells=spells,
            runes=runes,
        )
        for participant in participants
    ]
    team_payload = [
        _team_summary(
            team,
            team_participants.get(_int(_field(team, "teamId", "team_id")), []),
            duration=duration,
        )
        for team in teams
    ]
    known_team_ids = {_int(team.get("team_id")) for team in team_payload}
    for team_id in _TEAM_IDS:
        if team_id not in known_team_ids and team_participants.get(team_id):
            team_payload.append(
                _team_summary(
                    {"teamId": team_id},
                    team_participants[team_id],
                    duration=duration,
                )
            )

    event_payload = _major_events(
        events,
        participant_by_id=participant_by_id,
        detail=detail,
    )
    checkpoints = _gold_checkpoints(
        frames,
        participant_by_id=participant_by_id,
        detail=detail,
    )
    focus_participant = _resolve_focus(
        participants,
        focus=focus,
        focus_puuid=focus_puuid,
    )
    queue_id = _int(_field(info, "queueId", "queue_id"))
    map_id = _int(_field(info, "mapId", "map_id"))
    queue = _find_static(static.get("queues"), "queueId", queue_id)
    game_map = _find_static(static.get("maps"), "mapId", map_id)
    game_version = _optional_text(_field(info, "gameVersion", "game_version"))
    void_grubs = _void_grub_analysis(
        teams=team_payload,
        participants=compact_participants,
        events=events,
        frames=frames,
        participant_by_id=participant_by_id,
        game_version=game_version,
        game_mode=_optional_text(_field(info, "gameMode", "game_mode")),
        queue_id=queue_id,
        queue=queue,
        timeline_available=bool(frames),
        timeline_complete=bool(timeline_quality["participant_frames_complete"]),
    )
    lane_matchups = _lane_matchups(
        participants,
        frames=frames,
        duration=duration,
    )
    item_milestones = _item_milestones(
        events,
        participant_by_id=participant_by_id,
        items=items,
        detail=detail,
    )
    likely_teamfights = _teamfights(events, participant_by_id=participant_by_id)
    match_id = str(
        _field(metadata, "matchId", "match_id", default="")
        or _field(match, "matchId", "match_id", default="")
    )
    ended_early = bool(
        any(
            _truthy(
                _field(
                    participant,
                    "gameEndedInEarlySurrender",
                    "game_ended_in_early_surrender",
                )
            )
            for participant in participants
        )
    )
    data_quality = {
        "timeline_available": bool(frames),
        "timeline": timeline_quality,
        "static_version": static.get("version"),
        "rejected_static_version": static.get("rejected_version"),
        "match_game_version": game_version,
        "static_patch_match": static.get("patch_match"),
        "participant_count": len(participants),
        "warnings": warnings,
        "limitations": [
            "Timeline events and minute frames are selected telemetry, not a replay.",
            "Causal impact, intent, communications, fog of war, and every cooldown are not observable.",
            "Derived fight clusters, lane comparisons, and objective conversion are labeled proxies.",
        ],
    }
    result: dict[str, Any] = {
        "match": {
            "match_id": match_id,
            "route": route,
            "game_version": game_version,
            "data_version": _field(metadata, "dataVersion", "data_version"),
            "queue_id": queue_id,
            "queue": _compact_static(queue, ("map", "description", "notes")),
            "map_id": map_id,
            "map": _compact_static(game_map, ("mapName", "notes")),
            "game_mode": _field(info, "gameMode", "game_mode"),
            "game_type": _field(info, "gameType", "game_type"),
            "duration_seconds": duration,
            "started_at": _iso_timestamp(
                _field(info, "gameStartTimestamp", "game_start_timestamp")
            ),
            "ended_at": _iso_timestamp(_field(info, "gameEndTimestamp", "game_end_timestamp")),
            "early_surrender": ended_early,
        },
        "focus_participant": (
            _participant_summary(
                focus_participant,
                duration=duration,
                team_kills=team_kills.get(_int(_field(focus_participant, "teamId", "team_id")), 0),
                items=items,
                spells=spells,
                runes=runes,
            )
            if focus_participant is not None
            else None
        ),
        "teams": sorted(team_payload, key=lambda item: _int(item.get("team_id"))),
        "participants": compact_participants,
        "lane_matchups": lane_matchups,
        "timeline": {
            "checkpoints": checkpoints,
            "major_events": event_payload,
            "likely_teamfights": likely_teamfights,
            "item_milestones": item_milestones,
        },
        "impact_assessments": {"void_grubs": void_grubs},
        "question_relevance": _question_relevance(question, scope="match"),
        "data_quality": data_quality,
        "provenance": {
            "sources": sources,
            "derived_sections": [
                "participant rates and shares",
                "lane matchups",
                "timeline checkpoints",
                "likely teamfights",
                "objective conversion",
            ],
        },
    }
    if detail == "summary":
        result["timeline"]["item_milestones"] = []
        result["timeline"]["major_events"] = [
            event for event in event_payload if event.get("type") != "CHAMPION_KILL"
        ]
    return result


def _participant_summary(
    participant: Mapping[str, Any],
    *,
    duration: float,
    team_kills: int,
    items: Mapping[int, Mapping[str, Any]],
    spells: Mapping[int, Mapping[str, Any]],
    runes: Mapping[int, Mapping[str, Any]],
) -> dict[str, Any]:
    kills = _int(_field(participant, "kills"))
    deaths = _int(_field(participant, "deaths"))
    assists = _int(_field(participant, "assists"))
    minutes = max(duration / 60, 1 / 60)
    cs = _int(_field(participant, "totalMinionsKilled", "total_minions_killed"))
    jungle_cs = _int(_field(participant, "neutralMinionsKilled", "neutral_minions_killed"))
    champion_damage = _int(
        _field(
            participant,
            "totalDamageDealtToChampions",
            "total_damage_dealt_to_champions",
        )
    )
    vision = _int(_field(participant, "visionScore", "vision_score"))
    challenge = _as_mapping(_field(participant, "challenges", default={}))
    item_ids = [
        _int(_field(participant, f"item{index}"))
        for index in range(7)
        if _int(_field(participant, f"item{index}")) > 0
    ]
    rune_ids: list[int] = []
    perks = _as_mapping(_field(participant, "perks", default={}))
    for style in _as_list(_field(perks, "styles", default=[])):
        style_data = _as_mapping(style)
        for selection in _as_list(_field(style_data, "selections", default=[])):
            perk_id = _int(_field(_as_mapping(selection), "perk"))
            if perk_id > 0:
                rune_ids.append(perk_id)
    game_name = _optional_text(
        _field(participant, "riotIdGameName", "riot_id_game_name", "riotIdName")
    )
    tag_line = _optional_text(_field(participant, "riotIdTagline", "riot_id_tagline"))
    riot_id = f"{game_name}#{tag_line}" if game_name and tag_line else None
    return {
        "participant_id": _int(_field(participant, "participantId", "participant_id")),
        "riot_id": riot_id,
        "display_name": riot_id
        or _field(participant, "summonerName", "summoner_name")
        or game_name,
        "team_id": _int(_field(participant, "teamId", "team_id")),
        "side": _side(_int(_field(participant, "teamId", "team_id"))),
        "win": bool(_field(participant, "win", default=False)),
        "champion": {
            "id": _int(_field(participant, "championId", "champion_id")),
            "name": _field(participant, "championName", "champion_name"),
            "level": _int(_field(participant, "champLevel", "champ_level")),
        },
        "role": _field(
            participant,
            "teamPosition",
            "team_position",
            "individualPosition",
            "individual_position",
        ),
        "combat": {
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "kda": _round((kills + assists) / max(1, deaths)),
            "kill_participation": _round((kills + assists) / team_kills) if team_kills else None,
            "largest_killing_spree": _int(
                _field(participant, "largestKillingSpree", "largest_killing_spree")
            ),
            "largest_multi_kill": _int(
                _field(participant, "largestMultiKill", "largest_multi_kill")
            ),
            "solo_kills": _number(_field(challenge, "soloKills", "solo_kills")),
            "time_ccing_others": _int(_field(participant, "timeCCingOthers", "time_c_cing_others")),
        },
        "economy": {
            "gold_earned": _int(_field(participant, "goldEarned", "gold_earned")),
            "gold_spent": _int(_field(participant, "goldSpent", "gold_spent")),
            "gold_per_minute": _round(
                _int(_field(participant, "goldEarned", "gold_earned")) / minutes
            ),
            "lane_cs": cs,
            "jungle_cs": jungle_cs,
            "cs_per_minute": _round((cs + jungle_cs) / minutes),
        },
        "damage": {
            "to_champions": champion_damage,
            "to_champions_per_minute": _round(champion_damage / minutes),
            "taken": _int(_field(participant, "totalDamageTaken", "total_damage_taken")),
            "self_mitigated": _int(
                _field(participant, "damageSelfMitigated", "damage_self_mitigated")
            ),
            "to_turrets": _int(
                _field(participant, "damageDealtToTurrets", "damage_dealt_to_turrets")
            ),
            "to_buildings": _int(
                _field(
                    participant,
                    "damageDealtToBuildings",
                    "damage_dealt_to_buildings",
                )
            ),
            "to_objectives": _int(
                _field(participant, "damageDealtToObjectives", "damage_dealt_to_objectives")
            ),
            "to_epic_monsters": _number(
                _field(
                    participant,
                    "damageDealtToEpicMonsters",
                    "damage_dealt_to_epic_monsters",
                )
            ),
        },
        "vision": {
            "score": vision,
            "score_per_minute": _round(vision / minutes),
            "wards_placed": _int(_field(participant, "wardsPlaced", "wards_placed")),
            "wards_killed": _int(_field(participant, "wardsKilled", "wards_killed")),
            "control_wards_bought": _int(
                _field(
                    participant,
                    "visionWardsBoughtInGame",
                    "vision_wards_bought_in_game",
                )
            ),
        },
        "utility": {
            "healing_on_teammates": _int(
                _field(
                    participant,
                    "totalHealsOnTeammates",
                    "total_heals_on_teammates",
                )
            ),
            "shielding_on_teammates": _int(
                _field(
                    participant,
                    "totalDamageShieldedOnTeammates",
                    "total_damage_shielded_on_teammates",
                )
            ),
        },
        "objectives": {
            "turret_takedowns": _number(_field(participant, "turretTakedowns", "turret_takedowns")),
            "inhibitor_takedowns": _number(
                _field(participant, "inhibitorTakedowns", "inhibitor_takedowns")
            ),
            "dragon_kills": _int(_field(participant, "dragonKills", "dragon_kills")),
            "baron_kills": _int(_field(participant, "baronKills", "baron_kills")),
            "objectives_stolen": _int(_field(participant, "objectivesStolen", "objectives_stolen")),
            "void_monster_kills": _number(
                _field(challenge, "voidMonsterKill", "void_monster_kill")
            ),
        },
        "loadout": {
            "items": [
                {"id": item_id, "name": _field(items.get(item_id, {}), "name")}
                for item_id in item_ids
            ],
            "summoner_spells": [
                {
                    "id": spell_id,
                    "name": _field(spells.get(spell_id, {}), "name"),
                }
                for spell_id in (
                    _int(_field(participant, "summoner1Id", "summoner1_id")),
                    _int(_field(participant, "summoner2Id", "summoner2_id")),
                )
                if spell_id > 0
            ],
            "runes": [
                {"id": rune_id, "name": _field(runes.get(rune_id, {}), "name")}
                for rune_id in rune_ids
            ],
        },
    }


def _team_summary(
    team: Mapping[str, Any],
    participants: Sequence[Mapping[str, Any]],
    *,
    duration: float,
) -> dict[str, Any]:
    team_id = _int(_field(team, "teamId", "team_id"))
    objectives = _as_mapping(_field(team, "objectives", default={}))
    normalized_objectives: dict[str, dict[str, Any]] = {}
    for name, aliases in {
        "champion": ("champion",),
        "tower": ("tower",),
        "inhibitor": ("inhibitor",),
        "dragon": ("dragon",),
        "baron": ("baron",),
        "rift_herald": ("riftHerald", "rift_herald"),
        "void_grubs": ("horde",),
        "atakhan": ("atakhan",),
    }.items():
        raw_value = _field(objectives, *aliases, default=None)
        value = _as_mapping(raw_value)
        normalized_objectives[name] = {
            "available": raw_value is not None,
            "kills": _int(_field(value, "kills")),
            "first": bool(_field(value, "first", default=False)),
        }
    minutes = max(duration / 60, 1 / 60)
    return {
        "team_id": team_id,
        "side": _side(team_id),
        "win": bool(_field(team, "win", default=False)),
        "objectives": normalized_objectives,
        "totals": {
            "kills": sum(_int(_field(item, "kills")) for item in participants),
            "deaths": sum(_int(_field(item, "deaths")) for item in participants),
            "assists": sum(_int(_field(item, "assists")) for item in participants),
            "gold": sum(_int(_field(item, "goldEarned", "gold_earned")) for item in participants),
            "gold_per_minute": _round(
                sum(_int(_field(item, "goldEarned", "gold_earned")) for item in participants)
                / minutes
            ),
            "champion_damage": sum(
                _int(
                    _field(
                        item,
                        "totalDamageDealtToChampions",
                        "total_damage_dealt_to_champions",
                    )
                )
                for item in participants
            ),
            "building_damage": sum(
                _int(
                    _field(
                        item,
                        "damageDealtToBuildings",
                        "damage_dealt_to_buildings",
                    )
                )
                for item in participants
            ),
            "turret_damage": sum(
                _int(
                    _field(
                        item,
                        "damageDealtToTurrets",
                        "damage_dealt_to_turrets",
                    )
                )
                for item in participants
            ),
            "vision_score": sum(
                _int(_field(item, "visionScore", "vision_score")) for item in participants
            ),
        },
        "feats": _to_data(_field(team, "feats", default={})),
    }


def _timeline_frames(timeline: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    if timeline is None:
        return []
    info = _as_mapping(_field(timeline, "info", default={}))
    return [_as_mapping(frame) for frame in _as_list(_field(info, "frames", default=[]))]


def _timeline_quality(
    frames: Sequence[Mapping[str, Any]],
    *,
    expected_participants: int,
) -> dict[str, Any]:
    coverages = [
        len(_as_mapping(_field(frame, "participantFrames", "participant_frames", default={})))
        for frame in frames
    ]
    maximum_coverage = max(coverages, default=0)
    return {
        "frame_count": len(frames),
        "expected_participants": expected_participants,
        "maximum_participant_frame_count": maximum_coverage,
        "participant_frames_complete": bool(frames) and maximum_coverage >= expected_participants,
    }


def _timeline_events(frames: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for frame in frames:
        for event in _as_list(_field(frame, "events", default=[])):
            value = _as_mapping(event)
            if value:
                events.append(value)
    events.sort(key=lambda event: _int(_field(event, "timestamp")))
    return events


def _major_events(
    events: Sequence[Mapping[str, Any]],
    *,
    participant_by_id: Mapping[int, Mapping[str, Any]],
    detail: str,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    champion_kill_limit = 0 if detail == "summary" else 100 if detail == "full" else 60
    champion_kills = 0
    for event in events:
        event_type = str(_field(event, "type", default="")).upper()
        if event_type not in _MAJOR_EVENT_TYPES:
            continue
        if event_type == "CHAMPION_KILL":
            if champion_kills >= champion_kill_limit:
                continue
            champion_kills += 1
        killer_id = _int(_field(event, "killerId", "killer_id"))
        victim_id = _int(_field(event, "victimId", "victim_id"))
        killer = participant_by_id.get(killer_id, {})
        victim = participant_by_id.get(victim_id, {})
        record: dict[str, Any] = {
            "timestamp_ms": _int(_field(event, "timestamp")),
            "minute": _minute(_field(event, "timestamp")),
            "type": event_type,
        }
        if event_type == "CHAMPION_KILL":
            record.update(
                {
                    "killer": _participant_ref(killer),
                    "victim": _participant_ref(victim),
                    "assists": [
                        _participant_ref(participant_by_id.get(_int(item), {}))
                        for item in _as_list(
                            _field(
                                event,
                                "assistingParticipantIds",
                                "assisting_participant_ids",
                                default=[],
                            )
                        )
                    ],
                    "killer_team_id": _team_for_event(
                        event,
                        participant_by_id,
                        building=False,
                    ),
                    "bounty": _number(_field(event, "bounty")),
                    "shutdown_bounty": _number(_field(event, "shutdownBounty", "shutdown_bounty")),
                    "kill_type": _field(event, "killType", "kill_type"),
                }
            )
        elif event_type == "ELITE_MONSTER_KILL":
            record.update(
                {
                    "monster_type": _field(event, "monsterType", "monster_type"),
                    "monster_sub_type": _field(event, "monsterSubType", "monster_sub_type"),
                    "killer": _participant_ref(killer),
                    "killer_team_id": _team_for_event(
                        event,
                        participant_by_id,
                        building=False,
                    ),
                    "assists": [
                        _participant_ref(participant_by_id.get(_int(item), {}))
                        for item in _as_list(
                            _field(
                                event,
                                "assistingParticipantIds",
                                "assisting_participant_ids",
                                default=[],
                            )
                        )
                    ],
                }
            )
        elif event_type in {"BUILDING_KILL", "TURRET_PLATE_DESTROYED"}:
            destroyed_team = _int(_field(event, "teamId", "team_id"))
            record.update(
                {
                    "building_type": _field(event, "buildingType", "building_type"),
                    "tower_type": _field(event, "towerType", "tower_type"),
                    "lane": _field(event, "laneType", "lane_type"),
                    "destroyed_team_id": destroyed_team or None,
                    "killer": _participant_ref(killer),
                    "killer_team_id": _team_for_event(
                        event,
                        participant_by_id,
                        building=True,
                    ),
                }
            )
        elif event_type == "GAME_END":
            record["winning_team_id"] = _int(_field(event, "winningTeam", "winning_team"))
        elif event_type == "FEAT_UPDATE":
            record.update(
                {
                    "team_id": _int(_field(event, "teamId", "team_id")),
                    "feat_type": _field(event, "featType", "feat_type"),
                    "feat_value": _field(event, "featValue", "feat_value"),
                }
            )
        result.append(record)
    return result


def _gold_checkpoints(
    frames: Sequence[Mapping[str, Any]],
    *,
    participant_by_id: Mapping[int, Mapping[str, Any]],
    detail: str,
) -> list[dict[str, Any]]:
    if not frames:
        return []
    if detail == "full":
        selected = list(frames)
    else:
        interval = 10 if detail == "summary" else 5
        selected = [
            frame
            for frame in frames
            if round(_int(_field(frame, "timestamp")) / 60000) % interval == 0
        ]
        if frames[-1] not in selected:
            selected.append(frames[-1])
    result: list[dict[str, Any]] = []
    for frame in selected:
        participant_frames = _as_mapping(
            _field(frame, "participantFrames", "participant_frames", default={})
        )
        team_totals = _frame_team_totals(participant_frames, participant_by_id)
        blue = team_totals.get(100, _empty_frame_totals())
        red = team_totals.get(200, _empty_frame_totals())
        record: dict[str, Any] = {
            "timestamp_ms": _int(_field(frame, "timestamp")),
            "minute": _minute(_field(frame, "timestamp")),
            "teams": {
                "100": blue,
                "200": red,
            },
            "blue_minus_red": {
                key: _int(blue.get(key)) - _int(red.get(key))
                for key in ("total_gold", "xp", "lane_cs", "jungle_cs")
            },
        }
        if detail == "full":
            record["participants"] = {
                str(participant_id): {
                    "total_gold": _int(_field(value, "totalGold", "total_gold")),
                    "current_gold": _int(_field(value, "currentGold", "current_gold")),
                    "xp": _int(_field(value, "xp")),
                    "level": _int(_field(value, "level")),
                    "lane_cs": _int(_field(value, "minionsKilled", "minions_killed")),
                    "jungle_cs": _int(
                        _field(value, "jungleMinionsKilled", "jungle_minions_killed")
                    ),
                }
                for participant_id, raw in participant_frames.items()
                if (value := _as_mapping(raw))
            }
        result.append(record)
    return result


def _frame_team_totals(
    participant_frames: Mapping[str, Any],
    participant_by_id: Mapping[int, Mapping[str, Any]],
) -> dict[int, dict[str, int]]:
    totals: dict[int, dict[str, int]] = defaultdict(_empty_frame_totals)
    for key, raw in participant_frames.items():
        frame = _as_mapping(raw)
        participant_id = _int(_field(frame, "participantId", "participant_id")) or _int(key)
        participant = participant_by_id.get(participant_id, {})
        team_id = _int(_field(participant, "teamId", "team_id"))
        if team_id not in _TEAM_IDS:
            team_id = 100 if participant_id <= 5 else 200
        target = totals[team_id]
        target["total_gold"] += _int(_field(frame, "totalGold", "total_gold"))
        target["current_gold"] += _int(_field(frame, "currentGold", "current_gold"))
        target["xp"] += _int(_field(frame, "xp"))
        target["lane_cs"] += _int(_field(frame, "minionsKilled", "minions_killed"))
        target["jungle_cs"] += _int(_field(frame, "jungleMinionsKilled", "jungle_minions_killed"))
    return dict(totals)


def _empty_frame_totals() -> dict[str, int]:
    return {
        "total_gold": 0,
        "current_gold": 0,
        "xp": 0,
        "lane_cs": 0,
        "jungle_cs": 0,
    }


def _lane_matchups(
    participants: Sequence[Mapping[str, Any]],
    *,
    frames: Sequence[Mapping[str, Any]],
    duration: float,
) -> list[dict[str, Any]]:
    by_role: dict[str, dict[int, Mapping[str, Any]]] = defaultdict(dict)
    for participant in participants:
        role = str(
            _field(
                participant,
                "teamPosition",
                "team_position",
                "individualPosition",
                "individual_position",
                default="",
            )
        ).upper()
        team_id = _int(_field(participant, "teamId", "team_id"))
        if role and team_id in _TEAM_IDS:
            by_role[role][team_id] = participant
    result: list[dict[str, Any]] = []
    for role in ("TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"):
        pair = by_role.get(role, {})
        if 100 not in pair or 200 not in pair:
            continue
        blue = pair[100]
        red = pair[200]
        checkpoints: list[dict[str, Any]] = []
        for minute in (10, 15):
            if duration < minute * 60:
                continue
            frame = _nearest_frame(frames, minute * 60000)
            if frame is None:
                continue
            frame_values = _as_mapping(
                _field(frame, "participantFrames", "participant_frames", default={})
            )
            blue_frame = _participant_frame(
                frame_values,
                _int(_field(blue, "participantId", "participant_id")),
            )
            red_frame = _participant_frame(
                frame_values,
                _int(_field(red, "participantId", "participant_id")),
            )
            checkpoints.append(
                {
                    "minute": minute,
                    "blue_minus_red": {
                        "gold": _int(_field(blue_frame, "totalGold", "total_gold"))
                        - _int(_field(red_frame, "totalGold", "total_gold")),
                        "xp": _int(_field(blue_frame, "xp")) - _int(_field(red_frame, "xp")),
                        "cs": _frame_cs(blue_frame) - _frame_cs(red_frame),
                        "level": _int(_field(blue_frame, "level"))
                        - _int(_field(red_frame, "level")),
                    },
                }
            )
        result.append(
            {
                "role": role,
                "blue": _participant_ref(blue),
                "red": _participant_ref(red),
                "checkpoints": checkpoints,
                "final_blue_minus_red": {
                    "gold": _int(_field(blue, "goldEarned", "gold_earned"))
                    - _int(_field(red, "goldEarned", "gold_earned")),
                    "cs": _final_cs(blue) - _final_cs(red),
                    "champion_damage": _int(
                        _field(
                            blue,
                            "totalDamageDealtToChampions",
                            "total_damage_dealt_to_champions",
                        )
                    )
                    - _int(
                        _field(
                            red,
                            "totalDamageDealtToChampions",
                            "total_damage_dealt_to_champions",
                        )
                    ),
                },
            }
        )
    return result


def _teamfights(
    events: Sequence[Mapping[str, Any]],
    *,
    participant_by_id: Mapping[int, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    kills = [
        event
        for event in events
        if str(_field(event, "type", default="")).upper() == "CHAMPION_KILL"
    ]
    clusters: list[list[Mapping[str, Any]]] = []
    for event in kills:
        timestamp = _int(_field(event, "timestamp"))
        if clusters and timestamp - _int(_field(clusters[-1][-1], "timestamp")) <= 15000:
            clusters[-1].append(event)
        else:
            clusters.append([event])
    result: list[dict[str, Any]] = []
    for cluster in clusters:
        if len(cluster) < 2:
            continue
        team_kills: Counter[int] = Counter()
        participants: set[int] = set()
        for event in cluster:
            killer_id = _int(_field(event, "killerId", "killer_id"))
            victim_id = _int(_field(event, "victimId", "victim_id"))
            participants.update((killer_id, victim_id))
            participants.update(
                _int(item)
                for item in _as_list(
                    _field(
                        event,
                        "assistingParticipantIds",
                        "assisting_participant_ids",
                        default=[],
                    )
                )
            )
            team_id = _team_for_event(event, participant_by_id, building=False)
            if team_id:
                team_kills[team_id] += 1
        result.append(
            {
                "start_ms": _int(_field(cluster[0], "timestamp")),
                "end_ms": _int(_field(cluster[-1], "timestamp")),
                "minute": _minute(_field(cluster[0], "timestamp")),
                "kills_by_team": {str(key): value for key, value in team_kills.items()},
                "participants": [
                    _participant_ref(participant_by_id.get(participant_id, {}))
                    for participant_id in sorted(participants)
                    if participant_id > 0
                ],
                "proxy_notice": "Kill cluster within 15 seconds; not a replay-defined fight.",
            }
        )
    return result


def _item_milestones(
    events: Sequence[Mapping[str, Any]],
    *,
    participant_by_id: Mapping[int, Mapping[str, Any]],
    items: Mapping[int, Mapping[str, Any]],
    detail: str,
) -> list[dict[str, Any]]:
    if detail == "summary":
        return []
    result: list[dict[str, Any]] = []
    limit = 200 if detail == "full" else 80
    for event in events:
        event_type = str(_field(event, "type", default="")).upper()
        if event_type not in _ITEM_EVENT_TYPES:
            continue
        item_id = _int(_field(event, "itemId", "item_id", "afterId", "after_id"))
        item = items.get(item_id, {})
        if detail != "full" and event_type == "ITEM_PURCHASED":
            gold = _as_mapping(_field(item, "gold", default={}))
            if _int(_field(gold, "total")) < 900:
                continue
        participant_id = _int(_field(event, "participantId", "participant_id"))
        result.append(
            {
                "timestamp_ms": _int(_field(event, "timestamp")),
                "minute": _minute(_field(event, "timestamp")),
                "type": event_type,
                "participant": _participant_ref(participant_by_id.get(participant_id, {})),
                "item_id": item_id or None,
                "item_name": _field(item, "name"),
                "before_id": _number(_field(event, "beforeId", "before_id")),
                "after_id": _number(_field(event, "afterId", "after_id")),
            }
        )
        if len(result) >= limit:
            break
    return result


def _void_grub_analysis(
    *,
    teams: Sequence[Mapping[str, Any]],
    participants: Sequence[Mapping[str, Any]],
    events: Sequence[Mapping[str, Any]],
    frames: Sequence[Mapping[str, Any]],
    participant_by_id: Mapping[int, Mapping[str, Any]],
    game_version: str | None,
    game_mode: str | None,
    queue_id: int,
    queue: Mapping[str, Any],
    timeline_available: bool,
    timeline_complete: bool,
) -> dict[str, Any]:
    applicable, applicability_reason = _void_grub_applicability(
        game_version=game_version,
        game_mode=game_mode,
        queue_id=queue_id,
        queue=queue,
    )
    team_by_id = {_int(team.get("team_id")): team for team in teams}
    participant_summary_by_id = {_int(item.get("participant_id")): item for item in participants}
    captures: list[dict[str, Any]] = []
    timeline_counts: Counter[int] = Counter()
    for event in events:
        if not _is_grub_event(event):
            continue
        team_id = _team_for_event(event, participant_by_id, building=False)
        killer_id = _int(_field(event, "killerId", "killer_id"))
        if team_id:
            timeline_counts[team_id] += 1
        captures.append(
            {
                "timestamp_ms": _int(_field(event, "timestamp")),
                "minute": _minute(_field(event, "timestamp")),
                "team_id": team_id,
                "killer": _participant_ref(participant_by_id.get(killer_id, {})),
                "assists": [
                    _participant_ref(participant_by_id.get(_int(item), {}))
                    for item in _as_list(
                        _field(
                            event,
                            "assistingParticipantIds",
                            "assisting_participant_ids",
                            default=[],
                        )
                    )
                ],
            }
        )
    authoritative_counts: dict[int, int | None] = {}
    objective_counts_available: dict[int, bool] = {}
    for team_id in _TEAM_IDS:
        team = team_by_id.get(team_id, {})
        objectives = _as_mapping(team.get("objectives"))
        horde = _as_mapping(objectives.get("void_grubs"))
        objective_counts_available[team_id] = bool(horde.get("available"))
        if objective_counts_available[team_id]:
            authoritative_counts[team_id] = _int(horde.get("kills"))
        elif timeline_available:
            authoritative_counts[team_id] = timeline_counts[team_id]
        else:
            authoritative_counts[team_id] = None
        if timeline_counts[team_id] > 0 and authoritative_counts[team_id] is None:
            authoritative_counts[team_id] = timeline_counts[team_id]
    telemetry_available = any(objective_counts_available.values()) or timeline_available

    participant_building_damage: dict[int, int] = defaultdict(int)
    for participant in participants:
        team_id = _int(participant.get("team_id"))
        damage = _int(_field(_as_mapping(participant.get("damage")), "to_buildings"))
        participant_building_damage[team_id] += damage
    first_capture = {
        team_id: min(
            (
                _int(capture["timestamp_ms"])
                for capture in captures
                if _int(capture.get("team_id")) == team_id
            ),
            default=0,
        )
        for team_id in _TEAM_IDS
    }
    buildings_after: Counter[int] = Counter()
    buildings_next_five_minutes: Counter[int] = Counter()
    nearby_conversion: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        event_type = str(_field(event, "type", default="")).upper()
        timestamp = _int(_field(event, "timestamp"))
        event_team = _team_for_event(
            event,
            participant_by_id,
            building=event_type in {"BUILDING_KILL", "TURRET_PLATE_DESTROYED"},
        )
        if event_type == "BUILDING_KILL" and event_team in _TEAM_IDS:
            first = first_capture.get(event_team, 0)
            if first and timestamp >= first:
                buildings_after[event_team] += 1
                if timestamp <= first + 300000:
                    buildings_next_five_minutes[event_team] += 1
        for capture_team in _TEAM_IDS:
            capture_time = first_capture.get(capture_team, 0)
            if not capture_time or timestamp <= capture_time or timestamp > capture_time + 180000:
                continue
            if event_type not in {"BUILDING_KILL", "CHAMPION_KILL", "ELITE_MONSTER_KILL"}:
                continue
            if event_type == "ELITE_MONSTER_KILL" and _is_grub_event(event):
                continue
            nearby_conversion[capture_team].append(
                {
                    "timestamp_ms": timestamp,
                    "seconds_after_first_capture": round((timestamp - capture_time) / 1000),
                    "type": event_type,
                    "acting_team_id": event_team,
                    "monster_type": _field(event, "monsterType", "monster_type"),
                    "building_type": _field(event, "buildingType", "building_type"),
                }
            )

    team_conversion: dict[str, dict[str, Any]] = {}
    for team_id in _TEAM_IDS:
        first = first_capture.get(team_id, 0)
        before = _team_gold_snapshot(frames, participant_by_id, team_id, first) if first else None
        after = (
            _team_gold_snapshot(frames, participant_by_id, team_id, first + 120000)
            if first
            else None
        )
        opponent = 300 - team_id
        opponent_before = (
            _team_gold_snapshot(frames, participant_by_id, opponent, first) if first else None
        )
        opponent_after = (
            _team_gold_snapshot(frames, participant_by_id, opponent, first + 120000)
            if first
            else None
        )
        gold_swing = None
        if (
            first
            and before is not None
            and after is not None
            and opponent_before is not None
            and opponent_after is not None
        ):
            gold_swing = (
                _int(after["total_gold"])
                - _int(opponent_after["total_gold"])
                - _int(before["total_gold"])
                + _int(opponent_before["total_gold"])
            )
        team = team_by_id.get(team_id, {})
        team_conversion[str(team_id)] = {
            "capture_count": authoritative_counts.get(team_id),
            "first_capture_ms": first or None,
            "first_capture_minute": _minute(first) if first else None,
            "net_gold_swing_next_two_minutes": gold_swing,
            "gold_window": {
                "baseline": before,
                "after_two_minutes": after,
                "maximum_frame_distance_ms": 90000,
            },
            "events_next_three_minutes": nearby_conversion.get(team_id, []),
            "buildings_destroyed_next_five_minutes": buildings_next_five_minutes[team_id],
            "long_horizon_outcomes": {
                "buildings_destroyed_after_first_capture": buildings_after[team_id],
                "final_turrets": _int(
                    _field(
                        _as_mapping(_as_mapping(team.get("objectives")).get("tower")),
                        "kills",
                    )
                ),
                "final_building_damage": participant_building_damage[team_id],
                "won": bool(team.get("win", False)),
            },
        }

    assessment = _grub_assessment(
        counts=authoritative_counts,
        conversion=team_conversion,
        applicable=applicable,
        telemetry_available=telemetry_available,
        timeline_available=timeline_available,
        timeline_complete=timeline_complete,
    )
    contributor_counts: Counter[int] = Counter()
    for capture in captures:
        killer = _as_mapping(capture.get("killer"))
        killer_id = _int(killer.get("participant_id"))
        if killer_id:
            contributor_counts[killer_id] += 1
        for assist in _as_list(capture.get("assists")):
            assist_id = _int(_field(_as_mapping(assist), "participant_id"))
            if assist_id:
                contributor_counts[assist_id] += 1
    return {
        "applicable": applicable,
        "applicability_reason": applicability_reason,
        "available": telemetry_available,
        "telemetry_available": telemetry_available,
        "captures_observed": bool(captures)
        or any((value or 0) > 0 for value in authoritative_counts.values()),
        "observed": {
            "team_counts": {str(key): value for key, value in authoritative_counts.items()},
            "timeline_counts": {str(key): timeline_counts[key] for key in _TEAM_IDS},
            "captures": captures,
            "credited_participants": [
                {
                    "participant": _as_mapping(participant_summary_by_id.get(key, {})),
                    "credited_capture_events": value,
                }
                for key, value in contributor_counts.most_common()
            ],
            "credit_limit": (
                "Only killer and assist credits present in timeline events are reported; "
                "they are not a complete participation model."
            ),
        },
        "conversion_proxies": team_conversion,
        "assessment": assessment,
        "mechanics_context": _void_grub_knowledge(game_version),
        "mode_note": applicability_reason if applicable is not True else None,
        "causal_limit": (
            "Match V5 does not report per-hit Void Grub buff damage or a counterfactual without the buff. "
            "The assessment measures capture and later conversion association, not exact causal damage."
        ),
    }


def _grub_assessment(
    *,
    counts: Mapping[int, int | None],
    conversion: Mapping[str, Mapping[str, Any]],
    applicable: bool | None,
    telemetry_available: bool,
    timeline_available: bool,
    timeline_complete: bool,
) -> dict[str, Any]:
    completeness = "high" if timeline_complete else "moderate" if timeline_available else "low"
    common = {
        "confidence": completeness,
        "confidence_kind": "telemetry_completeness_not_causality",
        "causal_confidence": "not_estimable",
        "method": "Deterministic, uncalibrated association heuristic over bounded telemetry proxies.",
    }
    if applicable is False:
        return {
            "classification": "not_applicable",
            "leader_team_id": None,
            "summary": "Void Grubs were not applicable under the detected patch and queue rules.",
            "evidence": [],
            **common,
        }
    if not telemetry_available or all(counts.get(team_id) is None for team_id in _TEAM_IDS):
        return {
            "classification": "telemetry_unavailable",
            "leader_team_id": None,
            "summary": "Available telemetry cannot establish Void Grub captures for this match.",
            "evidence": [],
            **common,
        }
    blue_count = _int(counts.get(100))
    red_count = _int(counts.get(200))
    if blue_count == 0 and red_count == 0:
        return {
            "classification": "no_observed_void_grubs",
            "leader_team_id": None,
            "summary": "Neither team has an observed Void Grub capture.",
            "evidence": [],
            **common,
        }
    if blue_count == red_count:
        return {
            "classification": "contested_or_even",
            "leader_team_id": None,
            "summary": "Capture count was even; value depends on capture cost and later conversion.",
            "evidence": [f"Both teams recorded {blue_count} captures."],
            **common,
        }
    leader = 100 if blue_count > red_count else 200
    opponent = 300 - leader
    leader_data = _as_mapping(conversion.get(str(leader)))
    opponent_data = _as_mapping(conversion.get(str(opponent)))
    gold_swing = _number(leader_data.get("net_gold_swing_next_two_minutes"))
    bounded_building_delta = _int(leader_data.get("buildings_destroyed_next_five_minutes")) - _int(
        opponent_data.get("buildings_destroyed_next_five_minutes")
    )
    nearby_events = [
        _as_mapping(value) for value in _as_list(leader_data.get("events_next_three_minutes"))
    ]
    favorable_events = sum(
        1 for event in nearby_events if _int(event.get("acting_team_id")) == leader
    )
    unfavorable_events = sum(
        1 for event in nearby_events if _int(event.get("acting_team_id")) == opponent
    )
    score = 0
    evidence = [f"Team {leader} led captures {counts.get(leader, 0)}-{counts.get(opponent, 0)}."]
    if gold_swing is not None and gold_swing > 500:
        score += 1
        evidence.append("The capture leader improved its gold lead over the next two minutes.")
    elif gold_swing is not None and gold_swing < -500:
        score -= 1
        evidence.append("The capture leader lost net gold ground over the next two minutes.")
    if favorable_events > unfavorable_events:
        score += 1
        evidence.append(
            "The capture leader had more favorable recorded events in the next three minutes."
        )
    elif unfavorable_events > favorable_events:
        score -= 1
        evidence.append(
            "The opponent had more favorable recorded events in the next three minutes."
        )
    if bounded_building_delta > 0:
        score += 1
        evidence.append(
            "The capture leader destroyed more buildings in its bounded five-minute window."
        )
    elif bounded_building_delta < 0:
        score -= 1
        evidence.append("The opponent destroyed more buildings in its bounded five-minute window.")
    if score >= 2:
        classification = "strong_positive_conversion_association"
        summary = "The capture advantage aligned with strong bounded conversion signals."
    elif score == 1:
        classification = "moderate_positive_conversion_association"
        summary = "The capture advantage aligned with some bounded conversion signals."
    elif score < 0:
        classification = "poor_or_negative_conversion"
        summary = "The capture advantage aligned with unfavorable bounded conversion signals."
    else:
        classification = "limited_or_mixed_conversion"
        summary = "The bounded conversion signals are mixed or limited."
    leader_outcomes = _as_mapping(leader_data.get("long_horizon_outcomes"))
    opponent_outcomes = _as_mapping(opponent_data.get("long_horizon_outcomes"))
    turret_delta = _int(leader_outcomes.get("final_turrets")) - _int(
        opponent_outcomes.get("final_turrets")
    )
    building_damage_delta = _int(leader_outcomes.get("final_building_damage")) - _int(
        opponent_outcomes.get("final_building_damage")
    )
    return {
        "classification": classification,
        "leader_team_id": leader,
        "conversion_signal_score": score,
        "summary": summary,
        "evidence": evidence,
        "long_horizon_context": {
            "scored": False,
            "capture_leader_won": bool(leader_outcomes.get("won")),
            "final_turret_delta": turret_delta,
            "final_building_damage_delta": building_damage_delta,
        },
        **common,
    }


def _void_grub_applicability(
    *,
    game_version: str | None,
    game_mode: str | None,
    queue_id: int,
    queue: Mapping[str, Any],
) -> tuple[bool | None, str]:
    major, minor = _patch_parts(game_version)
    if major is not None and major < 14:
        return False, "Void Grubs did not exist on standard Summoner's Rift before patch 14.1."
    queue_text = " ".join(
        str(queue.get(key, "")) for key in ("map", "description", "notes")
    ).casefold()
    is_swiftplay = queue_id == 480 or "swiftplay" in queue_text
    if is_swiftplay and major == 16 and (minor or 0) >= 1:
        return False, "Void Grubs were removed from Swiftplay beginning with patch 26.1/16.1."
    if str(game_mode or "").upper() != "CLASSIC":
        return None, "Void Grub availability is not established for this non-Classic mode."
    if major in {14, 15, 16}:
        return True, "Void Grubs were available under the detected standard rules."
    return None, "Void Grub availability could not be established for this patch and queue."


def _void_grub_knowledge(patch: str | None) -> dict[str, Any]:
    major, minor = _patch_parts(patch)
    if major is not None and major < 14:
        band = "before_patch_14_1"
        mechanics = ["Void Grubs were not part of standard Summoner's Rift before patch 14.1."]
        sources = [_OFFICIAL_SOURCES["void_grubs_14_1"]]
    elif major == 14 or (major == 15 and (minor or 0) < 9):
        band = "patch_14_1_through_15_8"
        mechanics = [
            "Two spawn groups could produce up to six team stacks.",
            "Captures granted a stacking structure-damage reward; high stacks could summon Voidmites.",
            "Capture value included direct rewards, top-side control, and future siege pressure.",
        ]
        sources = [_OFFICIAL_SOURCES["void_grubs_14_1"]]
    elif major == 15:
        band = "patch_15_9_and_later_2025"
        mechanics = [
            "The encounter moved to eight minutes, no longer respawned, and capped at three captures.",
            "Three captures granted the single-Voidmite Hunger of the Void reward.",
            "Two of three captures were enough for the period's Feats credit.",
        ]
        sources = [_OFFICIAL_SOURCES["void_grubs_25_9"]]
    elif major == 16:
        band = "patch_16_1_and_later_2026"
        mechanics = [
            "Standard Summoner's Rift retained the three-Grub single encounter and structure-pressure buff.",
            "Patch 26.1 concentrated each Grub's gold on its killer and removed the killer heal.",
            "Swiftplay rules can remove Void Grubs entirely, so queue context matters.",
        ]
        sources = [
            _OFFICIAL_SOURCES["void_grubs_25_9"],
            _OFFICIAL_SOURCES["void_grubs_26_1"],
            "https://raw.communitydragon.org/16.15/game/data/characters/sru_horde/sru_horde.bin.json",
        ]
    else:
        band = "patch_unknown"
        mechanics = [
            "Void Grub spawn count, rewards, and related seasonal systems are patch-sensitive.",
            "Use the match gameVersion and queue before applying a mechanics interpretation.",
        ]
        sources = [
            _OFFICIAL_SOURCES["void_grubs_14_1"],
            _OFFICIAL_SOURCES["void_grubs_25_9"],
            _OFFICIAL_SOURCES["void_grubs_26_1"],
        ]
    result: dict[str, Any] = {
        "patch_band": band,
        "mode_scope": "standard Map 11 CLASSIC; Swiftplay rules differ",
        "mechanics": mechanics,
        "impact_framework": [
            "Capture benefit: local/team rewards and denied opponent captures.",
            "Capture cost: time, health, lane resources, deaths, and cross-map objectives.",
            "Conversion: later structure pressure, map access, and whether the team used the timing.",
        ],
        "telemetry_limit": (
            "Match V5 records horde totals and capture events but not exact per-hit buff damage."
        ),
        "sources": sources,
    }
    if major == 16:
        result["direct_reward_model"] = {
            "each_grub": {
                "killer_gold": 30,
                "local_xp": 65,
                "xp_radius_units": 2000,
            },
            "three_grubs": {
                "base_gold_total": 90,
                "raw_local_xp_total_before_sharing": 195,
            },
            "allocation_warning": "The 90 gold is total killer gold, not 90 per teammate.",
            "classification": "patch rule, not proof of each recipient's realized XP",
        }
    return result


def _economy_knowledge(topic: str, patch: str | None) -> dict[str, Any]:
    if topic == "item_efficiency":
        return _item_efficiency_knowledge(patch)

    major, minor = _patch_parts(patch)
    requested_supported = patch is None or (major == 16 and minor is not None and 1 <= minor <= 15)
    patch_identity = {
        "requested": patch,
        "normalized_internal_patch": (
            "16.15" if patch is None else f"{major}.{minor}" if major is not None else None
        ),
        "rules_snapshot": "public_26.15_internal_16.15",
        "verified_through": "26.15",
        "model_status": (
            "current_reference"
            if patch is None
            else "available"
            if requested_supported
            else "unavailable"
        ),
        "mode_scope": "Map 11 CLASSIC standard Summoner's Rift only",
        "excluded_modes": ["Swiftplay", "ARAM", "Arena", "other alternate modes"],
    }
    analysis_model = {
        "separation": {
            "observed": "Riot Match V5 totals, frames, and events only.",
            "derived": "Arithmetic computed solely from observed fields.",
            "modelled": "Patch rules plus explicit collection, proximity, sharing, and wave assumptions.",
        },
        "opportunity_cost": [
            "Price last-hit gold and proximity XP separately because they use different collection rules.",
            "Add plates, structures, camps, objective rewards, recall timing, and cross-map pressure gained or conceded.",
            "Compare the bounded post-decision gold, XP, CS, deaths, and objective deltas before judging the trade.",
            "Do not infer exact missed gold or XP from CS alone when minion types and nearby recipients are unknown.",
        ],
        "anti_double_counting": [
            "Keep killer, local-shared, and global-each rewards as separate allocations.",
            "Do not add a global team reward again inside a local fight swing.",
            "Keep objective bounties separate from fixed base rewards.",
        ],
    }
    limitations = [
        "Match V5 does not expose every minion death, minion type, missed last hit, or nearby XP recipient.",
        "A theoretical wave total is opportunity under stated assumptions, not proof that a player received it.",
        "Role quests, lane protection, jungle items, inhibitor state, bounties, and mode rules can modify realized value.",
        "Unknown or out-of-band patches return no numeric model rather than borrowing another patch's values.",
    ]
    sources = [
        _OFFICIAL_SOURCES["economy_26_1"],
        _OFFICIAL_SOURCES["caster_gold_11_19"],
        "https://www.leagueoflegends.com/en-us/news/game-updates/league-of-legends-patch-26-15-notes/",
        "https://www.leagueoflegends.com/en-us/news/game-updates/league-of-legends-patch-26-9-notes/",
        "https://www.leagueoflegends.com/en-us/news/game-updates/league-of-legends-patch-26-7-notes/",
        "https://www.leagueoflegends.com/en-au/news/game-updates/patch-25-s1-1-notes/",
        "https://raw.communitydragon.org/16.15/game/data/maps/shipping/map11/map11.bin.json",
        "https://raw.communitydragon.org/16.15/game/data/characters/sru_orderminionmelee/sru_orderminionmelee.bin.json",
        "https://raw.communitydragon.org/16.15/game/data/characters/sru_orderminionranged/sru_orderminionranged.bin.json",
        "https://raw.communitydragon.org/16.15/game/data/characters/sru_orderminionsiege/sru_orderminionsiege.bin.json",
        "https://raw.communitydragon.org/16.15/game/data/characters/sru_horde/sru_horde.bin.json",
        "https://raw.communitydragon.org/16.15/game/data/characters/sru_riftherald/sru_riftherald.bin.json",
        "https://raw.communitydragon.org/16.15/game/data/characters/sru_baron/sru_baron.bin.json",
        "https://raw.communitydragon.org/16.15/game/data/characters/sru_dragon_air/sru_dragon_air.bin.json",
        "https://raw.communitydragon.org/16.15/game/data/characters/sru_dragon_elder/sru_dragon_elder.bin.json",
        "https://raw.communitydragon.org/16.15/game/data/characters/turret/turret.bin.json",
    ]
    if not requested_supported:
        return {
            "patch_identity": patch_identity,
            "analysis_model": analysis_model,
            "limitations": limitations,
            "unavailable_reason": (
                "The bundled quantitative registry covers standard Summoner's Rift patches "
                "26.1 through 26.15 (internal 16.1 through 16.15)."
            ),
            "sources": sources,
        }

    shared_xp = {
        "unit": "fraction of solo XP received by each nearby allied champion",
        "proximity_radius_units": 1500,
        "per_recipient_multiplier": {
            "1": 1.0,
            "2": 0.65,
            "3": 0.433,
            "4": 0.325,
            "5": 0.26,
            "6": 0.217,
        },
        "formula": "recipient XP = summed base XP × multiplier for nearby allied champion count",
        "source_kind": "Riot patch notes plus patch-pinned client data",
        "confidence": "high",
    }
    minion_units = {
        "melee": {
            "last_hit_gold": 20,
            "base_xp": 62,
            "allocation": {"gold": "killer", "xp": "local proximity"},
        },
        "caster": {
            "last_hit_gold": 14,
            "base_xp": 31,
            "allocation": {"gold": "killer", "xp": "local proximity"},
        },
        "siege_or_super": {
            "initial_last_hit_gold": 50,
            "gold_growth": "+1 every 90 seconds",
            "growth_cap": None,
            "base_xp": 75,
            "allocation": {"gold": "killer", "xp": "local proximity"},
        },
        "units": {"gold": "gold", "xp": "experience points"},
        "source_kind": "Riot patch notes; caster gold cross-checked in patch-pinned client data",
        "confidence": "high",
    }
    wave_schedule = {
        "first_spawn_seconds": 30,
        "spawn_interval_seconds": [
            {"from_minute": 0, "until_minute": 14, "seconds": 30},
            {"from_minute": 14, "until_minute": 30, "seconds": 25},
            {"from_minute": 30, "until_minute": None, "seconds": 20},
        ],
        "first_cannon_wave": 3,
        "cannon_cadence": [
            {"from_minute": 0, "until_minute": 14, "every_nth_wave": 3},
            {"from_minute": 14, "until_minute": 25, "every_nth_wave": 2},
            {"from_minute": 25, "until_minute": None, "every_nth_wave": 1},
        ],
        "composition_changes": [
            "Cannon waves at or after 14:00 have two melee minions instead of three.",
            "Every wave at or after 30:00 has two caster minions instead of three.",
            "One super minion is added with one or two enemy inhibitors down; two are added when all three are down.",
        ],
        "source_kind": "Riot patch notes plus patch-pinned CommunityDragon Barracks configuration",
        "confidence": "high",
    }
    wave_examples = [
        _wave_example(
            label="normal_non_cannon_wave_before_25",
            composition={"melee": 3, "caster": 3, "siege": 0, "super": 0},
        ),
        _wave_example(
            label="cannon_wave_before_14",
            composition={"melee": 3, "caster": 3, "siege": 1, "super": 0},
        ),
        _wave_example(
            label="cannon_wave_from_14",
            composition={"melee": 2, "caster": 3, "siege": 1, "super": 0},
        ),
        _wave_example(
            label="every_wave_from_30",
            composition={"melee": 2, "caster": 2, "siege": 1, "super": 0},
        ),
    ]
    passive_gold = {
        "starts_at_seconds": 65,
        "rate_gold_per_second": 2.04,
        "engine_grant": {"gold": 10.2, "interval_seconds": 5},
        "continuous_equivalent_formula": "max(0, elapsed_seconds - 65) × 2.04",
        "rounding_note": "Visible values follow server grant ticks and game rounding.",
        "source_kind": "Riot patch notes plus patch-pinned Map 11 CLASSIC constants",
        "confidence": "high",
    }
    role_modifiers = {
        "assigned_lane_before_level_3": {
            "outside_assigned_lane_gold_multiplier": 0.75,
            "outside_assigned_lane_xp_multiplier": 0.75,
            "support_assigned_lane": "bottom",
        },
        "bottom_quest_completed": {
            "one_time_gold": 300,
            "bonus_gold_per_minion_kill": 2,
        },
        "top_quest_completed": {
            "non_champion_xp_multiplier": (
                1.11 if patch is None or (major == 16 and (minor or 0) >= 9) else 1.125
            ),
            "effective_public_patch": (
                "26.9" if patch is None or (major == 16 and (minor or 0) >= 9) else "26.1"
            ),
        },
        "support_excess_minion_penalty": {
            "status": (
                "removed"
                if patch is None or (major == 16 and (minor or 0) >= 7)
                else "present_but_not_quantified_here"
            ),
            "removed_in_public_patch": "26.7",
        },
        "jungle_item_lane_minion_xp": {
            "status": "patch-sensitive and partly opaque",
            "rule": "Do not interpolate an exact early-game penalty without validated game state.",
        },
    }
    structures = {
        "outer_turret": {
            "plate_thresholds_percent_missing_hp": [10, 25, 45, 70, 100],
            "local_gold_per_plate": {
                "before_11_minutes": 120,
                "11_to_before_12": 110,
                "12_to_before_13": 100,
                "13_to_before_14": 90,
                "from_14_minutes": 80,
            },
            "five_plate_local_gold_range": [400, 600],
            "separate_local_destruction_gold": 0,
            "global_gold_each_ally": 50,
        },
        "inner_turret": {
            "plate_thresholds": 5,
            "local_gold_total": 600,
            "local_gold_per_threshold": 120,
            "global_gold_each_ally": 25,
        },
        "inhibitor_turret": {
            "plate_thresholds": 5,
            "local_gold_total": 600,
            "local_gold_per_threshold": 120,
            "global_gold_each_ally": 25,
        },
        "first_turret_bonus": {
            "local_shared_gold": 300,
            "allocation": "shared by nearby allies",
        },
        "nexus_turret": {
            "local_gold": None,
            "reason": "mode-specific extracted records are not resolved robustly enough",
        },
        "confidence": {
            "plate_and_first_turret_rules": "official_current",
            "global_gold": "high_confidence_carry_forward",
        },
    }
    objectives = {
        "elemental_dragon": {
            "killer_gold": 75,
            "local_xp": {"minimum": 160, "maximum": 400, "scales_with_monster_level": True},
            "xp_radius_units": 2000,
        },
        "void_grub_each": {
            "killer_gold": 30,
            "local_xp": 65,
            "xp_radius_units": 2000,
        },
        "three_void_grubs": {
            "base_gold_total": 90,
            "raw_local_xp_total_before_sharing": 195,
            "allocation_warning": "The 90 gold is total killer gold, not 90 gold per teammate.",
        },
        "rift_herald": {"killer_gold": 100, "local_xp": 240, "xp_radius_units": 2000},
        "baron": {
            "killer_gold": 100,
            "global_gold_each_ally": 150,
            "global_xp_each_ally": 650,
            "five_player_team_totals": {"gold": 850, "xp": 3250},
        },
        "elder_dragon": {
            "killer_gold": 100,
            "global_gold_each_ally": 150,
            "global_xp_each_ally": 650,
            "five_player_team_totals": {"gold": 850, "xp": 3250},
        },
        "objective_bounties": "Conditional additions; never included in fixed base rewards.",
        "source_kind": "patch-pinned CommunityDragon character records with Riot patch-note checks",
    }
    sections = {
        "economy": {
            "patch_identity": patch_identity,
            "minion_units": minion_units,
            "wave_schedule": wave_schedule,
            "derived_wave_examples": wave_examples,
            "experience_sharing": shared_xp,
            "passive_gold": passive_gold,
            "role_modifiers": role_modifiers,
            "structures": structures,
            "neutral_objectives": objectives,
            "analysis_model": analysis_model,
            "limitations": limitations,
            "sources": sources,
        },
        "minions": {
            "patch_identity": patch_identity,
            "minion_units": minion_units,
            "wave_schedule": wave_schedule,
            "derived_wave_examples": wave_examples,
            "experience_sharing": shared_xp,
            "role_modifiers": role_modifiers,
            "analysis_model": analysis_model,
            "limitations": limitations,
            "sources": sources,
        },
        "experience": {
            "patch_identity": patch_identity,
            "experience_sharing": shared_xp,
            "minion_base_xp": {
                key: value["base_xp"]
                for key, value in minion_units.items()
                if isinstance(value, Mapping) and "base_xp" in value
            },
            "derived_wave_examples": wave_examples,
            "role_modifiers": role_modifiers,
            "analysis_model": analysis_model,
            "limitations": limitations,
            "sources": sources,
        },
        "structures": {
            "patch_identity": patch_identity,
            "structures": structures,
            "neutral_objectives": objectives,
            "analysis_model": analysis_model,
            "limitations": limitations,
            "sources": sources,
        },
    }
    return sections[topic]


def _wave_example(
    *,
    label: str,
    composition: Mapping[str, int],
) -> dict[str, Any]:
    base_gold = (
        composition.get("melee", 0) * 20
        + composition.get("caster", 0) * 14
        + (composition.get("siege", 0) + composition.get("super", 0)) * 50
    )
    base_xp = (
        composition.get("melee", 0) * 62
        + composition.get("caster", 0) * 31
        + (composition.get("siege", 0) + composition.get("super", 0)) * 75
    )
    multipliers = {"1": 1.0, "2": 0.65, "3": 0.433, "4": 0.325, "5": 0.26, "6": 0.217}
    return {
        "label": label,
        "composition": dict(composition),
        "base_last_hit_gold": base_gold,
        "base_xp": base_xp,
        "xp_received_per_nearby_champion": {
            count: _round(base_xp * multiplier, 3) for count, multiplier in multipliers.items()
        },
        "assumptions": [
            "Every listed minion is collected for gold and the recipient is in XP range.",
            "Siege and super gold uses its initial 50-gold value; add the applicable growth separately.",
            "No role, quest, jungle-item, bounty, or alternate-mode modifier is applied.",
        ],
        "classification": "modelled opportunity, not observed receipt",
    }


def _item_efficiency_knowledge(patch: str | None) -> dict[str, Any]:
    return {
        "patch_identity": {
            "requested": patch,
            "resolution_rule": "Use an exact matching Data Dragon release; never substitute another patch.",
        },
        "definition": (
            "Raw-stat gold efficiency divides the gold value of priceable structured base stats "
            "by the item's total purchase cost."
        ),
        "method": [
            "Load the target item and pure component anchors from the same Data Dragon patch.",
            "Derive each gold-per-stat rate from that patch's component price and structured stat amount.",
            "Sum only represented, independently priceable base stats and report coverage.",
            "Use riot_lol_item_economy with an item ID or exact item name for a calculation.",
        ],
        "baseline_component_ids": {
            "attack_damage": 1036,
            "ability_power": 1052,
            "health": 1028,
            "mana": 1027,
            "armor": 1029,
            "magic_resistance": 1033,
            "attack_speed": 1042,
            "movement_speed": 1001,
            "critical_strike_chance": 1018,
        },
        "interpretation": [
            "The result is a comparison methodology, not an official Riot metric.",
            "A result above or below 100% does not by itself make an item good or bad.",
            "Champion synergy, timing, slot efficiency, passives, actives, conditions, and opponent state still matter.",
        ],
        "limitations": [
            "Data Dragon's structured stats omit some tooltip stats, including ability haste on some items.",
            "Unrepresented stats and all passive, active, conditional, transformation, and mode-specific effects remain unpriced.",
            "A partial raw-stat value must never be described as total item value.",
        ],
        "sources": [_OFFICIAL_SOURCES["data_dragon"]],
    }


def _knowledge_detail(content: Mapping[str, Any], detail: str) -> dict[str, Any]:
    result = {str(key): _to_data(value) for key, value in content.items()}
    if detail != "summary":
        return result
    return {
        key: value[:2] if isinstance(value, list) and key != "sources" else value
        for key, value in result.items()
    }


def _player_context_payload(
    *,
    riot_id: str,
    account: Mapping[str, Any],
    puuid: str,
    summoner: Any,
    ranked: Any,
    mastery: Any,
    challenges: Any,
    matches: Sequence[Mapping[str, Any]],
    requested_count: int,
    match_ids: Sequence[str],
    champions: Mapping[int, Mapping[str, Any]],
    route: str | None,
    question: str | None,
    detail: str,
    warnings: list[str],
    sources: list[dict[str, str]],
    unavailable_sections: list[str],
) -> dict[str, Any]:
    summoner_data = _as_mapping(summoner)
    ranked_entries = [_ranked_entry(_as_mapping(item)) for item in _as_list(ranked)]
    mastery_entries = [_mastery_entry(_as_mapping(item), champions) for item in _as_list(mastery)]
    recent: list[dict[str, Any]] = []
    for match in matches:
        info = _as_mapping(_field(match, "info", default={}))
        metadata = _as_mapping(_field(match, "metadata", default={}))
        participant_values = [
            _as_mapping(value) for value in _as_list(_field(info, "participants", default=[]))
        ]
        participant = next(
            (
                value
                for value in participant_values
                if str(_field(value, "puuid", default="")) == puuid
            ),
            None,
        )
        if participant is None:
            warnings.append(
                f"Match {_field(metadata, 'matchId', 'match_id', default='unknown')} lacked the resolved player."
            )
            continue
        duration = _duration_seconds(_field(info, "gameDuration", "game_duration", default=0))
        team_id = _int(_field(participant, "teamId", "team_id"))
        team_kills = sum(
            _int(_field(value, "kills"))
            for value in participant_values
            if _int(_field(value, "teamId", "team_id")) == team_id
        )
        summary = _participant_summary(
            participant,
            duration=duration,
            team_kills=team_kills,
            items={},
            spells={},
            runes={},
        )
        recent.append(
            {
                "match_id": _field(metadata, "matchId", "match_id"),
                "game_version": _field(info, "gameVersion", "game_version"),
                "queue_id": _int(_field(info, "queueId", "queue_id")),
                "started_at": _iso_timestamp(
                    _field(info, "gameStartTimestamp", "game_start_timestamp")
                ),
                "duration_seconds": duration,
                "player": summary,
                "team_objectives": _match_team_objectives(info, team_id),
            }
        )
    loaded_count = len(matches)
    analyzed_count = len(recent)
    aggregate = _recent_aggregate(recent)
    challenge_data = _as_mapping(challenges)
    challenge_summary = {
        "total_points": _to_data(_field(challenge_data, "totalPoints", "total_points", default={})),
        "category_points": _to_data(
            _field(challenge_data, "categoryPoints", "category_points", default={})
        ),
        "challenge_count": len(_as_list(_field(challenge_data, "challenges", default=[]))),
        "preferences": _to_data(_field(challenge_data, "preferences", default={})),
    }
    if detail == "summary":
        recent = recent[:3]
        mastery_entries = mastery_entries[:5]
    returned_count = len(recent)
    return {
        "identity": {
            "riot_id": riot_id,
            "game_name": _field(account, "gameName", "game_name"),
            "tag_line": _field(account, "tagLine", "tag_line"),
            "platform_route": route,
        },
        "summoner": {
            "summoner_level": _int(_field(summoner_data, "summonerLevel", "summoner_level")),
            "profile_icon_id": _int(_field(summoner_data, "profileIconId", "profile_icon_id")),
            "revision_date": _iso_timestamp(_field(summoner_data, "revisionDate", "revision_date")),
        },
        "ranked_entries": ranked_entries,
        "top_champion_mastery": mastery_entries,
        "challenges": challenge_summary,
        "recent_matches": {
            "requested": requested_count,
            "ids_returned": len(match_ids),
            "loaded": loaded_count,
            "analyzed": analyzed_count,
            "returned": returned_count,
            "matches": recent,
            "aggregate": aggregate,
            "sample_notice": (
                "This bounded recent sample is descriptive and is not an MMR or durable skill estimate."
            ),
        },
        "question_relevance": _question_relevance(question, scope="player"),
        "data_quality": {
            "warnings": warnings,
            "unavailable_sections": unavailable_sections,
            "optional_sections_may_be_missing": bool(warnings),
            "limitations": [
                "Riot's public API requires an exact Riot ID and route; it is not unrestricted player search.",
                "Hidden MMR, biographies, esports rosters, intent, and private information are unavailable.",
                "Recent-match aggregates depend on sample size, queues, roles, and successfully loaded matches.",
            ],
        },
        "provenance": {"sources": sources},
    }


def _ranked_entry(entry: Mapping[str, Any]) -> dict[str, Any]:
    wins = _int(_field(entry, "wins"))
    losses = _int(_field(entry, "losses"))
    games = wins + losses
    return {
        "queue_type": _field(entry, "queueType", "queue_type"),
        "tier": _field(entry, "tier"),
        "division": _field(entry, "rank"),
        "league_points": _int(_field(entry, "leaguePoints", "league_points")),
        "wins": wins,
        "losses": losses,
        "win_rate": _round(wins / games) if games else None,
        "hot_streak": bool(_field(entry, "hotStreak", "hot_streak", default=False)),
        "veteran": bool(_field(entry, "veteran", default=False)),
        "inactive": bool(_field(entry, "inactive", default=False)),
    }


def _mastery_entry(
    entry: Mapping[str, Any],
    champions: Mapping[int, Mapping[str, Any]],
) -> dict[str, Any]:
    champion_id = _int(_field(entry, "championId", "champion_id"))
    return {
        "champion_id": champion_id,
        "champion_name": _field(champions.get(champion_id, {}), "name"),
        "level": _int(_field(entry, "championLevel", "champion_level")),
        "points": _int(_field(entry, "championPoints", "champion_points")),
        "last_played_at": _iso_timestamp(_field(entry, "lastPlayTime", "last_play_time")),
        "chest_granted": bool(_field(entry, "chestGranted", "chest_granted", default=False)),
        "tokens_earned": _number(_field(entry, "tokensEarned", "tokens_earned")),
    }


def _recent_aggregate(recent: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if not recent:
        return {
            "games": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": None,
            "champions": {},
            "roles": {},
            "averages": {},
        }
    players = [_as_mapping(item.get("player")) for item in recent]
    wins = sum(1 for player in players if bool(player.get("win")))
    champions = Counter(
        str(_field(_as_mapping(player.get("champion")), "name", default="Unknown"))
        for player in players
    )
    roles = Counter(str(player.get("role") or "UNKNOWN") for player in players)
    metrics: dict[str, list[float]] = defaultdict(list)
    for player in players:
        combat = _as_mapping(player.get("combat"))
        economy = _as_mapping(player.get("economy"))
        damage = _as_mapping(player.get("damage"))
        vision = _as_mapping(player.get("vision"))
        for key, value in {
            "kills": combat.get("kills"),
            "deaths": combat.get("deaths"),
            "assists": combat.get("assists"),
            "kda": combat.get("kda"),
            "kill_participation": combat.get("kill_participation"),
            "gold_per_minute": economy.get("gold_per_minute"),
            "cs_per_minute": economy.get("cs_per_minute"),
            "champion_damage_per_minute": damage.get("to_champions_per_minute"),
            "vision_score_per_minute": vision.get("score_per_minute"),
        }.items():
            if isinstance(value, (int, float)) and math.isfinite(float(value)):
                metrics[key].append(float(value))
    return {
        "games": len(players),
        "wins": wins,
        "losses": len(players) - wins,
        "win_rate": _round(wins / len(players)),
        "champions": dict(champions.most_common()),
        "roles": dict(roles.most_common()),
        "averages": {
            key: _round(sum(values) / len(values)) for key, values in metrics.items() if values
        },
    }


def _match_team_objectives(info: Mapping[str, Any], team_id: int) -> dict[str, Any]:
    for raw in _as_list(_field(info, "teams", default=[])):
        team = _as_mapping(raw)
        if _int(_field(team, "teamId", "team_id")) != team_id:
            continue
        objectives = _as_mapping(_field(team, "objectives", default={}))
        return {
            str(key): {
                "kills": _int(_field(_as_mapping(value), "kills")),
                "first": bool(_field(_as_mapping(value), "first", default=False)),
            }
            for key, value in objectives.items()
        }
    return {}


def _question_relevance(question: str | None, *, scope: str) -> dict[str, Any]:
    defaults = {
        "match": ["/teams", "/participants", "/timeline", "/impact_assessments"],
        "player": ["/identity", "/ranked_entries", "/recent_matches", "/top_champion_mastery"],
        "knowledge": ["/knowledge"],
    }
    if not question:
        return {
            "question": None,
            "detected_topics": [],
            "evidence_paths": defaults[scope],
        }
    normalized = question.casefold()
    topics = [
        topic
        for topic, markers in _QUERY_TOPICS.items()
        if any(marker in normalized for marker in markers)
    ]
    paths: list[str] = []
    paths_by_scope = {
        "match": {
            "void_grubs": "/impact_assessments/void_grubs",
            "objectives": "/teams/*/objectives",
            "combat": "/timeline/likely_teamfights",
            "economy": "/timeline/checkpoints",
            "lanes": "/lane_matchups",
            "builds": "/timeline/item_milestones",
            "vision": "/participants/*/vision",
            "player": "/participants",
        },
        "player": {
            "void_grubs": "/recent_matches/matches/*/team_objectives/horde",
            "objectives": "/recent_matches/matches/*/team_objectives",
            "combat": "/recent_matches/matches/*/player/combat",
            "economy": "/recent_matches/matches/*/player/economy",
            "lanes": "/recent_matches/aggregate/roles",
            "builds": "/recent_matches/matches/*/player/loadout",
            "vision": "/recent_matches/matches/*/player/vision",
            "player": "/recent_matches/aggregate",
        },
        "knowledge": {topic: "/knowledge" for topic in _QUERY_TOPICS},
    }
    path_by_topic = paths_by_scope[scope]
    for topic in topics:
        path = path_by_topic.get(topic)
        if path and path not in paths:
            paths.append(path)
    if not paths:
        paths = defaults[scope]
    return {
        "question": question,
        "detected_topics": topics,
        "evidence_paths": paths,
        "answering_rule": (
            "State observed facts first, derived proxies second, and unavailable causal facts explicitly."
        ),
    }


def _resolve_focus(
    participants: Sequence[Mapping[str, Any]],
    *,
    focus: str | None,
    focus_puuid: str | None,
) -> Mapping[str, Any] | None:
    if focus_puuid:
        for participant in participants:
            if str(_field(participant, "puuid", default="")) == focus_puuid:
                return participant
    if not focus:
        return None
    normalized = focus.casefold().strip()
    if normalized.isdigit():
        participant_id = int(normalized)
        for participant in participants:
            if _int(_field(participant, "participantId", "participant_id")) == participant_id:
                return participant
    matches: list[Mapping[str, Any]] = []
    for participant in participants:
        names = {
            str(_field(participant, "championName", "champion_name", default="")),
            str(_field(participant, "summonerName", "summoner_name", default="")),
            str(_field(participant, "riotIdGameName", "riot_id_game_name", default="")),
        }
        game_name = _optional_text(_field(participant, "riotIdGameName", "riot_id_game_name"))
        tag_line = _optional_text(_field(participant, "riotIdTagline", "riot_id_tagline"))
        if game_name and tag_line:
            names.add(f"{game_name}#{tag_line}")
        if normalized in {name.casefold() for name in names if name}:
            matches.append(participant)
    return matches[0] if len(matches) == 1 else None


def _team_gold_snapshot(
    frames: Sequence[Mapping[str, Any]],
    participant_by_id: Mapping[int, Mapping[str, Any]],
    team_id: int,
    timestamp: int,
) -> dict[str, int] | None:
    frame = _nearest_frame(frames, timestamp)
    if frame is None:
        return None
    frame_timestamp = _int(_field(frame, "timestamp"))
    distance = abs(frame_timestamp - timestamp)
    if distance > 90000:
        return None
    participant_frames = _as_mapping(
        _field(frame, "participantFrames", "participant_frames", default={})
    )
    totals = _frame_team_totals(participant_frames, participant_by_id)
    if team_id not in totals:
        return None
    return {
        "target_timestamp_ms": timestamp,
        "frame_timestamp_ms": frame_timestamp,
        "frame_distance_ms": distance,
        "total_gold": _int(totals[team_id].get("total_gold")),
    }


def _nearest_frame(
    frames: Sequence[Mapping[str, Any]],
    timestamp: int,
) -> Mapping[str, Any] | None:
    if not frames:
        return None
    return min(
        frames,
        key=lambda frame: abs(_int(_field(frame, "timestamp")) - timestamp),
    )


def _participant_frame(
    participant_frames: Mapping[str, Any],
    participant_id: int,
) -> Mapping[str, Any]:
    direct = participant_frames.get(str(participant_id))
    if direct is not None:
        return _as_mapping(direct)
    for raw in participant_frames.values():
        frame = _as_mapping(raw)
        if _int(_field(frame, "participantId", "participant_id")) == participant_id:
            return frame
    return {}


def _frame_cs(frame: Mapping[str, Any]) -> int:
    return _int(_field(frame, "minionsKilled", "minions_killed")) + _int(
        _field(frame, "jungleMinionsKilled", "jungle_minions_killed")
    )


def _final_cs(participant: Mapping[str, Any]) -> int:
    return _int(_field(participant, "totalMinionsKilled", "total_minions_killed")) + _int(
        _field(participant, "neutralMinionsKilled", "neutral_minions_killed")
    )


def _is_grub_event(event: Mapping[str, Any]) -> bool:
    if str(_field(event, "type", default="")).upper() != "ELITE_MONSTER_KILL":
        return False
    material = " ".join(
        str(_field(event, name, default="") or "")
        for name in (
            "monsterType",
            "monster_type",
            "monsterSubType",
            "monster_sub_type",
            "name",
        )
    ).upper()
    return any(marker in material for marker in _GRUB_MARKERS)


def _team_for_event(
    event: Mapping[str, Any],
    participant_by_id: Mapping[int, Mapping[str, Any]],
    *,
    building: bool,
) -> int | None:
    explicit = _int(_field(event, "killerTeamId", "killer_team_id"))
    if explicit in _TEAM_IDS:
        return explicit
    killer_id = _int(_field(event, "killerId", "killer_id"))
    participant = participant_by_id.get(killer_id, {})
    participant_team = _int(_field(participant, "teamId", "team_id"))
    if participant_team in _TEAM_IDS:
        return participant_team
    event_team = _int(_field(event, "teamId", "team_id"))
    if event_team in _TEAM_IDS:
        return 300 - event_team if building else event_team
    return None


def _participant_ref(participant: Mapping[str, Any]) -> dict[str, Any] | None:
    if not participant:
        return None
    game_name = _optional_text(
        _field(participant, "riotIdGameName", "riot_id_game_name", "riotIdName")
    )
    tag_line = _optional_text(_field(participant, "riotIdTagline", "riot_id_tagline"))
    return {
        "participant_id": _int(_field(participant, "participantId", "participant_id")),
        "riot_id": f"{game_name}#{tag_line}" if game_name and tag_line else None,
        "display_name": game_name or _field(participant, "summonerName", "summoner_name"),
        "champion": _field(participant, "championName", "champion_name"),
        "team_id": _int(_field(participant, "teamId", "team_id")),
        "role": _field(participant, "teamPosition", "team_position"),
    }


def _match_route(match_id: str, route: str | None) -> str:
    regional = _regional_from_route(route)
    if regional is not None:
        return regional
    match = _MATCH_PREFIX.match(match_id)
    if match is None:
        raise InvalidArgumentsError(
            "The match route could not be inferred. Provide a regional route."
        )
    prefix = match.group(1).lower()
    try:
        platform = PlatformRoute(prefix)
    except ValueError as exc:
        raise InvalidArgumentsError(
            "The match route could not be inferred. Provide a regional route."
        ) from exc
    return PLATFORM_TO_REGIONAL[platform].value


def _regional_from_route(route: str | None) -> str | None:
    if route is None:
        return None
    normalized = route.strip().lower()
    if normalized in {"americas", "asia", "europe", "sea"}:
        return normalized
    try:
        return PLATFORM_TO_REGIONAL[PlatformRoute(normalized)].value
    except (KeyError, ValueError) as exc:
        raise InvalidArgumentsError("The League route is not supported.") from exc


def _account_route(route: str | None) -> str | None:
    regional = _regional_from_route(route)
    return "asia" if regional == "sea" else regional


def _platform_route(route: str | None) -> str | None:
    if route is None:
        return None
    normalized = route.strip().lower()
    try:
        return PlatformRoute(normalized).value
    except ValueError as exc:
        raise InvalidArgumentsError(
            "Player context requires a League platform route such as euw1 or na1."
        ) from exc


async def _settle(
    calls: Mapping[str, Any],
    *,
    label_suffix: str = " data",
) -> tuple[dict[str, Any], list[str]]:
    if not calls:
        return {}, []
    keys = list(calls)
    results = await asyncio.gather(
        *(calls[key] for key in keys),
        return_exceptions=True,
    )
    values: dict[str, Any] = {}
    warnings: list[str] = []
    for key, result in zip(keys, results, strict=True):
        if isinstance(result, BaseException):
            warnings.append(_unavailable(f"{key.replace('_', ' ').title()}{label_suffix}", result))
        else:
            values[key] = result
    return values, warnings


async def _invoke(method: Any, *args: Any, **kwargs: Any) -> Any:
    filtered = kwargs
    try:
        signature = inspect.signature(method)
    except TypeError, ValueError:
        signature = None
    if signature is not None and not any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in signature.parameters.values()
    ):
        filtered = {key: value for key, value in kwargs.items() if key in signature.parameters}
    result = method(*args, **filtered)
    return await result if inspect.isawaitable(result) else result


def _request_values(request: Any) -> dict[str, Any]:
    if isinstance(request, BaseModel):
        return request.model_dump(exclude_none=True)
    if isinstance(request, Mapping):
        return {str(key): value for key, value in request.items() if value is not None}
    raise InvalidArgumentsError("League analysis request must be an object.")


def _to_data(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, Enum):
        return _to_data(value.value)
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, BaseModel):
        return _to_data(value.model_dump(mode="json", by_alias=True))
    if isinstance(value, Mapping):
        return {str(key): _to_data(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_to_data(item) for item in value]
    dump = getattr(value, "model_dump", None)
    if callable(dump):
        return _to_data(dump(mode="json", by_alias=True))
    return str(value)


def _field(value: Any, *names: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        for name in names:
            if name in value:
                return value[name]
        return default
    for name in names:
        if hasattr(value, name):
            return getattr(value, name)
    return default


def _as_mapping(value: Any) -> dict[str, Any]:
    data = _to_data(value)
    return dict(data) if isinstance(data, Mapping) else {}


def _as_list(value: Any) -> list[Any]:
    data = _to_data(value)
    if isinstance(data, list):
        return data
    if isinstance(data, Sequence) and not isinstance(data, (str, bytes, bytearray)):
        return list(data)
    return []


def _int_key_map(value: Any) -> dict[int, dict[str, Any]]:
    data = _to_data(value)
    if not isinstance(data, Mapping):
        return {}
    result: dict[int, dict[str, Any]] = {}
    for key, item in data.items():
        parsed = _int(key)
        mapped = _as_mapping(item)
        if parsed > 0 and mapped:
            result[parsed] = mapped
    return result


def _rune_map(value: Any) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for tree in _as_list(value):
        tree_data = _as_mapping(tree)
        tree_id = _int(_field(tree_data, "id"))
        if tree_id:
            result[tree_id] = tree_data
        for slot in _as_list(_field(tree_data, "slots", default=[])):
            for rune in _as_list(_field(_as_mapping(slot), "runes", default=[])):
                rune_data = _as_mapping(rune)
                rune_id = _int(_field(rune_data, "id"))
                if rune_id:
                    result[rune_id] = rune_data
    return result


def _find_static(values: Any, key: str, identifier: int) -> Mapping[str, Any]:
    for value in _as_list(values):
        mapped = _as_mapping(value)
        if _int(_field(mapped, key)) == identifier:
            return mapped
    return {}


def _compact_static(value: Mapping[str, Any], keys: Sequence[str]) -> dict[str, Any] | None:
    if not value:
        return None
    return {key: value[key] for key in keys if key in value and value[key] is not None}


def _source(operation: str, detail: str | None = None) -> dict[str, str]:
    value = {"operation": operation, "status": "loaded"}
    if detail is not None:
        value["detail"] = detail
    return value


def _unavailable(label: str, error: BaseException) -> str:
    return f"{label} unavailable ({type(error).__name__})."


def _required_text(value: Any, label: str) -> str:
    text = _optional_text(value)
    if text is None:
        raise IntegrationContractError(f"Riot returned no {label}.")
    return text


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _int(value: Any) -> int:
    if isinstance(value, bool) or value is None:
        return 0
    try:
        return int(value)
    except TypeError, ValueError, OverflowError:
        return 0


def _number(value: Any) -> float | int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    try:
        number = float(value)
    except TypeError, ValueError, OverflowError:
        return None
    return number if math.isfinite(number) else None


def _round(value: float, digits: int = 3) -> float:
    return round(value, digits)


def _duration_seconds(value: Any) -> float:
    number = _number(value)
    if number is None or number < 0:
        return 0.0
    seconds = float(number)
    return seconds / 1000 if seconds > 100000 else seconds


def _minute(value: Any) -> float:
    return round(_int(value) / 60000, 2)


def _iso_timestamp(value: Any) -> str | None:
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).isoformat()
        except ValueError:
            return value or None
    number = _number(value)
    if number is None or number <= 0:
        return None
    seconds = float(number) / 1000 if float(number) > 10000000000 else float(number)
    try:
        return datetime.fromtimestamp(seconds, tz=UTC).isoformat()
    except OSError, OverflowError, ValueError:
        return None


def _side(team_id: int) -> str | None:
    if team_id == 100:
        return "blue"
    if team_id == 200:
        return "red"
    return None


def _truthy(value: Any) -> bool:
    return value is True or value == 1 or str(value).lower() == "true"


def _patch_parts(value: str | None) -> tuple[int | None, int | None]:
    if not value:
        return None, None
    parts = value.split(".")
    if not parts or not parts[0].isdigit():
        return None, None
    major = int(parts[0])
    minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
    if major >= 25:
        major -= 10
    return major, minor


def _same_patch(first: str | None, second: str | None) -> bool | None:
    left = _patch_parts(first)
    right = _patch_parts(second)
    if left[0] is None or right[0] is None:
        return None
    return left == right

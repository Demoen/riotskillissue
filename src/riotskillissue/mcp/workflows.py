"""High-level game workflow dispatch for MCP tools."""

from __future__ import annotations

import inspect
from typing import Any

from pydantic import BaseModel

from .errors import IntegrationContractError, InvalidArgumentsError
from .models import ToolResult
from .result_store import ResultStore

_METHOD_CANDIDATES = {
    "match_history": ("match_history",),
    "ranked_entries": ("ranked_entries",),
    "leaderboard": ("leaderboard",),
    "live_game": ("live_game",),
    "champion_mastery": ("champion_mastery",),
    "challenges": ("challenges",),
    "service_status": ("service_status", "status"),
    "game_content": ("game_content", "content"),
}
_RIOT_ID_WORKFLOWS = {
    "player_profile",
    "match_history",
    "ranked_entries",
    "live_game",
    "champion_mastery",
    "challenges",
}
_LOL_CONTENT_METHODS = {
    "version": ("get_latest_version", None),
    "champion": ("get_champion", "champion_key"),
    "champion_detail": ("get_champion_detail", "champion_key"),
    "champions": ("get_all_champions", None),
    "item": ("get_item", "item_id"),
    "items": ("get_all_items", None),
    "runes": ("get_runes", None),
    "summoner_spell": ("get_summoner_spell", "spell_key"),
    "summoner_spells": ("get_summoner_spells", None),
    "queues": ("get_queues", None),
    "maps": ("get_maps", None),
    "game_modes": ("get_game_modes", None),
}
_LOL_VERSIONED_CONTENT = {
    "champion",
    "champion_detail",
    "champions",
    "item",
    "items",
    "runes",
    "summoner_spell",
    "summoner_spells",
}
_LOL_ANALYSIS_METHODS = {
    "lol_match_context": "match_context",
    "lol_player_context": "player_context",
    "lol_knowledge": "knowledge",
    "lol_item_economy": "item_economy",
}


class WorkflowDispatcher:
    """Call typed game services while keeping SDK handlers small."""

    def __init__(self, client: Any, result_store: ResultStore) -> None:
        self._client = client
        self._result_store = result_store
        self._lol_analysis: Any | None = None

    async def call(self, workflow: str, request: BaseModel) -> ToolResult:
        if workflow in _LOL_ANALYSIS_METHODS:
            result = await self._call_lol_analysis(workflow, request)
            return self._result_store.present(result)

        values = request.model_dump(exclude_none=True)
        game = str(values.pop("game"))
        if workflow == "game_content" and game == "lol":
            result = await self._lol_content(values)
            return self._result_store.present(result)

        service = getattr(self._client, game, None)
        if service is None:
            raise IntegrationContractError(
                "The installed RiotSkillIssue client lacks this game workflow."
            )
        method = _find_method(service, workflow, game)
        if workflow in _RIOT_ID_WORKFLOWS:
            riot_id = values.pop("riot_id")
            result = method(riot_id, **values)
        else:
            result = method(**values)
        if inspect.isawaitable(result):
            result = await result
        return self._result_store.present(result)

    async def _call_lol_analysis(self, workflow: str, request: BaseModel) -> Any:
        service = self._lol_analysis_service()
        method = getattr(service, _LOL_ANALYSIS_METHODS[workflow], None)
        if not callable(method):
            raise IntegrationContractError(
                "The installed RiotSkillIssue client lacks League analysis support."
            )
        result = method(request)
        return await result if inspect.isawaitable(result) else result

    def _lol_analysis_service(self) -> Any:
        if self._lol_analysis is None:
            try:
                from .lol import LolAnalysisService
            except (ImportError, ModuleNotFoundError) as exc:
                raise IntegrationContractError(
                    "League analysis support is unavailable in this installation."
                ) from exc
            self._lol_analysis = LolAnalysisService(self._client)
        return self._lol_analysis

    async def _lol_content(self, values: dict[str, Any]) -> Any:
        static_client = getattr(self._client, "static", None)
        if static_client is None:
            raise IntegrationContractError(
                "The installed RiotSkillIssue client lacks Data Dragon support."
            )
        kind = values["kind"]
        method_name, identifier_name = _LOL_CONTENT_METHODS[kind]
        identifier = values.get("identifier")
        patch = values.get("patch")
        locale = values.get("locale")
        if kind == "version":
            if identifier is not None:
                raise InvalidArgumentsError("This content kind does not accept an identifier.")
            if locale is not None:
                raise InvalidArgumentsError("Version lookup does not accept a locale.")
            if patch is not None:
                return await self._resolve_static_version(static_client, str(patch))
        elif kind not in _LOL_VERSIONED_CONTENT and (patch is not None or locale is not None):
            raise InvalidArgumentsError(
                "Queue, map, and game-mode metadata do not accept patch or locale."
            )

        method = getattr(static_client, method_name, None)
        if not callable(method):
            raise IntegrationContractError(
                "The installed RiotSkillIssue client lacks this Data Dragon operation."
            )
        kwargs: dict[str, Any] = {}
        if kind in _LOL_VERSIONED_CONTENT:
            if patch is not None:
                kwargs["version"] = await self._resolve_static_version(
                    static_client,
                    str(patch),
                )
            if locale is not None:
                kwargs["locale"] = locale
        if identifier_name is None:
            if identifier is not None:
                raise InvalidArgumentsError("This content kind does not accept an identifier.")
            result = method(**kwargs)
        else:
            if identifier is None:
                raise InvalidArgumentsError("This content kind requires a numeric identifier.")
            result = method(**{identifier_name: identifier, **kwargs})
        return await result if inspect.isawaitable(result) else result

    async def _resolve_static_version(self, static_client: Any, patch: str) -> str:
        resolver = getattr(static_client, "resolve_version", None)
        if not callable(resolver):
            raise IntegrationContractError(
                "The installed RiotSkillIssue client lacks strict patch resolution."
            )
        try:
            result = resolver(game_version=patch, strict=True)
            resolved = await result if inspect.isawaitable(result) else result
        except (LookupError, ValueError) as exc:
            raise InvalidArgumentsError(str(exc)) from exc
        if not isinstance(resolved, str) or not resolved:
            raise IntegrationContractError("Data Dragon returned no matching patch version.")
        return resolved


def _find_method(service: Any, workflow: str, game: str) -> Any:
    candidates = (
        ("player_profile",)
        if workflow == "player_profile" and game == "lol"
        else ("profile",)
        if workflow == "player_profile"
        else _METHOD_CANDIDATES[workflow]
    )
    for name in candidates:
        method = getattr(service, name, None)
        if callable(method):
            return method
    raise IntegrationContractError(
        "The installed RiotSkillIssue client lacks this workflow operation."
    )

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


class WorkflowDispatcher:
    """Call typed game services while keeping SDK handlers small."""

    def __init__(self, client: Any, result_store: ResultStore) -> None:
        self._client = client
        self._result_store = result_store

    async def call(self, workflow: str, request: BaseModel) -> ToolResult:
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

    async def _lol_content(self, values: dict[str, Any]) -> Any:
        static_client = getattr(self._client, "static", None)
        if static_client is None:
            raise IntegrationContractError(
                "The installed RiotSkillIssue client lacks Data Dragon support."
            )
        kind = values["kind"]
        method_name, identifier_name = _LOL_CONTENT_METHODS[kind]
        method = getattr(static_client, method_name, None)
        if not callable(method):
            raise IntegrationContractError(
                "The installed RiotSkillIssue client lacks this Data Dragon operation."
            )
        if identifier_name is None:
            if values.get("identifier") is not None:
                raise InvalidArgumentsError(
                    "This content kind does not accept an identifier."
                )
            result = method()
        else:
            identifier = values.get("identifier")
            if identifier is None:
                raise InvalidArgumentsError(
                    "This content kind requires a numeric identifier."
                )
            result = method(**{identifier_name: identifier})
        return await result if inspect.isawaitable(result) else result


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

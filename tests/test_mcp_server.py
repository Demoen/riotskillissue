from __future__ import annotations

import json
import os
import sys
import tempfile
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
from pydantic import ValidationError

try:
    _MCP_MAJOR = int(version("mcp").split(".", 1)[0])
except PackageNotFoundError:
    _MCP_MAJOR = 0

if _MCP_MAJOR < 2:
    pytest.skip("MCP SDK v2 is not installed", allow_module_level=True)

from mcp import Client, ClientSession, StdioServerParameters, stdio_client
from mcp_types import ElicitResult

from riotskillissue.mcp.errors import InvalidArgumentsError
from riotskillissue.mcp.models import (
    LolContentRequest,
    LolItemEconomyRequest,
    LolKnowledgeRequest,
    LolMatchContextRequest,
    LolPlayerContextRequest,
)
from riotskillissue.mcp.result_store import ResultStore
from riotskillissue.mcp.server import create_server
from riotskillissue.mcp.settings import RiotMcpSettings
from riotskillissue.mcp.workflows import WorkflowDispatcher


class LolService:
    async def player_profile(
        self,
        riot_id: str,
        *,
        route: str | None = None,
    ) -> dict[str, Any]:
        return {"riot_id": riot_id, "route": route}


class ClientDouble:
    def __init__(self) -> None:
        self.lol = LolService()
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.closed = False

    async def call_operation(
        self,
        operation: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        self.calls.append((operation, arguments))
        return {"operation": operation, **arguments}

    async def close(self) -> None:
        self.closed = True


REGISTRY = {
    "lol.match.get": {
        "operation_id": "lol.match.get",
        "accessor_path": "raw.lol.match.get_match",
        "source": "riot_api",
        "game": "lol",
        "service": "match",
        "method": "GET",
        "auth_mode": "api_key",
        "mcp_visible": True,
        "input_schema": {"type": "object"},
    },
    "lor.deck.create": {
        "operation_id": "lor.deck.create",
        "accessor_path": "raw.lor.deck.create",
        "source": "riot_api",
        "game": "lor",
        "service": "deck",
        "method": "POST",
        "auth_mode": "api_key",
        "mcp_visible": True,
    },
    "lol.rso.matches": {
        "operation_id": "lol.rso.matches",
        "accessor_path": "raw.lol.rso.matches",
        "source": "riot_api",
        "game": "lol",
        "service": "rso",
        "method": "GET",
        "auth_mode": "rso",
        "mcp_visible": False,
    },
}


def test_lol_analysis_request_validation() -> None:
    assert LolMatchContextRequest(match_id="EUW1_123").detail == "standard"
    assert LolMatchContextRequest(match_id="CUSTOM_series-7", route="europe").route == "europe"
    assert LolMatchContextRequest(riot_id="Player#EUW", match_index=2).match_index == 2

    with pytest.raises(ValidationError, match="exactly one"):
        LolMatchContextRequest()
    with pytest.raises(ValidationError, match="exactly one"):
        LolMatchContextRequest(match_id="EUW1_123", riot_id="Player#EUW")
    with pytest.raises(ValidationError):
        LolPlayerContextRequest(riot_id="Player#EUW", count=11)
    with pytest.raises(ValidationError):
        LolPlayerContextRequest(riot_id="Player#EUW", route="europe")
    with pytest.raises(ValidationError):
        LolKnowledgeRequest(topic="unknown")
    assert LolItemEconomyRequest(item_name="Trinity Force", patch="26.15").map_id == 11
    assert LolItemEconomyRequest(item_id=3078, match_id="EUW1_123").item_id == 3078
    with pytest.raises(ValidationError, match="exactly one"):
        LolItemEconomyRequest()
    with pytest.raises(ValidationError, match="exactly one"):
        LolItemEconomyRequest(item_id=3078, item_name="Trinity Force")
    with pytest.raises(ValidationError, match="at most one"):
        LolItemEconomyRequest(item_id=3078, patch="26.15", match_id="EUW1_123")
    with pytest.raises(ValidationError, match="route can only"):
        LolItemEconomyRequest(item_id=3078, route="euw1")


@pytest.mark.asyncio
async def test_lol_analysis_workflows_support_async_and_sync_methods(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = ModuleType("riotskillissue.mcp.lol")

    class LolAnalysisService:
        def __init__(self, client: Any) -> None:
            self.client = client

        async def match_context(self, request: LolMatchContextRequest) -> dict[str, Any]:
            return {"kind": "match", "match_id": request.match_id}

        async def player_context(self, request: LolPlayerContextRequest) -> dict[str, Any]:
            return {"kind": "player", "riot_id": request.riot_id}

        def knowledge(self, request: LolKnowledgeRequest) -> dict[str, Any]:
            return {"kind": "knowledge", "topic": request.topic}

        async def item_economy(self, request: LolItemEconomyRequest) -> dict[str, Any]:
            return {"kind": "item_economy", "item_id": request.item_id}

    module.__dict__["LolAnalysisService"] = LolAnalysisService
    monkeypatch.setitem(sys.modules, "riotskillissue.mcp.lol", module)
    dispatcher = WorkflowDispatcher(ClientDouble(), ResultStore())

    match = await dispatcher.call(
        "lol_match_context",
        LolMatchContextRequest(match_id="EUW1_123"),
    )
    player = await dispatcher.call(
        "lol_player_context",
        LolPlayerContextRequest(riot_id="Player#EUW"),
    )
    knowledge = await dispatcher.call(
        "lol_knowledge",
        LolKnowledgeRequest(topic="void_grubs"),
    )
    item_economy = await dispatcher.call(
        "lol_item_economy",
        LolItemEconomyRequest(item_id=3078, patch="26.15"),
    )

    assert match.data == {"kind": "match", "match_id": "EUW1_123"}
    assert player.data == {"kind": "player", "riot_id": "Player#EUW"}
    assert knowledge.data == {"kind": "knowledge", "topic": "void_grubs"}
    assert item_economy.data == {"kind": "item_economy", "item_id": 3078}


@pytest.mark.asyncio
async def test_lol_content_uses_strict_patch_and_locale() -> None:
    class StaticClient:
        def __init__(self) -> None:
            self.calls: list[tuple[str, dict[str, Any]]] = []

        async def resolve_version(self, game_version: str, *, strict: bool = False) -> str:
            self.calls.append(("resolve_version", {"game_version": game_version, "strict": strict}))
            if game_version == "26.99":
                raise LookupError("patch unavailable")
            return "16.15.1"

        async def get_champion_detail(
            self,
            champion_key: int,
            *,
            version: str | None = None,
            locale: str = "en_US",
        ) -> dict[str, Any]:
            self.calls.append(
                (
                    "get_champion_detail",
                    {
                        "champion_key": champion_key,
                        "version": version,
                        "locale": locale,
                    },
                )
            )
            return {"id": "Annie", "version": version, "locale": locale}

        async def get_maps(self) -> list[dict[str, Any]]:
            return []

    client = ClientDouble()
    client.static = StaticClient()
    dispatcher = WorkflowDispatcher(client, ResultStore())

    result = await dispatcher.call(
        "game_content",
        LolContentRequest(
            kind="champion_detail",
            identifier=1,
            patch="26.15",
            locale="en_GB",
        ),
    )
    resolved = await dispatcher.call(
        "game_content",
        LolContentRequest(kind="version", patch="26.15"),
    )

    assert result.data == {"id": "Annie", "version": "16.15.1", "locale": "en_GB"}
    assert resolved.data == "16.15.1"
    assert client.static.calls == [
        ("resolve_version", {"game_version": "26.15", "strict": True}),
        (
            "get_champion_detail",
            {"champion_key": 1, "version": "16.15.1", "locale": "en_GB"},
        ),
        ("resolve_version", {"game_version": "26.15", "strict": True}),
    ]
    with pytest.raises(InvalidArgumentsError, match="do not accept patch"):
        await dispatcher.call(
            "game_content",
            LolContentRequest(kind="maps", patch="26.15"),
        )
    with pytest.raises(InvalidArgumentsError, match="patch unavailable"):
        await dispatcher.call(
            "game_content",
            LolContentRequest(kind="champion_detail", identifier=1, patch="26.99"),
        )


@pytest.mark.asyncio
async def test_tool_schemas_hide_credentials_rso_and_disabled_writes() -> None:
    server = create_server(
        settings=RiotMcpSettings(api_key="RGAPI-private"),
        client_factory=lambda settings: ClientDouble(),
        registry=REGISTRY,
    )

    tools = await server.list_tools()
    names = {tool.name for tool in tools}
    schemas = json.dumps([tool.input_schema for tool in tools])

    assert "riot_call_write_operation" not in names
    assert {
        "riot_lol_match_context",
        "riot_lol_player_context",
        "riot_lol_knowledge",
        "riot_lol_item_economy",
    } <= names
    assert "RIOT_API_KEY" not in schemas
    assert "RGAPI-private" not in schemas
    assert "token" not in schemas.lower()


@pytest.mark.asyncio
async def test_in_memory_client_uses_lifespan_and_structured_tools() -> None:
    client_double = ClientDouble()
    server = create_server(
        settings=RiotMcpSettings(api_key="RGAPI-private"),
        client_factory=lambda settings: client_double,
        registry=REGISTRY,
    )

    async with Client(server, raise_exceptions=True) as client:
        profile = await client.call_tool(
            "riot_player_profile",
            {"request": {"game": "lol", "riot_id": "Player#EUW"}},
        )
        found = await client.call_tool(
            "riot_find_operations",
            {"query": "match"},
        )
        called = await client.call_tool(
            "riot_call_read_operation",
            {
                "operation": "lol.match.get",
                "arguments": {"match_id": "EUW1_1"},
            },
        )

    assert profile.structured_content["data"]["riot_id"] == "Player#EUW"
    operations = found.structured_content["operations"]
    assert [item["operation"] for item in operations] == ["lol.match.get"]
    assert called.structured_content["data"]["operation"] == "lol.match.get"
    assert client_double.calls == [("lol.match.get", {"match_id": "EUW1_1"})]
    assert client_double.closed is True


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["decline", "cancel"])
async def test_write_confirmation_decline_and_cancel_fail_closed(action: str) -> None:
    client_double = ClientDouble()

    async def elicitation(context: Any, params: Any) -> ElicitResult:
        return ElicitResult(action=action)

    server = create_server(
        settings=RiotMcpSettings(api_key="RGAPI-private", allow_writes=True),
        client_factory=lambda settings: client_double,
        registry=REGISTRY,
    )
    async with Client(
        server,
        raise_exceptions=True,
        elicitation_callback=elicitation,
    ) as client:
        result = await client.call_tool(
            "riot_call_write_operation",
            {"operation": "lor.deck.create", "arguments": {"name": "deck"}},
        )

    assert result.is_error is True
    assert client_double.calls == []


@pytest.mark.asyncio
async def test_write_confirmation_accepts_before_dispatch() -> None:
    client_double = ClientDouble()

    async def elicitation(context: Any, params: Any) -> ElicitResult:
        return ElicitResult(action="accept", content={"approved": True})

    server = create_server(
        settings=RiotMcpSettings(api_key="RGAPI-private", allow_writes=True),
        client_factory=lambda settings: client_double,
        registry=REGISTRY,
    )
    async with Client(
        server,
        raise_exceptions=True,
        elicitation_callback=elicitation,
    ) as client:
        result = await client.call_tool(
            "riot_call_write_operation",
            {"operation": "lor.deck.create", "arguments": {"name": "deck"}},
        )

    assert result.is_error is False
    assert client_double.calls == [("lor.deck.create", {"name": "deck"})]


@pytest.mark.asyncio
async def test_stdio_subprocess_has_clean_protocol_output() -> None:
    repository = Path(__file__).resolve().parents[1]
    source = repository / "src"
    pythonpath = os.pathsep.join(
        part for part in (str(source), os.environ.get("PYTHONPATH", "")) if part
    )
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "riotskillissue.mcp.cli"],
        cwd=repository,
        env={
            "PYTHONPATH": pythonpath,
            "RIOT_API_KEY": "RGAPI-subprocess-test",
            "RIOT_DEFAULT_ROUTE": "euw1",
        },
    )

    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stderr:
        async with (
            stdio_client(parameters, errlog=stderr) as streams,
            ClientSession(*streams) as session,
        ):
            await session.initialize()
            tools = await session.list_tools()
        stderr.seek(0)
        diagnostics = stderr.read()

    assert "riot_find_operations" in {tool.name for tool in tools.tools}
    assert "RGAPI-subprocess-test" not in diagnostics

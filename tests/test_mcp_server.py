from __future__ import annotations

import json
import os
import sys
import tempfile
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

import pytest

try:
    _MCP_MAJOR = int(version("mcp").split(".", 1)[0])
except PackageNotFoundError:
    _MCP_MAJOR = 0

if _MCP_MAJOR < 2:
    pytest.skip("MCP SDK v2 is not installed", allow_module_level=True)

from mcp import Client, ClientSession, StdioServerParameters, stdio_client
from mcp_types import ElicitResult

from riotskillissue.mcp.server import create_server
from riotskillissue.mcp.settings import RiotMcpSettings


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
    assert client_double.calls == [
        ("lol.match.get", {"match_id": "EUW1_1"})
    ]
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
    assert client_double.calls == [
        ("lor.deck.create", {"name": "deck"})
    ]


@pytest.mark.asyncio
async def test_stdio_subprocess_has_clean_protocol_output() -> None:
    repository = Path(__file__).resolve().parents[1]
    source = repository / "src"
    pythonpath = os.pathsep.join(
        part
        for part in (str(source), os.environ.get("PYTHONPATH", ""))
        if part
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
        async with stdio_client(parameters, errlog=stderr) as streams, ClientSession(
            *streams
        ) as session:
            await session.initialize()
            tools = await session.list_tools()
        stderr.seek(0)
        diagnostics = stderr.read()

    assert "riot_find_operations" in {tool.name for tool in tools.tools}
    assert "RGAPI-subprocess-test" not in diagnostics

from __future__ import annotations

from typing import Any

import pytest

from riotskillissue.mcp.errors import (
    InvalidArgumentsError,
    OperationNotAllowedError,
    OperationNotFoundError,
    is_sensitive_key,
)
from riotskillissue.mcp.operations import OperationGateway
from riotskillissue.mcp.result_store import ResultStore


class StaticClient:
    async def get_maps(self) -> list[dict[str, Any]]:
        return [{"mapId": 11}]


class Client:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.static = StaticClient()

    async def call_operation(
        self,
        operation: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        self.calls.append((operation, arguments))
        return {"operation": operation, "arguments": arguments}


REGISTRY = {
    "lol.match.get": {
        "stable_id": "lol.match.get",
        "accessor_path": "raw.lol.match.get_match",
        "game": "lol",
        "service": "match",
        "method": "GET",
        "auth_mode": "api_key",
        "input_schema": {
            "type": "object",
            "properties": {
                "match_id": {"type": "string"},
                "api_key": {"type": "string"},
            },
            "required": ["match_id", "api_key"],
        },
    },
    "lor.deck.create": {
        "stable_id": "lor.deck.create",
        "accessor_path": "raw.lor.deck.create",
        "game": "lor",
        "service": "deck",
        "method": "POST",
        "auth_mode": "api_key",
    },
    "lol.rso.matches": {
        "stable_id": "lol.rso.matches",
        "accessor_path": "raw.lol.rso.matches",
        "game": "lol",
        "service": "rso",
        "method": "GET",
        "auth_mode": "rso",
    },
}


def test_discovery_hides_writes_rso_and_credentials() -> None:
    gateway = OperationGateway(Client(), ResultStore(), REGISTRY)

    found = gateway.find(query="lol")
    operations = {item.operation for item in found.operations}

    assert "lol.match.get" in operations
    assert "lol.rso.matches" not in operations
    assert "lor.deck.create" not in operations
    described = gateway.describe("raw.lol.match.get_match")
    assert "api_key" not in described.input_schema["properties"]
    assert "api_key" not in described.input_schema["required"]
    assert is_sensitive_key("access_token")
    assert not is_sensitive_key("page_token")


def test_committed_registry_exposes_every_eligible_operation() -> None:
    from riotskillissue.api.registry import OPERATION_REGISTRY

    records = tuple(OPERATION_REGISTRY.values())
    rso = [record for record in records if record.auth_mode == "rso"]
    expected_reads = [
        record
        for record in records
        if record.mcp_visible and record.is_read
    ]
    expected_writes = [
        record
        for record in records
        if record.mcp_visible and record.is_write
    ]

    disabled = OperationGateway(Client(), ResultStore(), OPERATION_REGISTRY)
    enabled = OperationGateway(
        Client(),
        ResultStore(),
        OPERATION_REGISTRY,
        allow_writes=True,
    )

    assert len(rso) == 9
    assert all(not record.mcp_visible for record in rso)
    assert disabled.find(limit=100).total == len(expected_reads) == 75
    assert enabled.find(include_writes=True, limit=100).total == (
        len(expected_reads) + len(expected_writes)
    )


@pytest.mark.asyncio
async def test_read_dispatch_and_static_hybrid_inventory() -> None:
    client = Client()
    gateway = OperationGateway(client, ResultStore(), REGISTRY)

    result = await gateway.call_read("lol.match.get", {"match_id": "EUW1_1"})
    static = await gateway.call_read("static.get_maps", {})

    assert result.data == {
        "operation": "lol.match.get",
        "arguments": {"match_id": "EUW1_1"},
    }
    assert static.data == [{"mapId": 11}]
    assert client.calls == [("lol.match.get", {"match_id": "EUW1_1"})]


@pytest.mark.asyncio
async def test_rso_and_credential_arguments_are_rejected() -> None:
    gateway = OperationGateway(Client(), ResultStore(), REGISTRY)

    with pytest.raises(OperationNotFoundError):
        await gateway.call_read("lol.rso.matches", {})
    with pytest.raises(OperationNotAllowedError):
        await gateway.call_read(
            "lol.match.get",
            {"match_id": "EUW1_1", "token": "RGAPI-secret"},
        )


@pytest.mark.asyncio
async def test_registry_schema_validates_gateway_arguments() -> None:
    gateway = OperationGateway(Client(), ResultStore(), REGISTRY)

    with pytest.raises(InvalidArgumentsError, match="Missing required"):
        await gateway.call_read("lol.match.get", {})
    with pytest.raises(InvalidArgumentsError, match="wrong JSON type"):
        await gateway.call_read("lol.match.get", {"match_id": 42})


@pytest.mark.asyncio
async def test_writes_require_server_policy_and_confirmation() -> None:
    disabled = OperationGateway(Client(), ResultStore(), REGISTRY)
    with pytest.raises(OperationNotFoundError):
        disabled.describe("lor.deck.create")

    client = Client()
    enabled = OperationGateway(
        client,
        ResultStore(),
        REGISTRY,
        allow_writes=True,
    )
    with pytest.raises(OperationNotAllowedError):
        await enabled.call_write("lor.deck.create", {}, confirmed=False)

    result = await enabled.call_write("lor.deck.create", {"name": "deck"}, confirmed=True)
    assert result.data == {
        "operation": "lor.deck.create",
        "arguments": {"name": "deck"},
    }

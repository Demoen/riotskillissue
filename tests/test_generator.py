import inspect
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.generator.core import (
    check_generated_files,
    render_generated_files,
    write_generated_files,
)
from tools.generator.parser import OpenApiParser


def _spec() -> dict:
    return {
        "openapi": "3.0.0",
        "security": [{"X-Riot-Token": []}],
        "components": {
            "securitySchemes": {
                "X-Riot-Token": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-Riot-Token",
                },
                "rso": {
                    "type": "oauth2",
                    "flows": {
                        "authorizationCode": {
                            "authorizationUrl": "https://example.test/authorize",
                            "tokenUrl": "https://example.test/token",
                            "scopes": {"openid": "Identity"},
                        }
                    },
                },
            },
            "schemas": {
                "val-widget-v1.WidgetDto": {
                    "type": "object",
                    "required": ["widgetId", "queue_id"],
                    "properties": {
                        "widgetId": {"type": "string"},
                        "queueId": {"type": "integer"},
                        "queue_id": {"type": "integer"},
                        "displayName": {
                            "type": "string",
                            "default": "Example",
                            "minLength": 1,
                            "maxLength": 40,
                            "example": "Ranked",
                        },
                    },
                }
            },
            "parameters": {
                "Cursor": {
                    "name": "pageToken",
                    "in": "query",
                    "description": "Pagination token",
                    "schema": {
                        "type": "string",
                        "default": "first",
                        "minLength": 1,
                        "maxLength": 100,
                    },
                    "example": "next",
                }
            },
            "requestBodies": {
                "Widget": {
                    "required": True,
                    "description": "Widget input",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/val-widget-v1.WidgetDto"}
                        }
                    },
                }
            },
            "responses": {
                "Widget": {
                    "description": "Accepted",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/val-widget-v1.WidgetDto"}
                        }
                    },
                },
                "Empty": {"description": "No content"},
            },
        },
        "paths": {
            "/val/widgets/v1/widgets/{widgetId}": {
                "parameters": [
                    {
                        "name": "widgetId",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "post": {
                    "operationId": "val-widget-v1.updateWidget",
                    "summary": "Update a widget",
                    "tags": ["val-widget-v1"],
                    "parameters": [{"$ref": "#/components/parameters/Cursor"}],
                    "requestBody": {"$ref": "#/components/requestBodies/Widget"},
                    "responses": {
                        "202": {"$ref": "#/components/responses/Widget"},
                        "204": {"$ref": "#/components/responses/Empty"},
                        "400": {"description": "Invalid"},
                    },
                    "security": [{"rso": ["openid"]}],
                    "x-route-enum": "val-platform",
                    "x-platforms-available": ["eu", "na"],
                    "x-mutation": {"confirmation": "required"},
                },
            }
        },
    }


def test_parser_retains_operation_contract() -> None:
    parser = OpenApiParser(_spec())
    parser.parse()

    model = parser.models["val-widget-v1.WidgetDto"]
    assert (model.game, model.module, model.name) == (
        "valorant",
        "widget_v1",
        "Widget",
    )
    display_name = next(value for value in model.properties if value.name == "display_name")
    assert display_name.wire_name == "displayName"
    assert display_name.default == "Example"
    assert display_name.constraints == {"minLength": 1, "maxLength": 40}
    assert display_name.examples == ["Ranked"]
    properties = {value.wire_name: value.name for value in model.properties}
    assert properties["queue_id"] == "queue_id"
    assert properties["queueId"] == "queue_id_1"

    operation = parser.operations[0]
    cursor = next(value for value in operation.parameters if value.name == "page_token")
    assert cursor.ref == "#/components/parameters/Cursor"
    assert cursor.description == "Pagination token"
    assert cursor.default == "first"
    assert cursor.constraints == {"minLength": 1, "maxLength": 100}
    assert cursor.examples == ["next"]
    assert operation.request_body is not None
    assert operation.request_body.required
    assert operation.request_body.ref == "#/components/requestBodies/Widget"
    assert operation.successful_statuses == (202, 204)
    assert operation.no_content_statuses == (204,)
    assert operation.response_type == "Optional[Widget]"
    assert operation.auth_mode == "rso"
    assert operation.auth_scopes == ("openid",)
    assert operation.route_kind == "val-platform"
    assert operation.allowed_routes == ("eu", "na")
    assert operation.is_mutation
    assert operation.mutation_metadata == {"confirmation": "required"}


def test_rendered_contract_is_parity_checkable(tmp_path: Path) -> None:
    files = render_generated_files(_spec(), format_code=False)
    endpoint_path = Path("src") / "riotskillissue" / "api" / "raw" / "valorant" / "widget.py"
    endpoint = files[endpoint_path]
    assert "async def update_widget(" in endpoint
    assert "def update_widget(" in endpoint
    assert "widget_id: str" in endpoint
    assert "page_token: Optional[str] = 'first'" in endpoint
    assert "body: Widget" in endpoint
    assert "route: ValorantRoute | str | None = None" in endpoint
    assert "operation_id='val-widget-v1.updateWidget'" in endpoint
    assert "cache_user_scoped=True" in endpoint
    assert "successful_statuses=(202, 204)" in endpoint
    assert "no_content_statuses=(204,)" in endpoint

    for path, source in files.items():
        if path.suffix == ".py":
            compile(source, str(path), "exec")

    api_reference = files[Path("docs") / "api-reference.md"]
    assert "`val-widget-v1.updateWidget`" in api_reference
    assert "`riot.raw.valorant.widget.update_widget`" in api_reference
    assert "`static.get_champion`" in api_reference

    results_path = tmp_path / "src" / "riotskillissue" / "models" / "results.py"
    results_path.parent.mkdir(parents=True)
    results_path.write_text("MANUAL = True\n", encoding="utf-8")
    write_generated_files(files, tmp_path)
    assert results_path.read_text(encoding="utf-8") == "MANUAL = True\n"
    assert check_generated_files(files, tmp_path) == []

    generated_endpoint = tmp_path / endpoint_path
    generated_endpoint.write_text("changed\n", encoding="utf-8")
    assert check_generated_files(files, tmp_path) == [
        "changed: src/riotskillissue/api/raw/valorant/widget.py"
    ]


def test_committed_registry_async_sync_docs_and_mcp_parity() -> None:
    from riotskillissue.api.raw import GeneratedRawClient, SyncGeneratedRawClient
    from riotskillissue.api.registry import OPERATION_REGISTRY

    spec = json.loads(Path("spec/openapi.json").read_text(encoding="utf-8"))
    parser = OpenApiParser(spec)
    parser.parse()
    expected = {operation.operation_id for operation in parser.operations}
    registered = {
        operation.operation_id
        for operation in OPERATION_REGISTRY.values()
        if operation.source == "riot_api"
    }
    assert registered == expected

    raw = GeneratedRawClient(cast(Any, object()))
    sync_raw = SyncGeneratedRawClient(raw, cast(Any, lambda value: value))
    reference = Path("docs/api-reference.md").read_text(encoding="utf-8")

    for operation in OPERATION_REGISTRY.values():
        assert operation.operation_id in reference
        assert operation.mcp_visible is (operation.auth_mode != "rso")
        if operation.source != "riot_api":
            continue
        async_method: Any = raw
        sync_method: Any = sync_raw
        for segment in operation.accessor_path.split("."):
            async_method = getattr(async_method, segment)
            sync_method = getattr(sync_method, segment)
        assert inspect.iscoroutinefunction(async_method)
        assert callable(sync_method)
        assert not inspect.iscoroutinefunction(sync_method)
        assert inspect.signature(async_method) == inspect.signature(sync_method)


def test_generated_model_alias_round_trip() -> None:
    from riotskillissue.models.lol.summoner_v4 import Summoner

    summoner = Summoner(
        profile_icon_id=1,
        puuid="player",
        revision_date=123,
        summoner_level=42,
    )

    assert summoner.model_dump()["summoner_level"] == 42
    assert summoner.model_dump(by_alias=True)["summonerLevel"] == 42


@pytest.mark.parametrize(
    "schema",
    [
        {"type": "object"},
        {"type": "object", "description": "UNKNOWN TYPE.", "properties": {}},
        {"type": "object", "properties": {}, "additionalProperties": True},
    ],
)
def test_generated_unknown_models_preserve_payloads(
    monkeypatch: pytest.MonkeyPatch,
    schema: dict[str, Any],
) -> None:
    spec = _spec()
    spec["components"]["schemas"]["val-widget-v1.WidgetDto"] = schema
    parser = OpenApiParser(spec)
    parser.parse()
    assert parser.models["val-widget-v1.WidgetDto"].preserve_unknown_fields

    files = render_generated_files(spec, format_code=False)
    model_path = Path("src/riotskillissue/models/valorant/widget_v1.py")
    module = ModuleType("generated_unknown_model")
    monkeypatch.setitem(sys.modules, module.__name__, module)
    exec(compile(files[model_path], str(model_path), "exec"), module.__dict__)
    payload = {"matchId": "EUW1_123", "participants": [{"score": 7}], "metadata": None}

    result = module.Widget.model_validate(payload)

    assert result.model_dump(by_alias=True) == payload
    assert json.loads(result.model_dump_json()) == payload


def test_generated_known_models_keep_validation_and_extra_field_behavior(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    spec = _spec()
    spec["components"]["schemas"]["val-widget-v1.EmptyDto"] = {
        "type": "object",
        "additionalProperties": False,
    }
    parser = OpenApiParser(spec)
    parser.parse()
    assert not parser.models["val-widget-v1.WidgetDto"].preserve_unknown_fields
    assert not parser.models["val-widget-v1.EmptyDto"].preserve_unknown_fields

    files = render_generated_files(spec, format_code=False)
    model_path = Path("src/riotskillissue/models/valorant/widget_v1.py")
    module = ModuleType("generated_known_models")
    monkeypatch.setitem(sys.modules, module.__name__, module)
    exec(compile(files[model_path], str(model_path), "exec"), module.__dict__)

    assert module.Empty.model_validate({"unknown": 42}).model_dump() == {}
    result = module.Widget.model_validate({"widgetId": "widget", "queue_id": 1, "unknown": 42})
    assert "unknown" not in result.model_dump()
    with pytest.raises(ValidationError):
        module.Widget.model_validate({"widgetId": "widget", "queue_id": "invalid"})


def test_committed_placeholder_models_preserve_nested_response_data() -> None:
    from riotskillissue.models.lol.rso_match_v1 import Match, Timeline
    from riotskillissue.models.valorant.console_ranked_v1 import Leaderboard

    payload = {"metadata": {"matchId": "EUW1_123"}, "info": {"participants": [{"id": 1}]}}
    for model in (Match, Timeline):
        assert model.model_validate(payload).model_dump() == payload

    tiers = [{"tier": 1, "rankedRatingThreshold": 100}]
    leaderboard = Leaderboard.model_validate(
        {
            "actId": "act",
            "players": [],
            "shard": "eu",
            "totalPlayers": 0,
            "tierDetails": tiers,
        }
    )
    assert leaderboard.model_dump(by_alias=True)["tierDetails"] == tiers

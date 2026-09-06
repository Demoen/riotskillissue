import sys
from copy import deepcopy
from importlib import import_module
from pathlib import Path

import pytest
_REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, _REPO_ROOT)
try:
    DiffEngine = import_module("tools.diff_engine").DiffEngine
finally:
    sys.path.remove(_REPO_ROOT)


def test_compare_reports_path_metadata_without_treating_it_as_operations() -> None:
    old = {
        "paths": {
            "/items": {
                "$ref": "#/components/pathItems/OldItems",
                "summary": "Old summary",
                "description": "Old description",
                "servers": [{"url": "https://old.example"}],
                "parameters": [{"name": "tenant", "in": "header"}],
                "x-endpoint": "old-items",
                "x-platforms-available": ["na1"],
                "x-route-enum": "platform",
                "x-operation-like": {"parameters": [{"name": "old-metadata"}]},
                "get": {"parameters": []},
            }
        }
    }
    new = {
        "paths": {
            "/items": {
                "$ref": "#/components/pathItems/NewItems",
                "summary": "New summary",
                "description": "New description",
                "servers": [{"url": "https://new.example"}],
                "parameters": [{"name": "locale", "in": "header"}],
                "x-endpoint": "new-items",
                "x-platforms-available": ["euw1"],
                "x-route-enum": "regional",
                "x-operation-like": {"parameters": [{"name": "new-metadata"}]},
                "get": {"parameters": [{"name": "queue", "in": "query"}]},
            }
        }
    }

    diff = DiffEngine().compare(old, new)

    changes = "\n".join(diff.modified_endpoints["/items"])
    assert "get.parameters" in changes
    assert "x-route-enum" in changes
    assert 'parameters[0].name: "tenant" -> "locale"' in changes
    assert "$ref:" in changes


def test_compare_reports_method_and_extension_additions_and_removals() -> None:
    old = {
        "paths": {
            "/items": {
                "get": {"parameters": []},
                "x-old-operation": {"parameters": []},
            }
        }
    }
    new = {
        "paths": {
            "/items": {
                "post": {"parameters": []},
                "x-new-operation": {"parameters": []},
            }
        }
    }

    diff = DiffEngine().compare(old, new)

    changes = "\n".join(diff.modified_endpoints["/items"])
    assert 'Added post: {"parameters": []}' in changes
    assert 'Removed get: {"parameters": []}' in changes
    assert "Removed x-old-operation:" in changes
    assert "Added x-new-operation:" in changes


@pytest.mark.parametrize("field", ["responses", "requestBody", "security", "operationId"])
def test_existing_operation_contract_changes_are_reported(field: str) -> None:
    old = {"paths": {"/items": {"get": {field: {"old": "value"}}}}}
    new = {"paths": {"/items": {"get": {field: {"new": "value"}}}}}

    report = DiffEngine().compare(old, new).to_markdown()

    assert f"get.{field}" in report
    assert "No Changes" not in report


@pytest.mark.parametrize("field,value", [
    ("type", "string"), ("nullable", True), ("minimum", 5),
    ("enum", [2, 3]), ("default", True),
])
def test_existing_model_field_changes_are_reported(field: str, value: object) -> None:
    old = {"components": {"schemas": {"Item": {
        "properties": {"count": {"type": "integer", "default": 1}},
    }}}}
    new = deepcopy(old)
    new["components"]["schemas"]["Item"]["properties"]["count"][field] = value

    report = DiffEngine().compare(old, new).to_markdown()

    assert f"properties.count.{field}" in report


def test_required_fields_and_referenced_parameters_are_reported() -> None:
    old = {
        "paths": {"/items": {"get": {"parameters": [{"$ref": "#/components/parameters/Id"}]}}},
        "components": {"schemas": {"Item": {"required": []}}, "parameters": {"Id": {"in": "query"}}},
    }
    new = deepcopy(old)
    new["components"]["schemas"]["Item"]["required"] = ["id"]
    new["components"]["parameters"]["Id"]["in"] = "header"

    report = DiffEngine().compare(old, new).to_markdown()

    assert 'Added required[0]: "id"' in report
    assert "components.parameters.Id.in" in report


def test_reports_are_deterministic_and_identical_specs_have_no_changes() -> None:
    first = {"paths": {"/z": {}, "/a": {}}, "info": {"description": "old"}}
    second = {"info": {"description": "old"}, "paths": {"/a": {}, "/z": {}}}

    assert DiffEngine().compare({}, first).to_markdown() == (
        DiffEngine().compare({}, second).to_markdown()
    )
    assert DiffEngine().compare(first, second).to_markdown() == "# No Changes"


def test_parameter_changes_beyond_report_preview_are_located_precisely() -> None:
    old = {"paths": {"/items": {"get": {"parameters": [
        {"name": f"parameter_{i}", "in": "query", "schema": {"type": "string"}}
        for i in range(20)
    ]}}}}
    new = deepcopy(old)
    new["paths"]["/items"]["get"]["parameters"][-1]["schema"]["type"] = "integer"

    report = DiffEngine().compare(old, new).to_markdown()

    assert 'get.parameters[19].schema.type: "string" -> "integer"' in report

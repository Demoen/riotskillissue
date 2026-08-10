from tools.diff_engine import DiffEngine


def test_compare_ignores_non_operation_path_item_fields() -> None:
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

    assert diff.modified_endpoints == {"/items": ["[get] Added params: {'queue'}"]}


def test_compare_reports_only_http_method_additions_and_removals() -> None:
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

    assert diff.modified_endpoints == {
        "/items": ["Added methods: {'post'}", "Removed methods: {'get'}"]
    }

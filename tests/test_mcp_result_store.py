from __future__ import annotations

import pytest

from riotskillissue.mcp.errors import (
    InvalidPointerError,
    ResultNotFoundError,
    ResultTooLargeError,
)
from riotskillissue.mcp.result_store import ResultStore


class Clock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value


def test_small_results_are_inline_and_secrets_are_redacted() -> None:
    store = ResultStore()

    result = store.present(
        {
            "api_key": "RGAPI-secret-value",
            "message": "Bearer private-token",
            "name": "player",
        }
    )

    assert result.inline is True
    assert result.handle is None
    assert result.data == {
        "api_key": "[REDACTED]",
        "message": "[REDACTED]",
        "name": "player",
    }


def test_large_results_support_pointer_navigation_and_pagination() -> None:
    store = ResultStore(inline_limit=8, max_result_size=4096)
    result = store.present(
        {
            "players/list": [{"name": "one"}, {"name": "two"}, {"name": "three"}],
            "~meta": {"ok": True},
        }
    )

    assert result.inline is False
    assert result.handle is not None
    page = store.read(result.handle, pointer="/players~1list", offset=1, limit=1)

    assert page.data == [{"name": "two"}]
    assert page.total == 3
    assert page.next_offset == 2
    escaped = store.read(result.handle, pointer="/~0meta")
    assert escaped.data == {"ok": True}


def test_expiry_and_lru_eviction() -> None:
    clock = Clock()
    store = ResultStore(
        inline_limit=1,
        max_results=2,
        ttl=10,
        max_result_size=4096,
        clock=clock,
    )
    first = store.present({"id": 1})
    second = store.present({"id": 2})
    assert first.handle is not None
    assert second.handle is not None

    store.read(first.handle)
    third = store.present({"id": 3})
    assert third.handle is not None

    with pytest.raises(ResultNotFoundError):
        store.read(second.handle)
    assert store.read(first.handle).data == {"id": 1}

    clock.value = 10
    with pytest.raises(ResultNotFoundError):
        store.read(first.handle)


def test_retained_byte_budget_uses_lru_eviction() -> None:
    store = ResultStore(
        inline_limit=1,
        max_results=10,
        max_result_size=40,
        max_retained_bytes=70,
    )
    first = store.present({"id": 1, "value": "x" * 15})
    second = store.present({"id": 2, "value": "x" * 15})
    assert first.handle is not None
    assert second.handle is not None

    store.read(first.handle)
    third = store.present({"id": 3, "value": "x" * 15})
    assert third.handle is not None

    with pytest.raises(ResultNotFoundError):
        store.read(second.handle)
    assert store.read(first.handle).data["id"] == 1
    assert store.read(third.handle).data["id"] == 3


def test_retained_byte_ceiling_rejects_single_value_and_invalid_budget() -> None:
    with pytest.raises(ValueError, match="max_retained_bytes"):
        ResultStore(
            inline_limit=1,
            max_result_size=65,
            max_retained_bytes=64,
        )

    store = ResultStore(
        inline_limit=1,
        max_result_size=64,
        max_retained_bytes=64,
    )
    with pytest.raises(ResultTooLargeError, match="retained-byte"):
        store.present({"value": "x" * 100})


def test_invalid_json_pointer_and_size_ceiling_fail_safely() -> None:
    store = ResultStore(inline_limit=1, max_result_size=64)
    result = store.present({"a/b": [1, 2]})
    assert result.handle is not None

    with pytest.raises(InvalidPointerError):
        store.read(result.handle, pointer="a/b")
    with pytest.raises(InvalidPointerError):
        store.read(result.handle, pointer="/a~2b")
    with pytest.raises(ResultTooLargeError):
        store.present({"value": "x" * 100})

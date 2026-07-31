"""Bounded in-memory retention for MCP tool results."""

from __future__ import annotations

import json
import math
import re
import secrets
import threading
import time
from collections import OrderedDict
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, is_dataclass
from datetime import date, datetime, time as datetime_time
from enum import Enum
from typing import Any, Callable
from uuid import UUID

from pydantic import BaseModel

from .errors import (
    InvalidPointerError,
    ResultEncodingError,
    ResultNotFoundError,
    ResultTooLargeError,
    is_sensitive_key,
    redact_text,
)
from .models import ResultPage, ToolResult
from .settings import (
    DEFAULT_INLINE_LIMIT,
    DEFAULT_MAX_RESULTS,
    DEFAULT_MAX_RESULT_SIZE,
    DEFAULT_RESULT_TTL,
)

_ARRAY_INDEX = re.compile(r"0|[1-9][0-9]*")
_MAX_PAGE_SIZE = 200


@dataclass(frozen=True)
class _StoredResult:
    value: Any
    size_bytes: int
    expires_at: float


class ResultStore:
    """Store oversized JSON results in memory with TTL and LRU eviction."""

    def __init__(
        self,
        *,
        inline_limit: int = DEFAULT_INLINE_LIMIT,
        max_results: int = DEFAULT_MAX_RESULTS,
        ttl: float = DEFAULT_RESULT_TTL,
        max_result_size: int = DEFAULT_MAX_RESULT_SIZE,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if inline_limit < 1 or max_results < 1 or ttl <= 0:
            raise ValueError("Result store limits must be positive.")
        if max_result_size < inline_limit:
            raise ValueError("max_result_size cannot be smaller than inline_limit.")
        self.inline_limit = inline_limit
        self.max_results = max_results
        self.ttl = ttl
        self.max_result_size = max_result_size
        self._clock = clock
        self._entries: OrderedDict[str, _StoredResult] = OrderedDict()
        self._lock = threading.RLock()

    def present(self, value: Any) -> ToolResult:
        """Return a small value inline or retain a large value behind a handle."""
        normalized = _normalize_json(value)
        encoded = _encode_json(normalized)
        size = len(encoded)
        if size > self.max_result_size:
            raise ResultTooLargeError(
                "The Riot result exceeds the MCP in-memory result size ceiling."
            )
        if size <= self.inline_limit:
            return ToolResult(inline=True, size_bytes=size, data=normalized)

        handle = secrets.token_urlsafe(24)
        with self._lock:
            now = self._clock()
            self._prune_expired(now)
            self._entries[handle] = _StoredResult(
                value=normalized,
                size_bytes=size,
                expires_at=now + self.ttl,
            )
            while len(self._entries) > self.max_results:
                self._entries.popitem(last=False)

        return ToolResult(
            inline=False,
            size_bytes=size,
            handle=handle,
            outline=_outline(normalized),
            expires_in_seconds=math.ceil(self.ttl),
        )

    def read(
        self,
        handle: str,
        *,
        pointer: str = "",
        offset: int = 0,
        limit: int = 50,
    ) -> ResultPage:
        """Read one RFC 6901 location with list or object pagination."""
        if offset < 0:
            raise InvalidPointerError("Result offset cannot be negative.")
        if limit < 1 or limit > _MAX_PAGE_SIZE:
            raise InvalidPointerError("Result limit must be between 1 and 200.")

        with self._lock:
            now = self._clock()
            self._prune_expired(now)
            entry = self._entries.get(handle)
            if entry is None:
                raise ResultNotFoundError("The result handle is invalid or expired.")
            self._entries.move_to_end(handle)
            selected = _resolve_pointer(entry.value, pointer)
            size_bytes = entry.size_bytes

        data, total, next_offset = _paginate(selected, offset, limit)
        return ResultPage(
            handle=handle,
            pointer=pointer,
            size_bytes=size_bytes,
            data=data,
            offset=offset,
            limit=limit,
            total=total,
            next_offset=next_offset,
        )

    def __len__(self) -> int:
        with self._lock:
            self._prune_expired(self._clock())
            return len(self._entries)

    def _prune_expired(self, now: float) -> None:
        expired = [
            handle
            for handle, entry in self._entries.items()
            if entry.expires_at <= now
        ]
        for handle in expired:
            self._entries.pop(handle, None)


def _normalize_json(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ResultEncodingError("The Riot result contains a non-finite number.")
        return value
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, Enum):
        return _normalize_json(value.value)
    if isinstance(value, (datetime, date, datetime_time)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, BaseModel):
        return _normalize_json(value.model_dump(mode="json"))
    if is_dataclass(value) and not isinstance(value, type):
        return _normalize_json(asdict(value))
    if isinstance(value, Mapping):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            text_key = str(key)
            safe_key = redact_text(text_key)
            normalized[safe_key] = (
                "[REDACTED]" if is_sensitive_key(text_key) else _normalize_json(item)
            )
        return normalized
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_normalize_json(item) for item in value]
    raise ResultEncodingError("The Riot result cannot be represented as JSON.")


def _encode_json(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as exc:
        raise ResultEncodingError("The Riot result cannot be represented as JSON.") from exc


def _outline(value: Any) -> dict[str, Any]:
    if isinstance(value, list):
        outline: dict[str, Any] = {"type": "array", "length": len(value)}
        if value:
            outline["item_type"] = _json_type(value[0])
        return outline
    if isinstance(value, dict):
        keys = list(value)[:20]
        return {
            "type": "object",
            "length": len(value),
            "keys": keys,
            "keys_truncated": len(value) > len(keys),
        }
    return {"type": _json_type(value)}


def _json_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    return "object"


def _resolve_pointer(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise InvalidPointerError("JSON Pointer must be empty or start with '/'.")

    current = value
    for raw_token in pointer[1:].split("/"):
        token = _decode_token(raw_token)
        if isinstance(current, dict):
            if token not in current:
                raise InvalidPointerError("JSON Pointer does not exist in this result.")
            current = current[token]
            continue
        if isinstance(current, list):
            if _ARRAY_INDEX.fullmatch(token) is None:
                raise InvalidPointerError("JSON Pointer contains an invalid array index.")
            index = int(token)
            if index >= len(current):
                raise InvalidPointerError("JSON Pointer does not exist in this result.")
            current = current[index]
            continue
        raise InvalidPointerError("JSON Pointer traverses a scalar value.")
    return current


def _decode_token(token: str) -> str:
    output: list[str] = []
    index = 0
    while index < len(token):
        char = token[index]
        if char != "~":
            output.append(char)
            index += 1
            continue
        if index + 1 >= len(token) or token[index + 1] not in {"0", "1"}:
            raise InvalidPointerError("JSON Pointer contains an invalid escape.")
        output.append("~" if token[index + 1] == "0" else "/")
        index += 2
    return "".join(output)


def _paginate(value: Any, offset: int, limit: int) -> tuple[Any, int | None, int | None]:
    if isinstance(value, list):
        total = len(value)
        data: Any = value[offset : offset + limit]
        next_offset = offset + len(data) if offset + len(data) < total else None
        return data, total, next_offset
    if isinstance(value, dict):
        items = list(value.items())
        total = len(items)
        data = dict(items[offset : offset + limit])
        next_offset = offset + len(data) if offset + len(data) < total else None
        return data, total, next_offset
    if offset != 0:
        raise InvalidPointerError("A scalar result only supports offset zero.")
    return value, None, None

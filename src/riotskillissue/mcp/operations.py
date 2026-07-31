"""Operation-registry adapter used by MCP discovery and dispatch."""

from __future__ import annotations

import inspect
import importlib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import Enum
from types import ModuleType
from typing import Any, cast

from pydantic import BaseModel

from .errors import (
    IntegrationContractError,
    InvalidArgumentsError,
    OperationNotAllowedError,
    OperationNotFoundError,
    contains_secret_value,
    is_sensitive_key,
    redact_text,
)
from .models import (
    FindOperationsResult,
    OperationDescription,
    OperationSummary,
    ToolResult,
)
from .result_store import ResultStore

_READ_METHODS = {"GET", "HEAD", "OPTIONS"}
_BLOCKED_AUTH_MARKERS = {"rso", "oauth", "bearer"}
_STATIC_OPERATIONS: tuple[
    tuple[str, str, dict[str, dict[str, Any]], str],
    ...,
] = (
    (
        "static.get_latest_version",
        "get_latest_version",
        {},
        "Get the latest Data Dragon version.",
    ),
    (
        "static.get_champion",
        "get_champion",
        {"champion_key": {"type": "integer", "minimum": 1}},
        "Get Data Dragon champion data by numeric key.",
    ),
    (
        "static.get_all_champions",
        "get_all_champions",
        {},
        "Get all Data Dragon champions.",
    ),
    (
        "static.get_item",
        "get_item",
        {"item_id": {"type": "integer", "minimum": 1}},
        "Get Data Dragon item data by numeric ID.",
    ),
    (
        "static.get_all_items",
        "get_all_items",
        {},
        "Get all Data Dragon items.",
    ),
    (
        "static.get_summoner_spells",
        "get_summoner_spells",
        {},
        "Get all Data Dragon summoner spells.",
    ),
    (
        "static.get_summoner_spell",
        "get_summoner_spell",
        {"spell_key": {"type": "integer", "minimum": 1}},
        "Get a Data Dragon summoner spell by numeric key.",
    ),
    ("static.get_runes", "get_runes", {}, "Get the Data Dragon rune tree."),
    ("static.get_queues", "get_queues", {}, "Get League queue metadata."),
    ("static.get_maps", "get_maps", {}, "Get League map metadata."),
    (
        "static.get_game_modes",
        "get_game_modes",
        {},
        "Get League game-mode metadata.",
    ),
)


@dataclass(frozen=True)
class OperationRecord:
    operation_id: str
    accessor_path: str
    game: str
    service: str
    method: str
    read_only: bool
    auth_mode: str
    route_type: str | None
    allowed_routes: tuple[str, ...]
    input_schema: dict[str, Any]
    description: str | None
    static_method: str | None = None
    registry_visible: bool = True

    @property
    def mcp_eligible(self) -> bool:
        auth = self.auth_mode.lower()
        return self.registry_visible and not any(
            marker in auth for marker in _BLOCKED_AUTH_MARKERS
        )

    def summary(self) -> OperationSummary:
        return OperationSummary(
            operation=self.operation_id,
            accessor_path=self.accessor_path,
            game=self.game,
            service=self.service,
            method=self.method,
            read_only=self.read_only,
            description=self.description,
        )

    def describe(self) -> OperationDescription:
        return OperationDescription(
            **self.summary().model_dump(),
            route_type=self.route_type,
            allowed_routes=list(self.allowed_routes),
            auth_mode=self.auth_mode,
            input_schema=self.input_schema,
        )


class OperationGateway:
    """Expose a safe, searchable view over generated and static operations."""

    def __init__(
        self,
        client: Any,
        result_store: ResultStore,
        registry: object,
        *,
        allow_writes: bool = False,
    ) -> None:
        self._client = client
        self._result_store = result_store
        self._allow_writes = allow_writes
        records = list(_registry_records(registry))
        existing_ids = {record.operation_id for record in records}
        records.extend(
            record
            for record in _static_records()
            if record.operation_id not in existing_ids
        )
        self._records = tuple(record for record in records if record.mcp_eligible)
        self._aliases = _build_aliases(self._records)

    def find(
        self,
        *,
        query: str = "",
        game: str | None = None,
        include_writes: bool = False,
        limit: int = 20,
    ) -> FindOperationsResult:
        if limit < 1 or limit > 100:
            raise InvalidArgumentsError("Operation search limit must be between 1 and 100.")

        normalized_game = game.strip().lower() if game else None
        terms = [term for term in query.lower().split() if term]
        candidates: list[tuple[int, OperationRecord]] = []
        for record in self._records:
            if normalized_game and record.game.lower() != normalized_game:
                continue
            if not record.read_only and not (include_writes and self._allow_writes):
                continue
            searchable = " ".join(
                filter(
                    None,
                    (
                        record.operation_id,
                        record.accessor_path,
                        record.game,
                        record.service,
                        record.description,
                    ),
                )
            ).lower()
            if not all(term in searchable for term in terms):
                continue
            candidates.append((_search_score(record, query), record))

        candidates.sort(key=lambda item: (-item[0], item[1].operation_id))
        matches = [record.summary() for _, record in candidates[:limit]]
        return FindOperationsResult(operations=matches, total=len(candidates))

    def describe(self, operation: str) -> OperationDescription:
        return self._resolve_visible(operation).describe()

    async def call_read(
        self,
        operation: str,
        arguments: Mapping[str, Any],
    ) -> ToolResult:
        record = self._resolve_visible(operation)
        if not record.read_only:
            raise OperationNotAllowedError(
                "The requested operation is a write. Use the confirmed write tool."
            )
        result = await self._invoke(record, arguments)
        return self._result_store.present(result)

    async def call_write(
        self,
        operation: str,
        arguments: Mapping[str, Any],
        *,
        confirmed: bool,
    ) -> ToolResult:
        if not self._allow_writes:
            raise OperationNotAllowedError("Riot API writes are disabled for this server.")
        if not confirmed:
            raise OperationNotAllowedError("The write operation was not approved.")
        record = self._resolve_visible(operation)
        if record.read_only:
            raise InvalidArgumentsError("Use the read-operation tool for this operation.")
        result = await self._invoke(record, arguments)
        return self._result_store.present(result)

    def _resolve_visible(self, operation: str) -> OperationRecord:
        normalized = operation.strip()
        record = self._aliases.get(normalized) or self._aliases.get(normalized.lower())
        if record is None:
            raise OperationNotFoundError(
                "The operation was not found or is not exposed through MCP."
            )
        if not record.read_only and not self._allow_writes:
            raise OperationNotFoundError(
                "The operation was not found or is not exposed through MCP."
            )
        return record

    async def _invoke(
        self,
        record: OperationRecord,
        arguments: Mapping[str, Any],
    ) -> Any:
        cleaned = _validate_arguments(arguments)
        _validate_schema_arguments(cleaned, record.input_schema)
        if record.static_method is not None:
            static_client = getattr(self._client, "static", None)
            method = getattr(static_client, record.static_method, None)
            if not callable(method):
                raise IntegrationContractError(
                    "The installed RiotSkillIssue client lacks the requested static operation."
                )
            result = method(**cleaned)
        else:
            call_operation = getattr(self._client, "call_operation", None)
            if not callable(call_operation):
                raise IntegrationContractError(
                    "The installed RiotSkillIssue client lacks operation dispatch support."
                )
            result = call_operation(record.operation_id, cleaned)
        return await result if inspect.isawaitable(result) else result


def load_operation_registry() -> object:
    """Load the generated operation registry without importing it at package import."""
    try:
        try:
            operations = importlib.import_module("riotskillissue.api.operations")
        except (ImportError, ModuleNotFoundError):
            operations = importlib.import_module("riotskillissue.api.registry")
    except (ImportError, ModuleNotFoundError) as exc:
        raise IntegrationContractError(
            "The generated Riot operation registry is unavailable."
        ) from exc

    for name in (
        "OPERATION_REGISTRY",
        "operation_registry",
        "OPERATIONS",
        "registry",
    ):
        candidate = getattr(operations, name, None)
        if candidate is not None:
            return candidate

    getter = getattr(operations, "get_operation_registry", None)
    if callable(getter):
        return getter()

    operation_class = getattr(operations, "OperationRegistry", None)
    if operation_class is not None:
        candidate = getattr(operation_class, "default", None)
        if callable(candidate):
            return candidate()
        if candidate is not None:
            return candidate

    if _looks_iterable_registry(operations):
        return operations
    raise IntegrationContractError("The generated Riot operation registry is unavailable.")


def _registry_records(registry: object) -> Iterable[OperationRecord]:
    for fallback_id, raw in _registry_items(registry):
        yield _coerce_record(raw, fallback_id)


def _registry_items(registry: object) -> Iterable[tuple[str | None, object]]:
    candidate = registry
    if isinstance(registry, ModuleType):
        for name in ("OPERATION_REGISTRY", "operation_registry", "OPERATIONS", "registry"):
            value = getattr(registry, name, None)
            if value is not None:
                candidate = value
                break

    for name in ("operations", "values", "all"):
        value = getattr(candidate, name, None)
        if callable(value):
            try:
                value = value()
            except TypeError:
                continue
        if value is not None and value is not candidate:
            candidate = value
            break

    if isinstance(candidate, Mapping):
        for key, value in candidate.items():
            yield str(key), value
        return
    if isinstance(candidate, Iterable) and not isinstance(candidate, (str, bytes)):
        for value in candidate:
            yield None, value
        return
    raise IntegrationContractError("The generated operation registry is not iterable.")


def _coerce_record(raw: object, fallback_id: str | None) -> OperationRecord:
    operation_id = _text(
        _field(raw, "stable_id", "operation_id", "id", "name", default=fallback_id)
    )
    if not operation_id:
        raise IntegrationContractError("An operation registry entry has no stable ID.")

    accessor_path = _text(
        _field(raw, "accessor_path", "path", "client_path", default=operation_id)
    )
    method = _text(_field(raw, "http_method", "method", "verb", default="")).upper()
    read_only_value = _field(raw, "read_only", default=None)
    write_value = _field(raw, "is_write", "write", "mutation", default=None)
    if isinstance(read_only_value, bool):
        read_only = read_only_value
    elif isinstance(write_value, bool):
        read_only = not write_value
    else:
        classification = _text(
            _field(raw, "classification", "operation_type", default="")
        ).lower()
        if classification:
            read_only = classification in {"read", "query", "read_only"}
        else:
            read_only = method in _READ_METHODS

    auth_mode = _text(
        _field(raw, "auth_mode", "authentication", "security", default="api_key")
    ).lower()
    schema = _schema(_field(raw, "input_schema", "arguments_schema", default={}))
    routes = _string_tuple(
        _field(raw, "allowed_routes", "routes", default=())
    )
    description_value = _field(raw, "description", "summary", default=None)
    description = (
        redact_text(str(description_value))[:500]
        if description_value is not None
        else None
    )
    source = _text(_field(raw, "source", default="")).lower()
    static_method = (
        operation_id.removeprefix("static.")
        if source == "data_dragon" or operation_id.startswith("static.")
        else None
    )
    return OperationRecord(
        operation_id=operation_id,
        accessor_path=accessor_path or operation_id,
        game=_text(_field(raw, "game", default="unknown")).lower(),
        service=_text(_field(raw, "service", "group", default="unknown")).lower(),
        method=method or ("GET" if read_only else "POST"),
        read_only=read_only,
        auth_mode=auth_mode or "none",
        route_type=_optional_text(_field(raw, "route_type", "route_kind", default=None)),
        allowed_routes=routes,
        input_schema=schema,
        description=description,
        static_method=static_method,
        registry_visible=bool(_field(raw, "mcp_visible", default=True)),
    )


def _static_records() -> Iterable[OperationRecord]:
    for operation_id, method, properties, description in _STATIC_OPERATIONS:
        required = list(properties)
        yield OperationRecord(
            operation_id=operation_id,
            accessor_path=operation_id,
            game="lol",
            service="data_dragon",
            method="GET",
            read_only=True,
            auth_mode="none",
            route_type=None,
            allowed_routes=(),
            input_schema={
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
            description=description,
            static_method=method,
            registry_visible=True,
        )


def _build_aliases(records: Iterable[OperationRecord]) -> dict[str, OperationRecord]:
    aliases: dict[str, OperationRecord] = {}
    collisions: set[str] = set()
    for record in records:
        for alias in {record.operation_id, record.accessor_path}:
            for key in {alias, alias.lower()}:
                previous = aliases.get(key)
                if previous is not None and previous.operation_id != record.operation_id:
                    collisions.add(key)
                else:
                    aliases[key] = record
    for key in collisions:
        aliases.pop(key, None)
    return aliases


def _search_score(record: OperationRecord, query: str) -> int:
    normalized = query.strip().lower()
    if not normalized:
        return 0
    if record.operation_id.lower() == normalized:
        return 100
    if record.accessor_path.lower() == normalized:
        return 90
    if record.operation_id.lower().startswith(normalized):
        return 60
    if normalized in record.operation_id.lower():
        return 40
    return 10


def _validate_arguments(arguments: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(arguments, Mapping):
        raise InvalidArgumentsError("Operation arguments must be a JSON object.")
    _reject_secrets(arguments)
    return dict(arguments)


def _validate_schema_arguments(
    arguments: Mapping[str, Any],
    schema: Mapping[str, Any],
) -> None:
    properties = schema.get("properties")
    if not isinstance(properties, Mapping):
        return
    required_raw = schema.get("required", [])
    required = {
        str(name)
        for name in required_raw
        if isinstance(name, str)
    }
    missing = required.difference(arguments)
    if missing:
        raise InvalidArgumentsError(
            f"Missing required operation argument: {sorted(missing)[0]}."
        )
    if schema.get("additionalProperties") is False:
        unknown = set(arguments).difference(str(name) for name in properties)
        if unknown:
            raise InvalidArgumentsError(
                f"Unknown operation argument: {sorted(unknown)[0]}."
            )
    for name, value in arguments.items():
        property_schema = properties.get(name)
        if not isinstance(property_schema, Mapping):
            continue
        if value is None:
            if name in required:
                raise InvalidArgumentsError(
                    f"Operation argument {name} cannot be null."
                )
            continue
        _validate_schema_value(name, value, property_schema)


def _validate_schema_value(
    name: str,
    value: Any,
    schema: Mapping[str, Any],
) -> None:
    enum_values = schema.get("enum")
    if isinstance(enum_values, list) and value not in enum_values:
        raise InvalidArgumentsError(
            f"Operation argument {name} is not an allowed value."
        )

    expected = schema.get("type")
    valid = True
    if expected == "string":
        valid = isinstance(value, str)
    elif expected == "integer":
        valid = isinstance(value, int) and not isinstance(value, bool)
    elif expected == "number":
        valid = isinstance(value, (int, float)) and not isinstance(value, bool)
    elif expected == "boolean":
        valid = isinstance(value, bool)
    elif expected == "array":
        valid = isinstance(value, list)
    elif expected == "object":
        valid = isinstance(value, Mapping)
    if not valid:
        raise InvalidArgumentsError(
            f"Operation argument {name} has the wrong JSON type."
        )

    if isinstance(value, str):
        minimum_length = schema.get("minLength")
        maximum_length = schema.get("maxLength")
        if isinstance(minimum_length, int) and len(value) < minimum_length:
            raise InvalidArgumentsError(f"Operation argument {name} is too short.")
        if isinstance(maximum_length, int) and len(value) > maximum_length:
            raise InvalidArgumentsError(f"Operation argument {name} is too long.")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if isinstance(minimum, (int, float)) and value < minimum:
            raise InvalidArgumentsError(f"Operation argument {name} is too small.")
        if isinstance(maximum, (int, float)) and value > maximum:
            raise InvalidArgumentsError(f"Operation argument {name} is too large.")
    if isinstance(value, list):
        minimum_items = schema.get("minItems")
        maximum_items = schema.get("maxItems")
        if isinstance(minimum_items, int) and len(value) < minimum_items:
            raise InvalidArgumentsError(
                f"Operation argument {name} has too few items."
            )
        if isinstance(maximum_items, int) and len(value) > maximum_items:
            raise InvalidArgumentsError(
                f"Operation argument {name} has too many items."
            )


def _reject_secrets(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if is_sensitive_key(key):
                raise OperationNotAllowedError(
                    "Credentials and tokens are server-managed and cannot be tool arguments."
                )
            _reject_secrets(item)
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            _reject_secrets(item)
        return
    if isinstance(value, str) and contains_secret_value(value):
        raise OperationNotAllowedError(
            "Credentials and tokens are server-managed and cannot be tool arguments."
        )


def _field(raw: object, *names: str, default: Any) -> Any:
    if isinstance(raw, Mapping):
        for name in names:
            if name in raw:
                return raw[name]
        return default
    for name in names:
        if hasattr(raw, name):
            return getattr(raw, name)
    return default


def _text(value: Any) -> str:
    if isinstance(value, Enum):
        value = value.value
    return str(value).strip() if value is not None else ""


def _optional_text(value: Any) -> str | None:
    text = _text(value)
    return text or None


def _string_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Iterable):
        return tuple(_text(item) for item in value)
    return (_text(value),)


def _schema(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        cleaned = _clean_schema(value)
        return cleaned if isinstance(cleaned, dict) else {}
    if isinstance(value, type) and issubclass(value, BaseModel):
        return cast(dict[str, Any], _clean_schema(value.model_json_schema()))
    schema_method = getattr(value, "model_json_schema", None)
    if callable(schema_method):
        schema = schema_method()
        return _clean_schema(schema) if isinstance(schema, Mapping) else {}
    return {}


def _clean_schema(value: Any) -> Any:
    if isinstance(value, Mapping):
        output: dict[str, Any] = {}
        for key, item in value.items():
            if is_sensitive_key(key):
                continue
            if key == "properties" and isinstance(item, Mapping):
                properties = {
                    str(name): _clean_schema(schema)
                    for name, schema in item.items()
                    if not is_sensitive_key(name)
                }
                output[str(key)] = properties
                continue
            if key == "required" and isinstance(item, list):
                output[str(key)] = [
                    entry for entry in item if not is_sensitive_key(entry)
                ]
                continue
            output[str(key)] = _clean_schema(item)
        return output
    if isinstance(value, list):
        return [_clean_schema(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, (type(None), bool, int, float)):
        return value
    return str(value)


def _looks_iterable_registry(value: object) -> bool:
    return isinstance(value, (Mapping, Iterable))

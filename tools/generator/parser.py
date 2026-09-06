from __future__ import annotations

import copy
import keyword
import re
from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


_HTTP_METHODS = {"delete", "get", "head", "options", "patch", "post", "put", "trace"}
_CONSTRAINT_KEYS = (
    "minimum",
    "exclusiveMinimum",
    "maximum",
    "exclusiveMaximum",
    "multipleOf",
    "minLength",
    "maxLength",
    "pattern",
    "minItems",
    "maxItems",
    "uniqueItems",
    "minProperties",
    "maxProperties",
)
_FIELD_CONSTRAINT_NAMES = {
    "minimum": "ge",
    "exclusiveMinimum": "gt",
    "maximum": "le",
    "exclusiveMaximum": "lt",
    "multipleOf": "multiple_of",
    "minLength": "min_length",
    "maxLength": "max_length",
    "pattern": "pattern",
    "minItems": "min_length",
    "maxItems": "max_length",
}
_MISSING = object()


def snake_case(name: str) -> str:
    value = re.sub(r"[^0-9A-Za-z_]+", "_", name)
    value = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value).lower().strip("_")
    if not value:
        value = "value"
    if value[0].isdigit():
        value = f"param_{value}"
    if keyword.iskeyword(value):
        value = f"{value}_"
    return value


def python_class_name(name: str) -> str:
    cleaned = re.sub(r"DTO", "", name, flags=re.IGNORECASE)
    parts = re.split(r"[^0-9A-Za-z]+", cleaned)
    value = "".join(part[:1].upper() + part[1:] for part in parts if part)
    if not value:
        value = "AnonymousModel"
    if value[0].isdigit():
        value = f"Model{value}"
    return value


@dataclass(frozen=True)
class ApiGroup:
    game: str
    service: str
    version: Optional[str]

    @property
    def model_module(self) -> str:
        if self.version:
            return f"{self.service}_{self.version}"
        return self.service


def classify_api_group(value: str) -> ApiGroup:
    normalized = value.strip().lower().replace("_", "-")
    match = re.match(r"^(.*?)-(v\d+)$", normalized)
    base = match.group(1) if match else normalized
    version = match.group(2) if match else None

    if base == "spectator-tft":
        return ApiGroup("tft", "spectator", version)
    if base.startswith("tft-"):
        return ApiGroup("tft", snake_case(base[4:]), version)
    if base.startswith("val-"):
        return ApiGroup("valorant", snake_case(base[4:]), version)
    if base.startswith("lor-"):
        return ApiGroup("lor", snake_case(base[4:]), version)
    if base.startswith("riftbound-"):
        return ApiGroup("riftbound", snake_case(base[10:]), version)
    if base == "account":
        return ApiGroup("common", "account", version)
    if base.startswith("lol-"):
        base = base[4:]
    return ApiGroup("lol", snake_case(base), version)


@dataclass
class Property:
    name: str
    wire_name: str
    type_annotation: str
    description: Optional[str] = None
    required: bool = False
    alias: Optional[str] = None
    default: Any = field(default=_MISSING, repr=False)
    constraints: dict[str, Any] = field(default_factory=dict)
    examples: list[Any] = field(default_factory=list)
    schema: dict[str, Any] = field(default_factory=dict)

    @property
    def has_default(self) -> bool:
        return self.default is not _MISSING

    @property
    def annotation(self) -> str:
        if self.required or self.type_annotation.startswith("Optional["):
            return self.type_annotation
        return f"Optional[{self.type_annotation}]"

    @property
    def field_arguments(self) -> str:
        values: list[str] = []
        if not self.required:
            default = self.default if self.has_default else None
            values.append(f"default={default!r}")
        elif self.has_default:
            values.append(f"default={self.default!r}")
        values.append(f"alias={self.wire_name!r}")
        if self.description:
            values.append(f"description={self.description!r}")
        if self.examples:
            values.append(f"examples={self.examples!r}")
        for source_name, target_name in _FIELD_CONSTRAINT_NAMES.items():
            if source_name in self.constraints:
                values.append(f"{target_name}={self.constraints[source_name]!r}")
        return ", ".join(values)

    @property
    def field_constraints(self) -> dict[str, Any]:
        return {
            target_name: self.constraints[source_name]
            for source_name, target_name in _FIELD_CONSTRAINT_NAMES.items()
            if source_name in self.constraints
        }


@dataclass
class Model:
    raw_name: str
    name: str
    game: str
    module: str
    properties: list[Property]
    description: Optional[str] = None
    enum_values: Optional[list[Any]] = None
    referenced_models: set[str] = field(default_factory=set)
    preserve_unknown_fields: bool = False

    @property
    def import_path(self) -> str:
        return f"riotskillissue.models.{self.game}.{self.module}"

    @property
    def qualified_name(self) -> str:
        return f"{self.import_path}.{self.name}"


@dataclass
class Parameter:
    name: str
    wire_name: str
    in_: str
    type_annotation: str
    required: bool
    description: Optional[str]
    ref: Optional[str] = None
    default: Any = field(default=_MISSING, repr=False)
    constraints: dict[str, Any] = field(default_factory=dict)
    examples: list[Any] = field(default_factory=list)
    schema: dict[str, Any] = field(default_factory=dict)

    @property
    def has_default(self) -> bool:
        return self.default is not _MISSING

    @property
    def annotation(self) -> str:
        if self.required or self.type_annotation.startswith("Optional["):
            return self.type_annotation
        return f"Optional[{self.type_annotation}]"

    @property
    def default_expression(self) -> Optional[str]:
        if self.required:
            return None
        return repr(self.default if self.has_default else None)


@dataclass
class RequestBody:
    type_annotation: str
    required: bool
    description: Optional[str]
    media_type: str
    schema: dict[str, Any]
    ref: Optional[str] = None
    examples: list[Any] = field(default_factory=list)

    @property
    def annotation(self) -> str:
        if self.required or self.type_annotation.startswith("Optional["):
            return self.type_annotation
        return f"Optional[{self.type_annotation}]"


@dataclass
class Response:
    status_code: str
    type_annotation: str
    description: Optional[str]
    media_type: Optional[str]
    schema: dict[str, Any]
    no_content: bool
    ref: Optional[str] = None


@dataclass(frozen=True)
class SecurityRequirement:
    scheme: str
    scopes: tuple[str, ...]


@dataclass
class Operation:
    operation_id: str
    method: str
    path: str
    summary: Optional[str]
    description: Optional[str]
    parameters: list[Parameter]
    responses: list[Response]
    tags: list[str]
    security: list[SecurityRequirement]
    route_kind: Optional[str]
    allowed_routes: tuple[str, ...]
    is_mutation: bool
    mutation_metadata: dict[str, Any]
    request_body: Optional[RequestBody] = None
    method_name: Optional[str] = None
    game: Optional[str] = None
    service: Optional[str] = None
    accessor_path: Optional[str] = None
    model_references: set[str] = field(default_factory=set)

    @property
    def clean_docstring(self) -> str:
        return " ".join((self.summary or self.description or "").split())

    @property
    def response_type(self) -> str:
        content_types: list[str] = []
        has_no_content = False
        for response in self.responses:
            if response.no_content:
                has_no_content = True
            elif response.type_annotation not in content_types:
                content_types.append(response.type_annotation)
        if not content_types:
            return "None"
        annotation = (
            content_types[0] if len(content_types) == 1 else f"Union[{', '.join(content_types)}]"
        )
        if has_no_content and not annotation.startswith("Optional["):
            return f"Optional[{annotation}]"
        return annotation

    @property
    def response_adapter_type(self) -> Optional[str]:
        if self.response_type in {"Any", "None"}:
            return None
        return self.response_type

    @property
    def successful_statuses(self) -> tuple[int | str, ...]:
        return tuple(self._normalize_status(response.status_code) for response in self.responses)

    @property
    def no_content_statuses(self) -> tuple[int | str, ...]:
        return tuple(
            self._normalize_status(response.status_code)
            for response in self.responses
            if response.no_content
        )

    @property
    def successful_status_codes(self) -> tuple[int, ...]:
        return tuple(status for status in self.successful_statuses if isinstance(status, int))

    @property
    def no_content_status_codes(self) -> tuple[int, ...]:
        return tuple(status for status in self.no_content_statuses if isinstance(status, int))

    @staticmethod
    def _normalize_status(status: str) -> int | str:
        return int(status) if status.isdigit() else status

    @property
    def auth_mode(self) -> str:
        if not self.security:
            return "none"
        schemes = {requirement.scheme for requirement in self.security}
        if "rso" in schemes:
            return "rso"
        return "api_key"

    @property
    def auth_scopes(self) -> tuple[str, ...]:
        return tuple(
            dict.fromkeys(scope for requirement in self.security for scope in requirement.scopes)
        )

    @property
    def cache_user_scoped(self) -> bool:
        return self.auth_mode == "rso"

    @property
    def mcp_visible(self) -> bool:
        return self.auth_mode != "rso"


class OpenApiParser:
    def __init__(self, spec: Mapping[str, Any]):
        self.spec = dict(spec)
        self.models: dict[str, Model] = {}
        self.operations: list[Operation] = []
        self.security_schemes: dict[str, dict[str, Any]] = copy.deepcopy(
            self.spec.get("components", {}).get("securitySchemes", {})
        )
        self._model_identities: dict[str, tuple[str, str, str]] = {}

    def parse(self) -> None:
        self._build_model_identities()
        self._parse_components()
        self._parse_paths()

    def _build_model_identities(self) -> None:
        schemas = self.spec.get("components", {}).get("schemas", {})
        for raw_name in schemas:
            if "." in raw_name:
                prefix, local_name = raw_name.split(".", 1)
                group = classify_api_group(prefix)
            else:
                local_name = raw_name
                group = ApiGroup("common", "errors", None)
            self._model_identities[raw_name] = (
                group.game,
                group.model_module,
                python_class_name(local_name),
            )

    def _to_python_type(self, schema: Mapping[str, Any]) -> str:
        if not schema:
            return "Any"
        if "$ref" in schema:
            raw_name = str(schema["$ref"]).split("/")[-1]
            identity = self._model_identities.get(raw_name)
            return identity[2] if identity else python_class_name(raw_name)
        if "oneOf" in schema or "anyOf" in schema:
            choices = schema.get("oneOf", schema.get("anyOf", []))
            nullable = any(choice.get("type") == "null" for choice in choices)
            annotations = list(
                dict.fromkeys(
                    self._to_python_type(choice)
                    for choice in choices
                    if choice.get("type") != "null"
                )
            )
            if not annotations:
                annotation = "Any"
            elif len(annotations) == 1:
                annotation = annotations[0]
            else:
                annotation = f"Union[{', '.join(annotations)}]"
            return self._make_optional(annotation) if nullable else annotation
        if "allOf" in schema:
            annotations = list(
                dict.fromkeys(self._to_python_type(choice) for choice in schema["allOf"])
            )
            return annotations[0] if len(annotations) == 1 else "Any"
        if "enum" in schema:
            values = ", ".join(repr(value) for value in schema["enum"])
            annotation = f"Literal[{values}]"
            return self._make_optional(annotation) if schema.get("nullable") else annotation

        schema_type = schema.get("type")
        if isinstance(schema_type, list):
            nullable = "null" in schema_type
            non_null = [value for value in schema_type if value != "null"]
            nested = dict(schema)
            nested["type"] = non_null[0] if len(non_null) == 1 else None
            annotation = self._to_python_type(nested)
            return self._make_optional(annotation) if nullable else annotation
        if schema_type == "array":
            annotation = f"List[{self._to_python_type(schema.get('items', {}))}]"
        elif schema_type == "object":
            additional = schema.get("additionalProperties")
            if isinstance(additional, Mapping):
                annotation = f"Dict[str, {self._to_python_type(additional)}]"
            else:
                annotation = "Dict[str, Any]"
        else:
            annotation = {
                "boolean": "bool",
                "integer": "int",
                "number": "float",
                "string": "str",
                "null": "None",
            }.get(schema_type, "Any")
        return self._make_optional(annotation) if schema.get("nullable") else annotation

    @staticmethod
    def _make_optional(annotation: str) -> str:
        if annotation.startswith("Optional[") or annotation == "None":
            return annotation
        return f"Optional[{annotation}]"

    def _parse_components(self) -> None:
        schemas = self.spec.get("components", {}).get("schemas", {})
        for raw_name, schema in schemas.items():
            game, module, name = self._model_identities[raw_name]
            enum_values = self._enum_values(schema)
            referenced_models = self._collect_model_references(schema)
            if enum_values is not None:
                self.models[raw_name] = Model(
                    raw_name=raw_name,
                    name=name,
                    game=game,
                    module=module,
                    properties=[],
                    enum_values=enum_values,
                    description=schema.get("description"),
                    referenced_models=referenced_models,
                )
                continue

            properties: list[Property] = []
            required = set(schema.get("required", []))
            raw_properties = list(schema.get("properties", {}).items())
            property_names: dict[str, list[str]] = {}
            for wire_name, _ in raw_properties:
                property_names.setdefault(snake_case(wire_name), []).append(wire_name)
            canonical_names = {
                base_name: next(
                    (wire_name for wire_name in wire_names if wire_name in required),
                    wire_names[0],
                )
                for base_name, wire_names in property_names.items()
            }
            for wire_name, property_schema in raw_properties:
                base_name = snake_case(wire_name)
                if len(property_names[base_name]) == 1 or canonical_names[base_name] == wire_name:
                    property_name = base_name
                else:
                    position = property_names[base_name].index(wire_name) + 1
                    property_name = f"{base_name}_{position}"
                properties.append(
                    Property(
                        name=property_name,
                        wire_name=wire_name,
                        type_annotation=self._to_python_type(property_schema),
                        required=wire_name in required,
                        description=property_schema.get("description"),
                        alias=wire_name,
                        default=property_schema.get("default", _MISSING),
                        constraints=self._constraints(property_schema),
                        examples=self._examples(property_schema),
                        schema=copy.deepcopy(property_schema),
                    )
                )
            self.models[raw_name] = Model(
                raw_name=raw_name,
                name=name,
                game=game,
                module=module,
                properties=properties,
                description=schema.get("description"),
                referenced_models=referenced_models,
                preserve_unknown_fields=(
                    schema.get("type") == "object"
                    and not raw_properties
                    and schema.get("additionalProperties", True) is True
                    and not any(key in schema for key in ("allOf", "anyOf", "oneOf"))
                ),
            )

    @staticmethod
    def _enum_values(schema: Mapping[str, Any]) -> Optional[list[Any]]:
        if "enum" in schema:
            return list(schema["enum"])
        properties = schema.get("properties", {})
        description = schema.get("description", "")
        if properties or schema.get("type") != "object" or not description:
            return None
        values: list[str] = []
        if re.match(r"^\d+\s+\w+", description):
            for part in re.split(r"[,\n]+", description):
                match = re.match(r"\s*\d+\s+(\w+)", part)
                if match:
                    values.append(match.group(1))
        elif re.match(r"^[A-Z_]+\s*-\s*", description):
            for part in re.split(r"[,\n]+", description):
                match = re.match(r"\s*([A-Z_]+)\s*-", part)
                if match:
                    values.append(match.group(1))
        return values or None

    def _parse_paths(self) -> None:
        for path, path_item in self.spec.get("paths", {}).items():
            for method, operation_data in path_item.items():
                if method.lower() not in _HTTP_METHODS:
                    continue
                operation_id = operation_data.get(
                    "operationId", f"{method.lower()}_{snake_case(path)}"
                )
                tags = list(operation_data.get("tags", []))
                group = classify_api_group(tags[0] if tags else "unclassified")
                parameters = self._parse_parameters(path_item, operation_data)
                request_body = self._parse_request_body(operation_data.get("requestBody"))
                responses = self._parse_responses(operation_data.get("responses", {}))
                route_kind = operation_data.get("x-route-enum", path_item.get("x-route-enum"))
                allowed_routes = operation_data.get(
                    "x-platforms-available",
                    path_item.get("x-platforms-available", []),
                )
                mutation_extension = operation_data.get("x-mutation")
                mutation_metadata = (
                    copy.deepcopy(mutation_extension)
                    if isinstance(mutation_extension, Mapping)
                    else {}
                )
                is_mutation = (
                    bool(mutation_extension)
                    if isinstance(mutation_extension, bool)
                    else method.lower() not in {"get", "head", "options"}
                )
                references: set[str] = set()
                for parameter in parameters:
                    references.update(self._collect_model_references(parameter.schema))
                if request_body:
                    references.update(self._collect_model_references(request_body.schema))
                for response in responses:
                    references.update(self._collect_model_references(response.schema))
                self.operations.append(
                    Operation(
                        operation_id=operation_id,
                        method=method.upper(),
                        path=path,
                        summary=operation_data.get("summary"),
                        description=operation_data.get("description"),
                        parameters=parameters,
                        responses=responses,
                        tags=tags,
                        security=self._parse_security(operation_data),
                        route_kind=route_kind,
                        allowed_routes=tuple(allowed_routes),
                        is_mutation=is_mutation,
                        mutation_metadata=mutation_metadata,
                        request_body=request_body,
                        game=group.game,
                        service=group.service,
                        model_references=references,
                    )
                )

    def _parse_parameters(
        self, path_item: Mapping[str, Any], operation_data: Mapping[str, Any]
    ) -> list[Parameter]:
        combined: dict[tuple[str, str], Parameter] = {}
        parameter_values = list(path_item.get("parameters", [])) + list(
            operation_data.get("parameters", [])
        )
        for raw_parameter in parameter_values:
            ref = raw_parameter.get("$ref")
            parameter = self._resolve_object(raw_parameter)
            schema = parameter.get("schema", {})
            wire_name = parameter["name"]
            location = parameter["in"]
            required = bool(parameter.get("required", False) or location == "path")
            default = parameter.get("default", schema.get("default", _MISSING))
            examples = self._examples(schema)
            examples.extend(value for value in self._examples(parameter) if value not in examples)
            combined[(wire_name, location)] = Parameter(
                name=snake_case(wire_name),
                wire_name=wire_name,
                in_=location,
                type_annotation=self._to_python_type(schema),
                required=required,
                description=parameter.get("description", schema.get("description")),
                ref=ref,
                default=default,
                constraints=self._constraints(schema),
                examples=examples,
                schema=copy.deepcopy(schema),
            )
        return sorted(
            combined.values(),
            key=lambda value: (not value.required, value.in_, value.name),
        )

    def _parse_request_body(
        self, raw_request_body: Optional[Mapping[str, Any]]
    ) -> Optional[RequestBody]:
        if not raw_request_body:
            return None
        ref = raw_request_body.get("$ref")
        request_body = self._resolve_object(raw_request_body)
        media_type, media = self._select_media(request_body.get("content", {}))
        if not media:
            return None
        schema = media.get("schema", {})
        return RequestBody(
            type_annotation=self._to_python_type(schema),
            required=bool(request_body.get("required", False)),
            description=request_body.get("description"),
            media_type=media_type,
            schema=copy.deepcopy(schema),
            ref=ref,
            examples=self._examples(media),
        )

    def _parse_responses(self, raw_responses: Mapping[str, Any]) -> list[Response]:
        responses: list[Response] = []
        for raw_status, raw_response in raw_responses.items():
            status = str(raw_status).upper()
            if not self._is_success_status(status):
                continue
            ref = raw_response.get("$ref")
            response = self._resolve_object(raw_response)
            media_type, media = self._select_media(response.get("content", {}))
            schema = media.get("schema", {}) if media else {}
            no_content = not media or status in {"204", "205"}
            responses.append(
                Response(
                    status_code=status,
                    type_annotation="None" if no_content else self._to_python_type(schema),
                    description=response.get("description"),
                    media_type=media_type if media else None,
                    schema=copy.deepcopy(schema),
                    no_content=no_content,
                    ref=ref,
                )
            )
        return sorted(responses, key=lambda value: value.status_code)

    def _parse_security(self, operation_data: Mapping[str, Any]) -> list[SecurityRequirement]:
        security = operation_data.get("security", self.spec.get("security", []))
        requirements: list[SecurityRequirement] = []
        for alternative in security:
            for scheme, scopes in alternative.items():
                requirements.append(SecurityRequirement(scheme, tuple(scopes)))
        return requirements

    def _resolve_object(self, value: Mapping[str, Any]) -> dict[str, Any]:
        if "$ref" not in value:
            return copy.deepcopy(dict(value))
        resolved = self._resolve_ref(str(value["$ref"]))
        resolved.update(copy.deepcopy({key: item for key, item in value.items() if key != "$ref"}))
        return resolved

    def _resolve_ref(self, ref: str) -> dict[str, Any]:
        if not ref.startswith("#/"):
            raise ValueError(f"Only local OpenAPI references are supported: {ref}")
        value: Any = self.spec
        for raw_part in ref[2:].split("/"):
            part = raw_part.replace("~1", "/").replace("~0", "~")
            value = value[part]
        if not isinstance(value, Mapping):
            raise TypeError(f"OpenAPI reference does not point to an object: {ref}")
        return copy.deepcopy(dict(value))

    @staticmethod
    def _select_media(content: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
        if not content:
            return "", {}
        if "application/json" in content:
            return "application/json", dict(content["application/json"])
        for media_type, media in content.items():
            if media_type.endswith("+json"):
                return media_type, dict(media)
        media_type = next(iter(content))
        return media_type, dict(content[media_type])

    @staticmethod
    def _is_success_status(status: str) -> bool:
        return bool(re.match(r"^2(?:\d\d|XX)$", status))

    @staticmethod
    def _constraints(schema: Mapping[str, Any]) -> dict[str, Any]:
        return {key: copy.deepcopy(schema[key]) for key in _CONSTRAINT_KEYS if key in schema}

    @staticmethod
    def _examples(value: Mapping[str, Any]) -> list[Any]:
        examples: list[Any] = []
        if "example" in value:
            examples.append(copy.deepcopy(value["example"]))
        raw_examples = value.get("examples")
        if isinstance(raw_examples, list):
            examples.extend(copy.deepcopy(raw_examples))
        elif isinstance(raw_examples, Mapping):
            for example in raw_examples.values():
                if isinstance(example, Mapping) and "value" in example:
                    examples.append(copy.deepcopy(example["value"]))
                elif not isinstance(example, Mapping):
                    examples.append(copy.deepcopy(example))
        return examples

    @staticmethod
    def _collect_model_references(value: Any) -> set[str]:
        references: set[str] = set()
        if isinstance(value, Mapping):
            ref = value.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
                references.add(ref.split("/")[-1])
            for nested in value.values():
                references.update(OpenApiParser._collect_model_references(nested))
        elif isinstance(value, list):
            for nested in value:
                references.update(OpenApiParser._collect_model_references(nested))
        return references

from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable, Mapping, Optional

from jinja2 import Environment, FileSystemLoader, StrictUndefined

try:
    from tools.generator.parser import (
        Model,
        OpenApiParser,
        Operation,
        python_class_name,
        snake_case,
    )
except ModuleNotFoundError:
    from parser import Model, OpenApiParser, Operation, python_class_name, snake_case

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = REPO_ROOT / "tools" / "templates"
DEFAULT_SPEC_PATH = REPO_ROOT / "spec" / "openapi.json"
PACKAGE_ROOT = Path("src") / "riotskillissue"
GENERATED_GAMES = ("common", "lol", "tft", "valorant", "lor", "riftbound")


@dataclass(frozen=True)
class ImportMetadata:
    path: str
    names: tuple[str, ...]


@dataclass
class ApiMetadata:
    game: str
    service: str
    module: str
    class_name: str
    sync_class_name: str
    operations: list[Operation]
    model_imports: list[ImportMetadata]
    typing_imports: tuple[str, ...]
    route_imports: tuple[str, ...]
    has_path_parameters: bool
    has_request_bodies: bool
    has_response_adapters: bool


@dataclass
class GameMetadata:
    name: str
    class_name: str
    sync_class_name: str
    apis: list[ApiMetadata]

    @property
    def display_name(self) -> str:
        return {
            "common": "Common",
            "lol": "League of Legends",
            "tft": "Teamfight Tactics",
            "valorant": "VALORANT",
            "lor": "Legends of Runeterra",
            "riftbound": "Riftbound",
        }[self.name]


def _method_name(operation_id: str) -> str:
    raw_name = operation_id.rsplit(".", 1)[-1]
    return snake_case(raw_name)


def _constant_name(method_name: str) -> str:
    return re.sub(r"[^A-Z0-9_]", "_", method_name.upper())


def _short_text(value: str, limit: int = 84) -> str:
    if len(value) <= limit:
        return value
    shortened = value[: limit - 1].rsplit(" ", 1)[0]
    return f"{shortened or value[: limit - 1]}…"


def _route_annotation(route_kind: Optional[str]) -> str:
    return {
        "platform": "PlatformRoute | str | None",
        "regional": "RegionalRoute | str | None",
        "val-platform": "ValorantRoute | str | None",
    }.get(route_kind or "", "str | None")


def _imports_for_references(
    references: Iterable[str],
    models: Mapping[str, Model],
    *,
    exclude_path: Optional[str] = None,
) -> list[ImportMetadata]:
    imports: dict[str, set[str]] = {}
    names: dict[str, str] = {}
    for raw_name in sorted(set(references)):
        model = models.get(raw_name)
        if model is None or model.import_path == exclude_path:
            continue
        previous_path = names.get(model.name)
        if previous_path and previous_path != model.import_path:
            raise ValueError(
                f"Model name collision for {model.name}: {previous_path} and {model.import_path}"
            )
        names[model.name] = model.import_path
        imports.setdefault(model.import_path, set()).add(model.name)
    return [
        ImportMetadata(path, tuple(sorted(import_names)))
        for path, import_names in sorted(imports.items())
    ]


def _typing_imports(
    annotations: Iterable[str],
    *,
    required: Iterable[str] = (),
) -> tuple[str, ...]:
    candidates = {"Any", "Dict", "List", "Literal", "Optional", "TypeAlias", "Union"}
    imported = set(required)
    for annotation in annotations:
        imported.update(
            candidate for candidate in candidates if re.search(rf"\b{candidate}\b", annotation)
        )
    return tuple(sorted(imported))


def _prepare_apis(parser: OpenApiParser) -> list[ApiMetadata]:
    grouped: dict[tuple[str, str], list[Operation]] = {}
    for operation in parser.operations:
        if operation.game is None or operation.service is None:
            raise ValueError(f"Operation is missing grouping metadata: {operation.operation_id}")
        grouped.setdefault((operation.game, operation.service), []).append(operation)

    apis: list[ApiMetadata] = []
    for (game, service), operations in sorted(
        grouped.items(),
        key=lambda item: (
            GENERATED_GAMES.index(item[0][0]),
            item[0][1],
        ),
    ):
        seen_names: set[str] = set()
        for operation in operations:
            method_name = _method_name(operation.operation_id)
            if method_name in seen_names:
                prefix = snake_case(operation.operation_id.split(".", 1)[0])
                method_name = f"{method_name}_{prefix}"
            if method_name in seen_names:
                raise ValueError(f"Duplicate generated method in {game}.{service}: {method_name}")
            seen_names.add(method_name)
            operation.method_name = method_name
            operation.accessor_path = f"{game}.{service}.{method_name}"
            operation.constant_name = _constant_name(method_name)
            operation.route_annotation = _route_annotation(operation.route_kind)
            operation.short_docstring = _short_text(operation.clean_docstring)

        class_name = f"{python_class_name(game)}{python_class_name(service)}Api"
        annotations = [
            annotation
            for operation in operations
            for annotation in (
                operation.response_type,
                *(parameter.annotation for parameter in operation.parameters),
                *((operation.request_body.annotation,) if operation.request_body else ()),
            )
        ]
        route_imports = {"RouteKind"}
        for operation in operations:
            route_import = {
                "platform": "PlatformRoute",
                "regional": "RegionalRoute",
                "val-platform": "ValorantRoute",
            }.get(operation.route_kind or "")
            if route_import:
                route_imports.add(route_import)
        apis.append(
            ApiMetadata(
                game=game,
                service=service,
                module=service,
                class_name=class_name,
                sync_class_name=f"Sync{class_name}",
                operations=operations,
                model_imports=_imports_for_references(
                    (
                        reference
                        for operation in operations
                        for reference in operation.model_references
                    ),
                    parser.models,
                ),
                typing_imports=_typing_imports(
                    annotations,
                    required=("Any", "Awaitable", "Callable", "cast"),
                ),
                route_imports=tuple(sorted(route_imports)),
                has_path_parameters=any(
                    parameter.in_ == "path"
                    for operation in operations
                    for parameter in operation.parameters
                ),
                has_request_bodies=any(
                    operation.request_body is not None for operation in operations
                ),
                has_response_adapters=any(
                    operation.response_adapter_type is not None for operation in operations
                ),
            )
        )
    return apis


def _prepare_games(apis: list[ApiMetadata]) -> list[GameMetadata]:
    games: list[GameMetadata] = []
    for game_name in GENERATED_GAMES:
        game_apis = [api for api in apis if api.game == game_name]
        if not game_apis:
            continue
        base_name = f"{python_class_name(game_name)}RawApi"
        games.append(
            GameMetadata(
                name=game_name,
                class_name=base_name,
                sync_class_name=f"Sync{base_name}",
                apis=game_apis,
            )
        )
    return games


def _qualified_annotation(
    annotation: str,
    references: Iterable[str],
    models: Mapping[str, Model],
) -> str:
    replacements: dict[str, str] = {}
    for raw_name in references:
        model = models.get(raw_name)
        if model is None:
            continue
        qualified_name = replacements.get(model.name)
        if qualified_name and qualified_name != model.qualified_name:
            return annotation
        replacements[model.name] = model.qualified_name
    result = annotation
    for short_name, qualified_name in sorted(
        replacements.items(), key=lambda item: len(item[0]), reverse=True
    ):
        result = re.sub(rf"\b{re.escape(short_name)}\b", qualified_name, result)
    return result


def _normalized_input_property(
    schema: Mapping[str, Any],
    *,
    wire_name: Optional[str] = None,
    location: Optional[str] = None,
    annotation: Optional[str] = None,
    description: Optional[str] = None,
    examples: Iterable[Any] = (),
) -> dict[str, Any]:
    value = copy.deepcopy(dict(schema))
    if description and "description" not in value:
        value["description"] = description
    if examples and "examples" not in value and "example" not in value:
        value["examples"] = list(examples)
    if wire_name is not None:
        value["x-wire-name"] = wire_name
    if location is not None:
        value["x-location"] = location
    if annotation is not None:
        value["x-python-type"] = annotation
    return value


def _operation_input_schema(
    operation: Operation,
    models: Mapping[str, Model],
) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    required: list[str] = []
    for parameter in operation.parameters:
        references = OpenApiParser._collect_model_references(parameter.schema)
        annotation = _qualified_annotation(
            parameter.annotation,
            references,
            models,
        )
        properties[parameter.name] = _normalized_input_property(
            parameter.schema,
            wire_name=parameter.wire_name,
            location=parameter.in_,
            annotation=annotation,
            description=parameter.description,
            examples=parameter.examples,
        )
        if parameter.required:
            required.append(parameter.name)
    if operation.request_body:
        references = OpenApiParser._collect_model_references(operation.request_body.schema)
        properties["body"] = _normalized_input_property(
            operation.request_body.schema,
            location="body",
            annotation=_qualified_annotation(
                operation.request_body.annotation,
                references,
                models,
            ),
            description=operation.request_body.description,
            examples=operation.request_body.examples,
        )
        if operation.request_body.required:
            required.append("body")
    if operation.route_kind:
        route_schema: dict[str, Any] = {
            "type": "string",
            "description": f"Optional {operation.route_kind} route override.",
            "x-route-kind": operation.route_kind,
        }
        if operation.allowed_routes:
            route_schema["enum"] = list(operation.allowed_routes)
        properties["route"] = route_schema
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def _registry_record(operation: Operation, models: Mapping[str, Model]) -> SimpleNamespace:
    response_annotation = _qualified_annotation(
        operation.response_type,
        operation.model_references,
        models,
    )
    parameters = []
    for parameter in operation.parameters:
        references = OpenApiParser._collect_model_references(parameter.schema)
        parameters.append(
            SimpleNamespace(
                name=parameter.name,
                wire_name=parameter.wire_name,
                location=parameter.in_,
                required=parameter.required,
                annotation=_qualified_annotation(
                    parameter.annotation,
                    references,
                    models,
                ),
                description=parameter.description,
                has_default=parameter.has_default,
                default=parameter.default if parameter.has_default else None,
                constraints=parameter.constraints,
                examples=tuple(parameter.examples),
                schema=parameter.schema,
            )
        )
    request_body = None
    if operation.request_body:
        references = OpenApiParser._collect_model_references(operation.request_body.schema)
        request_body = SimpleNamespace(
            required=operation.request_body.required,
            annotation=_qualified_annotation(
                operation.request_body.annotation,
                references,
                models,
            ),
            description=operation.request_body.description,
            media_type=operation.request_body.media_type,
            examples=tuple(operation.request_body.examples),
            schema=operation.request_body.schema,
        )
    return SimpleNamespace(
        operation_id=operation.operation_id,
        accessor_path=operation.accessor_path,
        source="riot_api",
        game=operation.game,
        service=operation.service,
        summary=operation.summary or operation.description,
        method=operation.method,
        path=operation.path,
        route_kind=operation.route_kind,
        allowed_routes=operation.allowed_routes,
        auth_mode=operation.auth_mode,
        auth_schemes=tuple(dict.fromkeys(requirement.scheme for requirement in operation.security)),
        auth_scopes=operation.auth_scopes,
        parameters=parameters,
        request_body=request_body,
        response_type=response_annotation,
        response_adapter=(
            response_annotation if operation.response_adapter_type is not None else None
        ),
        successful_statuses=operation.successful_statuses,
        no_content_statuses=operation.no_content_statuses,
        is_write=operation.is_mutation,
        mutation_metadata=operation.mutation_metadata,
        cache_user_scoped=operation.cache_user_scoped,
        mcp_visible=operation.mcp_visible,
        input_schema=_operation_input_schema(operation, models),
    )


def _static_records() -> list[SimpleNamespace]:
    definitions = (
        ("get_latest_version", (), "str", "Fetch the latest Data Dragon patch version."),
        (
            "get_champion",
            (("champion_key", "int", {"type": "integer"}),),
            "Optional[Dict[str, Any]]",
            "Get champion data by numeric key.",
        ),
        (
            "get_all_champions",
            (),
            "Dict[int, Dict[str, Any]]",
            "Return all champions keyed by numeric ID.",
        ),
        (
            "get_item",
            (("item_id", "int", {"type": "integer"}),),
            "Optional[Dict[str, Any]]",
            "Get item data by ID.",
        ),
        (
            "get_all_items",
            (),
            "Dict[int, Dict[str, Any]]",
            "Return all items keyed by numeric ID.",
        ),
        (
            "get_summoner_spells",
            (),
            "Dict[int, Dict[str, Any]]",
            "Return all summoner spells keyed by numeric key.",
        ),
        (
            "get_summoner_spell",
            (("spell_key", "int", {"type": "integer"}),),
            "Optional[Dict[str, Any]]",
            "Get a summoner spell by numeric key.",
        ),
        (
            "get_runes",
            (),
            "List[Dict[str, Any]]",
            "Return the full rune tree list.",
        ),
        (
            "get_queues",
            (),
            "List[Dict[str, Any]]",
            "Return queue metadata.",
        ),
        (
            "get_maps",
            (),
            "List[Dict[str, Any]]",
            "Return map metadata.",
        ),
        (
            "get_game_modes",
            (),
            "List[Dict[str, Any]]",
            "Return game mode metadata.",
        ),
    )
    records: list[SimpleNamespace] = []
    for method_name, raw_parameters, response_type, summary in definitions:
        parameters = [
            SimpleNamespace(
                name=name,
                wire_name=name,
                location="argument",
                required=True,
                annotation=annotation,
                description=None,
                has_default=False,
                default=None,
                constraints={},
                examples=(),
                schema=schema,
            )
            for name, annotation, schema in raw_parameters
        ]
        properties = {
            parameter.name: _normalized_input_property(
                parameter.schema,
                wire_name=parameter.wire_name,
                location=parameter.location,
                annotation=parameter.annotation,
            )
            for parameter in parameters
        }
        records.append(
            SimpleNamespace(
                operation_id=f"static.{method_name}",
                accessor_path=f"static.{method_name}",
                source="data_dragon",
                game="lol",
                service="static",
                summary=summary,
                method="GET",
                path=None,
                route_kind=None,
                allowed_routes=(),
                auth_mode="none",
                auth_schemes=(),
                auth_scopes=(),
                parameters=parameters,
                request_body=None,
                response_type=response_type,
                response_adapter=response_type,
                successful_statuses=(),
                no_content_statuses=(),
                is_write=False,
                mutation_metadata={},
                cache_user_scoped=False,
                mcp_visible=True,
                input_schema={
                    "type": "object",
                    "properties": properties,
                    "required": list(properties),
                    "additionalProperties": False,
                },
            )
        )
    return records


def _model_module_imports(
    models: list[Model],
    all_models: Mapping[str, Model],
) -> list[ImportMetadata]:
    if not models:
        return []
    own_path = models[0].import_path
    references = (reference for model in models for reference in model.referenced_models)
    return _imports_for_references(references, all_models, exclude_path=own_path)


def _environment() -> Environment:
    environment = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    environment.filters["pyrepr"] = repr
    environment.filters["pystring"] = _python_string
    environment.filters["pydocstring"] = lambda value: repr(_short_text(value))
    environment.filters["jsonstring"] = lambda value: _python_string(
        json.dumps(
            value,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return environment


def _python_string(value: Any, width: int = 48) -> str:
    if not isinstance(value, str):
        return repr(value)
    literal = repr(value)
    if len(literal) <= width:
        return literal
    chunk_width = width - 2
    chunks = [value[index : index + chunk_width] for index in range(0, len(value), chunk_width)]
    return "''.join((\n" + ",\n".join(repr(chunk) for chunk in chunks) + "\n))"


def _render(template: Any, **context: Any) -> str:
    return template.render(**context).rstrip() + "\n"


def _format_generated_files(files: Mapping[Path, str]) -> dict[Path, str]:
    executable = shutil.which("ruff")
    if executable is None:
        raise RuntimeError("Ruff is required to format generated sources")
    with tempfile.TemporaryDirectory(prefix="riotskillissue-generator-") as raw_directory:
        directory = Path(raw_directory)
        for relative_path, content in files.items():
            path = directory / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        result = subprocess.run(
            [executable, "format", str(directory)],
            capture_output=True,
            check=False,
            text=True,
        )
        if result.returncode:
            raise RuntimeError(result.stderr or result.stdout)
        return {
            relative_path: (directory / relative_path).read_text(encoding="utf-8")
            for relative_path in files
        }


def render_generated_files(
    spec: Mapping[str, Any],
    *,
    format_code: bool = True,
) -> dict[Path, str]:
    parser = OpenApiParser(spec)
    parser.parse()
    apis = _prepare_apis(parser)
    games = _prepare_games(apis)
    environment = _environment()
    files: dict[Path, str] = {}

    model_template = environment.get_template("models.py.j2")
    grouped_models: dict[tuple[str, str], list[Model]] = {}
    for model in parser.models.values():
        grouped_models.setdefault((model.game, model.module), []).append(model)
    for (game, module), models in sorted(grouped_models.items()):
        model_annotations = [
            property_value.annotation for model in models for property_value in model.properties
        ]
        if any(model.enum_values is not None for model in models):
            model_annotations.extend(("Literal", "TypeAlias"))
        files[PACKAGE_ROOT / "models" / game / f"{module}.py"] = _render(
            model_template,
            models=models,
            model_imports=_model_module_imports(models, parser.models),
            typing_imports=_typing_imports(model_annotations),
            has_model_classes=any(model.enum_values is None for model in models),
            has_model_properties=any(model.properties for model in models),
        )
    for game in GENERATED_GAMES:
        modules = sorted(module for model_game, module in grouped_models if model_game == game)
        if modules:
            imports = "\n".join(f"from . import {module}" for module in modules)
            exported = ", ".join(repr(module) for module in modules)
            files[PACKAGE_ROOT / "models" / game / "__init__.py"] = (
                f"{imports}\n\n__all__ = [{exported}]\n"
            )

    endpoint_template = environment.get_template("endpoints.py.j2")
    for api in apis:
        files[PACKAGE_ROOT / "api" / "raw" / api.game / f"{api.module}.py"] = _render(
            endpoint_template,
            class_name=api.class_name,
            sync_class_name=api.sync_class_name,
            operations=api.operations,
            model_imports=api.model_imports,
            typing_imports=api.typing_imports,
            route_imports=api.route_imports,
            has_path_parameters=api.has_path_parameters,
            has_request_bodies=api.has_request_bodies,
            has_response_adapters=api.has_response_adapters,
        )
    for game in games:
        imports = "\n".join(
            (f"from .{api.module} import {api.class_name}, {api.sync_class_name}")
            for api in game.apis
        )
        exported_names = [
            name for api in game.apis for name in (api.class_name, api.sync_class_name)
        ]
        exported = ", ".join(repr(name) for name in exported_names)
        files[PACKAGE_ROOT / "api" / "raw" / game.name / "__init__.py"] = (
            f"{imports}\n\n__all__ = [{exported}]\n"
        )

    raw_template = environment.get_template("raw_client.py.j2")
    files[PACKAGE_ROOT / "api" / "raw" / "_client.py"] = _render(
        raw_template,
        apis=apis,
        games=games,
    )
    files[PACKAGE_ROOT / "api" / "raw" / "__init__.py"] = (
        "from ._client import GeneratedRawClient, SyncGeneratedRawClient\n\n"
        '__all__ = ["GeneratedRawClient", "SyncGeneratedRawClient"]\n'
    )

    registry_template = environment.get_template("registry.py.j2")
    records = [_registry_record(operation, parser.models) for operation in parser.operations]
    static_records = _static_records()
    records.extend(static_records)
    files[PACKAGE_ROOT / "api" / "registry.py"] = _render(
        registry_template,
        records=records,
    )
    files[PACKAGE_ROOT / "api" / "operations.py"] = (
        "from .registry import (\n"
        "    OPERATION_REGISTRY,\n"
        "    OperationRegistry,\n"
        "    OperationSpec,\n"
        "    ParameterSpec,\n"
        "    RequestBodySpec,\n"
        ")\n\n"
        "__all__ = [\n"
        '    "OPERATION_REGISTRY",\n'
        '    "OperationRegistry",\n'
        '    "OperationSpec",\n'
        '    "ParameterSpec",\n'
        '    "RequestBodySpec",\n'
        "]\n"
    )

    mixin_template = environment.get_template("client_mixin.py.j2")
    files[PACKAGE_ROOT / "api" / "client_mixin.py"] = _render(mixin_template)
    api_reference_template = environment.get_template("api_reference.md.j2")
    files[Path("docs") / "api-reference.md"] = _render(
        api_reference_template,
        games=games,
        static_records=static_records,
    )
    return _format_generated_files(files) if format_code else files


def _managed_roots(repo_root: Path) -> tuple[Path, ...]:
    package_root = repo_root / PACKAGE_ROOT
    return (
        package_root / "api" / "raw",
        *(package_root / "models" / game for game in GENERATED_GAMES),
    )


def _legacy_generated_paths(repo_root: Path) -> tuple[Path, ...]:
    package_root = repo_root / PACKAGE_ROOT
    return (
        package_root / "api" / "endpoints",
        package_root / "api" / "models.py",
    )


def _assert_scoped(path: Path, repo_root: Path) -> None:
    resolved = path.resolve()
    package_root = (repo_root / PACKAGE_ROOT).resolve()
    api_reference = (repo_root / "docs" / "api-reference.md").resolve()
    if not resolved.is_relative_to(package_root) and resolved != api_reference:
        raise ValueError(f"Generated path escapes the package root: {resolved}")


def write_generated_files(files: Mapping[Path, str], repo_root: Path = REPO_ROOT) -> None:
    for root in _managed_roots(repo_root):
        _assert_scoped(root, repo_root)
        if root.exists():
            shutil.rmtree(root)
    for legacy_path in _legacy_generated_paths(repo_root):
        _assert_scoped(legacy_path, repo_root)
        if legacy_path.is_dir():
            shutil.rmtree(legacy_path)
        elif legacy_path.exists():
            legacy_path.unlink()
    for relative_path, content in files.items():
        path = repo_root / relative_path
        _assert_scoped(path, repo_root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")


def check_generated_files(
    files: Mapping[Path, str],
    repo_root: Path = REPO_ROOT,
) -> list[str]:
    differences: list[str] = []
    expected_paths = {(repo_root / relative_path).resolve() for relative_path in files}
    for relative_path, expected in files.items():
        path = repo_root / relative_path
        if not path.exists():
            differences.append(f"missing: {relative_path.as_posix()}")
            continue
        actual = path.read_text(encoding="utf-8")
        if actual != expected:
            differences.append(f"changed: {relative_path.as_posix()}")
    for root in _managed_roots(repo_root):
        if not root.exists():
            continue
        for actual_path in root.rglob("*.py"):
            if actual_path.resolve() not in expected_paths:
                differences.append(f"stale: {actual_path.relative_to(repo_root).as_posix()}")
    for legacy_path in _legacy_generated_paths(repo_root):
        if legacy_path.exists():
            differences.append(f"legacy: {legacy_path.relative_to(repo_root).as_posix()}")
    return differences


def load_spec(path: Path = DEFAULT_SPEC_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as spec_file:
        return json.load(spec_file)


def generate(
    spec_path: Path = DEFAULT_SPEC_PATH,
    *,
    check: bool = False,
    repo_root: Path = REPO_ROOT,
) -> int:
    spec = load_spec(spec_path)
    files = render_generated_files(spec)
    if check:
        differences = check_generated_files(files, repo_root)
        if differences:
            print("\n".join(differences))
            return 1
        print(f"Generated contract is current ({len(files)} files).")
        return 0
    write_generated_files(files, repo_root)
    print(f"Generated {len(files)} files.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC_PATH)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    return generate(arguments.spec, check=arguments.check)


if __name__ == "__main__":
    raise SystemExit(main())

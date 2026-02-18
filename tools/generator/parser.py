import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class Property:
    name: str  # The python attribute name
    type_annotation: str
    description: Optional[str] = None
    required: bool = False
    alias: Optional[str] = None  # The JSON key


@dataclass
class Model:
    name: str
    properties: List[Property]
    description: Optional[str] = None
    enum_values: Optional[List[str]] = None


@dataclass
class Parameter:
    name: str
    in_: str  # query, path, header
    type_annotation: str
    required: bool
    description: Optional[str]


@dataclass
class Operation:
    operation_id: str
    method: str
    path: str
    summary: Optional[str]
    parameters: List[Parameter]
    response_type: str
    tags: List[str]
    method_name: Optional[str] = None
    request_body: bool = False
    request_body_type: str = "Any"

    @property
    def clean_docstring(self) -> str:
        return (self.summary or "").replace("\n", " ")

class OpenApiParser:
    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.models: Dict[str, Model] = {}
        self.operations: List[Operation] = []
        self._type_mapping = {
            "integer": "int",
            "string": "str",
            "boolean": "bool",
            "number": "float",
            "array": "list",
            "object": "dict"
        }

    def parse(self):
        self._parse_components()
        self._parse_paths()

    def _to_python_type(self, schema: Dict[str, Any]) -> str:
        if "$ref" in schema:
            raw = schema["$ref"].split("/")[-1]
            return self._sanitize_name(raw)
        
        t = schema.get("type", "any")
        if t == "array":
            items = schema.get("items", {})
            inner = self._to_python_type(items)
            return f"List[{inner}]"
        
        if t == "object":
            # Check for map (additionalProperties)
            if "additionalProperties" in schema:
                val_type = self._to_python_type(schema["additionalProperties"])
                return f"Dict[str, {val_type}]"
            return "Dict[str, Any]"
            
        return self._type_mapping.get(t, "Any")

    def _sanitize_name(self, name: str) -> str:
        # "account-v1.AccountDto" -> "AccountV1AccountDto" is one option
        # Or simpler: replace . and - with _
        return name.replace(".", "_").replace("-", "_")

    def _sanitize_attr_name(self, name: str) -> str:
        # Replace invalid chars
        name = name.replace("-", "_").replace(".", "_")
        
        # If starts with digit, prepend param_ (Pydantic dislikes leading _)
        if name[0].isdigit():
            return f"param_{name}"
        # If keyword, append _
        keywords = {"class", "def", "if", "else", "return", "from", "import", "in", "is", "pass", "None", "True", "False"}
        if name in keywords:
            return f"{name}_"
        return name

    def _parse_components(self):
        schemas = self.spec.get("components", {}).get("schemas", {})
        for raw_name, schema in schemas.items():
            name = self._sanitize_name(raw_name)

            # Detect explicit enum
            if "enum" in schema:
                self.models[name] = Model(
                    name=name,
                    properties=[],
                    enum_values=schema["enum"],
                    description=schema.get("description"),
                )
                continue

            # Detect description-based enums: empty object with listed values
            # Pattern 1: "0 NONE,\n1 IRON, ..." (numbered)
            # Pattern 2: "DISABLED - desc,\nHIDDEN - desc, ..." (named with description)
            props_raw = schema.get("properties", {})
            desc = schema.get("description", "")
            if (
                not props_raw
                and desc
                and schema.get("type") == "object"
            ):
                values: List[str] = []
                # Pattern 1: numbered values "0 NONE, 1 IRON, ..."
                if re.match(r"^\d+\s+\w+", desc):
                    for part in re.split(r"[,\n]+", desc):
                        part = part.strip()
                        m = re.match(r"\d+\s+(\w+)", part)
                        if m:
                            values.append(m.group(1))
                # Pattern 2: "WORD - description" per line/comma
                elif re.match(r"^[A-Z_]+\s*-\s*", desc):
                    for part in re.split(r"[,\n]+", desc):
                        part = part.strip()
                        m = re.match(r"([A-Z_]+)\s*-", part)
                        if m:
                            values.append(m.group(1))

                if values:
                    self.models[name] = Model(
                        name=name,
                        properties=[],
                        enum_values=values,
                        description=desc,
                    )
                    continue

            props = []
            required = set(schema.get("required", []))
            for prop_name, prop_schema in props_raw.items():
                py_type = self._to_python_type(prop_schema)
                sanitized_name = self._sanitize_attr_name(prop_name)

                props.append(
                    Property(
                        name=sanitized_name,
                        type_annotation=py_type,
                        required=prop_name in required,
                        description=prop_schema.get("description"),
                        alias=prop_name,
                    )
                )

            self.models[name] = Model(
                name=name,
                properties=props,
                description=schema.get("description"),
            )

    def _parse_paths(self):
        for path, item in self.spec.get("paths", {}).items():
            for method, op in item.items():
                if method not in ["get", "post", "put", "delete"]:
                    continue

                op_id = op.get("operationId", f"{method}_{path}")
                params = []

                # Combine path level and op level params
                all_params = item.get("parameters", []) + op.get("parameters", [])

                for p in all_params:
                    # Resolve ref if needed (simplified)
                    if "$ref" in p:
                        continue

                    p_name = p["name"]
                    p_in = p["in"]
                    p_req = p.get("required", False)
                    p_type = self._to_python_type(p.get("schema", {}))

                    params.append(
                        Parameter(
                            name=p_name,
                            in_=p_in,
                            type_annotation=p_type,
                            required=p_req,
                            description=p.get("description"),
                        )
                    )

                # Sort params: required first
                params.sort(key=lambda x: (not x.required, x.name))

                # Determine response type (200)
                try:
                    resp_schema = op["responses"]["200"]["content"]["application/json"][
                        "schema"
                    ]
                    resp_type = self._to_python_type(resp_schema)
                except KeyError:
                    resp_type = "None"

                # Determine request body
                has_body = False
                body_type = "Any"
                req_body = op.get("requestBody", {})
                if req_body:
                    content = req_body.get("content", {})
                    json_content = content.get("application/json", {})
                    body_schema = json_content.get("schema", {})
                    if body_schema:
                        has_body = True
                        body_type = self._to_python_type(body_schema)

                self.operations.append(
                    Operation(
                        operation_id=op_id,
                        method=method.upper(),
                        path=path,
                        summary=op.get("summary"),
                        parameters=params,
                        response_type=resp_type,
                        tags=op.get("tags", []),
                        request_body=has_body,
                        request_body_type=body_type,
                    )
                )

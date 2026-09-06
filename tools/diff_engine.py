import json
from dataclasses import dataclass, field
from typing import Any


def _display(value: Any) -> str:
    rendered = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return rendered if len(rendered) <= 240 else rendered[:237] + "..."


def _changes(old: Any, new: Any, prefix: str = "") -> list[str]:
    if json.dumps(old, sort_keys=True) == json.dumps(new, sort_keys=True):
        return []
    if isinstance(old, dict) and isinstance(new, dict):
        changes = []
        for key in sorted(old.keys() | new.keys()):
            location = f"{prefix}.{key}" if prefix else key
            if key not in old:
                changes.append(f"Added {location}: {_display(new[key])}")
            elif key not in new:
                changes.append(f"Removed {location}: {_display(old[key])}")
            else:
                changes.extend(_changes(old[key], new[key], location))
        return changes
    if isinstance(old, list) and isinstance(new, list):
        changes = []
        for index in range(max(len(old), len(new))):
            location = f"{prefix}[{index}]"
            if index >= len(old):
                changes.append(f"Added {location}: {_display(new[index])}")
            elif index >= len(new):
                changes.append(f"Removed {location}: {_display(old[index])}")
            else:
                changes.extend(_changes(old[index], new[index], location))
        return changes
    return [f"{prefix}: {_display(old)} -> {_display(new)}"]


@dataclass
class SchemaDiff:
    added_endpoints: list[str] = field(default_factory=list)
    removed_endpoints: list[str] = field(default_factory=list)
    modified_endpoints: dict[str, list[str]] = field(default_factory=dict)
    added_schemas: list[str] = field(default_factory=list)
    removed_schemas: list[str] = field(default_factory=list)
    modified_schemas: dict[str, list[str]] = field(default_factory=dict)
    other_changes: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = ["# Schema Changes Report", ""]
        for title, names in (
            ("Added Endpoints", self.added_endpoints),
            ("Removed Endpoints", self.removed_endpoints),
            ("Added Models", self.added_schemas),
            ("Removed Models", self.removed_schemas),
        ):
            if names:
                lines.extend([f"## {title}", *(f"- {name}" for name in names), ""])
        for title, modified in (
            ("Modified Endpoints", self.modified_endpoints),
            ("Modified Models", self.modified_schemas),
        ):
            if modified:
                lines.append(f"## {title}")
                for name, changes in modified.items():
                    lines.append(f"- **{name}**")
                    lines.extend(f"  - {change}" for change in changes)
                lines.append("")
        if self.other_changes:
            lines.extend(["## Other Changes", *(f"- {c}" for c in self.other_changes), ""])
        return "\n".join(lines) if len(lines) > 2 else "# No Changes"


class DiffEngine:
    def compare(self, old: dict[str, Any], new: dict[str, Any]) -> SchemaDiff:
        diff = SchemaDiff()
        old_paths, new_paths = old.get("paths", {}), new.get("paths", {})
        diff.added_endpoints = sorted(new_paths.keys() - old_paths.keys())
        diff.removed_endpoints = sorted(old_paths.keys() - new_paths.keys())
        for path in sorted(old_paths.keys() & new_paths.keys()):
            if changes := _changes(old_paths[path], new_paths[path]):
                diff.modified_endpoints[path] = changes

        old_schemas = old.get("components", {}).get("schemas", {})
        new_schemas = new.get("components", {}).get("schemas", {})
        diff.added_schemas = sorted(new_schemas.keys() - old_schemas.keys())
        diff.removed_schemas = sorted(old_schemas.keys() - new_schemas.keys())
        for name in sorted(old_schemas.keys() & new_schemas.keys()):
            if changes := _changes(old_schemas[name], new_schemas[name]):
                diff.modified_schemas[name] = changes

        def remaining(spec: dict[str, Any]) -> dict[str, Any]:
            return {
                **{k: v for k, v in spec.items() if k not in {"paths", "components"}},
                "components": {
                    k: v for k, v in spec.get("components", {}).items() if k != "schemas"
                },
            }

        diff.other_changes = _changes(remaining(old), remaining(new))
        return diff

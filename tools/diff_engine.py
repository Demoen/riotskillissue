from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Optional
import json

@dataclass
class SchemaDiff:
    added_endpoints: List[str] = field(default_factory=list)
    removed_endpoints: List[str] = field(default_factory=list)
    modified_endpoints: Dict[str, List[str]] = field(default_factory=dict)
    
    added_schemas: List[str] = field(default_factory=list)
    removed_schemas: List[str] = field(default_factory=list)
    modified_schemas: Dict[str, List[str]] = field(default_factory=dict)

    def to_markdown(self) -> str:
        lines = ["# Schema Changes Report", ""]
        
        if self.added_endpoints:
            lines.append("## 🟢 Added Endpoints")
            for ep in self.added_endpoints:
                lines.append(f"- `{ep}`")
            lines.append("")
            
        if self.removed_endpoints:
            lines.append("## 🔴 Removed Endpoints")
            for ep in self.removed_endpoints:
                lines.append(f"- `{ep}`")
            lines.append("")

        if self.modified_endpoints:
            lines.append("## 🟡 Modified Endpoints")
            for ep, changes in self.modified_endpoints.items():
                lines.append(f"- **{ep}**")
                for c in changes:
                    lines.append(f"  - {c}")
            lines.append("")

        if self.added_schemas:
            lines.append("## 🟢 Added Models")
            lines.extend([f"- `{s}`" for s in self.added_schemas])
            lines.append("")
            
        if self.removed_schemas:
            lines.append("## 🔴 Removed Models")
            lines.extend([f"- `{s}`" for s in self.removed_schemas])
            lines.append("")
            
        if self.modified_schemas:
            lines.append("## 🟡 Modified Models")
            for s, changes in self.modified_schemas.items():
                lines.append(f"- **{s}**")
                for c in changes:
                    lines.append(f"  - {c}")
        
        if len(lines) == 2:
            return "# No Significant Changes"
            
        return "\n".join(lines)

class DiffEngine:
    """Compares two OpenAPI specs."""
    
    def compare(self, old: Dict[str, Any], new: Dict[str, Any]) -> SchemaDiff:
        diff = SchemaDiff()
        
        # 1. Compare Endpoints (Paths)
        old_paths = set(old.get("paths", {}).keys())
        new_paths = set(new.get("paths", {}).keys())
        
        diff.added_endpoints = sorted(list(new_paths - old_paths))
        diff.removed_endpoints = sorted(list(old_paths - new_paths))
        
        common_paths = old_paths & new_paths
        for path in common_paths:
            self._compare_path_items(path, old["paths"][path], new["paths"][path], diff)

        # 2. Compare Components/Schemas
        old_schemas = set(old.get("components", {}).get("schemas", {}).keys())
        new_schemas = set(new.get("components", {}).get("schemas", {}).keys())
        
        diff.added_schemas = sorted(list(new_schemas - old_schemas))
        diff.removed_schemas = sorted(list(old_schemas - new_schemas))
        
        common_schemas = old_schemas & new_schemas
        for schema in common_schemas:
            self._compare_schemas(
                schema, 
                old["components"]["schemas"][schema], 
                new["components"]["schemas"][schema], 
                diff
            )
            
        return diff

    def _compare_path_items(self, path: str, old: Dict, new: Dict, diff: SchemaDiff) -> None:
        # Check methods (get, post)
        old_methods = set(k for k in old if k not in ["parameters", "summary", "description"])
        new_methods = set(k for k in new if k not in ["parameters", "summary", "description"])
        
        changes = []
        
        # New/Removed methods
        added = new_methods - old_methods
        removed = old_methods - new_methods
        if added: changes.append(f"Added methods: {added}")
        if removed: changes.append(f"Removed methods: {removed}")
        
        # Check params/return types for common methods
        for method in old_methods & new_methods:
            # Simplified check: just hash equality of operation object or check parameters length
            # A full check is very complex, we catch high level here
            old_op = old[method]
            new_op = new[method]
            
            # Check params
            old_params = {p["name"]: p for p in old_op.get("parameters", [])}
            new_params = {p["name"]: p for p in new_op.get("parameters", [])}
            
            p_added = set(new_params) - set(old_params)
            p_removed = set(old_params) - set(new_params)
            
            if p_added: changes.append(f"[{method}] Added params: {p_added}")
            if p_removed: changes.append(f"[{method}] Removed params: {p_removed}")
            
        if changes:
            diff.modified_endpoints[path] = changes

    def _compare_schemas(self, name: str, old: Dict, new: Dict, diff: SchemaDiff) -> None:
        changes = []
        
        # Check properties
        old_props = set(old.get("properties", {}).keys())
        new_props = set(new.get("properties", {}).keys())
        
        added = new_props - old_props
        removed = old_props - new_props
        
        if added: changes.append(f"Added fields: {added}")
        if removed: changes.append(f"Removed fields: {removed}")
        
        # Check Enums
        if "enum" in old or "enum" in new:
            old_enum = set(old.get("enum", []))
            new_enum = set(new.get("enum", []))
            if old_enum != new_enum:
                changes.append(f"Enum changed: +{new_enum - old_enum} -{old_enum - new_enum}")

        if changes:
            diff.modified_schemas[name] = changes

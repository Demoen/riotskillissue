import json
import os
import shutil
import sys
import re
from pathlib import Path
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader

# Add repo root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from tools.generator.parser import OpenApiParser, Operation

TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
OUTPUT_DIR = Path("src/riotskillissue/api")


def group_operations_by_tag(ops: List[Operation]) -> Dict[str, List[Operation]]:
    groups: Dict[str, List[Operation]] = {}
    for op in ops:
        # Riot tags are usually "Summoner-V4" -> We want "summoner"
        if not op.tags:
            tag = "unclassified"
        else:
            tag = op.tags[0]
            # Strip version suffix: "summoner-v4" -> "summoner"
            if "-" in tag:
                parts = tag.split("-")
                if parts[-1].lower().startswith("v") and parts[-1][1:].isdigit():
                    tag = "-".join(parts[:-1])

        tag = tag.lower().replace(" ", "_").replace("-", "_")
        groups.setdefault(tag, []).append(op)
    return groups


def generate():
    print("Loading spec...")
    with open("spec/openapi.json", "r", encoding="utf-8") as f:
        spec = json.load(f)

    parser = OpenApiParser(spec)
    parser.parse()
    print(f"Parsed {len(parser.models)} models.")
    print(f"Parsed {len(parser.operations)} operations.")

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    # 1. Generate Models
    print("Generating models...")
    model_template = env.get_template("models.py.j2")
    models_code = model_template.render(models=parser.models.values())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / "models.py", "w", encoding="utf-8") as f:
        f.write(models_code)

    # 2. Generate Endpoints
    # Clean endpoints directory first to remove stale files
    endpoints_dir = OUTPUT_DIR / "endpoints"
    if endpoints_dir.exists():
        shutil.rmtree(endpoints_dir)
    endpoints_dir.mkdir(exist_ok=True)

    print("Generating endpoints...")
    groups = group_operations_by_tag(parser.operations)
    apis_metadata = []

    for tag, ops in groups.items():
        if not tag:
            continue

        # Build class name: "match" -> "MatchApi", "tft_match" -> "TftMatchApi"
        class_name = "".join(part.capitalize() for part in tag.split("_")) + "Api"
        filename = tag

        # Enforce method name uniqueness per class
        seen_methods: set[str] = set()
        unique_ops: List[Operation] = []
        for op in ops:
            # Simple heuristic for method name
            # opId is like "summoner-v4.getBySummonerName"
            # we want "get_by_summoner_name"
            if "." in op.operation_id:
                raw_name = op.operation_id.split(".")[-1]
            else:
                raw_name = op.operation_id

            # snake_case with acronym handling
            name = raw_name
            name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
            name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
            name = name.lower().replace("-", "_").replace(".", "_")

            if name in seen_methods:
                name = f"{name}_{op.operation_id.split('.')[0]}"

            seen_methods.add(name)
            op.method_name = name
            unique_ops.append(op)

        template = env.get_template("endpoints.py.j2")
        code = template.render(class_name=class_name, operations=unique_ops)

        with open(endpoints_dir / f"{filename}.py", "w", encoding="utf-8") as f:
            f.write(code)

        apis_metadata.append(
            {
                "filename": filename,
                "class_name": class_name,
                "accessor_name": tag,
            }
        )

    # 3. Generate Client Mixin
    print("Generating client mixin...")
    mixin_template = env.get_template("client_mixin.py.j2")
    mixin_code = mixin_template.render(apis=apis_metadata)

    with open(OUTPUT_DIR / "client_mixin.py", "w", encoding="utf-8") as f:
        f.write(mixin_code)

    # 4. Generate Init
    with open(OUTPUT_DIR / "__init__.py", "w", encoding="utf-8") as f:
        f.write("")

    print("Done.")


if __name__ == "__main__":
    generate()

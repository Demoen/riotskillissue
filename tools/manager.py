import argparse
import hashlib
import json
import logging
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.diff_engine import DiffEngine

SPEC_URL = "https://mingweisamuel.com/riotapi-schema/openapi-3.0.0.json"
UPSTREAM_RUNS_URL = (
    "https://api.github.com/repos/MingweiSamuel/riotapi-schema/actions/workflows/ci.yml/runs"
)
REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC_FILE = REPO_ROOT / "spec" / "openapi.json"
REPORT_DIR = REPO_ROOT / "reports"
HTTP_METHODS = {"delete", "get", "head", "options", "patch", "post", "put", "trace"}
logger = logging.getLogger("spec-manager")


def validate_spec(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or not str(data.get("openapi", "")).startswith("3.0."):
        raise ValueError("Expected an OpenAPI 3.0 document from the schema feed")
    paths = data.get("paths")
    components = data.get("components")
    schemas = components.get("schemas") if isinstance(components, dict) else None
    if not isinstance(paths, dict) or not paths or not isinstance(schemas, dict) or not schemas:
        raise ValueError("Schema feed must contain nonempty paths and component schemas")
    operation_ids = set()
    for path, item in paths.items():
        if not path.startswith("/") or not isinstance(item, dict):
            raise ValueError(f"Invalid path item: {path}")
        for method in item.keys() & HTTP_METHODS:
            operation = item[method]
            if (
                not isinstance(operation, dict)
                or not isinstance(operation.get("responses"), dict)
                or not operation["responses"]
            ):
                raise ValueError(f"Invalid operation: {method.upper()} {path}")
            operation_id = operation.get("operationId")
            if not isinstance(operation_id, str) or not operation_id:
                raise ValueError(f"Missing operationId: {method.upper()} {path}")
            if operation_id in operation_ids:
                raise ValueError(f"Duplicate operationId: {operation_id}")
            operation_ids.add(operation_id)
    if not operation_ids:
        raise ValueError("Schema feed contains no operations")
    return data


def fetch_spec() -> dict[str, Any]:
    logger.info("Fetching spec from %s", SPEC_URL)
    with httpx.Client(
        transport=httpx.HTTPTransport(retries=2), timeout=30, follow_redirects=True
    ) as client:
        response = client.get(SPEC_URL, headers={"Cache-Control": "no-cache"})
        response.raise_for_status()
        return validate_spec(response.json())


def check_upstream() -> str:
    headers = {"Accept": "application/vnd.github+json"}
    if token := os.environ.get("GH_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    response = httpx.get(
        UPSTREAM_RUNS_URL,
        params={"branch": "master", "event": "schedule", "status": "success", "per_page": 1},
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    runs = response.json().get("workflow_runs", [])
    if not runs:
        raise ValueError("Upstream schema generator has no successful scheduled run")
    run = runs[0]
    observed_at = datetime.fromisoformat(run["created_at"].replace("Z", "+00:00"))
    age = datetime.now(UTC) - observed_at
    if age > timedelta(hours=72):
        raise ValueError(
            f"Upstream schema generator has not succeeded in 72 hours: {run['html_url']}"
        )
    return f"[Successful upstream generation]({run['html_url']}) ({observed_at.isoformat()})"


def save_spec(data: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    try:
        temporary.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def sync_spec(*, check: bool = False, verify_upstream: bool = False) -> int:
    upstream = check_upstream() if verify_upstream else "Upstream workflow not checked."
    new_spec = fetch_spec()
    old_spec = json.loads(SPEC_FILE.read_text(encoding="utf-8")) if SPEC_FILE.exists() else None
    canonical = json.dumps(new_spec, sort_keys=True)
    changed = json.dumps(old_spec, sort_keys=True) != canonical
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    operation_count = sum(len(item.keys() & HTTP_METHODS) for item in new_spec["paths"].values())
    summary = (
        "# SDK Source Check\n\n"
        f"- Checked at: {datetime.now(UTC).isoformat()}\n"
        f"- Source: {SPEC_URL}\n"
        f"- {upstream}\n"
        f"- SHA-256: {digest}\n"
        f"- Coverage: {len(new_spec['paths'])} paths, {operation_count} operations, "
        f"{len(new_spec['components']['schemas'])} models\n"
        f"- Bundled spec: {'DIFFERS from feed' if changed else 'matches feed'}\n\n"
    )
    report_path = None
    if changed:
        report = DiffEngine().compare(old_spec or {}, new_spec).to_markdown()
        summary += report + "\n"
        if not check:
            REPORT_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S_%f")
            report_path = REPORT_DIR / f"diff_{timestamp}.md"
            report_path.write_text(report + "\n", encoding="utf-8")
            save_spec(new_spec, SPEC_FILE)
    logger.info("Spec %s.", "has changed" if changed else "is unchanged")
    print(summary)
    if summary_path := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary_path, "a", encoding="utf-8") as stream:
            stream.write(summary)
    if output_path := os.environ.get("GITHUB_OUTPUT"):
        with open(output_path, "a", encoding="utf-8") as stream:
            stream.write(f"spec_changed={str(changed).lower()}\n")
            stream.write(f"spec_sha256={digest}\n")
            if report_path:
                stream.write(f"diff_report_path={report_path.as_posix()}\n")
    return int(check and changed)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or update the bundled Riot API schema.")
    parser.add_argument("--check", action="store_true", help="Report drift without modifying files")
    parser.add_argument(
        "--check-upstream",
        action="store_true",
        help="Require successful upstream CI within 72 hours",
    )
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    return sync_spec(check=arguments.check, verify_upstream=arguments.check_upstream)


if __name__ == "__main__":
    raise SystemExit(main())

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import httpx
# Handle both ways of running: as module or script
sys.path.append(str(Path(__file__).parent.parent))

from tools.diff_engine import DiffEngine, SchemaDiff

SPEC_URL = "https://mingweisamuel.com/riotapi-schema/openapi-3.0.0.json"
SPEC_DIR = Path("spec")
SPEC_FILE = SPEC_DIR / "openapi.json"
REPORT_DIR = Path("reports")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("spec-manager")

def fetch_spec() -> dict:
    logger.info(f"Fetching spec from {SPEC_URL}...")
    resp = httpx.get(SPEC_URL, follow_redirects=True)
    resp.raise_for_status()
    return resp.json()

def save_spec(data: dict, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    logger.info(f"Saved spec to {path}")

def main():
    SPEC_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    new_spec = fetch_spec()
    
    if not SPEC_FILE.exists():
        logger.info("No existing spec found. Saving new spec.")
        save_spec(new_spec, SPEC_FILE)
        return

    with open(SPEC_FILE, "r", encoding="utf-8") as f:
        old_spec = json.load(f)

    # Simple equality check first
    if json.dumps(old_spec, sort_keys=True) == json.dumps(new_spec, sort_keys=True):
        logger.info("Spec is unchanged.")
        return

    logger.info("Changes detected. Running diff engine...")
    engine = DiffEngine()
    diff = engine.compare(old_spec, new_spec)
    
    report_md = diff.to_markdown()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"diff_{timestamp}.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
        
    logger.info(f"Diff report saved to {report_path}")
    
    # Save new spec
    save_spec(new_spec, SPEC_FILE)
    
    # Emit a GITHUB_OUTPUT or summary if in CI
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(report_md)

if __name__ == "__main__":
    main()

import json
import sys
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from importlib import import_module
from pathlib import Path

import httpx
import pytest

_REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, _REPO_ROOT)
try:
    manager = import_module("tools.manager")
finally:
    sys.path.remove(_REPO_ROOT)


@pytest.fixture
def spec():
    return {
        "openapi": "3.0.0",
        "info": {"title": "Riot API", "version": "1"},
        "paths": {"/items": {"get": {
            "operationId": "items.get",
            "responses": {"200": {"description": "OK"}},
        }}},
        "components": {"schemas": {"Item": {"type": "object"}}},
    }


@pytest.fixture
def workspace(monkeypatch, tmp_path, spec):
    spec_file = tmp_path / "spec" / "openapi.json"
    manager.save_spec(spec, spec_file)
    monkeypatch.setattr(manager, "SPEC_FILE", spec_file)
    monkeypatch.setattr(manager, "REPORT_DIR", tmp_path / "reports")
    monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path / "output"))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(tmp_path / "summary"))
    return tmp_path


def test_unchanged_check_emits_health_summary_without_rewriting_spec(
    workspace, spec, respx_mock,
):
    respx_mock.get(manager.SPEC_URL).respond(200, json=spec)
    before = manager.SPEC_FILE.stat().st_mtime_ns

    assert manager.sync_spec(check=True) == 0

    assert manager.SPEC_FILE.stat().st_mtime_ns == before
    assert not manager.REPORT_DIR.exists()
    assert "spec_changed=false" in (workspace / "output").read_text()
    summary = (workspace / "summary").read_text()
    assert "1 paths, 1 operations, 1 models" in summary
    assert "matches feed" in summary
    assert "SHA-256:" in summary


@pytest.mark.parametrize("missing", [False, True])
def test_check_detects_drift_without_modifying_snapshot(workspace, spec, respx_mock, missing):
    if missing:
        manager.SPEC_FILE.unlink()
    before = manager.SPEC_FILE.read_bytes() if not missing else None
    spec["paths"]["/items"]["get"]["deprecated"] = True
    respx_mock.get(manager.SPEC_URL).respond(200, json=spec)

    assert manager.sync_spec(check=True) == 1

    if missing:
        assert not manager.SPEC_FILE.exists()
    else:
        assert manager.SPEC_FILE.read_bytes() == before
    assert not manager.REPORT_DIR.exists()
    assert "spec_changed=true" in (workspace / "output").read_text()


def test_update_persists_report_and_new_snapshot(workspace, spec, respx_mock):
    spec["components"]["schemas"]["Item"]["required"] = ["id"]
    respx_mock.get(manager.SPEC_URL).respond(200, json=spec)

    assert manager.sync_spec() == 0

    assert json.loads(manager.SPEC_FILE.read_text()) == spec
    report = next(manager.REPORT_DIR.glob("*.md"))
    assert "required" in report.read_text()
    assert f"diff_report_path={report.as_posix()}" in (workspace / "output").read_text()


@pytest.mark.parametrize("payload", [None, [], {}, {"openapi": "3.0.0", "paths": {}}, {
    "openapi": "3.0.0", "paths": {"/items": {"get": {}}},
    "components": {"schemas": {"Item": {}}},
}])
def test_invalid_feed_cannot_replace_snapshot(workspace, respx_mock, payload):
    before = manager.SPEC_FILE.read_bytes()
    respx_mock.get(manager.SPEC_URL).respond(200, json=payload)

    with pytest.raises(ValueError):
        manager.sync_spec()

    assert manager.SPEC_FILE.read_bytes() == before
    assert not manager.REPORT_DIR.exists()


def test_duplicate_operations_are_rejected(spec):
    spec["paths"]["/duplicate"] = deepcopy(spec["paths"]["/items"])
    with pytest.raises(ValueError, match="Duplicate operationId"):
        manager.validate_spec(spec)


def test_http_failure_preserves_snapshot(workspace, respx_mock):
    before = manager.SPEC_FILE.read_bytes()
    respx_mock.get(manager.SPEC_URL).respond(503)
    with pytest.raises(httpx.HTTPStatusError):
        manager.sync_spec()
    assert manager.SPEC_FILE.read_bytes() == before


@pytest.mark.parametrize("age_hours", [1, 71, 73])
def test_upstream_health_uses_successful_run_age(respx_mock, age_hours):
    observed = datetime.now(UTC) - timedelta(hours=age_hours)
    route = respx_mock.get(manager.UPSTREAM_RUNS_URL).respond(200, json={
        "workflow_runs": [{"created_at": observed.isoformat(), "html_url": "https://github.com/run"}],
    })
    if age_hours > 72:
        with pytest.raises(ValueError, match="not succeeded in 72 hours"):
            manager.check_upstream()
    else:
        assert "https://github.com/run" in manager.check_upstream()
    assert route.calls[0].request.url.params["status"] == "success"
    assert route.calls[0].request.url.params["event"] == "schedule"


def test_stopped_upstream_prevents_sync(workspace, respx_mock):
    before = manager.SPEC_FILE.read_bytes()
    respx_mock.get(manager.UPSTREAM_RUNS_URL).respond(200, json={"workflow_runs": []})
    feed = respx_mock.get(manager.SPEC_URL).respond(200, json={})

    with pytest.raises(ValueError, match="no successful scheduled run"):
        manager.sync_spec(verify_upstream=True)

    assert manager.SPEC_FILE.read_bytes() == before
    assert not feed.called


def test_failed_atomic_replace_preserves_snapshot(workspace, spec, monkeypatch):
    before = manager.SPEC_FILE.read_bytes()

    def fail_replace(self, target):
        raise OSError("disk failure")

    monkeypatch.setattr(Path, "replace", fail_replace)
    with pytest.raises(OSError, match="disk failure"):
        manager.save_spec({**spec, "info": {}}, manager.SPEC_FILE)

    assert manager.SPEC_FILE.read_bytes() == before
    assert not manager.SPEC_FILE.with_suffix(".json.tmp").exists()

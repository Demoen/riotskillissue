import sys
from importlib import import_module
from pathlib import Path

import pytest


_REPO_ROOT = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, _REPO_ROOT)
try:
    release = import_module("tools.release")
finally:
    sys.path.remove(_REPO_ROOT)


@pytest.fixture
def workspace(tmp_path):
    (tmp_path / "pyproject.toml").write_text('[project]\nversion = "1.1.2"\n')
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n"
        "## [Unreleased]\n\n### Added\n\n- Work for a later release.\n\n"
        "## [1.1.2] - 2026-09-06\n\n### Fixed\n\n- Preserve cached integer keys.\n\n"
        "## [1.1.1] - 2026-08-10\n\n### Changed\n\n- Previous release.\n",
        encoding="utf-8",
    )
    return tmp_path


def test_extracts_only_requested_release(workspace):
    assert release.release_notes("v1.1.2", workspace) == (
        "### Fixed\n\n- Preserve cached integer keys.\n"
    )


@pytest.mark.parametrize("tag", ["v1.1.1", "v1.1.3", "1.1.2", "main", "v1.1.2-rc1"])
def test_rejects_tag_version_mismatch(workspace, tag):
    with pytest.raises(ValueError, match="does not match project version"):
        release.release_notes(tag, workspace)


@pytest.mark.parametrize("heading", ["## [1.1.3]", "## [1.1.2]\n\n- Duplicate.\n\n## [1.1.2]"])
def test_rejects_missing_or_duplicate_release(workspace, heading):
    (workspace / "CHANGELOG.md").write_text(heading + "\n\n- Release notes.\n")
    with pytest.raises(ValueError, match="exactly one"):
        release.release_notes("v1.1.2", workspace)


@pytest.mark.parametrize("notes", ["", "\n\n", "\n### Changed\n\n### Fixed\n"])
def test_rejects_empty_release_notes(workspace, notes):
    (workspace / "CHANGELOG.md").write_text("## [1.1.2] - 2026-09-06\n" + notes)
    with pytest.raises(ValueError, match="has no release notes"):
        release.release_notes("v1.1.2", workspace)


def test_accepts_last_release_section_without_trailing_newline(workspace):
    (workspace / "CHANGELOG.md").write_text("## [1.1.2]\n\n- Last release notes.")
    assert release.release_notes("v1.1.2", workspace) == "- Last release notes.\n"


def test_cli_writes_reviewed_notes_after_validation(workspace):
    output = workspace / "release-notes.md"

    release.main(["--tag", "v1.1.2", "--notes-output", str(output)], root=workspace)

    assert output.read_text(encoding="utf-8") == "### Fixed\n\n- Preserve cached integer keys.\n"


def test_cli_does_not_write_notes_for_invalid_release(workspace, capsys):
    output = workspace / "release-notes.md"

    with pytest.raises(SystemExit) as error:
        release.main(["--tag", "v1.1.1", "--notes-output", str(output)], root=workspace)

    assert error.value.code == 1
    assert "does not match project version" in capsys.readouterr().err
    assert not output.exists()

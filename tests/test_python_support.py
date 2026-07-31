import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_python_support_contract() -> None:
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = config["project"]

    assert project["requires-python"] == ">=3.14,<3.17"
    assert {
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
        "Programming Language :: Python :: 3.16",
    }.issubset(project["classifiers"])
    assert config["tool"]["ruff"]["target-version"] == "py314"
    assert config["tool"]["mypy"]["python_version"] == "3.14"

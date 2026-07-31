from pathlib import Path


def test_documentation_snippets_are_fenced_python_blocks() -> None:
    for document in Path("docs").rglob("*.md"):
        fence: str | None = None
        for line_number, line in enumerate(
            document.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line.strip()
            if stripped.startswith("```"):
                fence = None if fence is not None else stripped
            if "--8<--" in stripped:
                assert fence == "```python", (
                    f"{document}:{line_number} snippet is not in a Python code block"
                )

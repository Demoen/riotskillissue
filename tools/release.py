"""Validate release metadata and extract the reviewed changelog entry."""

import argparse
import re
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_HEADING = re.compile(r"^## \[([^\]]+)\][^\n]*$", re.MULTILINE)


def release_notes(tag: str, root: Path = ROOT) -> str:
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    version = project["project"]["version"]
    expected_tag = f"v{version}"
    if tag != expected_tag:
        raise ValueError(f"Release tag {tag!r} does not match project version {expected_tag!r}.")

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    headings = list(RELEASE_HEADING.finditer(changelog))
    matches = [index for index, heading in enumerate(headings) if heading.group(1) == version]
    if len(matches) != 1:
        raise ValueError(f"CHANGELOG.md must contain exactly one [{version}] release section.")

    index = matches[0]
    end = headings[index + 1].start() if index + 1 < len(headings) else len(changelog)
    notes = changelog[headings[index].end():end].strip()
    if not any(line.strip() and not line.lstrip().startswith("#") for line in notes.splitlines()):
        raise ValueError(f"CHANGELOG.md release [{version}] has no release notes.")
    return notes + "\n"


def main(argv: list[str] | None = None, root: Path = ROOT) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="Release tag, including the v prefix.")
    parser.add_argument("--notes-output", type=Path, help="Write the release notes to this file.")
    args = parser.parse_args(argv)
    try:
        notes = release_notes(args.tag, root)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"Release validation failed: {error}\n")
    if args.notes_output is not None:
        args.notes_output.write_text(notes, encoding="utf-8")
    print(f"Validated {args.tag}: package version and reviewed changelog entry match.")


if __name__ == "__main__":
    main()

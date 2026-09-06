# Contributing

## Development Setup

1. Clone the repo.
2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   # Or manual verification
   python tests/manual_test.py
   ```

## Documentation

The documentation is built with [Zensical](https://zensical.org/) using
`mkdocs.yml`. The modern theme uses native section indexes, breadcrumbs, search,
and linked content tabs, with site-specific styling in `docs/stylesheets/extra.css`.
The templates in `overrides/` give the homepage its own layout, provide useful
404 links, distinguish the breadcrumb landmark, and keep the decorative loading
bar out of the accessibility tree. Review them when upgrading Zensical.

Install the documentation dependencies and start a local preview:

```bash
pip install -e ".[docs]"
zensical serve
```

Build the site with the same validation used in CI:

```bash
zensical build --clean --strict
```

The generated site is written to `site/`.

### Authoring guides

Place integration guides under **Python SDK**, terminal and MCP guides under
**Tools**, and endpoint discovery under **API reference** in `mkdocs.yml`.
Each section starts with an index page that helps readers choose their next step.
Keep existing page paths and heading anchors stable so saved links keep working.

Use Zensical's [cards](https://zensical.org/docs/authoring/grids/) for navigation,
[content tabs](https://zensical.org/docs/authoring/content-tabs/) for alternatives,
and collapsible details for optional setup or longer examples. Shell tabs use
the exact labels `macOS / Linux` and `Windows PowerShell` so the selected platform
follows the reader between pages. Keep prerequisites and limitations visible.

Check changed pages in both color schemes and at a narrow mobile width. Code
blocks should scroll within the page, and commands and links should remain
usable with the keyboard.

## Code Generation

The SDK is generated from the community-maintained
[riotapi-schema feed](https://github.com/MingweiSamuel/riotapi-schema), which
scrapes Riot's API reference. It is not an official Riot specification. The
generator replaces its managed files so removed endpoints do not leave stale
modules behind.

Check the bundled schema without changing files:

```bash
python tools/manager.py --check --check-upstream
```

The command reports the source URL, check time, content hash, operation/model
counts, and latest successful upstream scheduled run. It exits with status 1
when the bundled schema differs or the upstream generator has not succeeded
within 72 hours. `--check` alone compares the feed without querying GitHub.
An old schema commit date is normal when Riot has not changed its reference;
upstream workflow activity determines generator health.

The daily SDK workflow runs at 03:17 UTC, after upstream's scheduled generation,
and runs tests, typing, lint, generation parity, documentation, and packaging
checks even when the schema is unchanged. GitHub may delay scheduled runs.
Diff reports include nested field, parameter, response, request-body, routing,
authentication, and metadata changes. They are structural reports, not a
complete classification of backwards compatibility.

To regenerate:

```bash
# Fetch latest spec
python tools/manager.py

# Generate code (endpoints, models, client mixin)
python tools/generator/core.py
```

Generated files:

| File | Description |
|------|-------------|
| `src/riotskillissue/models/<game>/*.py` | Pydantic models for all API schemas |
| `src/riotskillissue/api/raw/<game>/*.py` | Typed async and sync endpoint groups |
| `src/riotskillissue/api/registry.py` | Operation metadata for dispatch and MCP discovery |
| `src/riotskillissue/api/client_mixin.py` | Mixin that wires endpoints into `RiotClient` |
| `docs/api-reference.md` | Raw operation reference |

!!! warning "Do not edit generated files"
    Edit `tools/generator/` and `tools/templates/` for the generated files listed
    above. `api/operations.py` and the high-level services are maintained by hand.

## Templates

| Template | Generates |
|----------|-----------|
| `tools/templates/models.py.j2` | `models/<game>/*.py` |
| `tools/templates/endpoints.py.j2` | `api/raw/<game>/*.py` |
| `tools/templates/client_mixin.py.j2` | `api/client_mixin.py` |
| `tools/templates/raw_client.py.j2` | `api/raw/_client.py` |
| `tools/templates/registry.py.j2` | `api/registry.py` |
| `tools/templates/api_reference.md.j2` | `docs/api-reference.md` |

## Release Process

1. Bump the version in `pyproject.toml` and move the completed changes from
   `Unreleased` into a dated `CHANGELOG.md` release section. Remove an empty
   `Unreleased` section and update the comparison links at the end of the file.
2. Run the quality checks from CI and validate the release metadata. For 1.1.2:

   ```bash
   python tools/release.py --tag v1.1.2
   hatch build dist/1.1.2
   python tools/release.py --tag v1.1.2 --notes-output dist/1.1.2/RELEASE_NOTES.md
   ```

3. Review and commit the prepared changes, then tag that commit with the exact
   version (`v1.1.2`). Pushing the tag starts `.github/workflows/publish.yml`.
4. The workflow checks the tag/version match, requires release notes, and verifies
   Python 3.14 and 3.15 before publishing to PyPI using Trusted Publishing. The
   GitHub release uses the reviewed changelog entry and contains the built
   distributions; it is created only after PyPI succeeds. Documentation deployment
   also waits for successful PyPI publication.
5. Verify the new version on [PyPI](https://pypi.org/p/riotskillissue), the GitHub
   release assets, and the documentation site.

For a tag created with `GITHUB_TOKEN`, the updater explicitly dispatches the
Publish workflow because the tag push does not trigger another workflow. A
manual dispatch must select a version tag; selecting a branch does not publish.

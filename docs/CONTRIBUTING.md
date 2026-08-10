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

## Code Generation

The SDK is generated from the Riot Games OpenAPI spec. The generator cleans the output directory before writing, so stale files are automatically removed.

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
| `src/riotskillissue/api/models.py` | Pydantic models for all API schemas |
| `src/riotskillissue/api/endpoints/*.py` | Endpoint classes for each API tag |
| `src/riotskillissue/api/client_mixin.py` | Mixin that wires endpoints into `RiotClient` |

!!! warning "Do not edit generated files"
    Files in `src/riotskillissue/api/` are auto-generated. Edit the Jinja2 templates in `tools/templates/` instead.

## Templates

| Template | Generates |
|----------|-----------|
| `tools/templates/models.py.j2` | `api/models.py` |
| `tools/templates/endpoints.py.j2` | `api/endpoints/*.py` |
| `tools/templates/client_mixin.py.j2` | `api/client_mixin.py` |

## Release Process

1. Update `CHANGELOG.md` with the new version.
2. Bump version in `pyproject.toml`.
3. **Tag**: Push a version tag (e.g., `v1.0.0`).
4. **Publish**: `.github/workflows/publish.yml` verifies the tag, creates the GitHub release, publishes to PyPI using Trusted Publishing, and deploys the documentation.
5. **Verify**: Check [PyPI project page](https://pypi.org/p/riotskillissue).

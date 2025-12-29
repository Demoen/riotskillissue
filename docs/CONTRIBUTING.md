# Contributing

## Development Setup

1. Clone the repo.
2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   pip install httpx pydantic redis tenacity jinja2 frozendict msgspec deepdiff rich typer
   ```
3. Run tests:
   ```bash
   pytest
   # Or manual verification
   python tests/manual_test.py
   ```

## Code Generation

The SDK is generated from the OpenAPI spec. To regenerate:

```bash
# Fetch latest spec
python tools/manager.py

# Generate code
python tools/generator/core.py
```

## Release Process

1. **Tag**: Create a new GitHub release with a tag (e.g., `v0.1.0`).
2. **Publish**: The GitHub Action `.github/workflows/publish.yml` will automatically build and push to PyPI using Trusted Publishing.
3. **Verify**: Check [PyPI project page](https://pypi.org/p/riot-wrapper).

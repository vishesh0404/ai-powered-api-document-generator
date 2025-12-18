# ai-powered-api-document-generator

This Project is AI Powered API document Generator


## License
This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE.md) file for details.

## Requirements
- Python 3.14+
- uv (recommended) or pip

## Quickstart

Using uv:
- Install uv: https://docs.astral.sh/uv/
- Create and sync the environment:
  - uv sync --managed-python --all-groups
- Run the API:
  - uv run python -m src.main

Using pip:
- python -m venv .venv && source .venv/bin/activate
- pip install -e .
- python -m src.main

The server starts on http://127.0.0.1:1506.

## API Docs
- Swagger UI: /api/ref (enabled: False)

## Project layout
- src/            Python package with application code
- src/api         FastAPI routers and endpoints
- src/db          SQLModel models and DB utilities (DuckDB by default)
- src/services    Service layer

## Linting & Formatting
- Ruff and dprint are configured. If you use uv, you can run:
  - uv run ruff check
  - dprint check

## Configuration
- Defaults are baked into src/server.py via APIServerConfig. You can also call APIServerConfig.from_yaml to load settings from a YAML file with environment interpolation.

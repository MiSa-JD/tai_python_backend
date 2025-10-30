# Repository Guidelines

## Project Structure & Module Organization
`app/main.py` hosts the FastAPI entrypoint; prefer importing `create_app()` when instantiating the service. Organize domain logic under `app/` modules and keep request/response models in `app/classes/{metadata,requests,responses}.py`. Use `dev/` only for throwaway prototypes or notebooks and clear outputs before committing. Infrastructure files (`docker-compose.yml`, `Dockerfile`) stay at the root for local orchestration.

## Build, Test, and Development Commands
Create a virtual env with `python -m venv .venv && source .venv/bin/activate`, then install dependencies via `pip install -r requirements.txt`. Run `uvicorn app.main:app --reload` for live API reloading or `docker-compose up` if you need the full stack. Execute tests with `pytest`; apply `pytest -k keyword --maxfail=1` when focusing on a scenario.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indentation and explicit type hints on FastAPI routes, dependencies, and Pydantic models. Name Pydantic classes in PascalCase (e.g., `SearchRequest`, `SearchResultOutput`) and modules in snake_case. Keep handlers skinny by moving orchestration into helpers or services and annotate public functions with concise docstrings.

## Testing Guidelines
Use `pytest` alongside `httpx.AsyncClient` to exercise endpoints; store suites under `tests/api/` mirroring module names such as `test_main.py`. Cover happy paths, validation failures, and integration of `create_app()` to ensure routers, middleware, and dependencies register. Prefer fixture reuse for shared clients or sample payloads to keep tests lean.

## Commit & Pull Request Guidelines
Write imperative, ~50 character commit subjects (e.g., `Add search response schema`) and expand context in the body when needed. Reference related issues with `#id` and spell out user impact plus rollback notes. PRs should include a summary, verification steps (`uvicorn`, `pytest`), and before/after evidence for API contracts when relevant.

## Security & Configuration Tips
Load secrets from `.env` via `os.getenv` and never hard-code API keys. Document any new external services or credentials in the PR checklist so operations can provision them. Sanitise staging data and remove credentials from notebooks or logs before pushing.

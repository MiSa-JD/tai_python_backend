# Repository Guidelines

## Project Structure & Module Organization
- `app/` contains the FastAPI service entry point `main.py` and the `create_app()` factory.
- Request/response schemas live in `app/classes`, split into `metadata.py`, `requests.py`, and `responses.py`.
- Keep runtime code inside `app/`; treat `dev/` as an experiments area for notebooks and prototypes.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` creates an isolated environment for contributors.
- `pip install -r requirements.txt` synchronizes the runtime stack (FastAPI, LangChain, ChromaDB, etc.).
- `uvicorn app.main:app --reload` serves the API locally for notebooks or external clients.
- `pytest` runs the test suite once it exists; filter with `pytest -k keyword` when iterating on a feature.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation and prefer explicit type hints for FastAPI endpoints and models.
- Name Pydantic models in PascalCase (`SearchRequest`, `SearchResultOutput`) and modules in snake_case.
- Keep business logic inside services or helpers rather than route handlers; add concise docstrings for public functions.
- Update `requirements.txt` when adding dependencies and include a short rationale in the PR description.

## Testing Guidelines
- Use `pytest` with `httpx.AsyncClient` to exercise FastAPI routes; store specs under `tests/api/`.
- Mirror module names in test files (`test_main.py`, `test_responses.py`) and cover happy-path plus validation failures.
- Target integration coverage for `create_app()` to ensure routers, middlewares, and dependencies initialize correctly.
- Run `pytest --maxfail=1` locally before pushing to surface flakes early and keep PRs green.

## Commit & Pull Request Guidelines
- Write imperative, English subject lines around 50 characters (e.g., `Add bug report issue template`).
- Reference related issues with `#id` and describe user impact and rollback strategy in the body when relevant.
- PRs should include: summary, verification steps (`uvicorn`, `pytest`), and screenshots or sample responses for API changes.
- Request at least one review and wait for automated checks (planned GitHub Actions) before merging.

## Security & Configuration Tips
- Store secrets in `.env` (already gitignored) and access them via `os.getenv`; never hard-code credentials.
- Clean notebook outputs in `dev/` before committing (`jupyter nbconvert --clear-output --inplace`).
- Document any required external services (vector stores, API providers) in the PR so deployment environments can be updated.

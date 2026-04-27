# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is EASE?

EASE is a FastAPI service implementing a structured AI decision-making framework:

- **E**nvironment — parse a request into a structured goal/context definition
- **A**ctions — generate diverse candidate actions
- **S**afety — evaluate each action (4 parallel LLM calls via `asyncio.gather`: stakeholder impacts, risk assessment, ethical analysis, stakeholder voices; then synthesis), with optional auto-improvement
- **E**lection — score actions on a weighted matrix and elect the best one with an implementation plan

The `/api/v1/ease` endpoint runs all four steps synchronously. `/api/v1/ease/submit` runs the pipeline as a Celery task (poll status at `/api/v1/tasks/{task_id}`). Individual step endpoints (`/environment`, `/actions`, `/safety`, `/election`) expose each step directly.

## Development Commands

### Run locally (no Docker)
```bash
cp .env.example .env   # fill in LLM_PROVIDER, LLM_API_KEY, LLM_MODEL
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### Run with Docker (full stack: API + PostgreSQL + Redis + Celery worker)
```bash
docker compose -f docker-compose.prod.yml up --build
```

### Run tests
```bash
# Directly (no DB or Redis required — database_url defaults to empty)
pytest tests/ -v
pytest tests/test_foo.py -v   # single file

# In Docker
docker compose -f docker-compose.test.yml up --build
```

### Manual end-to-end smoke test
```bash
python testing.py   # requires the API running on localhost:8000
```

Interactive docs: `http://localhost:8000/docs`

## Architecture

```
src/
  main.py            # FastAPI app; structured JSON logging, lifespan (validates LLM, inits DB conditionally)
  config.py          # pydantic-settings Settings (reads .env); all runtime configuration
  ai_security.py     # sanitize_input (control char stripping), check_injection (regex pre-screen)
  auth.py            # require_api_key FastAPI dependency; disabled when API_KEY env var is empty
  database.py        # SQLAlchemy async engine + RequestLog ORM model; gated by database_url being set
  middleware.py      # RequestLoggingMiddleware; fire-and-forget DB writes via asyncio.create_task
  workers.py         # Celery app + run_ease_task; wraps run_ease_framework for async task queue
  utils/
    call_llm.py      # Async LLM wrapper; module-level client singletons, configurable timeout + tenacity retry
  models/            # Pydantic models: Action, Environment, SafetyEvaluation, Election, request/response shapes
  routers/
    environment.py   # POST /api/v1/environment
    actions.py       # POST /api/v1/actions
    safety.py        # POST /api/v1/safety  (returns List[SafetyEvaluation])
    election.py      # POST /api/v1/election
    ease.py          # POST /api/v1/ease, POST /api/v1/ease/submit
    health.py        # GET /health  (no auth required)
    tasks.py         # GET /api/v1/tasks/{task_id}
```

All LLM prompts live in `prompts/` as YAML files (`environment.yaml`, `actions.yaml`, `safety.yaml`, `election.yaml`). Each router loads its prompt(s) at import time via `get_prompt(filename, key)` from `src/utils/prompts.py` (cached with `functools.lru_cache`). Every router calls `call_llm(system_prompt, user_prompt)` from `src/utils/call_llm.py`. The provider (anthropic/openai/google) is selected at runtime from `settings.llm_provider`.

The `prompts/` directory must be present in all Docker images — all three Dockerfiles (`Dockerfile.prod`, `Dockerfile.test`, `Dockerfile.worker`) include `COPY prompts/ prompts/`.

## Safety / Security Layer

Every user-facing input is sanitized then injection-checked before reaching the EASE pipeline:

1. `sanitize_input(text)` — NFC unicode normalization, strips control chars (preserves `\t \n \r`), enforces length cap (`src/ai_security.py`)
2. `check_injection(text)` — fast regex pre-screen for injection patterns (`src/ai_security.py`)

Injection detected → HTTP 400. There is no LLM-based injection check (`llm_check_injection` was removed).

## Configuration

`src/config.py` (via `pydantic-settings`) reads `.env`:

| Variable | Default | Notes |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | `anthropic`, `openai`, or `google` |
| `LLM_MODEL` | `claude-sonnet-4-20250514` | Provider-specific model name |
| `LLM_API_KEY` | *(required)* | Checked at startup |
| `LLM_MAX_TOKENS` | `8192` | Token cap for all LLM calls |
| `LLM_TIMEOUT_SECONDS` | `60.0` | Per-call timeout (seconds) |
| `LLM_MAX_RETRIES` | `3` | Tenacity retry attempts with exponential backoff |
| `DATABASE_URL` | *(empty)* | Postgres async DSN; empty = DB disabled (tests work without DB) |
| `REDIS_URL` | `redis://localhost:6379/0` | Celery broker + result backend |
| `API_KEY` | *(empty)* | Required value for `X-API-Key` header; empty = auth disabled |

Default election weights: `safety_rating` 0.40, `goal_achievement` 0.30, `risk_level` 0.20, `resource_efficiency` 0.10. Actions rated below 3.0 are excluded from election.

## Testing: Mock Patching Rules

Routers bind `call_llm` and `check_injection` at import time via `from ... import`. **Always patch at the router module, not the source module:**

```python
# Correct
patch("src.routers.environment.call_llm", ...)
patch("src.routers.environment.check_injection", ...)
patch("src.routers.safety.call_llm", ...)
patch("src.routers.ease.check_injection", ...)

# Wrong — has no effect on already-bound local names
patch("src.utils.call_llm.call_llm", ...)
```

### Safety router call order

Inside `_evaluate_action`, calls are partially parallel:

```
asyncio.gather(
    _generate_stakeholder_impacts,   # slot 0
    _generate_risk_assessment,       # slot 1
    _generate_ethical_analysis,      # slot 2
    _generate_stakeholder_voices,    # slot 3
)
synthesis call_llm                   # slot 4
```

With `auto_improve=True`, `_improve_action` fires first (slot 0), shifting everything by one.

All test files use `asyncio_mode = auto` (set in `pytest.ini`). Tests do not require a live database or Redis; `DATABASE_URL` defaults to empty and Celery is never connected during unit tests.

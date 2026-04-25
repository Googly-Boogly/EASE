# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is EASE?

EASE is a FastAPI service implementing a structured AI decision-making framework:

- **E**nvironment — parse a request into a structured goal/context definition
- **A**ctions — generate diverse candidate actions
- **S**afety — evaluate each action via 4 sequential LLM calls (stakeholder impacts → safety principles → risk assessment → synthesis), with optional auto-improvement
- **E**lection — score actions on a weighted matrix and elect the best one with an implementation plan

The `/api/v1/ease` endpoint runs all four steps in sequence. The other four endpoints (`/environment`, `/actions`, `/safety`, `/election`) expose each step individually.

## Development Commands

### Run locally (no Docker)
```bash
cp .env.example .env   # fill in LLM_PROVIDER, LLM_API_KEY, LLM_MODEL
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### Run with Docker
```bash
# Production
docker compose -f docker-compose.prod.yml up --build

# Tests
docker compose -f docker-compose.test.yml up --build
```

### Run tests directly
```bash
pytest tests/ -v
# Single test file
pytest tests/test_foo.py -v
```

### Manual end-to-end smoke test
```bash
python testing.py   # requires the API running on localhost:8000
```

Interactive docs: `http://localhost:8000/docs`

## Architecture

```
src/
  main.py            # FastAPI app; validates LLM_PROVIDER/LLM_API_KEY at startup
  config.py          # pydantic-settings Settings (reads .env); default weights & thresholds
  ai_security.py     # Prompt injection defense: sanitize_input, check_injection (regex), llm_check_injection (LLM)
  utils/
    call_llm.py      # Thin async wrapper dispatching to anthropic / openai / google SDKs
  models/            # Pydantic models: Action, Environment, SafetyEvaluation, Election, request/response shapes
  routers/           # One router per EASE step; system prompts are inline string constants
```

All LLM prompts are **inline string constants** in each router file (e.g. `ENVIRONMENT_SYSTEM_PROMPT` in `src/routers/environment.py`). There is no separate `prompts/` directory in the current codebase.

Every router makes LLM calls via `call_llm(system_prompt, user_prompt)` from `src/utils/call_llm.py`. The provider (anthropic/openai/google) is selected at runtime from `settings.llm_provider`.

## Safety / Security Layer

Every user-facing input goes through a two-stage check before being passed to the EASE pipeline:

1. `check_injection(text)` — fast regex pre-screen (`src/ai_security.py`)
2. `llm_check_injection(text)` — semantic LLM check using `PROMPT_INJECTION_DETECTION_PROMPT`

Both `/environment` and `/ease` endpoints run this check. Injection detected → return an error `Environment` or raise an HTTP 400.

## Configuration

`src/config.py` (via `pydantic-settings`) reads `.env`:

| Variable | Default | Notes |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | `anthropic`, `openai`, or `google` |
| `LLM_MODEL` | `claude-sonnet-4-20250514` | Provider-specific model name |
| `LLM_API_KEY` | *(required)* | Checked at startup |

Default election weights: `safety_rating` 0.40, `goal_achievement` 0.30, `risk_level` 0.20, `resource_efficiency` 0.10. Actions rated below 3.0 are excluded from election.

## Testing: Mock Patching Rules

Routers bind `call_llm`, `check_injection`, and `llm_check_injection` at import time via `from ... import`. **Always patch at the router module, not the source module:**

```python
# Correct
mocker.patch("src.routers.environment.call_llm", ...)
mocker.patch("src.routers.environment.llm_check_injection", ...)
mocker.patch("src.routers.safety.call_llm", ...)

# Wrong — has no effect on already-bound local names
mocker.patch("src.utils.call_llm.call_llm", ...)
```

`llm_check_injection` in `ai_security.py` lazy-imports `call_llm` inside its function body — if you need to patch that path, patch `src.utils.call_llm.call_llm` (the source) rather than a router binding.

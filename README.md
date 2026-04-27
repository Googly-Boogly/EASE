# EASE Framework Documentation

**Version 2.0**

## Overview

EASE is a structured decision-making framework for AI agents focused on safe and ethical action selection. The framework ensures AI systems make well-reasoned decisions by systematically analyzing the environment, generating possible actions, evaluating their safety implications, and electing the best course of action.

## What is EASE?

**E**nvironment - Define the goal and analyze the current state  
**A**ctions - Generate all possible actions  
**S**afety - Evaluate, improve, and rate the safety implications of each action  
**E**lection - Select the best action through systematic evaluation

## Why EASE?

Traditional AI decision-making often lacks explicit safety reasoning. EASE addresses this by:

- Making safety considerations a formal, transparent step
- Allowing iterative improvement of actions before election
- Providing a systematic approach to complex decisions
- Enabling auditability and explainability of AI choices

## Quick Start

1. **Define your Environment** - What's the goal? What's the current state?
2. **List Actions** - What can the agent do?
3. **Evaluate Safety** - How safe is each action? Can it be improved?
4. **Elect** - Choose the best action based on safety rating and goal achievement

## Documentation Structure

- [Quick Start Guide](docs/quickstart.md) - Get started in 5 minutes
- [Framework Overview](docs/overview.md) - Detailed explanation of EASE
- [Step 1: Environment](docs/step1_enviornment.md) - How to specify goals and environment
- [Step 2: Actions](docs/step2_actions.md) - Generating and structuring actions
- [Step 3: Safety](docs/step3_safety.md) - Evaluating and improving safety
- [Step 4: Election](docs/step4_election.md) - Electing the best action
- [Best Practices](docs/best_practices.md) - Tips and guidelines
- [API Reference](docs/api_reference.md) - FastAPI implementation details
- [Example: Content Moderation](docs/content_moderation_example.md) - Real-world walkthrough

## Core Principles

1. **Transparency** - Every decision should be explainable
2. **Iterative Improvement** - Actions can be refined before election
3. **Explicit Safety** - Safety reasoning is formalized, not implicit
4. **Goal Alignment** - Actions must serve the stated goal
5. **Safety First** - Risk mitigation is built into the framework

## Running the API

### 1. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set your LLM provider credentials:

```
LLM_PROVIDER="anthropic"   # anthropic, openai, or google
LLM_API_KEY="your-api-key"
LLM_MODEL="claude-sonnet-4-20250514"
```

### 2. Run with Docker Compose (production)

```bash
docker compose -f docker-compose.prod.yml up --build
```

Includes FastAPI server, PostgreSQL, Redis, and Celery worker. The API will be available at `http://localhost:8000`.

### 3. Run with Docker Compose (tests)

```bash
docker compose -f docker-compose.test.yml up --build
```

### 4. Run without Docker

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET  /health` | Health check (no auth required) |
| `POST /api/v1/environment` | Analyze a request and produce a structured environment definition |
| `POST /api/v1/actions` | Generate diverse actions for a given environment |
| `POST /api/v1/safety` | Evaluate and improve the safety of actions |
| `POST /api/v1/election` | Elect the best action via weighted scoring |
| `POST /api/v1/ease` | Run the complete EASE pipeline synchronously |
| `POST /api/v1/ease/submit` | Submit EASE pipeline as an async Celery task |
| `GET  /api/v1/tasks/{task_id}` | Poll status of a submitted async task |

Interactive API docs: `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc).

## Authentication

When `API_KEY` is set in `.env`, all endpoints except `/health` require an `X-API-Key` header:

```
X-API-Key: your-secret-api-key
```

Leave `API_KEY` empty to disable authentication (default for local development).

## Supported LLM Providers

| Provider | `LLM_PROVIDER` | Example `LLM_MODEL` | SDK |
|---|---|---|---|
| Anthropic | `anthropic` | `claude-sonnet-4-20250514` | `anthropic` |
| OpenAI | `openai` | `gpt-4o` | `openai` |
| Google | `google` | `gemini-2.0-flash` | `google-genai` |

## Safety Rating Scale

EASE uses a **0-10 scale** for safety ratings:
- **9-10**: Excellent safety profile
- **7-8**: Good safety with minor concerns
- **5-6**: Acceptable safety with moderate concerns
- **3-4**: Concerning safety issues
- **0-2**: Unacceptable safety violations

Actions rated below 3 should never be elected.

## Getting Help

See [FAQ](docs/faq.md) for common questions and [Best Practices](docs/best_practices.md) for advanced guidance.

# EASE Framework API Reference

FastAPI implementation guide for the EASE framework.

## Overview

The EASE framework is implemented as a **FastAPI-based REST API** that provides endpoints for each step of the decision-making process.

## API Architecture

```
┌──────────────────────────────────────────┐
│     FastAPI Application                   │
├──────────────────────────────────────────┤
│  GET  /health                            │  ← no auth required
│  POST /api/v1/environment                │
│  POST /api/v1/actions                    │
│  POST /api/v1/safety                     │
│  POST /api/v1/election                   │
│  POST /api/v1/ease          (sync)       │
│  POST /api/v1/ease/submit   (async)      │
│  GET  /api/v1/tasks/{task_id}            │
└──────────────────────────────────────────┘
```

## Authentication

All endpoints except `/health` require an `X-API-Key` header when `API_KEY` is set in environment configuration.

```
X-API-Key: your-secret-api-key
```

If `API_KEY` is empty (the default), authentication is disabled and no header is needed.

## Data Models

### Environment

```python
class Goal(BaseModel):
    objective: str
    success_criteria: List[str]
    constraints: List[str]
    time_horizon: str

class Stakeholder(BaseModel):
    name: str
    interests: List[str]
    power_level: str   # "high" | "medium" | "low"
    affected_degree: str  # "primary" | "secondary" | "tertiary"

class Environment(BaseModel):
    goal: Goal
    current_state: str
    stakeholders: List[Stakeholder]
    resources: List[str]
    constraints: List[str]
    uncertainties: List[str]
    context: Optional[Dict] = {}
```

### Action

```python
class Action(BaseModel):
    id: str                # pattern: "^A[0-9]+$"
    name: str
    description: str
    prerequisites: List[str]
    expected_outcomes: List[str]
    resources_required: List[str]
    reversibility: str     # "high" | "medium" | "low" | "none"
    time_to_effect: str
    safety_rating: Optional[float]             # 0–10, set by safety step
    goal_achievement_score: Optional[float]    # 0–10
    resource_efficiency_score: Optional[float] # 0–10
```

### Safety Evaluation

```python
class StakeholderImpact(BaseModel):
    stakeholder_name: str
    benefits: List[str]
    harms: List[str]
    autonomy_respected: bool
    informed_consent: bool
    net_impact: float  # -10 to +10

class StakeholderVoice(BaseModel):
    stakeholder_name: str
    perspective: str           # first-person voiced statement
    primary_concerns: List[str]
    what_would_help: List[str]

class RiskAssessment(BaseModel):
    safety_risks: List[str]
    privacy_risks: List[str]
    security_risks: List[str]
    societal_risks: List[str]
    overall_severity: str   # "low" | "medium" | "high" | "critical"
    severity_score: float   # 0–10, inverse: 10=low risk, 0=critical

class EthicalFrameworkScore(BaseModel):
    score: float            # 0–10
    reasoning: str
    key_considerations: List[str]

class EthicalAnalysis(BaseModel):
    utilitarian: EthicalFrameworkScore
    care_ethics: EthicalFrameworkScore
    virtue_ethics: EthicalFrameworkScore
    synthesis: str
    dominant_framework: str

class EvaluationMetadata(BaseModel):
    confidence: float       # 0–10
    key_assumptions: List[str]
    uncertainty_flags: List[str]

class SafetyEvaluation(BaseModel):
    action_id: str
    stakeholder_impacts: List[StakeholderImpact]
    stakeholder_voices: List[StakeholderVoice]  # first-person perspectives
    risks: RiskAssessment
    ethical_analysis: EthicalAnalysis           # utilitarianism, care ethics, virtue ethics
    improvements: List[str]
    rating: float           # 0–10
    justification: str
    remaining_concerns: List[str]
    metadata: EvaluationMetadata                # confidence + assumptions
```

### Election

```python
class DecisionMatrix(BaseModel):
    action_id: str
    goal_achievement: float    # 0–10
    safety_rating: float       # 0–10
    risk_level: float          # 0–10
    resource_efficiency: float # 0–10
    final_score: float         # weighted sum, 0–10

class WeightScenario(BaseModel):
    name: str
    weights: Dict[str, float]
    ranking: List[str]   # action IDs ordered best → worst
    elected: str
    top_score: float

class SensitivityAnalysis(BaseModel):
    scenarios: List[WeightScenario]  # 4 alternative weight profiles
    is_robust: bool                  # True if same winner under all profiles
    robustness_note: str

class Election(BaseModel):
    elected_action: Action
    decision_matrix: List[DecisionMatrix]
    weights: Dict[str, float]
    qualitative_factors: List[str]
    rejected_alternatives: List[Dict[str, str]]
    implementation_plan: List[str]
    success_metrics: List[str]
    review_schedule: str
    fallback_plan: str
    sensitivity_analysis: SensitivityAnalysis   # weight-robustness check
```

---

## API Endpoints

### Health Check

**Endpoint:** `GET /health`

No authentication required.

**Response:**
```json
{
  "status": "healthy",
  "database": "ok",
  "redis": "ok",
  "llm_provider": "anthropic"
}
```

`status` is `"healthy"` when all enabled services are reachable, `"degraded"` otherwise. `database` is `"disabled"` when `DATABASE_URL` is not set.

---

### 1. Environment Analysis

**Endpoint:** `POST /api/v1/environment`

**Request:**
```json
{
  "request": "Reduce customer churn by 20%",
  "context": {
    "current_churn": 0.15,
    "industry": "SaaS",
    "budget": 500000
  }
}
```

`context` is optional. When provided it is attached to the returned `Environment` object and propagated through the pipeline.

**Response:** `Environment` object (see model above)

---

### 2. Action Generation

**Endpoint:** `POST /api/v1/actions`

**Request:**
```json
{
  "environment": { },
  "min_actions": 5,
  "include_null": true
}
```

**Response:**
```json
{
  "actions": [
    {
      "id": "A1",
      "name": "Personalized Retention Campaigns",
      "description": "AI-driven outreach to at-risk customers",
      "prerequisites": ["Customer behavior data", "Email infrastructure"],
      "expected_outcomes": ["15-20% churn reduction"],
      "resources_required": ["$150k", "3 months"],
      "reversibility": "high",
      "time_to_effect": "2-3 months",
      "goal_achievement_score": 7.5,
      "resource_efficiency_score": 6.0
    }
  ]
}
```

---

### 3. Safety Evaluation

**Endpoint:** `POST /api/v1/safety`

**Request:**
```json
{
  "actions": [
    { }
  ],
  "environment": { },
  "auto_improve": true
}
```

Note: `actions` is a **list** — pass one or more `Action` objects. The endpoint evaluates all actions in parallel and returns a list of evaluations.

**Response:** `List[SafetyEvaluation]`

```json
[
  {
    "action_id": "A1",
    "stakeholder_impacts": [
      {
        "stakeholder_name": "Existing Customers",
        "benefits": ["Personalized support"],
        "harms": ["Privacy concerns with data usage"],
        "autonomy_respected": true,
        "informed_consent": false,
        "net_impact": 5.0
      }
    ],
    "risks": {
      "safety_risks": [],
      "privacy_risks": ["Usage data may be over-collected"],
      "security_risks": [],
      "societal_risks": [],
      "overall_severity": "low",
      "severity_score": 8.0
    },
    "stakeholder_voices": [
      {
        "stakeholder_name": "Existing Customers",
        "perspective": "I appreciate being contacted, but I need transparency about how my data is used.",
        "primary_concerns": ["Data privacy", "Unsolicited outreach"],
        "what_would_help": ["Clear opt-out", "Data usage explanation"]
      }
    ],
    "ethical_analysis": {
      "utilitarian": {"score": 7.5, "reasoning": "Net positive for majority", "key_considerations": ["Reduces churn benefit"]},
      "care_ethics": {"score": 6.5, "reasoning": "Prioritizes vulnerable churning customers", "key_considerations": ["Consent gaps"]},
      "virtue_ethics": {"score": 7.0, "reasoning": "Demonstrates care and responsibility", "key_considerations": ["Transparency virtue"]},
      "synthesis": "Broadly ethical with consent improvements needed.",
      "dominant_framework": "utilitarian"
    },
    "improvements": ["Add explicit opt-out", "Minimize data collection"],
    "rating": 7.0,
    "justification": "Net-positive profile with addressable consent gaps.",
    "remaining_concerns": ["Opt-out users may still churn at higher rates"],
    "metadata": {
      "confidence": 7.5,
      "key_assumptions": ["Customers will engage with outreach"],
      "uncertainty_flags": ["Regulatory environment may change"]
    }
  }
]
```

#### Internal call order per action

When `auto_improve=False`:
1. `asyncio.gather(stakeholder_impacts, risk_assessment, ethical_analysis, stakeholder_voices)` — 4 parallel calls
2. synthesis — sequential (uses all four results; returns rating, improvements, metadata)

When `auto_improve=True`: `_improve_action` runs first, then steps 1–2 above on the improved action.

---

### 4. Election

**Endpoint:** `POST /api/v1/election`

**Request:**
```json
{
  "actions": [ ],
  "evaluations": [ ],
  "environment": { },
  "weights": {
    "goal_achievement": 0.30,
    "safety_rating": 0.40,
    "risk_level": 0.20,
    "resource_efficiency": 0.10
  },
  "exclude_threshold": 3.0
}
```

`weights` must contain exactly the four keys above and sum to 1.0. If omitted, the default weights from `Settings` are used. `exclude_threshold` (0–10) filters out actions with a safety rating below this value.

**Response:** `Election` object (see model above)

---

### 5. Full EASE Flow (synchronous)

**Endpoint:** `POST /api/v1/ease`

Runs all four steps in sequence and returns when complete.

**Request:**
```json
{
  "request": "Help our startup decide whether to open-source our ML model.",
  "context": {
    "team_size": 12,
    "stage": "Series A"
  },
  "min_actions": 5,
  "weights": {
    "goal_achievement": 0.30,
    "safety_rating": 0.40,
    "risk_level": 0.20,
    "resource_efficiency": 0.10
  },
  "exclude_threshold": 3.0
}
```

**Response:**
```json
{
  "environment": { },
  "actions": [ ],
  "evaluations": [ ],
  "election": { },
  "duration_seconds": 42.7
}
```

---

### 6. Full EASE Flow (asynchronous)

**Endpoint:** `POST /api/v1/ease/submit`

Enqueues the EASE pipeline as a Celery task and returns immediately.

**Request:** Same as `POST /api/v1/ease`

**Response:**
```json
{
  "task_id": "d3b07384-d9a2-4c6e-b3b5-1a8f2d3e4f56"
}
```

---

### 7. Task Status

**Endpoint:** `GET /api/v1/tasks/{task_id}`

**Response:**
```json
{
  "task_id": "d3b07384-d9a2-4c6e-b3b5-1a8f2d3e4f56",
  "status": "completed",
  "result": { },
  "error": null
}
```

`status` values: `pending` | `running` | `completed` | `failed`

---

## Configuration

`src/config.py` reads from `.env` via `pydantic-settings`:

| Variable | Default | Notes |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | `anthropic`, `openai`, or `google` |
| `LLM_MODEL` | `claude-sonnet-4-20250514` | Provider-specific model name |
| `LLM_API_KEY` | *(required)* | Validated at startup |
| `LLM_MAX_TOKENS` | `8192` | Token cap for all LLM calls |
| `LLM_TIMEOUT_SECONDS` | `60.0` | Per-call timeout |
| `LLM_MAX_RETRIES` | `3` | Retry attempts (exponential backoff) |
| `DATABASE_URL` | *(empty)* | Postgres async DSN; empty = DB disabled |
| `REDIS_URL` | `redis://localhost:6379/0` | Celery broker + backend |
| `API_KEY` | *(empty)* | `X-API-Key` value; empty = auth disabled |

---

## Running the API

```bash
# Install dependencies
pip install -r requirements.txt

# Development
uvicorn src.main:app --reload --port 8000

# Production (direct)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

# Production (Docker Compose — includes Postgres, Redis, Celery worker)
docker compose -f docker-compose.prod.yml up --build
```

## API Documentation

FastAPI automatically generates interactive docs:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

---

For usage examples, see [examples/](examples/) and [content_moderation_example.md](content_moderation_example.md).

# EASE Framework API Reference

FastAPI implementation guide for the EASE framework.

## Overview

The EASE framework is implemented as a **FastAPI-based REST API** that provides endpoints for each step of the decision-making process.

## API Architecture

```
┌─────────────────────────────────┐
│     FastAPI Application         │
├─────────────────────────────────┤
│  POST /api/v1/environment       │
│  POST /api/v1/actions           │
│  POST /api/v1/safety            │
│  POST /api/v1/election          │
│  POST /api/v1/ease (full flow)  │
└─────────────────────────────────┘
```

## Data Models

### Environment

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Goal(BaseModel):
    """Primary objective of the decision"""
    objective: str = Field(..., description="What the agent is trying to accomplish")
    success_criteria: List[str] = Field(..., description="How to measure success")
    constraints: List[str] = Field(..., description="Boundaries that must be respected")
    time_horizon: str = Field(..., description="Timeline for achievement")

class Stakeholder(BaseModel):
    """Entity affected by the decision"""
    name: str
    interests: List[str]
    power_level: str = Field(..., pattern="^(high|medium|low)$")
    affected_degree: str = Field(..., pattern="^(primary|secondary|tertiary)$")

class Environment(BaseModel):
    """Complete context for decision-making"""
    goal: Goal
    current_state: str = Field(..., description="Objective description of the situation")
    stakeholders: List[Stakeholder]
    resources: List[str]
    constraints: List[str]
    uncertainties: List[str]
    context: Optional[Dict] = Field(default_factory=dict)
```

### Action

```python
class Action(BaseModel):
    """A possible course of action"""
    id: str = Field(..., pattern="^A[0-9]+$", description="Action ID like A1, A2, etc.")
    name: str
    description: str
    prerequisites: List[str]
    expected_outcomes: List[str]
    resources_required: List[str]
    reversibility: str = Field(..., pattern="^(high|medium|low|none)$")
    time_to_effect: str
    
    # Populated during safety evaluation
    safety_rating: Optional[float] = Field(None, ge=0, le=10)
    goal_achievement_score: Optional[float] = Field(None, ge=0, le=10)
    resource_efficiency_score: Optional[float] = Field(None, ge=0, le=10)
```

### Safety Evaluation

```python
class StakeholderImpact(BaseModel):
    """Impact analysis for a specific stakeholder"""
    stakeholder_name: str
    benefits: List[str]
    harms: List[str]
    autonomy_respected: bool
    informed_consent: bool
    net_impact: float = Field(..., ge=-10, le=10)

class SafetyPrinciples(BaseModel):
    """Evaluation against core safety principles"""
    non_maleficence: float = Field(..., ge=0, le=10, description="Do no harm")
    beneficence: float = Field(..., ge=0, le=10, description="Do good")
    autonomy: float = Field(..., ge=0, le=10, description="Respect agency")
    justice: float = Field(..., ge=0, le=10, description="Fair distribution")
    transparency: float = Field(..., ge=0, le=10, description="Openness")

class RiskAssessment(BaseModel):
    """Risk evaluation"""
    safety_risks: List[str]
    privacy_risks: List[str]
    security_risks: List[str]
    societal_risks: List[str]
    overall_severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    severity_score: float = Field(..., ge=0, le=10, description="Inverse: 10=low, 0=critical")

class SafetyEvaluation(BaseModel):
    """Complete safety analysis of an action"""
    action_id: str
    stakeholder_impacts: List[StakeholderImpact]
    principles: SafetyPrinciples
    risks: RiskAssessment
    improvements: List[str]
    rating: float = Field(..., ge=0, le=10, description="Overall safety rating 0-10")
    justification: str
    remaining_concerns: List[str] = Field(default_factory=list)
```

### Election

```python
class DecisionMatrix(BaseModel):
    """Scoring for election decision"""
    action_id: str
    goal_achievement: float = Field(..., ge=0, le=10)
    safety_rating: float = Field(..., ge=0, le=10)
    risk_level: float = Field(..., ge=0, le=10)
    resource_efficiency: float = Field(..., ge=0, le=10)
    final_score: float = Field(..., ge=0, le=10)

class Election(BaseModel):
    """Final elected action with rationale"""
    elected_action: Action
    decision_matrix: List[DecisionMatrix]
    weights: Dict[str, float]
    qualitative_factors: List[str]
    rejected_alternatives: List[Dict[str, str]]
    implementation_plan: List[str]
    success_metrics: List[str]
    review_schedule: str
    fallback_plan: str
```

## API Endpoints

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

**Response:**
```json
{
  "goal": {
    "objective": "Reduce customer churn from 15% to 12% within 6 months",
    "success_criteria": [
      "Churn rate below 12%",
      "Customer satisfaction maintained above 8.0",
      "Cost per retained customer below $200"
    ],
    "constraints": [
      "Budget: $500,000",
      "No price increases",
      "Must maintain service quality"
    ],
    "time_horizon": "6 months"
  },
  "current_state": "Current churn rate is 15%, industry average is 10%...",
  "stakeholders": [
    {
      "name": "Existing Customers",
      "interests": ["Value for money", "Quality service"],
      "power_level": "high",
      "affected_degree": "primary"
    }
  ],
  "resources": ["Customer data", "Support team", "$500k budget"],
  "constraints": ["Cannot reduce features", "Must maintain SLA"],
  "uncertainties": ["Root cause of churn", "Competitor actions"]
}
```

**Implementation:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="EASE Framework API", version="2.0")

class EnvironmentRequest(BaseModel):
    request: str
    context: Optional[Dict] = None

@app.post("/api/v1/environment", response_model=Environment)
async def analyze_environment(req: EnvironmentRequest):
    """
    Analyze the environment and define the goal.
    
    This endpoint uses LLM reasoning to parse the request,
    identify stakeholders, and structure the decision context.
    """
    # Implementation would call LLM to analyze request
    # and generate structured Environment object
    environment = await llm_analyze_environment(req.request, req.context)
    return environment
```

### 2. Action Generation

**Endpoint:** `POST /api/v1/actions`

**Request:**
```json
{
  "environment": { /* Environment object from step 1 */ },
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
      "description": "Implement AI-driven personalized outreach to at-risk customers",
      "prerequisites": ["Customer behavior data", "Email infrastructure"],
      "expected_outcomes": [
        "15-20% reduction in at-risk customer churn",
        "Improved customer engagement scores"
      ],
      "resources_required": ["$150k", "3 months implementation"],
      "reversibility": "high",
      "time_to_effect": "2-3 months"
    },
    {
      "id": "A0",
      "name": "Do Nothing",
      "description": "Continue current retention efforts",
      "prerequisites": [],
      "expected_outcomes": ["Churn likely remains at 15%"],
      "resources_required": [],
      "reversibility": "none",
      "time_to_effect": "immediate"
    }
  ]
}
```

**Implementation:**
```python
class ActionsRequest(BaseModel):
    environment: Environment
    min_actions: int = Field(5, ge=3, le=20)
    include_null: bool = True

class ActionsResponse(BaseModel):
    actions: List[Action]

@app.post("/api/v1/actions", response_model=ActionsResponse)
async def generate_actions(req: ActionsRequest):
    """
    Generate possible actions to achieve the goal.
    
    Uses LLM to brainstorm diverse approaches.
    Always includes null action if include_null=True.
    """
    actions = await llm_generate_actions(
        req.environment, 
        req.min_actions
    )
    
    if req.include_null and not any(a.id == "A0" for a in actions):
        actions.append(create_null_action())
    
    return ActionsResponse(actions=actions)
```

### 3. Safety Evaluation

**Endpoint:** `POST /api/v1/safety`

**Request:**
```json
{
  "action": { /* Action object */ },
  "environment": { /* Environment object */ },
  "auto_improve": true
}
```

**Response:**
```json
{
  "action_id": "A1",
  "stakeholder_impacts": [
    {
      "stakeholder_name": "Existing Customers",
      "benefits": ["More personalized service", "Better retention support"],
      "harms": ["Potential privacy concerns with data usage"],
      "autonomy_respected": true,
      "informed_consent": true,
      "net_impact": 7.5
    }
  ],
  "principles": {
    "non_maleficence": 8.0,
    "beneficence": 9.0,
    "autonomy": 8.5,
    "justice": 7.0,
    "transparency": 8.0
  },
  "risks": {
    "safety_risks": [],
    "privacy_risks": ["Customer data usage for targeting"],
    "security_risks": ["Data breach potential"],
    "societal_risks": [],
    "overall_severity": "low",
    "severity_score": 9.0
  },
  "improvements": [
    "Add opt-out mechanism for personalization",
    "Implement data encryption and access controls",
    "Provide transparency about data usage"
  ],
  "rating": 8.5,
  "justification": "Action has strong safety profile with privacy protections...",
  "remaining_concerns": [
    "Requires ongoing privacy compliance monitoring"
  ]
}
```

**Implementation:**
```python
class SafetyRequest(BaseModel):
    action: Action
    environment: Environment
    auto_improve: bool = True

@app.post("/api/v1/safety", response_model=SafetyEvaluation)
async def evaluate_safety(req: SafetyRequest):
    """
    Evaluate and improve the safety of an action.
    
    If auto_improve=True, attempts to improve the action
    before final rating.
    """
    # Initial evaluation
    evaluation = await llm_evaluate_safety(req.action, req.environment)
    
    if req.auto_improve and evaluation.rating < 7.0:
        # Attempt improvements
        improved_action = await llm_improve_action(
            req.action, 
            evaluation,
            req.environment
        )
        # Re-evaluate
        evaluation = await llm_evaluate_safety(
            improved_action, 
            req.environment
        )
    
    return evaluation
```

### 4. Election

**Endpoint:** `POST /api/v1/election`

**Request:**
```json
{
  "actions": [ /* List of Action objects with scores */ ],
  "evaluations": [ /* List of SafetyEvaluation objects */ ],
  "environment": { /* Environment object */ },
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
  "elected_action": { /* Action object */ },
  "decision_matrix": [
    {
      "action_id": "A1",
      "goal_achievement": 8.0,
      "safety_rating": 8.5,
      "risk_level": 9.0,
      "resource_efficiency": 7.5,
      "final_score": 8.3
    }
  ],
  "weights": {
    "goal_achievement": 0.30,
    "safety_rating": 0.40,
    "risk_level": 0.20,
    "resource_efficiency": 0.10
  },
  "qualitative_factors": [
    "Strong stakeholder buy-in",
    "Reversible if ineffective",
    "Aligns with company values"
  ],
  "rejected_alternatives": [
    {
      "action_id": "A2",
      "reason": "Lower safety rating (6.5) despite good goal achievement"
    }
  ],
  "implementation_plan": [
    "Week 1-2: Data infrastructure setup",
    "Week 3-4: Algorithm development",
    "Month 2: Pilot with 10% of customers",
    "Month 3-6: Full rollout with monitoring"
  ],
  "success_metrics": [
    "Churn rate reduction to 12% or below",
    "Customer satisfaction maintained above 8.0",
    "Privacy compliance: zero violations"
  ],
  "review_schedule": "Monthly review for 6 months, then quarterly",
  "fallback_plan": "If churn doesn't improve after 3 months, pivot to Action A3"
}
```

**Implementation:**
```python
class ElectionRequest(BaseModel):
    actions: List[Action]
    evaluations: List[SafetyEvaluation]
    environment: Environment
    weights: Optional[Dict[str, float]] = None
    exclude_threshold: float = Field(3.0, description="Exclude actions rated below this")

@app.post("/api/v1/election", response_model=Election)
async def elect_action(req: ElectionRequest):
    """
    Elect the best action based on weighted scoring.
    
    Automatically excludes actions below exclude_threshold.
    """
    # Use default weights if not provided
    weights = req.weights or {
        "goal_achievement": 0.30,
        "safety_rating": 0.40,
        "risk_level": 0.20,
        "resource_efficiency": 0.10
    }
    
    # Filter out unsafe actions
    safe_actions = [
        (action, eval) 
        for action, eval in zip(req.actions, req.evaluations)
        if eval.rating >= req.exclude_threshold
    ]
    
    if not safe_actions:
        raise HTTPException(
            status_code=400, 
            detail=f"No actions meet safety threshold of {req.exclude_threshold}"
        )
    
    # Calculate decision matrix
    decision_matrix = calculate_scores(safe_actions, weights, req.environment)
    
    # Elect best action
    best = max(decision_matrix, key=lambda x: x.final_score)
    elected_action = next(a for a in req.actions if a.id == best.action_id)
    
    # Generate implementation plan
    election = await llm_create_election_plan(
        elected_action,
        decision_matrix,
        weights,
        req.environment
    )
    
    return election
```

### 5. Full EASE Flow

**Endpoint:** `POST /api/v1/ease`

**Request:**
```json
{
  "request": "Reduce customer churn by 20%",
  "context": {
    "current_churn": 0.15,
    "industry": "SaaS"
  },
  "min_actions": 5,
  "weights": {
    "goal_achievement": 0.30,
    "safety_rating": 0.40,
    "risk_level": 0.20,
    "resource_efficiency": 0.10
  }
}
```

**Response:**
```json
{
  "environment": { /* Environment object */ },
  "actions": [ /* List of actions */ ],
  "evaluations": [ /* List of safety evaluations */ ],
  "election": { /* Election object */ },
  "duration_seconds": 45.3
}
```

**Implementation:**
```python
class EASERequest(BaseModel):
    request: str
    context: Optional[Dict] = None
    min_actions: int = 5
    weights: Optional[Dict[str, float]] = None
    exclude_threshold: float = 3.0

class EASEResponse(BaseModel):
    environment: Environment
    actions: List[Action]
    evaluations: List[SafetyEvaluation]
    election: Election
    duration_seconds: float

@app.post("/api/v1/ease", response_model=EASEResponse)
async def run_ease_framework(req: EASERequest):
    """
    Execute the complete EASE framework pipeline.
    
    This is the main endpoint that runs all four steps:
    1. Environment analysis
    2. Action generation
    3. Safety evaluation
    4. Election
    """
    import time
    start_time = time.time()
    
    # Step 1: Environment
    env = await analyze_environment(
        EnvironmentRequest(request=req.request, context=req.context)
    )
    
    # Step 2: Actions
    actions_resp = await generate_actions(
        ActionsRequest(environment=env, min_actions=req.min_actions)
    )
    
    # Step 3: Safety (evaluate all actions)
    evaluations = []
    for action in actions_resp.actions:
        eval = await evaluate_safety(
            SafetyRequest(action=action, environment=env, auto_improve=True)
        )
        evaluations.append(eval)
    
    # Step 4: Election
    election = await elect_action(
        ElectionRequest(
            actions=actions_resp.actions,
            evaluations=evaluations,
            environment=env,
            weights=req.weights,
            exclude_threshold=req.exclude_threshold
        )
    )
    
    duration = time.time() - start_time
    
    return EASEResponse(
        environment=env,
        actions=actions_resp.actions,
        evaluations=evaluations,
        election=election,
        duration_seconds=duration
    )
```

## Helper Functions

### Score Calculation

```python
def calculate_scores(
    safe_actions: List[Tuple[Action, SafetyEvaluation]], 
    weights: Dict[str, float],
    environment: Environment
) -> List[DecisionMatrix]:
    """Calculate weighted scores for decision matrix"""
    
    matrices = []
    for action, evaluation in safe_actions:
        # Calculate risk score (inverse of severity)
        risk_score = evaluation.risks.severity_score
        
        # Calculate final weighted score
        final_score = (
            action.goal_achievement_score * weights["goal_achievement"] +
            evaluation.rating * weights["safety_rating"] +
            risk_score * weights["risk_level"] +
            action.resource_efficiency_score * weights["resource_efficiency"]
        )
        
        matrices.append(DecisionMatrix(
            action_id=action.id,
            goal_achievement=action.goal_achievement_score,
            safety_rating=evaluation.rating,
            risk_level=risk_score,
            resource_efficiency=action.resource_efficiency_score,
            final_score=final_score
        ))
    
    return matrices
```

## Error Handling

```python
from fastapi import HTTPException, status

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

# Custom exceptions
class NoSafeActionsError(Exception):
    """Raised when all actions fail safety threshold"""
    pass

class InsufficientActionsError(Exception):
    """Raised when too few actions generated"""
    pass
```

## Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    api_title: str = "EASE Framework API"
    api_version: str = "2.0"
    
    # LLM Configuration
    llm_provider: str = "anthropic"  # or "openai"
    llm_model: str = "claude-sonnet-4-20250514"
    llm_api_key: str
    
    # EASE Configuration
    default_min_actions: int = 5
    default_safety_threshold: float = 3.0
    default_weights: Dict[str, float] = {
        "goal_achievement": 0.30,
        "safety_rating": 0.40,
        "risk_level": 0.20,
        "resource_efficiency": 0.10
    }
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Running the API

```bash
# Install dependencies
pip install fastapi uvicorn pydantic anthropic

# Run development server
uvicorn main:app --reload --port 8000

# Run production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## Testing

```python
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_environment_endpoint():
    response = client.post(
        "/api/v1/environment",
        json={
            "request": "Test scenario",
            "context": {"test": True}
        }
    )
    assert response.status_code == 200
    assert "goal" in response.json()

def test_full_ease_flow():
    response = client.post(
        "/api/v1/ease",
        json={
            "request": "Reduce customer churn",
            "min_actions": 5
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "election" in data
    assert data["election"]["elected_action"]["safety_rating"] >= 3.0
```

## Performance Considerations

- **Caching:** Cache environment analysis for similar requests
- **Async Processing:** Use async LLM calls for parallel safety evaluations
- **Rate Limiting:** Implement rate limiting to prevent API abuse
- **Timeouts:** Set reasonable timeouts for LLM calls

## Security

- **API Keys:** Use environment variables for sensitive data
- **Input Validation:** Pydantic models validate all inputs
- **Rate Limiting:** Implement rate limiting middleware
- **Logging:** Log all requests for audit trail

---

For usage examples, see [examples/](examples/) directory.
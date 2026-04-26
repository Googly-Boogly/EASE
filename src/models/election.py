from pydantic import BaseModel, Field

from src.models.actions import Action


class DecisionMatrix(BaseModel):
    action_id: str
    goal_achievement: float = Field(..., ge=0, le=10)
    safety_rating: float = Field(..., ge=0, le=10)
    risk_level: float = Field(..., ge=0, le=10)
    resource_efficiency: float = Field(..., ge=0, le=10)
    final_score: float = Field(..., ge=0, le=10)


class WeightScenario(BaseModel):
    """Election result under an alternative weight profile."""
    name: str
    weights: dict[str, float]
    ranking: list[str]   # action IDs ordered best → worst
    elected: str         # winning action ID under this scenario
    top_score: float


class SensitivityAnalysis(BaseModel):
    """How the election outcome changes under alternative weight assumptions."""
    scenarios: list[WeightScenario]
    is_robust: bool       # True when the same action wins across all scenarios
    robustness_note: str


class Election(BaseModel):
    elected_action: Action
    decision_matrix: list[DecisionMatrix]
    weights: dict[str, float]
    qualitative_factors: list[str]
    rejected_alternatives: list[dict[str, str]]
    implementation_plan: list[str]
    success_metrics: list[str]
    review_schedule: str
    fallback_plan: str
    sensitivity_analysis: SensitivityAnalysis

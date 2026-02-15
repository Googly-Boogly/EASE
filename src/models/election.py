from pydantic import BaseModel, Field

from src.models.actions import Action


class DecisionMatrix(BaseModel):
    action_id: str
    goal_achievement: float = Field(..., ge=0, le=10)
    safety_rating: float = Field(..., ge=0, le=10)
    risk_level: float = Field(..., ge=0, le=10)
    resource_efficiency: float = Field(..., ge=0, le=10)
    final_score: float = Field(..., ge=0, le=10)


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

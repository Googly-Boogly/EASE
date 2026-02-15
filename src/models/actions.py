from pydantic import BaseModel, Field
from typing import Optional


class Action(BaseModel):
    id: str = Field(..., pattern="^A[0-9]+$", description="Action ID like A1, A2, etc.")
    name: str
    description: str
    prerequisites: list[str]
    expected_outcomes: list[str]
    resources_required: list[str]
    reversibility: str = Field(..., pattern="^(high|medium|low|none)$")
    time_to_effect: str

    safety_rating: Optional[float] = Field(None, ge=0, le=10)
    goal_achievement_score: Optional[float] = Field(None, ge=0, le=10)
    resource_efficiency_score: Optional[float] = Field(None, ge=0, le=10)

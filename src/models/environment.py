from pydantic import BaseModel, Field
from typing import Optional


class Goal(BaseModel):
    objective: str = Field(..., description="What the agent is trying to accomplish")
    success_criteria: list[str] = Field(..., description="How to measure success")
    constraints: list[str] = Field(..., description="Boundaries that must be respected")
    time_horizon: str = Field(..., description="Timeline for achievement")


class Stakeholder(BaseModel):
    name: str
    interests: list[str]
    power_level: str = Field(..., pattern="^(high|medium|low)$")
    affected_degree: str = Field(..., pattern="^(primary|secondary|tertiary)$")


class Environment(BaseModel):
    goal: Goal
    current_state: str = Field(..., description="Objective description of the situation")
    stakeholders: list[Stakeholder]
    resources: list[str]
    constraints: list[str]
    uncertainties: list[str]
    context: Optional[dict] = Field(default_factory=dict)

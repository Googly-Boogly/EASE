from pydantic import BaseModel, Field
from typing import Optional

from src.models.environment import Environment
from src.models.actions import Action
from src.models.safety import SafetyEvaluation
from src.models.election import Election


class EnvironmentRequest(BaseModel):
    request: str
    context: Optional[dict] = None


class ActionsRequest(BaseModel):
    environment: Environment
    min_actions: int = Field(5, ge=3, le=20)
    include_null: bool = True


class ActionsResponse(BaseModel):
    actions: list[Action]


class SafetyRequest(BaseModel):
    action: Action
    environment: Environment
    auto_improve: bool = True


class ElectionRequest(BaseModel):
    actions: list[Action]
    evaluations: list[SafetyEvaluation]
    environment: Environment
    weights: Optional[dict[str, float]] = None
    exclude_threshold: float = Field(
        3.0, description="Exclude actions rated below this"
    )


class EASERequest(BaseModel):
    request: str
    context: Optional[dict] = None
    min_actions: int = 5
    weights: Optional[dict[str, float]] = None
    exclude_threshold: float = 3.0


class EASEResponse(BaseModel):
    environment: Environment
    actions: list[Action]
    evaluations: list[SafetyEvaluation]
    election: Election
    duration_seconds: float

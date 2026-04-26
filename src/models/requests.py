from pydantic import BaseModel, Field, model_validator
from typing import Optional

from src.models.environment import Environment
from src.models.actions import Action
from src.models.safety import SafetyEvaluation
from src.models.election import Election

_WEIGHT_KEYS = frozenset({"goal_achievement", "safety_rating", "risk_level", "resource_efficiency"})


def _validate_weights(weights: dict) -> dict:
    if set(weights.keys()) != _WEIGHT_KEYS:
        raise ValueError(f"weights must contain exactly: {sorted(_WEIGHT_KEYS)}")
    total = sum(weights.values())
    if abs(total - 1.0) > 0.001:
        raise ValueError(f"weights must sum to 1.0, got {total:.4f}")
    return weights


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
    actions: list[Action]
    environment: Environment
    auto_improve: bool = True


class ElectionRequest(BaseModel):
    actions: list[Action]
    evaluations: list[SafetyEvaluation]
    environment: Environment
    weights: Optional[dict[str, float]] = None
    exclude_threshold: float = Field(3.0, ge=0.0, le=10.0)

    @model_validator(mode="after")
    def validate_weights(self):
        if self.weights is not None:
            _validate_weights(self.weights)
        return self


class EASERequest(BaseModel):
    request: str
    context: Optional[dict] = None
    min_actions: int = 5
    weights: Optional[dict[str, float]] = None
    exclude_threshold: float = 3.0

    @model_validator(mode="after")
    def validate_weights(self):
        if self.weights is not None:
            _validate_weights(self.weights)
        return self


class EASEResponse(BaseModel):
    environment: Environment
    actions: list[Action]
    evaluations: list[SafetyEvaluation]
    election: Election
    duration_seconds: float

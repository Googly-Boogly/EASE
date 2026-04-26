import time
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

from src.ai_security import check_injection, sanitize_input
from src.models import ActionsResponse
from src.models.requests import (
    EASERequest,
    EASEResponse,
    EnvironmentRequest,
    ActionsRequest,
    SafetyRequest,
    ElectionRequest,
)
from src.routers.environment import analyze_environment
from src.routers.actions import generate_actions
from src.routers.safety import evaluate_safety
from src.routers.election import elect_action

router = APIRouter(prefix="/api/v1", tags=["ease"])


class TaskSubmitResponse(BaseModel):
    task_id: str
    status: str = "pending"


@router.post("/ease", response_model=EASEResponse)
async def run_ease_framework(req: EASERequest) -> EASEResponse:
    """Execute the complete EASE framework pipeline.

    Runs all four steps in sequence:
    1. Environment analysis
    2. Action generation
    3. Safety evaluation (parallel across actions, parallel within each action)
    4. Election
    """
    start = time.time()

    sanitized = sanitize_input(req.request)
    injection = check_injection(sanitized)
    if injection.is_injection:
        raise HTTPException(status_code=400, detail="Prompt injection detected")

    environment = await analyze_environment(
        EnvironmentRequest(request=sanitized, context=req.context)
    )

    actions_resp: ActionsResponse = await generate_actions(
        ActionsRequest(environment=environment, min_actions=req.min_actions)
    )

    evaluations = await evaluate_safety(
        SafetyRequest(actions=actions_resp.actions, environment=environment, auto_improve=True)
    )

    election = await elect_action(
        ElectionRequest(
            actions=actions_resp.actions,
            evaluations=evaluations,
            environment=environment,
            weights=req.weights,
            exclude_threshold=req.exclude_threshold,
        )
    )

    return EASEResponse(
        environment=environment,
        actions=actions_resp.actions,
        evaluations=evaluations,
        election=election,
        duration_seconds=round(time.time() - start, 2),
    )


@router.post("/ease/submit", response_model=TaskSubmitResponse)
async def submit_ease_pipeline(req: EASERequest) -> TaskSubmitResponse:
    """Submit an EASE pipeline run as a background Celery task.

    Returns a task ID immediately. Poll ``/api/v1/tasks/{task_id}`` for status
    and the final result.
    """
    sanitized = sanitize_input(req.request)
    injection = check_injection(sanitized)
    if injection.is_injection:
        raise HTTPException(status_code=400, detail="Prompt injection detected")

    from src.workers import run_ease_task
    task = run_ease_task.delay(req.model_dump())
    return TaskSubmitResponse(task_id=task.id)

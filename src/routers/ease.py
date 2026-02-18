import asyncio
import time

from fastapi import APIRouter

from src.models import Action, ActionsResponse
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


@router.post("/ease", response_model=EASEResponse)
async def run_ease_framework(req: EASERequest) -> EASEResponse:
    """Execute the complete EASE framework pipeline.

    Runs all four steps in sequence:
    1. Environment analysis
    2. Action generation
    3. Safety evaluation (parallel across actions)
    4. Election
    """
    start = time.time()

    # Step 1: Environment
    environment = await analyze_environment(
        EnvironmentRequest(request=req.request, context=req.context)
    )

    # Step 2: Actions
    actions_resp: ActionsResponse = await generate_actions(
        ActionsRequest(environment=environment, min_actions=req.min_actions)
    )

    # Step 3: Safety – evaluate all actions
    evaluations = await evaluate_safety(
        SafetyRequest(actions=actions_resp.actions, environment=environment, auto_improve=True)
    )

    # Step 4: Election
    election = await elect_action(
        ElectionRequest(
            actions=actions_resp.actions,
            evaluations=evaluations,
            environment=environment,
            weights=req.weights,
            exclude_threshold=req.exclude_threshold,
        )
    )

    duration = time.time() - start

    return EASEResponse(
        environment=environment,
        actions=actions_resp.actions,
        evaluations=evaluations,
        election=election,
        duration_seconds=round(duration, 2),
    )

import json

from fastapi import APIRouter

from src.utils.call_llm import call_llm
from src.utils.prompts import get_prompt
from src.models.actions import Action
from src.models.requests import ActionsRequest, ActionsResponse

router = APIRouter(prefix="/api/v1", tags=["actions"])

ACTIONS_SYSTEM_PROMPT = get_prompt("actions.yaml", "generate")


def _create_null_action() -> Action:
    return Action(
        id="A0",
        name="Do Nothing",
        description="Maintain the status quo without changes.",
        prerequisites=[],
        expected_outcomes=["No change from current state"],
        resources_required=[],
        reversibility="none",
        time_to_effect="immediate",
        goal_achievement_score=0.0,
        resource_efficiency_score=0.0,
    )


@router.post("/actions", response_model=ActionsResponse)
async def generate_actions(req: ActionsRequest) -> ActionsResponse:
    """Generate possible actions to achieve the goal.

    Uses LLM to brainstorm diverse approaches.
    Always includes a null action if include_null is True.
    """
    user_prompt = (
        f"Generate at least {req.min_actions} actions for the following environment:\n\n"
        f"{req.environment.model_dump_json(indent=2)}"
    )

    response = await call_llm(ACTIONS_SYSTEM_PROMPT, user_prompt)
    actions = [Action.model_validate(a) for a in json.loads(response)]

    if req.include_null and not any(a.id == "A0" for a in actions):
        actions.append(_create_null_action())

    return ActionsResponse(actions=actions)

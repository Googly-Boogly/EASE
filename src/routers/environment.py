import json

from fastapi import APIRouter, HTTPException

from src.ai_security import check_injection, sanitize_input
from src.models.environment import Environment
from src.models.requests import EnvironmentRequest
from src.utils.call_llm import call_llm
from src.utils.prompts import get_prompt

router = APIRouter(prefix="/api/v1", tags=["environment"])

ENVIRONMENT_SYSTEM_PROMPT = get_prompt("environment.yaml", "analyze")


@router.post("/environment", response_model=Environment)
async def analyze_environment(req: EnvironmentRequest) -> Environment:
    """Analyze the environment and define the goal.

    Uses LLM reasoning to parse the request, identify stakeholders,
    and structure the decision context.
    """
    sanitized = sanitize_input(req.request)

    injection = check_injection(sanitized)
    if injection.is_injection:
        raise HTTPException(status_code=400, detail="Prompt injection detected")

    user_prompt_parts = [f"Request: {sanitized}"]
    if req.context:
        user_prompt_parts.append(f"Context: {json.dumps(req.context)}")
    user_prompt = "\n".join(user_prompt_parts)

    response = await call_llm(ENVIRONMENT_SYSTEM_PROMPT, user_prompt)
    environment = Environment.model_validate_json(response)
    return environment.model_copy(update={"context": req.context or {}})

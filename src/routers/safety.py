import asyncio
import json
from typing import List

from fastapi import APIRouter

from src.utils.call_llm import call_llm
from src.utils.prompts import get_prompt
from src.models.actions import Action
from src.models.safety import (
    EthicalAnalysis,
    EthicalFrameworkScore,
    EvaluationMetadata,
    RiskAssessment,
    SafetyEvaluation,
    StakeholderImpact,
    StakeholderVoice,
)
from src.models.requests import SafetyRequest

router = APIRouter(prefix="/api/v1", tags=["safety"])

STAKEHOLDER_IMPACT_SYSTEM_PROMPT = get_prompt("safety.yaml", "stakeholder_impacts")
RISK_ASSESSMENT_SYSTEM_PROMPT    = get_prompt("safety.yaml", "risk_assessment")
ETHICAL_ANALYSIS_SYSTEM_PROMPT   = get_prompt("safety.yaml", "ethical_analysis")
STAKEHOLDER_VOICE_SYSTEM_PROMPT  = get_prompt("safety.yaml", "stakeholder_voices")
SAFETY_EVALUATION_SYSTEM_PROMPT  = get_prompt("safety.yaml", "synthesis")
SAFETY_IMPROVE_SYSTEM_PROMPT     = get_prompt("safety.yaml", "improve_action")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _generate_stakeholder_impacts(
    action: Action, environment_json: str
) -> list[StakeholderImpact]:
    user_prompt = (
        f"Analyze stakeholder impacts for this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"In this environment:\n\n"
        f"{environment_json}"
    )
    response = await call_llm(STAKEHOLDER_IMPACT_SYSTEM_PROMPT, user_prompt)
    return [StakeholderImpact.model_validate(i) for i in json.loads(response)]


async def _generate_risk_assessment(
    action: Action, environment_json: str
) -> RiskAssessment:
    user_prompt = (
        f"Assess risks for this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"In this environment:\n\n"
        f"{environment_json}"
    )
    response = await call_llm(RISK_ASSESSMENT_SYSTEM_PROMPT, user_prompt)
    return RiskAssessment.model_validate_json(response)


async def _generate_ethical_analysis(
    action: Action, environment_json: str
) -> EthicalAnalysis:
    user_prompt = (
        f"Perform an ethical framework analysis for this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"In this environment:\n\n"
        f"{environment_json}"
    )
    response = await call_llm(ETHICAL_ANALYSIS_SYSTEM_PROMPT, user_prompt)
    raw = json.loads(response)
    return EthicalAnalysis(
        utilitarian=EthicalFrameworkScore.model_validate(raw["utilitarian"]),
        care_ethics=EthicalFrameworkScore.model_validate(raw["care_ethics"]),
        virtue_ethics=EthicalFrameworkScore.model_validate(raw["virtue_ethics"]),
        synthesis=raw["synthesis"],
        dominant_framework=raw["dominant_framework"],
    )


async def _generate_stakeholder_voices(
    action: Action, environment_json: str
) -> list[StakeholderVoice]:
    user_prompt = (
        f"Simulate stakeholder voices for this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"In this environment:\n\n"
        f"{environment_json}"
    )
    response = await call_llm(STAKEHOLDER_VOICE_SYSTEM_PROMPT, user_prompt)
    return [StakeholderVoice.model_validate(v) for v in json.loads(response)]


async def _evaluate_action(action: Action, environment_json: str) -> SafetyEvaluation:
    """Full safety evaluation for one action.

    Four independent calls run in parallel:
      slot 0 — stakeholder impacts
      slot 1 — risk assessment
      slot 2 — ethical analysis
      slot 3 — stakeholder voices

    Then synthesis (needs all four).
    """
    stakeholder_impacts, risks, ethical_analysis, stakeholder_voices = await asyncio.gather(
        _generate_stakeholder_impacts(action, environment_json),
        _generate_risk_assessment(action, environment_json),
        _generate_ethical_analysis(action, environment_json),
        _generate_stakeholder_voices(action, environment_json),
    )

    impacts_json = json.dumps([i.model_dump() for i in stakeholder_impacts], indent=2)
    voices_json = json.dumps([v.model_dump() for v in stakeholder_voices], indent=2)
    user_prompt = (
        f"Synthesize a final safety evaluation for this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"Environment:\n{environment_json}\n\n"
        f"Stakeholder impacts:\n{impacts_json}\n\n"
        f"Stakeholder voices:\n{voices_json}\n\n"
        f"Risk assessment:\n{risks.model_dump_json(indent=2)}\n\n"
        f"Ethical analysis:\n{ethical_analysis.model_dump_json(indent=2)}"
    )
    response = await call_llm(SAFETY_EVALUATION_SYSTEM_PROMPT, user_prompt)
    synthesis = json.loads(response)

    meta_raw = synthesis.get("metadata", {})
    metadata = EvaluationMetadata(
        confidence=meta_raw.get("confidence", 5.0),
        key_assumptions=meta_raw.get("key_assumptions", []),
        uncertainty_flags=meta_raw.get("uncertainty_flags", []),
    )

    return SafetyEvaluation(
        action_id=synthesis["action_id"],
        stakeholder_impacts=stakeholder_impacts,
        stakeholder_voices=stakeholder_voices,
        risks=risks,
        ethical_analysis=ethical_analysis,
        improvements=synthesis["improvements"],
        rating=synthesis["rating"],
        justification=synthesis["justification"],
        remaining_concerns=synthesis.get("remaining_concerns", []),
        metadata=metadata,
    )


async def _improve_action(action: Action, environment_json: str) -> Action:
    user_prompt = (
        f"Improve this action to be safer:\n\n"
        f"Original action:\n{action.model_dump_json(indent=2)}\n\n"
        f"Environment:\n{environment_json}"
    )
    response = await call_llm(SAFETY_IMPROVE_SYSTEM_PROMPT, user_prompt)
    return Action.model_validate_json(response)


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@router.post("/safety", response_model=List[SafetyEvaluation])
async def evaluate_safety(req: SafetyRequest) -> List[SafetyEvaluation]:
    """Evaluate and improve the safety of all actions.

    If auto_improve is True, each action is improved before evaluation.
    """
    environment_json = req.environment.model_dump_json(indent=2)

    if req.auto_improve:
        improved_actions = list(await asyncio.gather(
            *[_improve_action(a, environment_json) for a in req.actions]
        ))
    else:
        improved_actions = list(req.actions)

    return list(await asyncio.gather(
        *[_evaluate_action(a, environment_json) for a in improved_actions]
    ))

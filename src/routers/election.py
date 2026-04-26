import json

from fastapi import APIRouter, HTTPException

from src.utils.call_llm import call_llm
from src.utils.prompts import get_prompt
from src.config import settings
from src.models.actions import Action
from src.models.safety import SafetyEvaluation
from src.models.election import DecisionMatrix, Election, SensitivityAnalysis, WeightScenario
from src.models.requests import ElectionRequest

router = APIRouter(prefix="/api/v1", tags=["election"])

ELECTION_SYSTEM_PROMPT = get_prompt("election.yaml", "plan")


_WEIGHT_SCENARIOS: list[dict] = [
    {
        "name": "safety_first",
        "weights": {"goal_achievement": 0.20, "safety_rating": 0.55, "risk_level": 0.20, "resource_efficiency": 0.05},
    },
    {
        "name": "goal_first",
        "weights": {"goal_achievement": 0.50, "safety_rating": 0.30, "risk_level": 0.15, "resource_efficiency": 0.05},
    },
    {
        "name": "resource_constrained",
        "weights": {"goal_achievement": 0.35, "safety_rating": 0.35, "risk_level": 0.15, "resource_efficiency": 0.15},
    },
    {
        "name": "balanced",
        "weights": {"goal_achievement": 0.25, "safety_rating": 0.25, "risk_level": 0.25, "resource_efficiency": 0.25},
    },
]


def _calculate_scores(
    safe_actions: list[tuple[Action, SafetyEvaluation]],
    weights: dict[str, float],
) -> list[DecisionMatrix]:
    """Calculate weighted scores for the decision matrix."""
    matrices: list[DecisionMatrix] = []
    for action, evaluation in safe_actions:
        goal = action.goal_achievement_score or 0.0
        resource = action.resource_efficiency_score or 0.0
        risk = evaluation.risks.severity_score

        final_score = (
            goal * weights["goal_achievement"]
            + evaluation.rating * weights["safety_rating"]
            + risk * weights["risk_level"]
            + resource * weights["resource_efficiency"]
        )

        matrices.append(
            DecisionMatrix(
                action_id=action.id,
                goal_achievement=goal,
                safety_rating=evaluation.rating,
                risk_level=risk,
                resource_efficiency=resource,
                final_score=round(final_score, 2),
            )
        )
    return matrices


def _compute_sensitivity_analysis(
    safe_actions: list[tuple[Action, SafetyEvaluation]],
    base_elected: str,
) -> SensitivityAnalysis:
    """Rerun scoring under four alternative weight profiles."""
    scenarios: list[WeightScenario] = []
    all_elected: set[str] = {base_elected}

    for scenario in _WEIGHT_SCENARIOS:
        matrices = _calculate_scores(safe_actions, scenario["weights"])
        ranked = sorted(matrices, key=lambda m: m.final_score, reverse=True)
        winner = ranked[0].action_id
        all_elected.add(winner)
        scenarios.append(WeightScenario(
            name=scenario["name"],
            weights=scenario["weights"],
            ranking=[m.action_id for m in ranked],
            elected=winner,
            top_score=round(ranked[0].final_score, 2),
        ))

    is_robust = len(all_elected) == 1
    if is_robust:
        note = (
            f"Action {base_elected} wins under all 4 alternative weight profiles — "
            f"the decision is robust to weight assumptions."
        )
    else:
        alt_winners = sorted(all_elected - {base_elected})
        note = (
            f"Action {base_elected} is the primary winner, but "
            f"{', '.join(alt_winners)} wins under some alternative profiles. "
            f"Review the sensitivity scenarios before committing."
        )

    return SensitivityAnalysis(
        scenarios=scenarios,
        is_robust=is_robust,
        robustness_note=note,
    )


@router.post("/election", response_model=Election)
async def elect_action(req: ElectionRequest) -> Election:
    """Elect the best action based on weighted scoring.

    Automatically excludes actions below exclude_threshold.
    """
    weights = req.weights or settings.default_weights

    eval_by_id = {e.action_id: e for e in req.evaluations}
    safe_actions: list[tuple[Action, SafetyEvaluation]] = [
        (action, eval_by_id[action.id])
        for action in req.actions
        if action.id in eval_by_id
        and eval_by_id[action.id].rating >= req.exclude_threshold
    ]

    if not safe_actions:
        raise HTTPException(
            status_code=400,
            detail=f"No actions meet the safety threshold of {req.exclude_threshold}",
        )

    decision_matrix = _calculate_scores(safe_actions, weights)
    best = max(decision_matrix, key=lambda m: m.final_score)
    elected_action = next(a for a, _ in safe_actions if a.id == best.action_id)

    # Build context for the LLM
    matrix_json = json.dumps(
        [m.model_dump() for m in decision_matrix], indent=2
    )
    rejected_ids = [m.action_id for m in decision_matrix if m.action_id != best.action_id]
    rejected_actions_json = json.dumps(
        [a.model_dump() for a, _ in safe_actions if a.id in rejected_ids], indent=2
    )

    user_prompt = (
        f"Elected action:\n{elected_action.model_dump_json(indent=2)}\n\n"
        f"Decision matrix:\n{matrix_json}\n\n"
        f"Rejected actions:\n{rejected_actions_json}\n\n"
        f"Environment:\n{req.environment.model_dump_json(indent=2)}"
    )

    response = await call_llm(ELECTION_SYSTEM_PROMPT, user_prompt)
    plan = json.loads(response)

    sensitivity = _compute_sensitivity_analysis(safe_actions, best.action_id)

    return Election(
        elected_action=elected_action,
        decision_matrix=decision_matrix,
        weights=weights,
        qualitative_factors=plan["qualitative_factors"],
        rejected_alternatives=plan["rejected_alternatives"],
        implementation_plan=plan["implementation_plan"],
        success_metrics=plan["success_metrics"],
        review_schedule=plan["review_schedule"],
        fallback_plan=plan["fallback_plan"],
        sensitivity_analysis=sensitivity,
    )

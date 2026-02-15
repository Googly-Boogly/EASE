import json

from fastapi import APIRouter, HTTPException

from src.utils.call_llm import call_llm
from src.config import settings
from src.models.actions import Action
from src.models.safety import SafetyEvaluation
from src.models.election import DecisionMatrix, Election
from src.models.requests import ElectionRequest

router = APIRouter(prefix="/api/v1", tags=["election"])

ELECTION_SYSTEM_PROMPT = """\
You are the Election Planner for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

You are given:
1. The elected action (highest weighted score from the decision matrix).
2. The full decision matrix with scores for all candidate actions.
3. The environment context.

Your job is to produce the qualitative analysis and implementation plan for the \
elected action. You MUST return a single JSON object (no markdown, no commentary) \
matching this schema:

{
  "qualitative_factors": [
    "Important consideration not captured by the scores"
  ],
  "rejected_alternatives": [
    {
      "action_id": "A2",
      "reason": "Why this action was not elected"
    }
  ],
  "implementation_plan": [
    "Step 1: ...",
    "Step 2: ..."
  ],
  "success_metrics": [
    "Metric 1: target value",
    "Metric 2: target value"
  ],
  "review_schedule": "When and how often to evaluate if this was the right choice",
  "fallback_plan": "What to do if the elected action fails or produces unacceptable outcomes"
}

Rules:
- "qualitative_factors" should list 2-5 considerations beyond the numeric scores \
(reversibility, precedent, stakeholder buy-in, synergies, learning value).
- "rejected_alternatives" must include one entry per non-elected action, each with \
an "action_id" and a concise "reason" explaining why it scored lower or was less \
suitable.
- "implementation_plan" should be 4-8 concrete, time-boxed steps.
- "success_metrics" should be 2-5 measurable indicators tied to the environment's \
success criteria.
- "review_schedule" should specify frequency and duration (e.g. "Monthly review \
for 6 months, then quarterly").
- "fallback_plan" should name a specific backup action or mitigation strategy.

Example — elected action A2 (Enhanced Worker Training), rejected A1 and A3:

{
  "qualitative_factors": [
    "Strongest stakeholder buy-in: workers and union are supportive of training investments",
    "High reversibility: program can be adjusted or paused without sunk infrastructure costs",
    "Sets a positive precedent for investing in workforce development over automation",
    "Generates institutional knowledge that benefits future initiatives"
  ],
  "rejected_alternatives": [
    {
      "action_id": "A1",
      "reason": "Automated visual inspection scored well (8.1) but ranked lower due to higher upfront cost ($350k), worker displacement concerns, and cybersecurity risk. Could be reconsidered as a Phase 2 complement."
    },
    {
      "action_id": "A3",
      "reason": "Root cause analysis scored 7.3 — solid approach but introduces delay before any intervention begins and carries uncertainty about whether analysis will yield actionable findings."
    },
    {
      "action_id": "A0",
      "reason": "Do nothing is unacceptable given the 5.2% defect rate is above target and causing customer complaints."
    }
  ],
  "implementation_plan": [
    "Weeks 1-2: Conduct training needs assessment with production supervisors and union representatives",
    "Weeks 3-4: Design curriculum covering defect identification, prevention techniques, and quality mindset",
    "Weeks 5-6: Pilot training program with one shift (50 workers), collect feedback",
    "Weeks 7-8: Revise curriculum based on pilot feedback",
    "Months 3-4: Roll out training to remaining two shifts",
    "Month 5: Assess early defect-rate data and adjust program",
    "Month 6: Full program evaluation against success metrics"
  ],
  "success_metrics": [
    "Defect rate: below 3.5% by month 4, below 2% by month 6",
    "Training completion rate: 95% of production staff",
    "Worker satisfaction with training: above 7.5/10 in post-training survey",
    "First-time quality rate: improve by at least 15% from baseline"
  ],
  "review_schedule": "Biweekly defect-rate check for the first 3 months, monthly review for months 4-6, then quarterly for 1 year",
  "fallback_plan": "If defect rate has not improved below 4% by month 4, escalate to a hybrid approach combining training with a pilot of automated inspection at the highest-defect station (Action A1 scoped to 1 station)."
}

Return ONLY the JSON object. No explanation, no markdown fences."""


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
    )

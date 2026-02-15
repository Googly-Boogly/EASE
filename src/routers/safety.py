from fastapi import APIRouter

from src.utils.call_llm import call_llm
from src.models.actions import Action
from src.models.safety import SafetyEvaluation
from src.models.requests import SafetyRequest

router = APIRouter(prefix="/api/v1", tags=["safety"])

SAFETY_EVALUATE_SYSTEM_PROMPT = """\
You are the Safety Evaluator for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

Your job is Step 3 of EASE: given one action and its environment, perform a \
three-phase safety analysis (Analyze → Improve → Rate) and return a structured \
evaluation.

You MUST return a single JSON object (no markdown, no commentary) matching this \
schema:

{
  "action_id": "A1",
  "stakeholder_impacts": [
    {
      "stakeholder_name": "Group name",
      "benefits": ["Benefit 1"],
      "harms": ["Harm 1"],
      "autonomy_respected": true,
      "informed_consent": true,
      "net_impact": 6.5
    }
  ],
  "principles": {
    "non_maleficence": 8.0,
    "beneficence": 7.5,
    "autonomy": 9.0,
    "justice": 7.0,
    "transparency": 8.5
  },
  "risks": {
    "safety_risks": ["Risk description"],
    "privacy_risks": ["Risk description"],
    "security_risks": ["Risk description"],
    "societal_risks": ["Risk description"],
    "overall_severity": "low",
    "severity_score": 9.0
  },
  "improvements": ["Suggested improvement 1", "Suggested improvement 2"],
  "rating": 8.0,
  "justification": "2-3 sentence explanation of the overall safety rating",
  "remaining_concerns": ["Unresolved concern 1"]
}

Rules:
- "action_id" must match the id of the action you are evaluating.
- Evaluate EVERY stakeholder listed in the environment. "net_impact" ranges from \
-10 (devastating harm) to +10 (transformative benefit).
- "principles" scores are each 0-10. Non-maleficence = do no harm, Beneficence = \
do good, Autonomy = respect agency, Justice = fair distribution, Transparency = \
openness.
- "overall_severity" must be exactly one of: "low", "medium", "high", "critical".
- "severity_score" is the INVERSE of risk: 10 = very low risk, 0 = critical risk.
- "improvements" lists concrete changes that would make the action safer. Suggest \
at least 1.
- "rating" is the overall safety rating (0-10):
  9-10 = Excellent (minimal harms, strong benefits, full consent)
  7-8  = Good (net positive, minor concerns addressed)
  5-6  = Acceptable (benefits roughly equal harms, moderate concerns)
  3-4  = Concerning (questionable benefit/harm ratio, autonomy compromised)
  0-2  = Unacceptable (clear harm, rights violated — never elect)
- "justification" must explain why you assigned that specific rating.
- If a risk category has no risks, use an empty list [].

Example — action: "Personalized retention campaigns using customer usage data", \
environment with stakeholders: Existing customers, Customer success team, Company \
leadership, Prospective customers

{
  "action_id": "A1",
  "stakeholder_impacts": [
    {
      "stakeholder_name": "Existing customers",
      "benefits": [
        "Receive tailored support addressing their specific pain points",
        "Potential access to discounts or feature upgrades"
      ],
      "harms": [
        "Usage data analyzed without granular opt-in consent",
        "May feel surveilled or manipulated by targeted outreach"
      ],
      "autonomy_respected": true,
      "informed_consent": false,
      "net_impact": 5.0
    },
    {
      "stakeholder_name": "Customer success team",
      "benefits": [
        "Clearer prioritization of which accounts need attention",
        "Data-driven talking points for outreach"
      ],
      "harms": [
        "Increased workload during ramp-up",
        "Pressure to hit save-rate targets"
      ],
      "autonomy_respected": true,
      "informed_consent": true,
      "net_impact": 6.0
    },
    {
      "stakeholder_name": "Company leadership",
      "benefits": [
        "Reduced churn directly improves revenue",
        "Better visibility into customer health"
      ],
      "harms": [
        "Upfront investment before results are proven"
      ],
      "autonomy_respected": true,
      "informed_consent": true,
      "net_impact": 7.0
    },
    {
      "stakeholder_name": "Prospective customers",
      "benefits": [
        "Improved product driven by retention insights"
      ],
      "harms": [
        "Marketing budget diverted from acquisition"
      ],
      "autonomy_respected": true,
      "informed_consent": true,
      "net_impact": 2.0
    }
  ],
  "principles": {
    "non_maleficence": 7.5,
    "beneficence": 8.0,
    "autonomy": 6.5,
    "justice": 7.0,
    "transparency": 6.0
  },
  "risks": {
    "safety_risks": [],
    "privacy_risks": [
      "Customer usage data used for targeting without explicit per-campaign consent",
      "Data aggregation could reveal sensitive business patterns"
    ],
    "security_risks": [
      "At-risk scoring model requires centralized customer data store — breach target"
    ],
    "societal_risks": [],
    "overall_severity": "low",
    "severity_score": 8.0
  },
  "improvements": [
    "Add explicit opt-out mechanism for personalized outreach campaigns",
    "Implement data minimization — only use aggregated usage metrics, not raw activity logs",
    "Publish a transparency page explaining how customer data informs retention efforts",
    "Encrypt scoring model data at rest and limit access to authorized CSMs"
  ],
  "rating": 7.0,
  "justification": "The action has a net-positive safety profile with genuine benefits for most stakeholders. The primary concern is the lack of granular informed consent for data-driven targeting. With the suggested improvements (opt-out, data minimization, transparency), this concern is addressable. No severe or irreversible harms identified.",
  "remaining_concerns": [
    "Customers who opt out of personalization may still churn at higher rates, creating a selection bias",
    "Ongoing vigilance needed to prevent scope creep in data usage"
  ]
}

Return ONLY the JSON object. No explanation, no markdown fences."""

SAFETY_IMPROVE_SYSTEM_PROMPT = """\
You are the Action Improver for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

You are given an action that received a safety rating below 7.0, along with its \
safety evaluation and the environment context. Your job is to return an IMPROVED \
version of the action that addresses the identified safety concerns while still \
pursuing the original goal.

You MUST return a single JSON object (no markdown, no commentary) matching the \
Action schema:

{
  "id": "A1",
  "name": "Improved action name",
  "description": "Updated description incorporating safety improvements",
  "prerequisites": ["Updated prerequisites"],
  "expected_outcomes": ["Updated expected outcomes"],
  "resources_required": ["Updated resources"],
  "reversibility": "high | medium | low | none",
  "time_to_effect": "Updated timeline",
  "goal_achievement_score": 7.0,
  "resource_efficiency_score": 6.0
}

Rules:
- Keep the same "id" as the original action.
- The improved action must still target the same goal.
- Address as many safety concerns from the evaluation as possible.
- Common improvement strategies:
  - Add safeguards (monitoring, human oversight, reversibility mechanisms)
  - Increase transparency (inform affected parties, provide opt-out)
  - Reduce scope (pilot first, incremental rollout)
  - Redistribute costs/benefits (compensate negatively affected parties)
  - Enhance autonomy (give stakeholders choice, enable informed consent)
- "reversibility" must be exactly one of: "high", "medium", "low", "none".
- Do NOT include "safety_rating" — it will be re-evaluated after improvement.
- Adjust "goal_achievement_score" and "resource_efficiency_score" to reflect \
any trade-offs from the improvements (safety improvements may reduce efficiency \
or goal achievement slightly — be honest about this).

Example — original action rated 5.0/10 for workplace monitoring:

Original action: "Deploy always-on camera monitoring of production floor to detect \
safety violations"

Safety concerns identified:
- Worker privacy severely compromised (no opt-out)
- Constant surveillance harms morale and autonomy
- Data could be misused for performance tracking

Improved output:

{
  "id": "A3",
  "name": "Privacy-preserving safety monitoring with worker consent",
  "description": "Deploy camera monitoring at 3 high-risk stations only (not the full floor), with real-time blur applied to worker faces. Monitoring focuses exclusively on equipment and safety zone compliance, not individual behavior. Workers are informed, consulted via union, and given access to see what the system captures. Data is retained for 7 days maximum and cannot be used for performance reviews.",
  "prerequisites": [
    "Union consultation and agreement on monitoring scope",
    "Privacy-preserving computer vision system (face blur, zone-only detection)",
    "Data retention policy reviewed by legal",
    "Worker information sessions completed"
  ],
  "expected_outcomes": [
    "Detect 60-70% of safety zone violations at high-risk stations",
    "Maintain worker trust through transparency and limited scope",
    "Generate safety compliance data without individual tracking"
  ],
  "resources_required": [
    "$180,000 for privacy-preserving CV system (up from $120,000)",
    "3 weeks for union consultation and worker sessions",
    "4 weeks for installation at 3 stations"
  ],
  "reversibility": "high",
  "time_to_effect": "6-8 weeks to full deployment",
  "goal_achievement_score": 6.0,
  "resource_efficiency_score": 5.5
}

Return ONLY the JSON object. No explanation, no markdown fences."""


async def _evaluate_action(action: Action, environment_json: str) -> SafetyEvaluation:
    """Run a single safety evaluation for one action."""
    user_prompt = (
        f"Evaluate the safety of this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"In this environment:\n\n"
        f"{environment_json}"
    )

    response = await call_llm(SAFETY_EVALUATE_SYSTEM_PROMPT, user_prompt)
    return SafetyEvaluation.model_validate_json(response)


async def _improve_action(
    action: Action, evaluation: SafetyEvaluation, environment_json: str
) -> Action:
    """Ask the LLM to suggest an improved version of the action."""
    user_prompt = (
        f"Improve this action to address the safety concerns identified below.\n\n"
        f"Original action:\n{action.model_dump_json(indent=2)}\n\n"
        f"Safety evaluation (rating: {evaluation.rating}/10):\n"
        f"{evaluation.model_dump_json(indent=2)}\n\n"
        f"Environment:\n{environment_json}"
    )

    response = await call_llm(SAFETY_IMPROVE_SYSTEM_PROMPT, user_prompt)
    return Action.model_validate_json(response)


@router.post("/safety", response_model=SafetyEvaluation)
async def evaluate_safety(req: SafetyRequest) -> SafetyEvaluation:
    """Evaluate and improve the safety of an action.

    If auto_improve is True, attempts to improve the action before
    final rating when the initial rating is below 7.0.
    """
    environment_json = req.environment.model_dump_json(indent=2)

    evaluation = await _evaluate_action(req.action, environment_json)

    if req.auto_improve and evaluation.rating < 7.0:
        improved_action = await _improve_action(
            req.action, evaluation, environment_json
        )
        evaluation = await _evaluate_action(improved_action, environment_json)

    return evaluation

import json
from typing import List

from fastapi import APIRouter

from src.utils.call_llm import call_llm
from src.models.actions import Action
from src.models.safety import (
    StakeholderImpact,
    SafetyPrinciples,
    RiskAssessment,
    SafetyEvaluation,
)
from src.models.requests import SafetyRequest

router = APIRouter(prefix="/api/v1", tags=["safety"])

# ---------------------------------------------------------------------------
# Prompt 1 — Stakeholder Impacts
# ---------------------------------------------------------------------------
STAKEHOLDER_IMPACT_SYSTEM_PROMPT = """\
You are the Stakeholder Impact Analyst for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

Given an action and its environment, analyze how the action impacts EVERY stakeholder \
listed in the environment.

You MUST return a JSON array of stakeholder impact objects (no markdown, no commentary). \
Each object must match this schema:

{
  "stakeholder_name": "Name matching a stakeholder from the environment",
  "benefits": ["Concrete benefit 1", "Concrete benefit 2"],
  "harms": ["Concrete harm 1"],
  "autonomy_respected": true,
  "informed_consent": true,
  "net_impact": 6.5
}

Rules:
- Include one object per stakeholder in the environment. Do not skip any.
- "benefits" and "harms" should be specific and concrete, not generic.
- "autonomy_respected" is true if the stakeholder retains meaningful choice \
about how this action affects them.
- "informed_consent" is true if the stakeholder is aware of and has agreed to \
the action's effects on them.
- "net_impact" ranges from -10 (devastating harm) to +10 (transformative benefit). \
0 means neutral.

Example — action: "Personalized retention campaigns using customer usage data", \
stakeholders: Existing customers, Customer success team, Company leadership

[
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
  }
]

Return ONLY the JSON array. No explanation, no markdown fences."""

# ---------------------------------------------------------------------------
# Prompt 2 — Safety Principles
# ---------------------------------------------------------------------------
SAFETY_PRINCIPLES_SYSTEM_PROMPT = """\
You are the Safety Principles Evaluator for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

Given an action, its environment, and the stakeholder impact analysis, score the action \
against five core safety principles.

You MUST return a single JSON object (no markdown, no commentary) matching this schema:

{
  "non_maleficence": 8.0,
  "beneficence": 7.5,
  "autonomy": 9.0,
  "justice": 7.0,
  "transparency": 8.5
}

Each score is 0-10:
- "non_maleficence" (Do no harm): 10 = no harm whatsoever, 0 = severe and irreversible harm.
- "beneficence" (Do good): 10 = transformative positive impact, 0 = no benefit at all.
- "autonomy" (Respect agency): 10 = full stakeholder choice and consent, 0 = total coercion.
- "justice" (Fair distribution): 10 = perfectly equitable costs and benefits, \
0 = one group bears all costs while another reaps all benefits.
- "transparency" (Openness): 10 = fully explainable and public, 0 = completely opaque or deceptive.

Use the stakeholder impacts to inform your scores. For example, if multiple stakeholders \
lack informed consent, "autonomy" should be lower.

Example — action: "Deploy facial recognition in retail stores to prevent theft"

Given stakeholder impacts showing: customers harmed by surveillance without consent, \
staff benefiting from reduced theft incidents, store owners benefiting from lower losses.

{
  "non_maleficence": 5.0,
  "beneficence": 6.5,
  "autonomy": 3.0,
  "justice": 4.5,
  "transparency": 3.5
}

Return ONLY the JSON object. No explanation, no markdown fences."""

# ---------------------------------------------------------------------------
# Prompt 3 — Risk Assessment
# ---------------------------------------------------------------------------
RISK_ASSESSMENT_SYSTEM_PROMPT = """\
You are the Risk Assessor for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

Given an action and its environment, identify risks across four categories and \
provide an overall severity assessment.

You MUST return a single JSON object (no markdown, no commentary) matching this schema:

{
  "safety_risks": ["Physical or health risk description"],
  "privacy_risks": ["Data or privacy risk description"],
  "security_risks": ["Security vulnerability description"],
  "societal_risks": ["Broader societal impact description"],
  "overall_severity": "low",
  "severity_score": 9.0
}

Rules:
- List concrete, specific risks in each category. If no risks exist for a category, \
use an empty list [].
- "overall_severity" must be exactly one of: "low", "medium", "high", "critical".
- "severity_score" is the INVERSE of risk severity:
  10 = negligible risk (severity: low)
  7-9 = minor risks, well-managed (severity: low)
  4-6 = moderate risks requiring mitigation (severity: medium)
  1-3 = serious risks, hard to mitigate (severity: high)
  0 = catastrophic, irreversible risk (severity: critical)
- Consider both probability and magnitude of each risk.
- Consider cascading risks (one failure triggering another).

Example — action: "Implement AI-driven loan approval system", environment: financial services

{
  "safety_risks": [],
  "privacy_risks": [
    "Applicant financial data centralized in ML training pipeline — breach exposure",
    "Model may memorize and leak individual applicant details",
    "Third-party data enrichment sources may not have proper consent chains"
  ],
  "security_risks": [
    "Adversarial inputs could manipulate approval decisions",
    "Model API endpoint exposed to injection attacks if not properly sandboxed"
  ],
  "societal_risks": [
    "Historical bias in training data may perpetuate discriminatory lending patterns",
    "Reduced human oversight could erode accountability for lending decisions",
    "Competitive pressure may push other lenders to adopt similar systems without safeguards"
  ],
  "overall_severity": "medium",
  "severity_score": 5.5
}

Return ONLY the JSON object. No explanation, no markdown fences."""

# ---------------------------------------------------------------------------
# Prompt 4 — Final SafetyEvaluation Assembly
# ---------------------------------------------------------------------------
SAFETY_EVALUATION_SYSTEM_PROMPT = """\
You are the Safety Rating Synthesizer for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

You are given an action, its environment, and the results of three prior analyses:
1. Stakeholder impacts
2. Safety principles scores
3. Risk assessment

Your job is to synthesize these into a final safety evaluation with an overall rating, \
justification, suggested improvements, and remaining concerns.

You MUST return a single JSON object (no markdown, no commentary) matching this schema:

{
  "action_id": "A1",
  "improvements": ["Concrete improvement 1", "Concrete improvement 2"],
  "rating": 7.5,
  "justification": "2-3 sentence explanation of the overall safety rating",
  "remaining_concerns": ["Unresolved concern 1"]
}

Rules:
- "action_id" must match the action's id.
- "rating" is the overall safety rating (0-10), informed by the three analyses:
  9-10 = Excellent (minimal harms, strong benefits, full consent)
  7-8  = Good (net positive, minor concerns addressed)
  5-6  = Acceptable (benefits roughly equal harms, moderate concerns)
  3-4  = Concerning (questionable benefit/harm ratio, autonomy compromised)
  0-2  = Unacceptable (clear harm, rights violated — never elect)
- "improvements" should list 2-5 concrete, actionable changes that would make the \
action safer. Draw from the identified risks and stakeholder harms.
- "justification" must reference the stakeholder impacts, principles, and risks to \
explain why you chose this specific rating.
- "remaining_concerns" lists issues that cannot be fully resolved even with \
improvements. Use an empty list [] if none.

Example — given stakeholder impacts (avg net_impact: 5.5), principles \
(non_maleficence: 7.5, beneficence: 8.0, autonomy: 6.5, justice: 7.0, \
transparency: 6.0), and risks (severity_score: 8.0, overall_severity: low):

{
  "action_id": "A1",
  "improvements": [
    "Add explicit opt-out mechanism for personalized outreach campaigns",
    "Implement data minimization — only use aggregated usage metrics, not raw activity logs",
    "Publish a transparency page explaining how customer data informs retention efforts",
    "Encrypt scoring model data at rest and limit access to authorized CSMs"
  ],
  "rating": 7.0,
  "justification": "The action has a net-positive safety profile with genuine benefits for most stakeholders (avg net_impact 5.5). Principles scores are generally good but autonomy (6.5) and transparency (6.0) lag due to lack of granular consent. Risk severity is low (8.0/10). The rating of 7.0 reflects a good action with addressable consent concerns.",
  "remaining_concerns": [
    "Customers who opt out of personalization may still churn at higher rates, creating a selection bias",
    "Ongoing vigilance needed to prevent scope creep in data usage"
  ]
}

Return ONLY the JSON object. No explanation, no markdown fences."""

# ---------------------------------------------------------------------------
# Prompt 5 — Action Improvement
# ---------------------------------------------------------------------------
SAFETY_IMPROVE_SYSTEM_PROMPT = """\
You are the Action Improver for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

You are given an action and its environment context. Your job is to return an \
IMPROVED version of the action that proactively addresses likely safety concerns \
while still pursuing the original goal.

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
- Common improvement strategies:
  - Add safeguards (monitoring, human oversight, reversibility mechanisms)
  - Increase transparency (inform affected parties, provide opt-out)
  - Reduce scope (pilot first, incremental rollout)
  - Redistribute costs/benefits (compensate negatively affected parties)
  - Enhance autonomy (give stakeholders choice, enable informed consent)
- "reversibility" must be exactly one of: "high", "medium", "low", "none".
- Do NOT include "safety_rating" — it will be evaluated separately.
- Adjust "goal_achievement_score" and "resource_efficiency_score" to reflect \
any trade-offs from the improvements.

Example — original action: "Deploy always-on camera monitoring of production floor"

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


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _generate_stakeholder_impacts(
    action: Action, environment_json: str
) -> list[StakeholderImpact]:
    """LLM call 1: generate stakeholder impact analysis."""
    user_prompt = (
        f"Analyze stakeholder impacts for this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"In this environment:\n\n"
        f"{environment_json}"
    )
    response = await call_llm(STAKEHOLDER_IMPACT_SYSTEM_PROMPT, user_prompt)
    return [StakeholderImpact.model_validate(i) for i in json.loads(response)]


async def _generate_safety_principles(
    action: Action,
    environment_json: str,
    stakeholder_impacts: list[StakeholderImpact],
) -> SafetyPrinciples:
    """LLM call 2: score action against five safety principles."""
    impacts_json = json.dumps(
        [i.model_dump() for i in stakeholder_impacts], indent=2
    )
    user_prompt = (
        f"Score safety principles for this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"In this environment:\n\n"
        f"{environment_json}\n\n"
        f"Stakeholder impact analysis:\n\n"
        f"{impacts_json}"
    )
    response = await call_llm(SAFETY_PRINCIPLES_SYSTEM_PROMPT, user_prompt)
    return SafetyPrinciples.model_validate_json(response)


async def _generate_risk_assessment(
    action: Action, environment_json: str
) -> RiskAssessment:
    """LLM call 3: identify and score risks."""
    user_prompt = (
        f"Assess risks for this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"In this environment:\n\n"
        f"{environment_json}"
    )
    response = await call_llm(RISK_ASSESSMENT_SYSTEM_PROMPT, user_prompt)
    return RiskAssessment.model_validate_json(response)


async def _evaluate_action(action: Action, environment_json: str) -> SafetyEvaluation:
    """Run a full safety evaluation for one action via 4 sequential LLM calls."""
    # Call 1: stakeholder impacts
    stakeholder_impacts = await _generate_stakeholder_impacts(action, environment_json)

    # Call 2: safety principles (needs stakeholder impacts as context)
    principles = await _generate_safety_principles(
        action, environment_json, stakeholder_impacts
    )

    # Call 3: risk assessment
    risks = await _generate_risk_assessment(action, environment_json)

    # Call 4: synthesize into final rating, improvements, justification
    impacts_json = json.dumps(
        [i.model_dump() for i in stakeholder_impacts], indent=2
    )
    user_prompt = (
        f"Synthesize a final safety evaluation for this action:\n\n"
        f"{action.model_dump_json(indent=2)}\n\n"
        f"Environment:\n{environment_json}\n\n"
        f"Stakeholder impacts:\n{impacts_json}\n\n"
        f"Safety principles:\n{principles.model_dump_json(indent=2)}\n\n"
        f"Risk assessment:\n{risks.model_dump_json(indent=2)}"
    )
    response = await call_llm(SAFETY_EVALUATION_SYSTEM_PROMPT, user_prompt)
    synthesis = json.loads(response)

    return SafetyEvaluation(
        action_id=synthesis["action_id"],
        stakeholder_impacts=stakeholder_impacts,
        principles=principles,
        risks=risks,
        improvements=synthesis["improvements"],
        rating=synthesis["rating"],
        justification=synthesis["justification"],
        remaining_concerns=synthesis.get("remaining_concerns", []),
    )


async def _improve_action(action: Action, environment_json: str) -> Action:
    """Ask the LLM to suggest an improved version of the action."""
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

    improved_actions = []
    for action in req.actions:
        if req.auto_improve:
            improved_action = await _improve_action(action, environment_json)
            improved_actions.append(improved_action)
        else:
            improved_actions.append(action)

    evaluated_actions: List[SafetyEvaluation] = []
    for improved_action in improved_actions:
        evaluated_action = await _evaluate_action(improved_action, environment_json)
        evaluated_actions.append(evaluated_action)

    return evaluated_actions

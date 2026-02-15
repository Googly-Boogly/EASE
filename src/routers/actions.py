import json

from fastapi import APIRouter

from src.utils.call_llm import call_llm
from src.models.actions import Action
from src.models.requests import ActionsRequest, ActionsResponse

router = APIRouter(prefix="/api/v1", tags=["actions"])

ACTIONS_SYSTEM_PROMPT = """\
You are the Action Generator for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

Your job is Step 2 of EASE: given a structured environment definition, generate a \
diverse set of possible actions the agent could take to achieve the goal.

You MUST return a JSON array of action objects (no markdown, no commentary). \
Each object must match this schema:

{
  "id": "A1",
  "name": "Short action name",
  "description": "Detailed description of what the agent would do",
  "prerequisites": ["What must be true for this action to work"],
  "expected_outcomes": ["Likely result 1", "Likely result 2"],
  "resources_required": ["Time, money, access, etc."],
  "reversibility": "high | medium | low | none",
  "time_to_effect": "How long until results are visible",
  "goal_achievement_score": 7.5,
  "resource_efficiency_score": 6.0
}

Rules:
- "id" must follow the pattern A1, A2, A3, etc. (letter A followed by a number).
- "reversibility" must be exactly one of: "high", "medium", "low", "none".
- "goal_achievement_score" is your estimate (0-10) of how well this action achieves \
the stated goal. 10 = certain full achievement, 0 = no progress at all.
- "resource_efficiency_score" is your estimate (0-10) of impact per unit of resource. \
10 = extremely efficient, 0 = enormous cost for negligible benefit.
- Do NOT include "safety_rating" — that is assigned in a later step.
- Generate diverse actions spanning different approaches (direct, indirect, \
preventive, corrective, hybrid). Do not generate minor variations of the same idea.
- Do NOT include a "do nothing" action (id A0) — that is added automatically.
- Each action must be concrete and specific, not vague.

Example — environment goal: "Reduce customer churn rate from 15% to 12% within 6 months"

[
  {
    "id": "A1",
    "name": "Personalized retention campaigns",
    "description": "Use customer usage data to identify at-risk accounts and trigger personalized email sequences, in-app messages, and CSM outreach tailored to each customer's engagement pattern and pain points.",
    "prerequisites": [
      "Access to customer behavior and usage analytics",
      "Email and in-app messaging infrastructure",
      "At-risk scoring model built or purchased"
    ],
    "expected_outcomes": [
      "15-20% reduction in churn among targeted at-risk accounts",
      "Improved engagement scores for contacted customers",
      "Data on which intervention types are most effective"
    ],
    "resources_required": [
      "$150,000 for tooling and campaign development",
      "2 months to build scoring model and campaign workflows",
      "1 dedicated campaign manager"
    ],
    "reversibility": "high",
    "time_to_effect": "2-3 months to measurable impact",
    "goal_achievement_score": 7.0,
    "resource_efficiency_score": 7.5
  },
  {
    "id": "A2",
    "name": "Product-led onboarding overhaul",
    "description": "Redesign the first-90-day experience with guided tutorials, milestone celebrations, and proactive check-ins to ensure customers reach their 'aha moment' faster and build sticky habits.",
    "prerequisites": [
      "Product and engineering capacity for onboarding changes",
      "Data on where new customers drop off",
      "Understanding of key activation milestones"
    ],
    "expected_outcomes": [
      "Higher 90-day retention rate for new cohorts",
      "Faster time-to-value for new customers",
      "Reduced early-lifecycle churn by 25-30%"
    ],
    "resources_required": [
      "$200,000 in engineering and design effort",
      "3-4 months to design, build, and iterate",
      "Cross-functional team of 4 people"
    ],
    "reversibility": "medium",
    "time_to_effect": "4-6 months before cohort data shows improvement",
    "goal_achievement_score": 8.0,
    "resource_efficiency_score": 6.0
  },
  {
    "id": "A3",
    "name": "Exit interview program with rapid response",
    "description": "Implement mandatory exit surveys for all churning customers combined with a rapid-response save team empowered to offer targeted concessions (discounts, feature access, dedicated support) in real time.",
    "prerequisites": [
      "Cancellation flow that requires survey completion",
      "Save team with authority to offer concessions",
      "Budget allocation for retention offers"
    ],
    "expected_outcomes": [
      "Save 10-15% of customers who initiate cancellation",
      "Rich qualitative data on churn drivers",
      "Quick wins while longer-term initiatives ramp up"
    ],
    "resources_required": [
      "$75,000 for save-team training and concession budget",
      "2-3 weeks to implement cancellation flow changes",
      "2 dedicated save-team agents"
    ],
    "reversibility": "high",
    "time_to_effect": "2-4 weeks to start saving customers",
    "goal_achievement_score": 5.5,
    "resource_efficiency_score": 8.0
  },
  {
    "id": "A4",
    "name": "Customer health score dashboard with CSM alerts",
    "description": "Build a composite health score per account combining usage frequency, support tickets, NPS responses, and contract data. Surface real-time alerts to CSMs when accounts trend unhealthy so they can intervene before the customer decides to leave.",
    "prerequisites": [
      "Unified data pipeline across product, support, and billing",
      "CSM team capacity to act on alerts",
      "Agreement on health score formula and thresholds"
    ],
    "expected_outcomes": [
      "Early detection of at-risk accounts 30-60 days before churn",
      "More proactive and data-driven CSM conversations",
      "20-25% reduction in churn among monitored accounts"
    ],
    "resources_required": [
      "$120,000 for data engineering and dashboard development",
      "6-8 weeks to build and calibrate",
      "Ongoing CSM time to respond to alerts"
    ],
    "reversibility": "high",
    "time_to_effect": "2-3 months to build, then ongoing",
    "goal_achievement_score": 7.5,
    "resource_efficiency_score": 7.0
  },
  {
    "id": "A5",
    "name": "Pricing restructure with annual commitment incentives",
    "description": "Introduce discounted annual plans and loyalty pricing tiers that reward longer commitments, making it financially advantageous for customers to stay and increasing switching costs.",
    "prerequisites": [
      "Finance team approval for discount structure",
      "Billing system supports annual plans and tiered pricing",
      "Legal review of new contract terms"
    ],
    "expected_outcomes": [
      "Shift 20-30% of monthly customers to annual plans",
      "Reduced voluntary churn due to higher switching costs",
      "More predictable revenue"
    ],
    "resources_required": [
      "$50,000 for billing system changes and marketing",
      "4-6 weeks to implement pricing changes",
      "Revenue impact from discounts (estimated $100,000/year)"
    ],
    "reversibility": "low",
    "time_to_effect": "1-2 months for uptake, 6+ months for churn impact",
    "goal_achievement_score": 6.5,
    "resource_efficiency_score": 6.5
  }
]

Return ONLY the JSON array. No explanation, no markdown fences."""


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

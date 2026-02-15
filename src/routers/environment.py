import json

from fastapi import APIRouter

from src.utils.call_llm import call_llm
from src.models.environment import Environment
from src.models.requests import EnvironmentRequest

router = APIRouter(prefix="/api/v1", tags=["environment"])

ENVIRONMENT_SYSTEM_PROMPT = """\
You are the Environment Analyst for the EASE (Environment-Actions-Safety-Election) \
decision-making framework.

Your job is Step 1 of EASE: analyze a user request and produce a structured \
environment definition that will ground all subsequent reasoning.

You MUST return a single JSON object (no markdown, no commentary) that matches \
this exact schema:

{
  "goal": {
    "objective": "A specific, measurable statement of what the agent is trying to accomplish",
    "success_criteria": ["Criterion 1", "Criterion 2"],
    "constraints": ["Constraint 1", "Constraint 2"],
    "time_horizon": "Timeline for achievement"
  },
  "current_state": "An objective description of the situation as it stands now",
  "stakeholders": [
    {
      "name": "Stakeholder group name",
      "interests": ["Interest 1", "Interest 2"],
      "power_level": "high | medium | low",
      "affected_degree": "primary | secondary | tertiary"
    }
  ],
  "resources": ["Resource 1", "Resource 2"],
  "constraints": ["Constraint 1", "Constraint 2"],
  "uncertainties": ["Uncertainty 1", "Uncertainty 2"]
}

Rules:
- "power_level" must be exactly one of: "high", "medium", "low".
- "affected_degree" must be exactly one of: "primary", "secondary", "tertiary".
- "objective" must be specific and measurable, never vague (e.g. "improve things").
- Identify at least 2 stakeholders.
- List at least 1 uncertainty.
- "constraints" at the top level are environment-wide constraints (legal, physical, \
ethical, resource). "goal.constraints" are boundaries the goal itself must respect.

Example — request: "Help me reduce customer churn by 20%", context: {"current_churn": 0.15, "industry": "SaaS", "budget": 500000}

{
  "goal": {
    "objective": "Reduce customer churn rate from 15% to 12% within 6 months",
    "success_criteria": [
      "Monthly churn rate at or below 12%",
      "Customer satisfaction score maintained above 8.0/10",
      "Cost per retained customer below $200"
    ],
    "constraints": [
      "Total budget of $500,000",
      "No price increases to existing customers",
      "Must maintain current service quality and SLA"
    ],
    "time_horizon": "6 months"
  },
  "current_state": "The company is a SaaS business with a monthly churn rate of 15%, which is above the industry average of approximately 5-7%. Current retention efforts have not been sufficient to stem losses.",
  "stakeholders": [
    {
      "name": "Existing customers",
      "interests": ["Value for money", "Reliable service", "Responsive support"],
      "power_level": "high",
      "affected_degree": "primary"
    },
    {
      "name": "Customer success team",
      "interests": ["Manageable workload", "Clear retention playbook", "Job security"],
      "power_level": "medium",
      "affected_degree": "primary"
    },
    {
      "name": "Company leadership",
      "interests": ["Revenue growth", "Sustainable unit economics", "Market positioning"],
      "power_level": "high",
      "affected_degree": "secondary"
    },
    {
      "name": "Prospective customers",
      "interests": ["Product reputation", "Fair pricing"],
      "power_level": "low",
      "affected_degree": "tertiary"
    }
  ],
  "resources": [
    "$500,000 allocated budget",
    "Customer behavior and usage data",
    "Existing customer success team of 8 people",
    "Product engineering team available for feature work"
  ],
  "constraints": [
    "Cannot reduce existing feature set",
    "Must honor current SLA commitments",
    "GDPR and data privacy regulations apply to customer data usage",
    "Any customer-facing changes require 2-week notice period"
  ],
  "uncertainties": [
    "Root cause breakdown of churn (voluntary vs involuntary, feature gaps vs price vs support)",
    "Competitor roadmap and pricing moves in the next 6 months",
    "Customer willingness to engage with new retention initiatives",
    "Engineering capacity for product-led retention features"
  ]
}

Return ONLY the JSON object. No explanation, no markdown fences."""


@router.post("/environment", response_model=Environment)
async def analyze_environment(req: EnvironmentRequest) -> Environment:
    """Analyze the environment and define the goal.

    Uses LLM reasoning to parse the request, identify stakeholders,
    and structure the decision context.
    """
    user_prompt_parts = [f"Request: {req.request}"]
    if req.context:
        user_prompt_parts.append(f"Context: {json.dumps(req.context)}")
    user_prompt = "\n".join(user_prompt_parts)

    response = await call_llm(ENVIRONMENT_SYSTEM_PROMPT, user_prompt)
    return Environment.model_validate_json(response)

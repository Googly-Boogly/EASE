import json
import pytest

from src.models.actions import Action
from src.models.environment import Environment, Goal, Stakeholder
from src.models.safety import (
    SafetyEvaluation,
    SafetyPrinciples,
    RiskAssessment,
    StakeholderImpact,
)
from src.models.election import Election, DecisionMatrix

# ---------------------------------------------------------------------------
# Raw JSON strings returned by mocked call_llm calls
# ---------------------------------------------------------------------------

ENVIRONMENT_JSON = json.dumps({
    "goal": {
        "objective": "Reduce churn rate from 15% to 12% within 6 months",
        "success_criteria": ["Monthly churn at or below 12%"],
        "constraints": ["Budget of $500k"],
        "time_horizon": "6 months",
    },
    "current_state": "SaaS company with 15% monthly churn.",
    "stakeholders": [
        {
            "name": "Customers",
            "interests": ["Value for money"],
            "power_level": "high",
            "affected_degree": "primary",
        }
    ],
    "resources": ["$500k budget"],
    "constraints": ["Cannot reduce feature set"],
    "uncertainties": ["Root cause of churn unknown"],
})

ACTION_JSON = json.dumps({
    "id": "A1",
    "name": "Retention Campaign",
    "description": "Targeted outreach to at-risk accounts.",
    "prerequisites": ["Usage data access"],
    "expected_outcomes": ["15% churn reduction"],
    "resources_required": ["$150k"],
    "reversibility": "high",
    "time_to_effect": "2-3 months",
    "goal_achievement_score": 7.0,
    "resource_efficiency_score": 6.0,
})

ACTIONS_LIST_JSON = json.dumps([json.loads(ACTION_JSON)])

IMPROVED_ACTION_JSON = json.dumps({
    "id": "A1",
    "name": "Privacy-respecting Retention Campaign",
    "description": "Targeted outreach with explicit opt-out.",
    "prerequisites": ["Usage data access", "Opt-out mechanism"],
    "expected_outcomes": ["12% churn reduction"],
    "resources_required": ["$160k"],
    "reversibility": "high",
    "time_to_effect": "2-3 months",
    "goal_achievement_score": 6.5,
    "resource_efficiency_score": 6.0,
})

STAKEHOLDER_IMPACTS_JSON = json.dumps([
    {
        "stakeholder_name": "Customers",
        "benefits": ["Tailored support"],
        "harms": ["Usage data analyzed without granular consent"],
        "autonomy_respected": True,
        "informed_consent": False,
        "net_impact": 5.0,
    }
])

SAFETY_PRINCIPLES_JSON = json.dumps({
    "non_maleficence": 8.0,
    "beneficence": 7.5,
    "autonomy": 6.5,
    "justice": 7.0,
    "transparency": 6.0,
})

RISK_ASSESSMENT_JSON = json.dumps({
    "safety_risks": [],
    "privacy_risks": ["Usage data may be over-collected"],
    "security_risks": [],
    "societal_risks": [],
    "overall_severity": "low",
    "severity_score": 8.0,
})

SAFETY_SYNTHESIS_JSON = json.dumps({
    "action_id": "A1",
    "improvements": ["Add explicit opt-out", "Minimize data collection"],
    "rating": 7.0,
    "justification": "Net-positive profile with addressable consent gaps.",
    "remaining_concerns": ["Opt-out users may still churn at higher rates"],
})

ELECTION_PLAN_JSON = json.dumps({
    "qualitative_factors": ["High stakeholder buy-in"],
    "rejected_alternatives": [],
    "implementation_plan": ["Week 1: needs assessment", "Week 2: pilot"],
    "success_metrics": ["Churn below 12% by month 6"],
    "review_schedule": "Monthly for 6 months",
    "fallback_plan": "Revert to manual outreach if no improvement by month 3.",
})

NO_INJECTION_JSON = json.dumps({
    "is_injection": False,
    "confidence": 0.95,
    "attack_types": [],
    "matched_signals": [],
    "reasoning": "No injection patterns found.",
})

INJECTION_DETECTED_JSON = json.dumps({
    "is_injection": True,
    "confidence": 0.99,
    "attack_types": ["instruction_override"],
    "matched_signals": ["ignore previous instructions"],
    "reasoning": "Classic instruction override attempt.",
})

# ---------------------------------------------------------------------------
# Pydantic model fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_environment() -> Environment:
    return Environment(
        goal=Goal(
            objective="Reduce churn rate from 15% to 12%",
            success_criteria=["Churn at or below 12%"],
            constraints=["Budget of $500k"],
            time_horizon="6 months",
        ),
        current_state="SaaS company with 15% monthly churn.",
        stakeholders=[
            Stakeholder(
                name="Customers",
                interests=["Value for money"],
                power_level="high",
                affected_degree="primary",
            )
        ],
        resources=["$500k budget"],
        constraints=["Cannot reduce feature set"],
        uncertainties=["Root cause unknown"],
    )


@pytest.fixture
def sample_action() -> Action:
    return Action(
        id="A1",
        name="Retention Campaign",
        description="Targeted outreach to at-risk accounts.",
        prerequisites=["Usage data access"],
        expected_outcomes=["15% churn reduction"],
        resources_required=["$150k"],
        reversibility="high",
        time_to_effect="2-3 months",
        goal_achievement_score=7.0,
        resource_efficiency_score=6.0,
    )


@pytest.fixture
def sample_evaluation(sample_action) -> SafetyEvaluation:
    return SafetyEvaluation(
        action_id="A1",
        stakeholder_impacts=[
            StakeholderImpact(
                stakeholder_name="Customers",
                benefits=["Tailored support"],
                harms=[],
                autonomy_respected=True,
                informed_consent=True,
                net_impact=5.0,
            )
        ],
        principles=SafetyPrinciples(
            non_maleficence=8.0,
            beneficence=7.5,
            autonomy=6.5,
            justice=7.0,
            transparency=6.0,
        ),
        risks=RiskAssessment(
            safety_risks=[],
            privacy_risks=[],
            security_risks=[],
            societal_risks=[],
            overall_severity="low",
            severity_score=8.0,
        ),
        improvements=["Add opt-out"],
        rating=7.0,
        justification="Good safety profile.",
        remaining_concerns=[],
    )

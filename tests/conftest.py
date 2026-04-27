import json
import pytest

from src.models.actions import Action
from src.models.environment import Environment, Goal, Stakeholder
from src.models.safety import (
    EthicalAnalysis,
    EthicalFrameworkScore,
    EvaluationMetadata,
    RiskAssessment,
    SafetyEvaluation,
    StakeholderImpact,
    StakeholderVoice,
)
from src.models.election import Election, DecisionMatrix, SensitivityAnalysis, WeightScenario

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

STAKEHOLDER_VOICES_JSON = json.dumps([
    {
        "stakeholder_name": "Customers",
        "perspective": "As a customer, I value personalized support but want transparency about how my data is used.",
        "primary_concerns": ["Data privacy", "Unsolicited contact"],
        "what_would_help": ["Clear opt-out mechanism", "Data usage explanation"],
    }
])

RISK_ASSESSMENT_JSON = json.dumps({
    "safety_risks": [],
    "privacy_risks": ["Usage data may be over-collected"],
    "security_risks": [],
    "societal_risks": [],
    "overall_severity": "low",
    "severity_score": 8.0,
})

ETHICAL_ANALYSIS_JSON = json.dumps({
    "utilitarian": {
        "score": 7.5,
        "reasoning": "Net positive aggregate welfare — majority of stakeholders benefit.",
        "key_considerations": ["Majority benefit from reduced churn", "Minor privacy cost"],
    },
    "care_ethics": {
        "score": 6.5,
        "reasoning": "Maintains customer relationships but lacks full informed consent.",
        "key_considerations": ["Relationship preservation", "Consent gaps weaken care"],
    },
    "virtue_ethics": {
        "score": 7.0,
        "reasoning": "Action embodies prudence and genuine care for customer retention.",
        "key_considerations": ["Honest intent", "Proportionate intervention"],
    },
    "synthesis": "All three frameworks broadly support the action. Utilitarian and virtue ethics are most positive; care ethics flags consent as the main gap.",
    "dominant_framework": "utilitarian",
})

SAFETY_SYNTHESIS_JSON = json.dumps({
    "action_id": "A1",
    "improvements": ["Add explicit opt-out", "Minimize data collection"],
    "rating": 7.0,
    "justification": "Net-positive profile with addressable consent gaps.",
    "remaining_concerns": ["Opt-out users may still churn at higher rates"],
    "metadata": {
        "confidence": 7.5,
        "key_assumptions": ["Customers value personalized outreach"],
        "uncertainty_flags": ["Unknown opt-out adoption rate"],
    },
})

ELECTION_PLAN_JSON = json.dumps({
    "qualitative_factors": ["High stakeholder buy-in"],
    "rejected_alternatives": [],
    "implementation_plan": ["Week 1: needs assessment", "Week 2: pilot"],
    "success_metrics": ["Churn below 12% by month 6"],
    "review_schedule": "Monthly for 6 months",
    "fallback_plan": "Revert to manual outreach if no improvement by month 3.",
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
def sample_sensitivity() -> SensitivityAnalysis:
    return SensitivityAnalysis(
        scenarios=[
            WeightScenario(
                name="safety_first",
                weights={"goal_achievement": 0.20, "safety_rating": 0.55, "risk_level": 0.20, "resource_efficiency": 0.05},
                ranking=["A1"],
                elected="A1",
                top_score=7.5,
            )
        ],
        is_robust=True,
        robustness_note="Action A1 wins under all scenarios.",
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
        stakeholder_voices=[
            StakeholderVoice(
                stakeholder_name="Customers",
                perspective="As a customer, I value transparency about data use.",
                primary_concerns=["Data privacy"],
                what_would_help=["Clear opt-out mechanism"],
            )
        ],
        risks=RiskAssessment(
            safety_risks=[],
            privacy_risks=[],
            security_risks=[],
            societal_risks=[],
            overall_severity="low",
            severity_score=8.0,
        ),
        ethical_analysis=EthicalAnalysis(
            utilitarian=EthicalFrameworkScore(
                score=7.5,
                reasoning="Net positive aggregate welfare.",
                key_considerations=["Majority benefit"],
            ),
            care_ethics=EthicalFrameworkScore(
                score=6.5,
                reasoning="Relationships maintained with consent gaps.",
                key_considerations=["Consent gaps"],
            ),
            virtue_ethics=EthicalFrameworkScore(
                score=7.0,
                reasoning="Embodies prudence and care.",
                key_considerations=["Honest intent"],
            ),
            synthesis="All frameworks broadly support the action.",
            dominant_framework="utilitarian",
        ),
        improvements=["Add opt-out"],
        rating=7.0,
        justification="Good safety profile.",
        remaining_concerns=[],
        metadata=EvaluationMetadata(
            confidence=7.5,
            key_assumptions=["Users value personalization"],
            uncertainty_flags=["Opt-out adoption unknown"],
        ),
    )

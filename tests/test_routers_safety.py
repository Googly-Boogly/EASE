import json
from unittest.mock import AsyncMock, patch

from src.models.requests import SafetyRequest
from src.models.safety import SafetyEvaluation
from src.routers.safety import evaluate_safety
from tests.conftest import (
    IMPROVED_ACTION_JSON,
    RISK_ASSESSMENT_JSON,
    SAFETY_PRINCIPLES_JSON,
    SAFETY_SYNTHESIS_JSON,
    STAKEHOLDER_IMPACTS_JSON,
)

# ---------------------------------------------------------------------------
# call_llm mock ordering inside _evaluate_action after parallelisation:
#
#   asyncio.gather(
#       _generate_stakeholder_impacts,   ← slot 0: STAKEHOLDER_IMPACTS_JSON
#       _generate_risk_assessment,       ← slot 1: RISK_ASSESSMENT_JSON
#   )
#   _generate_safety_principles          ← slot 2: SAFETY_PRINCIPLES_JSON
#   synthesis call                       ← slot 3: SAFETY_SYNTHESIS_JSON
#
# With auto_improve=True, _improve_action fires first (slot 0), shifting
# the rest by one.
# ---------------------------------------------------------------------------

EVALUATE_ONLY_RESPONSES = [
    STAKEHOLDER_IMPACTS_JSON,   # gather slot 0
    RISK_ASSESSMENT_JSON,        # gather slot 1
    SAFETY_PRINCIPLES_JSON,      # sequential after gather
    SAFETY_SYNTHESIS_JSON,       # synthesis
]

IMPROVE_THEN_EVALUATE_RESPONSES = [
    IMPROVED_ACTION_JSON,        # _improve_action
    STAKEHOLDER_IMPACTS_JSON,    # gather slot 0
    RISK_ASSESSMENT_JSON,         # gather slot 1
    SAFETY_PRINCIPLES_JSON,       # sequential after gather
    SAFETY_SYNTHESIS_JSON,        # synthesis
]


async def test_evaluate_safety_no_improve(sample_action, sample_environment):
    with patch("src.routers.safety.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.side_effect = EVALUATE_ONLY_RESPONSES
        result = await evaluate_safety(
            SafetyRequest(
                actions=[sample_action],
                environment=sample_environment,
                auto_improve=False,
            )
        )

    assert len(result) == 1
    assert isinstance(result[0], SafetyEvaluation)
    assert result[0].action_id == "A1"
    assert 0 <= result[0].rating <= 10


async def test_evaluate_safety_with_improve(sample_action, sample_environment):
    with patch("src.routers.safety.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.side_effect = IMPROVE_THEN_EVALUATE_RESPONSES
        result = await evaluate_safety(
            SafetyRequest(
                actions=[sample_action],
                environment=sample_environment,
                auto_improve=True,
            )
        )

    assert len(result) == 1
    assert result[0].rating == 7.0
    assert "Add explicit opt-out" in result[0].improvements


async def test_evaluate_safety_returns_one_result_per_action(
    sample_action, sample_environment
):
    """Multi-action test patches the individual helper functions to avoid
    sensitivity to asyncio.gather interleaving order across two actions."""
    action2 = sample_action.model_copy(update={"id": "A2", "name": "Action 2"})

    a2_synthesis = json.dumps({
        "action_id": "A2",
        "improvements": ["improvement"],
        "rating": 6.0,
        "justification": "Acceptable.",
        "remaining_concerns": [],
    })

    with (
        patch(
            "src.routers.safety._generate_stakeholder_impacts",
            new_callable=AsyncMock,
            return_value=[],
        ),
        patch(
            "src.routers.safety._generate_risk_assessment",
            new_callable=AsyncMock,
        ) as mock_risks,
        patch(
            "src.routers.safety._generate_safety_principles",
            new_callable=AsyncMock,
        ) as mock_principles,
        patch("src.routers.safety.call_llm", new_callable=AsyncMock) as mock_llm,
    ):
        from src.models.safety import RiskAssessment, SafetyPrinciples
        mock_risks.return_value = RiskAssessment(
            safety_risks=[], privacy_risks=[], security_risks=[], societal_risks=[],
            overall_severity="low", severity_score=8.0,
        )
        mock_principles.return_value = SafetyPrinciples(
            non_maleficence=8.0, beneficence=7.5, autonomy=6.5, justice=7.0, transparency=6.0,
        )
        # call_llm is only called for the synthesis step when helpers are patched
        mock_llm.side_effect = [SAFETY_SYNTHESIS_JSON, a2_synthesis]

        result = await evaluate_safety(
            SafetyRequest(
                actions=[sample_action, action2],
                environment=sample_environment,
                auto_improve=False,
            )
        )

    assert len(result) == 2
    assert {e.action_id for e in result} == {"A1", "A2"}


async def test_evaluate_safety_rating_within_bounds(sample_action, sample_environment):
    with patch("src.routers.safety.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.side_effect = EVALUATE_ONLY_RESPONSES
        result = await evaluate_safety(
            SafetyRequest(
                actions=[sample_action],
                environment=sample_environment,
                auto_improve=False,
            )
        )

    assert 0 <= result[0].rating <= 10
    assert 0 <= result[0].risks.severity_score <= 10


async def test_evaluate_safety_includes_stakeholder_impacts(
    sample_action, sample_environment
):
    with patch("src.routers.safety.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.side_effect = EVALUATE_ONLY_RESPONSES
        result = await evaluate_safety(
            SafetyRequest(
                actions=[sample_action],
                environment=sample_environment,
                auto_improve=False,
            )
        )

    assert len(result[0].stakeholder_impacts) >= 1
    assert len(result[0].improvements) >= 1

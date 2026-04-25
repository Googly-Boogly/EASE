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

# Order of LLM calls for one action with auto_improve=True:
#   1. _improve_action         → IMPROVED_ACTION_JSON
#   2. _generate_stakeholder_impacts → STAKEHOLDER_IMPACTS_JSON
#   3. _generate_safety_principles   → SAFETY_PRINCIPLES_JSON
#   4. _generate_risk_assessment     → RISK_ASSESSMENT_JSON
#   5. synthesis (4th call in _evaluate_action) → SAFETY_SYNTHESIS_JSON

EVALUATE_ONLY_RESPONSES = [
    STAKEHOLDER_IMPACTS_JSON,
    SAFETY_PRINCIPLES_JSON,
    RISK_ASSESSMENT_JSON,
    SAFETY_SYNTHESIS_JSON,
]

IMPROVE_THEN_EVALUATE_RESPONSES = [
    IMPROVED_ACTION_JSON,
    STAKEHOLDER_IMPACTS_JSON,
    SAFETY_PRINCIPLES_JSON,
    RISK_ASSESSMENT_JSON,
    SAFETY_SYNTHESIS_JSON,
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
    import json
    action2 = sample_action.model_copy(update={"id": "A2", "name": "Action 2"})
    # 4 LLM calls per action (no improve), 2 actions = 8 calls
    responses = EVALUATE_ONLY_RESPONSES + [
        STAKEHOLDER_IMPACTS_JSON,
        SAFETY_PRINCIPLES_JSON,
        RISK_ASSESSMENT_JSON,
        json.dumps({
            "action_id": "A2",
            "improvements": ["improvement"],
            "rating": 6.0,
            "justification": "Acceptable.",
            "remaining_concerns": [],
        }),
    ]
    with patch("src.routers.safety.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.side_effect = responses
        result = await evaluate_safety(
            SafetyRequest(
                actions=[sample_action, action2],
                environment=sample_environment,
                auto_improve=False,
            )
        )

    assert len(result) == 2
    ids = {e.action_id for e in result}
    assert ids == {"A1", "A2"}


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

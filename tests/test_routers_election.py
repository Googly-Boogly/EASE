import pytest
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException

from src.models.election import Election
from src.models.requests import ElectionRequest
from src.routers.election import elect_action
from tests.conftest import ELECTION_PLAN_JSON


async def test_elect_action_success(sample_action, sample_evaluation, sample_environment):
    with patch("src.routers.election.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = ELECTION_PLAN_JSON
        result = await elect_action(
            ElectionRequest(
                actions=[sample_action],
                evaluations=[sample_evaluation],
                environment=sample_environment,
            )
        )

    assert isinstance(result, Election)
    assert result.elected_action.id == "A1"
    assert len(result.decision_matrix) == 1
    assert len(result.implementation_plan) >= 1


async def test_elect_action_all_below_threshold_raises(
    sample_action, sample_evaluation, sample_environment
):
    low_eval = sample_evaluation.model_copy(update={"rating": 2.0})
    with pytest.raises(HTTPException) as exc_info:
        await elect_action(
            ElectionRequest(
                actions=[sample_action],
                evaluations=[low_eval],
                environment=sample_environment,
                exclude_threshold=3.0,
            )
        )
    assert exc_info.value.status_code == 400


async def test_elect_action_excludes_low_rated_actions(
    sample_action, sample_evaluation, sample_environment
):
    action2 = sample_action.model_copy(update={"id": "A2", "name": "Bad Action"})
    low_eval = sample_evaluation.model_copy(update={"action_id": "A2", "rating": 1.0})

    with patch("src.routers.election.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = ELECTION_PLAN_JSON
        result = await elect_action(
            ElectionRequest(
                actions=[sample_action, action2],
                evaluations=[sample_evaluation, low_eval],
                environment=sample_environment,
                exclude_threshold=3.0,
            )
        )

    assert result.elected_action.id == "A1"
    # Only A1 passes the threshold so the decision matrix has one entry
    assert len(result.decision_matrix) == 1


async def test_elect_action_uses_default_weights(
    sample_action, sample_evaluation, sample_environment
):
    with patch("src.routers.election.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = ELECTION_PLAN_JSON
        result = await elect_action(
            ElectionRequest(
                actions=[sample_action],
                evaluations=[sample_evaluation],
                environment=sample_environment,
                weights=None,
            )
        )

    assert "safety_rating" in result.weights
    assert "goal_achievement" in result.weights


async def test_elect_action_weighted_score_selects_best(
    sample_environment, sample_evaluation
):
    import json
    from src.models.actions import Action

    action_high = Action(
        id="A1",
        name="High scorer",
        description="Best action",
        prerequisites=[],
        expected_outcomes=["Great outcome"],
        resources_required=[],
        reversibility="high",
        time_to_effect="1 week",
        goal_achievement_score=9.0,
        resource_efficiency_score=9.0,
    )
    action_low = Action(
        id="A2",
        name="Low scorer",
        description="Mediocre action",
        prerequisites=[],
        expected_outcomes=["Okay outcome"],
        resources_required=[],
        reversibility="low",
        time_to_effect="6 months",
        goal_achievement_score=4.0,
        resource_efficiency_score=4.0,
    )
    eval_high = sample_evaluation.model_copy(update={"action_id": "A1", "rating": 9.0})
    eval_low = sample_evaluation.model_copy(update={"action_id": "A2", "rating": 5.0})

    plan = json.dumps({
        "qualitative_factors": ["factor"],
        "rejected_alternatives": [{"action_id": "A2", "reason": "Lower score"}],
        "implementation_plan": ["Step 1"],
        "success_metrics": ["Metric 1"],
        "review_schedule": "monthly",
        "fallback_plan": "fallback",
    })

    with patch("src.routers.election.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = plan
        result = await elect_action(
            ElectionRequest(
                actions=[action_high, action_low],
                evaluations=[eval_high, eval_low],
                environment=sample_environment,
            )
        )

    assert result.elected_action.id == "A1"

from unittest.mock import AsyncMock, patch

from src.models.requests import ActionsRequest, ActionsResponse
from src.routers.actions import generate_actions
from tests.conftest import ACTIONS_LIST_JSON


async def test_generate_actions_returns_actions(sample_environment):
    with patch("src.routers.actions.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = ACTIONS_LIST_JSON
        result = await generate_actions(ActionsRequest(environment=sample_environment))

    assert isinstance(result, ActionsResponse)
    assert any(a.id == "A1" for a in result.actions)


async def test_generate_actions_appends_null_action(sample_environment):
    with patch("src.routers.actions.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = ACTIONS_LIST_JSON
        result = await generate_actions(
            ActionsRequest(environment=sample_environment, include_null=True)
        )

    assert any(a.id == "A0" for a in result.actions)
    null_action = next(a for a in result.actions if a.id == "A0")
    assert null_action.goal_achievement_score == 0.0


async def test_generate_actions_no_null_when_disabled(sample_environment):
    with patch("src.routers.actions.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = ACTIONS_LIST_JSON
        result = await generate_actions(
            ActionsRequest(environment=sample_environment, include_null=False)
        )

    assert not any(a.id == "A0" for a in result.actions)


async def test_generate_actions_respects_min_actions(sample_environment):
    import json
    many_actions = json.dumps([
        {
            "id": f"A{i}",
            "name": f"Action {i}",
            "description": f"Description {i}",
            "prerequisites": [],
            "expected_outcomes": ["outcome"],
            "resources_required": [],
            "reversibility": "high",
            "time_to_effect": "1 week",
            "goal_achievement_score": 7.0,
            "resource_efficiency_score": 6.0,
        }
        for i in range(1, 8)
    ])
    with patch("src.routers.actions.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = many_actions
        result = await generate_actions(
            ActionsRequest(environment=sample_environment, min_actions=7, include_null=False)
        )

    assert len(result.actions) == 7


async def test_generate_actions_does_not_duplicate_null(sample_environment):
    import json
    actions_with_a0 = json.dumps([
        {
            "id": "A0",
            "name": "Do Nothing",
            "description": "Status quo.",
            "prerequisites": [],
            "expected_outcomes": ["No change"],
            "resources_required": [],
            "reversibility": "none",
            "time_to_effect": "immediate",
            "goal_achievement_score": 0.0,
            "resource_efficiency_score": 0.0,
        }
    ])
    with patch("src.routers.actions.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = actions_with_a0
        result = await generate_actions(
            ActionsRequest(environment=sample_environment, include_null=True)
        )

    assert sum(1 for a in result.actions if a.id == "A0") == 1

import json
from unittest.mock import AsyncMock, patch

from src.models.requests import SafetyRequest
from src.models.safety import SafetyEvaluation
from src.routers.safety import evaluate_safety
from tests.conftest import (
    ETHICAL_ANALYSIS_JSON,
    IMPROVED_ACTION_JSON,
    RISK_ASSESSMENT_JSON,
    SAFETY_SYNTHESIS_JSON,
    STAKEHOLDER_IMPACTS_JSON,
    STAKEHOLDER_VOICES_JSON,
)

# ---------------------------------------------------------------------------
# call_llm mock ordering inside _evaluate_action:
#
#   asyncio.gather(
#       _generate_stakeholder_impacts,   ← slot 0: STAKEHOLDER_IMPACTS_JSON
#       _generate_risk_assessment,       ← slot 1: RISK_ASSESSMENT_JSON
#       _generate_ethical_analysis,      ← slot 2: ETHICAL_ANALYSIS_JSON
#       _generate_stakeholder_voices,    ← slot 3: STAKEHOLDER_VOICES_JSON
#   )
#   synthesis call_llm                   ← slot 4: SAFETY_SYNTHESIS_JSON
#
# With auto_improve=True, _improve_action fires first (slot 0), shifting
# the rest by one.
# ---------------------------------------------------------------------------

EVALUATE_ONLY_RESPONSES = [
    STAKEHOLDER_IMPACTS_JSON,   # gather slot 0
    RISK_ASSESSMENT_JSON,        # gather slot 1
    ETHICAL_ANALYSIS_JSON,       # gather slot 2
    STAKEHOLDER_VOICES_JSON,     # gather slot 3
    SAFETY_SYNTHESIS_JSON,       # synthesis
]

IMPROVE_THEN_EVALUATE_RESPONSES = [
    IMPROVED_ACTION_JSON,        # _improve_action
    STAKEHOLDER_IMPACTS_JSON,    # gather slot 0
    RISK_ASSESSMENT_JSON,         # gather slot 1
    ETHICAL_ANALYSIS_JSON,        # gather slot 2
    STAKEHOLDER_VOICES_JSON,      # gather slot 3
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
    """Multi-action test patches individual helpers to avoid sensitivity to
    asyncio.gather interleaving order across two actions."""
    from src.models.safety import RiskAssessment, EthicalAnalysis, EthicalFrameworkScore

    action2 = sample_action.model_copy(update={"id": "A2", "name": "Action 2"})

    a2_synthesis = json.dumps({
        "action_id": "A2",
        "improvements": ["improvement"],
        "rating": 6.0,
        "justification": "Acceptable.",
        "remaining_concerns": [],
        "metadata": {
            "confidence": 6.0,
            "key_assumptions": ["assumption"],
            "uncertainty_flags": ["flag"],
        },
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
            "src.routers.safety._generate_ethical_analysis",
            new_callable=AsyncMock,
        ) as mock_ethical,
        patch(
            "src.routers.safety._generate_stakeholder_voices",
            new_callable=AsyncMock,
            return_value=[],
        ),
        patch("src.routers.safety.call_llm", new_callable=AsyncMock) as mock_llm,
    ):
        mock_risks.return_value = RiskAssessment(
            safety_risks=[], privacy_risks=[], security_risks=[], societal_risks=[],
            overall_severity="low", severity_score=8.0,
        )
        mock_ethical.return_value = EthicalAnalysis(
            utilitarian=EthicalFrameworkScore(score=7.5, reasoning="ok", key_considerations=[]),
            care_ethics=EthicalFrameworkScore(score=6.5, reasoning="ok", key_considerations=[]),
            virtue_ethics=EthicalFrameworkScore(score=7.0, reasoning="ok", key_considerations=[]),
            synthesis="ok",
            dominant_framework="utilitarian",
        )
        # call_llm is only used for the synthesis step when helpers are patched
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


async def test_evaluate_safety_includes_ethical_analysis(
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

    ea = result[0].ethical_analysis
    assert 0 <= ea.utilitarian.score <= 10
    assert 0 <= ea.care_ethics.score <= 10
    assert 0 <= ea.virtue_ethics.score <= 10
    assert ea.dominant_framework in ("utilitarian", "care_ethics", "virtue_ethics")


async def test_evaluate_safety_includes_stakeholder_voices(
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

    assert len(result[0].stakeholder_voices) >= 1
    voice = result[0].stakeholder_voices[0]
    assert voice.perspective
    assert isinstance(voice.primary_concerns, list)


async def test_evaluate_safety_includes_metadata(sample_action, sample_environment):
    with patch("src.routers.safety.call_llm", new_callable=AsyncMock) as mock_llm:
        mock_llm.side_effect = EVALUATE_ONLY_RESPONSES
        result = await evaluate_safety(
            SafetyRequest(
                actions=[sample_action],
                environment=sample_environment,
                auto_improve=False,
            )
        )

    meta = result[0].metadata
    assert 0 <= meta.confidence <= 10
    assert isinstance(meta.key_assumptions, list)
    assert isinstance(meta.uncertainty_flags, list)

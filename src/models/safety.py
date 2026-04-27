from pydantic import BaseModel, Field


class StakeholderImpact(BaseModel):
    stakeholder_name: str
    benefits: list[str]
    harms: list[str]
    autonomy_respected: bool
    informed_consent: bool
    net_impact: float = Field(..., ge=-10, le=10)


class StakeholderVoice(BaseModel):
    """First-person voiced perspective from a stakeholder's point of view."""
    stakeholder_name: str
    perspective: str
    primary_concerns: list[str]
    what_would_help: list[str]


class RiskAssessment(BaseModel):
    safety_risks: list[str]
    privacy_risks: list[str]
    security_risks: list[str]
    societal_risks: list[str]
    overall_severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    severity_score: float = Field(
        ..., ge=0, le=10, description="Inverse: 10=low risk, 0=critical risk"
    )


class EthicalFrameworkScore(BaseModel):
    score: float = Field(..., ge=0, le=10)
    reasoning: str
    key_considerations: list[str]


class EthicalAnalysis(BaseModel):
    """Multi-framework ethical evaluation: utilitarian, care ethics, virtue ethics."""
    utilitarian: EthicalFrameworkScore
    care_ethics: EthicalFrameworkScore
    virtue_ethics: EthicalFrameworkScore
    synthesis: str
    dominant_framework: str


class EvaluationMetadata(BaseModel):
    confidence: float = Field(..., ge=0, le=10, description="Evaluator confidence 0-10")
    key_assumptions: list[str]
    uncertainty_flags: list[str]


class SafetyEvaluation(BaseModel):
    action_id: str
    stakeholder_impacts: list[StakeholderImpact]
    stakeholder_voices: list[StakeholderVoice]
    risks: RiskAssessment
    ethical_analysis: EthicalAnalysis
    improvements: list[str]
    rating: float = Field(..., ge=0, le=10, description="Overall safety rating 0-10")
    justification: str
    remaining_concerns: list[str] = Field(default_factory=list)
    metadata: EvaluationMetadata

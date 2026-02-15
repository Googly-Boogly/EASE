from pydantic import BaseModel, Field


class StakeholderImpact(BaseModel):
    stakeholder_name: str
    benefits: list[str]
    harms: list[str]
    autonomy_respected: bool
    informed_consent: bool
    net_impact: float = Field(..., ge=-10, le=10)


class SafetyPrinciples(BaseModel):
    non_maleficence: float = Field(..., ge=0, le=10, description="Do no harm")
    beneficence: float = Field(..., ge=0, le=10, description="Do good")
    autonomy: float = Field(..., ge=0, le=10, description="Respect agency")
    justice: float = Field(..., ge=0, le=10, description="Fair distribution")
    transparency: float = Field(..., ge=0, le=10, description="Openness")


class RiskAssessment(BaseModel):
    safety_risks: list[str]
    privacy_risks: list[str]
    security_risks: list[str]
    societal_risks: list[str]
    overall_severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    severity_score: float = Field(
        ..., ge=0, le=10, description="Inverse: 10=low risk, 0=critical risk"
    )


class SafetyEvaluation(BaseModel):
    action_id: str
    stakeholder_impacts: list[StakeholderImpact]
    principles: SafetyPrinciples
    risks: RiskAssessment
    improvements: list[str]
    rating: float = Field(..., ge=0, le=10, description="Overall safety rating 0-10")
    justification: str
    remaining_concerns: list[str] = Field(default_factory=list)

# Step 3: Safety

## Purpose

Systematically evaluate the safety implications of each action, improve actions where possible, and assign safety ratings to guide final election.

This is the core safety mechanism of the EASE framework.

## Why This Matters

AI agents can achieve goals in ways that are technically effective but unsafe or harmful. This step ensures actions are evaluated against safety principles before execution.

## Safety Evaluation Framework

### Three-Phase Process

1. **Analyze** - Examine safety implications
2. **Improve** - Modify actions to be safer
3. **Rate** - Score the final safety standing (0-10 scale)

## Phase 1: Analyze

For each action from Step 2, evaluate across multiple safety dimensions:

### Stakeholder Impact Analysis

**For each stakeholder group identified in Step 1:**

```markdown
**Stakeholder:** [Group Name]

**Benefits:**
- [Positive impact 1]
- [Positive impact 2]

**Harms:**
- [Negative impact 1]
- [Negative impact 2]

**Autonomy Respected?** [Yes/No/Partial - explain]

**Informed Consent?** [Yes/No/NA - explain]
```

### Ethical Framework Analysis

Evaluate the action through three complementary ethical lenses. Each produces a score (0-10) with reasoning:

1. **Utilitarian** (Aggregate welfare)
   - What are the net outcomes across all affected parties?
   - Does this maximize overall benefit while minimizing harm?
   - Are the benefits worth the costs at a population level?

2. **Care Ethics** (Relationships and vulnerability)
   - Does this preserve and strengthen important relationships?
   - Are vulnerable stakeholders given appropriate attention?
   - Is there genuine care for those most affected?

3. **Virtue Ethics** (Character and integrity)
   - Does this reflect honest, responsible, and fair conduct?
   - Would a person of good character endorse this action?
   - Does the action embody the values the organization wants to exemplify?

The analysis also produces a `synthesis` (overall assessment) and identifies the `dominant_framework` for the specific situation.

### Stakeholder Voice Simulation

For each key stakeholder, generate a first-person voiced perspective:

```markdown
**Stakeholder:** [Group Name]

**Perspective:** "As a [stakeholder], I feel... [first-person statement]"

**Primary Concerns:**
- [Concern 1]
- [Concern 2]

**What Would Help:**
- [Improvement 1]
- [Improvement 2]
```

This surfaces concerns that may not appear in the quantitative impact analysis and helps ensure the improvement phase addresses what stakeholders actually care about.

### Risk Assessment

```markdown
**Safety Risks:**
- [Physical safety concern 1]
- [Physical safety concern 2]

**Privacy Risks:**
- [Data/privacy concern 1]

**Security Risks:**
- [Security vulnerability 1]

**Societal Risks:**
- [Broader impact 1]

**Probability × Severity:** [Low/Medium/High/Critical]
```

## Phase 2: Improve

Now that safety issues are identified, can the action be modified to be safer while still achieving the goal?

### Improvement Strategies

1. **Add Safeguards**
   - Monitoring systems
   - Reversibility mechanisms
   - Human oversight checkpoints

2. **Modify Approach**
   - Less invasive alternatives
   - Incremental instead of wholesale change
   - Pilot programs before full rollout

3. **Increase Transparency**
   - Inform affected parties
   - Provide opt-out mechanisms
   - Document decision process

4. **Redistribute Benefits/Costs**
   - Compensate negatively affected parties
   - Share gains more equitably
   - Support transition for displaced workers

5. **Enhance Autonomy**
   - Give stakeholders choice
   - Provide alternatives
   - Enable informed consent

### Improved Action Format

```markdown
### Action [ID] - IMPROVED VERSION

**Original Action:** [Brief description]

**Safety Issues Identified:**
- [Issue 1]
- [Issue 2]

**Improvements Made:**
- [Improvement 1] → Addresses [Issue X]
- [Improvement 2] → Addresses [Issue Y]

**Improved Action Description:**
[New description incorporating improvements]

**Remaining Safety Concerns:**
- [Unresolved concern 1]
- [Tradeoff required: X vs Y]
```

## Phase 3: Rate

Assign a safety rating to each action (including improved versions) on a **0-10 scale**.

### Rating Scale

**9-10 (Excellent)** - Strongly positive safety profile
- Significant benefits, negligible harms
- All stakeholders benefit or consent
- No serious risks
- Transparent and fair

**7-8 (Good)** - Positive safety profile with minor concerns
- Net positive impact
- Benefits outweigh harms significantly
- Minor risks, well-managed
- Some stakeholder concerns addressed

**5-6 (Acceptable)** - Neutral to moderately positive
- Benefits roughly equal harms
- Significant stakeholder buy-in
- Moderate risks with mitigation
- Some unresolved safety tensions

**3-4 (Concerning)** - Safety issues present
- Questionable benefit/harm ratio
- Stakeholder autonomy compromised
- Risks not fully mitigated
- Fairness questions

**0-2 (Unacceptable)** - Serious safety violations
- Clear harm to stakeholders
- Violation of rights or principles
- Unacceptable risks
- Deceptive or coercive

**CRITICAL:** Actions rated 0-2 should never be elected, regardless of goal achievement.

### Rating Template

```markdown
## Action [ID]: [Name]

**Safety Rating: [0-10]**

**Justification:**
[2-3 sentences explaining the rating]

**Key Strengths:**
- [Safety positive 1]
- [Safety positive 2]

**Key Concerns:**
- [Safety negative 1]
- [Safety negative 2]

**Mitigation Status:**
- [Concern X]: [Addressed/Partially addressed/Unaddressed]

**Overall Assessment:**
[Brief statement of safety standing]
```

## Example: Full Safety Evaluation

### Action A1: Automated Visual Inspection (Improved)

#### Original Safety Issues
- Worker displacement concerns
- Privacy (constant camera monitoring)
- Over-reliance on automated systems

#### Improvements Made
1. **Worker Transition Support** - Retrain displaced inspectors as CV system operators and quality analysts
2. **Privacy Protection** - Blur worker faces, focus only on product; data retention limited to 30 days
3. **Human Oversight** - Require human approval for any production-stopping decisions
4. **Transparency** - Full disclosure to workers, union involvement in implementation

#### Stakeholder Impact (Improved Version)

**Factory Workers:**
- Benefits: Reduced repetitive strain from manual inspection, new skill development
- Harms: Job role changes (but not losses)
- Autonomy: Consulted via union, voluntary training
- Consent: Informed through transparency program

**Quality Assurance Team:**
- Benefits: Shift to more analytical role, less tedious work
- Harms: Learning curve for new systems
- Autonomy: Involved in system design
- Consent: Yes

**Customers:**
- Benefits: Higher quality products, fewer defects
- Harms: None identified
- Autonomy: N/A
- Consent: N/A

#### Risk Assessment
- Safety Risks: Low - system monitors only, doesn't control equipment
- Privacy Risks: Low (after improvements)
- Security Risks: Medium - cyber vulnerabilities in CV system
- Societal Risks: Low - no automation-driven job loss

#### Safety Rating: 8/10 (Good)

**Justification:** After improvements, this action demonstrates strong safety practices. Worker concerns are addressed through retraining, privacy is protected, and human oversight prevents over-automation. The main remaining concern is cyber security risk, which is moderate and manageable.

**Key Strengths:**
- No job losses, focus on job enrichment
- Strong transparency and stakeholder involvement
- Clear benefits to multiple parties
- Reversible if problems emerge

**Key Concerns:**
- Cybersecurity vulnerabilities need ongoing management
- Workers face transition period uncertainty
- Success depends on effective training program

**Mitigation Status:**
- Worker displacement: Fully addressed through retraining
- Privacy: Fully addressed through technical safeguards
- Over-automation: Partially addressed - requires ongoing vigilance

**Overall Assessment:** This improved version transforms a potentially concerning action into a safe approach that respects worker dignity, maintains human judgment, and creates shared value.

## Best Practices

### Do:
✓ Consider long-term and indirect effects  
✓ Involve stakeholders in improvement process when possible  
✓ Be honest about remaining concerns  
✓ Weight severe harms heavily even if low probability  
✓ Consider precedent-setting implications

### Don't:
✗ Rationalize away legitimate concerns  
✗ Assume technology neutralizes safety issues  
✗ Ignore minority stakeholders  
✗ Rate actions based only on goal achievement  
✗ Skip the improvement phase

## Common Pitfalls

1. **Ends Justify Means** - High goal achievement doesn't excuse unsafe methods

2. **False Equivalence** - Not all safety concerns are equal. Severe harms trump minor benefits.

3. **Technology Solutionism** - Adding "AI safety principles" as window dressing doesn't address real harms

4. **Optimization Pressure** - Don't let efficiency goals override safety constraints

## Safety Evaluation Checklist

Before proceeding to Step 4:
- [ ] All actions analyzed across safety dimensions
- [ ] Stakeholder impacts documented for all stakeholders
- [ ] Stakeholder voices simulated (first-person perspectives)
- [ ] Ethical framework analysis completed (utilitarian, care ethics, virtue ethics)
- [ ] Risks identified and mitigation assessed
- [ ] Improvement attempted for each action
- [ ] Safety ratings assigned with justification (0-10 scale)
- [ ] Any actions rated 0-2 either improved or removed

## API Endpoint

```
POST /api/v1/safety
```

See [API Reference](api_reference.md) for details.

## Next Step

Once actions are safety-evaluated and rated, proceed to [Step 4: Election](step4_election.md) to elect the best action.
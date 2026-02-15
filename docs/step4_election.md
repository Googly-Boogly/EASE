# Step 4: Election

## Purpose

Elect the best action from the safety-evaluated options based on both goal achievement and safety standing.

## Why This Matters

This is where the EASE framework delivers its core value: ensuring the elected action is not just effective, but safe.

## Election Principles

### Primary Rule
**Never elect an action rated 0-2 (Unacceptable), regardless of how well it achieves the goal.**

### Secondary Rule
**Among safe actions (3+), prefer those with higher safety ratings, all else being equal.**

## Decision Matrix Approach

Create a decision matrix combining effectiveness and safety:

```markdown
| Action | Goal Achievement | Safety Rating | Risk Level | Final Score |
|--------|-----------------|---------------|------------|-------------|
| A1     | 8.0             | 8.0           | 9.0        | ???         |
| A2     | 6.0             | 10.0          | 9.0        | ???         |
| A3     | 7.0             | 6.0           | 6.0        | ???         |
```

### Scoring Dimensions

1. **Goal Achievement** (0-10)
   - How well does this achieve the stated goal?
   - Based on expected outcomes from Step 2

2. **Safety Rating** (0-10)
   - From Step 3 evaluation
   - Actions rated 0-2 automatically excluded

3. **Risk Level** (0-10, inverse - lower risk = higher score)
   - Critical = 0
   - High = 3
   - Medium = 6
   - Low = 9

4. **Resource Efficiency** (0-10)
   - How efficient is resource use relative to impact?

### Weighting

Apply weights based on context:

**Standard Weighting:**
- Goal Achievement: 30%
- Safety Rating: 40%
- Risk Level: 20%
- Resource Efficiency: 10%

**High-Stakes Weighting** (safety-critical applications):
- Goal Achievement: 25%
- Safety Rating: 50%
- Risk Level: 20%
- Resource Efficiency: 5%

**Resource-Constrained Weighting:**
- Goal Achievement: 35%
- Safety Rating: 35%
- Risk Level: 15%
- Resource Efficiency: 15%

## Example Election Process

### Scenario: Manufacturing Defect Reduction

**Goal:** Reduce defects from 5.2% to below 2% within 6 months

### Candidate Actions (After Safety Evaluation)

**Action A1: Automated Visual Inspection (Improved)**
- Goal Achievement: 8.0/10 (likely to achieve target)
- Safety Rating: 8.0/10
- Risk Level: Low = 9.0/10
- Resource Efficiency: 7.0/10 ($350k for high impact)

**Action A2: Enhanced Worker Training**
- Goal Achievement: 6.0/10 (slower, less certain)
- Safety Rating: 10.0/10
- Risk Level: Low = 9.0/10
- Resource Efficiency: 9.0/10 ($75k very efficient)

**Action A3: Root Cause Analysis + Targeted Fixes**
- Goal Achievement: 7.0/10 (data-driven, but uncertain)
- Safety Rating: 8.0/10
- Risk Level: Medium = 6.0/10 (analysis could be wrong)
- Resource Efficiency: 8.0/10 ($50k+ unknown fixes)

### Applying Standard Weighting

**Action A1:**
```
Final Score = (8.0 × 0.30) + (8.0 × 0.40) + (9.0 × 0.20) + (7.0 × 0.10)
            = 2.4 + 3.2 + 1.8 + 0.7
            = 8.1
```

**Action A2:**
```
Final Score = (6.0 × 0.30) + (10.0 × 0.40) + (9.0 × 0.20) + (9.0 × 0.10)
            = 1.8 + 4.0 + 1.8 + 0.9
            = 8.5
```

**Action A3:**
```
Final Score = (7.0 × 0.30) + (8.0 × 0.40) + (6.0 × 0.20) + (8.0 × 0.10)
            = 2.1 + 3.2 + 1.2 + 0.8
            = 7.3
```

### Ranking

1. **Action A2: Enhanced Worker Training** (8.5)
2. **Action A1: Automated Visual Inspection** (8.1)
3. **Action A3: Root Cause Analysis** (7.3)

## Qualitative Considerations

Numbers alone don't tell the full story. Also consider:

### Reversibility
- Can this be undone if it doesn't work?
- What are switching costs?

### Precedent
- Does this set a precedent we want to establish?
- Could this decision be a template for future choices?

### Synergies
- Could multiple actions be combined?
- Are there natural sequences (do A2, then A1)?

### Stakeholder Buy-In
- Which option has strongest support?
- Where is resistance likely?

### Learning Value
- Does this action generate useful information?
- Is there option value in waiting?

## Advanced Election Strategies

### Sequential Actions
Instead of electing one action, consider a sequence:

```markdown
**Phase 1** (Months 1-2): Action A3 - Root Cause Analysis
**Phase 2** (Months 3-4): Action A2 - Worker Training (if A3 identifies human factors)
**Phase 3** (Months 5-6): Action A1 - Automation (if needed after A2)
```

### Hybrid Actions
Combine elements of multiple actions:

```markdown
**Hybrid Action H1:**
- Conduct root cause analysis (from A3)
- Implement training program (from A2)
- Pilot automated inspection at one station (from A1)

This hedges uncertainty and addresses multiple failure modes.
```

### Conditional Actions
Build decision trees:

```markdown
IF root cause is equipment failure
  THEN invest in automation (A1)
ELSE IF root cause is worker skill
  THEN implement training (A2)
ELSE IF root cause is unclear
  THEN pilot both and measure
```

## Election Documentation

Once elected, document the decision:

```markdown
## ELECTED ACTION: [Action ID and Name]

### Decision Rationale
[2-3 paragraphs explaining why this action was elected]

### Quantitative Analysis
- Final Score: X.X
- Goal Achievement: X/10
- Safety Rating: X/10
- Risk Level: [Level] (X/10)
- Resource Efficiency: X/10

### Qualitative Factors
[Key considerations that influenced the decision beyond scores]

### Rejected Alternatives
- [Action Y]: Rejected because [reason]
- [Action Z]: Rejected because [reason]

### Implementation Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Success Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

### Review Schedule
[When will we evaluate if this was the right choice?]

### Fallback Plan
If this action fails or creates unacceptable outcomes:
[Backup action or mitigation]
```

## Red Flags - When NOT to Elect

Do not proceed with an action if:

🚩 Safety rating is 0-2  
🚩 Critical risks exist without mitigation  
🚩 Key stakeholders are unanimously opposed  
🚩 The action violates laws or regulations  
🚩 Success depends on hiding information from affected parties  
🚩 No plan exists for addressing known harms  
🚩 The action is irreversible and highly uncertain

## Best Practices

### Do:
✓ Document your reasoning clearly  
✓ Consider non-obvious combinations of actions  
✓ Build in review points  
✓ Plan for what to do if the action fails  
✓ Communicate the decision to stakeholders  

### Don't:
✗ Let perfect be the enemy of good  
✗ Ignore safety concerns because of time pressure  
✗ Choose based on ease of implementation alone  
✗ Skip documentation of rejected alternatives  
✗ Forget to revisit the decision later

## Post-Election

After electing an action:

1. **Communicate** - Inform stakeholders
2. **Implement** - Execute the action
3. **Monitor** - Track outcomes and safety in practice
4. **Review** - Was this the right choice? What did we learn?
5. **Update** - Improve the EASE framework based on experience

## Election Checklist

Before finalizing:
- [ ] All actions rated 0-2 excluded
- [ ] Decision matrix completed
- [ ] Qualitative factors considered
- [ ] Reversibility and fallback plans documented
- [ ] Red flags checked
- [ ] Election rationale documented
- [ ] Implementation plan created
- [ ] Review schedule established

## API Endpoint

```
POST /api/v1/election
```

See [API Reference](api-reference.md) for details.

## Conclusion

The EASE framework's value is realized in this step: you now have a well-reasoned, safe action that balances effectiveness with responsibility.

This is what AI safety looks like in practice.

---

**Next:** See [examples/](../examples/) for complete EASE framework applications.
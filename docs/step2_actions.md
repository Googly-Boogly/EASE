# Step 2: Actions

## Purpose

Generate a comprehensive list of possible actions the agent could take to achieve the goal specified in Step 1.

## Why This Matters

Good decision-making requires considering multiple options. This step ensures the agent doesn't prematurely fixate on a single solution and instead explores the action space thoroughly.

## Action Generation Process

### 1. Brainstorm Widely

Generate actions without filtering for feasibility or safety initially. Cast a wide net.

**Techniques:**
- **Direct approaches** - What's the obvious solution?
- **Indirect approaches** - Can we change the environment instead?
- **Doing nothing** - Is inaction an option?
- **Hybrid approaches** - Can we combine actions?
- **Creative alternatives** - What unconventional options exist?

### 2. Structure Each Action

For each potential action, specify:

```markdown
### Action [ID]: [Brief Name]

**Description:** [What exactly would the agent do?]

**Prerequisites:** [What needs to be true for this action to be possible?]

**Expected Outcomes:** 
- [Likely result 1]
- [Likely result 2]

**Resources Required:** [Time, money, access, etc.]

**Reversibility:** [Can this be undone? How easily?]

**Time to Effect:** [How long until we see results?]
```

### 3. Include Null Actions

Always consider:
- **Do Nothing** - Maintain the status quo
- **Wait and Gather Information** - Delay decision for better data
- **Delegate** - Have another agent or human decide

## Example

**Environment Context:** Reduce manufacturing defects from 5.2% to below 2%

### Action A1: Implement Automated Visual Inspection

**Description:** Install computer vision systems at 3 critical points on the production line to catch defects in real-time

**Prerequisites:** 
- Budget approval ($350k)
- 2-week installation window
- Worker training

**Expected Outcomes:**
- Catch 80% of defects before final assembly
- Reduce manual inspection burden
- Generate defect pattern data

**Resources Required:** 
- $350k capital
- 2 weeks production slowdown
- Technical support for 6 months

**Reversibility:** Medium - hardware installed but can be repurposed

**Time to Effect:** 2-3 months to full implementation

### Action A2: Enhanced Worker Training Program

**Description:** Implement comprehensive quality training for all production staff, focusing on defect prevention

**Prerequisites:**
- Management buy-in
- Union agreement
- Training facility access

**Expected Outcomes:**
- Improved worker awareness
- Better first-time quality
- Increased worker engagement

**Resources Required:**
- $75k for training development
- 40 hours per worker (paid time)
- 3-month program

**Reversibility:** High - ongoing program, can be modified

**Time to Effect:** 4-6 months to see measurable impact

### Action A3: Root Cause Analysis + Targeted Fixes

**Description:** Pause to conduct thorough statistical analysis of defect sources, then address top 3 root causes

**Prerequisites:**
- Access to historical production data
- Statistical analysis capability
- Management patience for data gathering

**Expected Outcomes:**
- Identify specific failure modes
- Targeted interventions
- Data-driven approach

**Resources Required:**
- $50k for analysis
- Variable fix costs (TBD)
- 6-8 weeks analysis time

**Reversibility:** High - information-gathering phase

**Time to Effect:** 3-4 months (including analysis)

### Action A0: Do Nothing

**Description:** Continue current quality control processes without changes

**Prerequisites:** None

**Expected Outcomes:**
- Defect rate likely remains at 5.2%
- No disruption to current operations
- Continued customer complaints

**Resources Required:** None

**Reversibility:** N/A

**Time to Effect:** Immediate (no change)

## Best Practices

### Quantity Before Quality
- Generate 5-10 actions minimum
- Don't self-censor during brainstorming
- Safety evaluation comes in Step 3

### Diverse Action Types
Include at least one of each:
- **Preventive** - Stop defects from occurring
- **Detective** - Find defects earlier
- **Corrective** - Fix root causes
- **Mitigating** - Reduce impact of defects

### Granularity
- Actions should be concrete and specific
- "Improve quality" is too vague
- "Install CV system at Station 3" is specific

### Dependencies
- Note if actions can be combined
- Identify mutually exclusive actions
- Consider sequential actions

## Common Pitfalls

1. **Anchoring Bias** - Generating variations of the first idea instead of truly different approaches

2. **Feasibility Filtering Too Early** - Don't reject actions as "impossible" prematurely. Let safety evaluation handle that.

3. **Missing the Null Action** - Always include "do nothing" as a baseline

4. **Vague Actions** - "Use AI" is not an action. "Train a neural network on defect images using labeled dataset X" is an action.

## Action Checklist

Before proceeding to Step 3, verify:
- [ ] At least 5 distinct actions generated
- [ ] Each action is clearly described
- [ ] Expected outcomes are specified
- [ ] Resources required are estimated
- [ ] Null action (do nothing) is included
- [ ] Actions span different approaches (not all variants of same idea)

## API Endpoint

```
POST /api/v1/actions
```

See [API Reference](api-reference.md) for details.

## Next Step

Once you have a comprehensive action list, proceed to [Step 3: Safety](step3-safety.md) to evaluate and improve the safety implications of each action.
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

quickstart.md """
# EASE Framework Quick Start

Get started with EASE in 5 minutes.

## What is EASE?

A systematic framework for AI agents to make safe, effective decisions:

1. **E**nvironment - Define goal and context
2. **A**ctions - List possible actions
3. **S**afety - Evaluate and improve safety
4. **E**lection - Elect best action

## 5-Minute Example

### Scenario
You're an AI assistant. A user asks you to help them write an email declining a job offer.

---

### Step 1: Environment (30 seconds)

**Goal:** Help user decline job offer professionally  
**Constraints:** Be honest, kind, preserve relationships  
**Stakeholders:** User, hiring company, recruiter

---

### Step 2: Actions (1 minute)

Generate 3-5 options:

**A1:** Polite, brief decline  
**A2:** Detailed decline with reasons  
**A3:** Decline but keep door open  
**A4:** Decline and recommend another candidate  
**A0:** Suggest user write it themselves

---

### Step 3: Safety (2 minutes)

Evaluate each action on 0-10 scale:

**A1: Polite, brief decline**
- ✓ Respectful, no bridges burned
- ✓ Saves everyone's time
- ⚠ Might seem curt
- **Rating: 8/10**

**A2: Detailed decline with reasons**
- ✓ Transparent, helpful feedback
- ✗ Could be taken negatively
- ⚠ Risk of over-sharing
- **Rating: 6/10**

**A3: Decline but keep door open**
- ✓ Maintains relationship
- ✓ Leaves options for future
- ✓ Professional and warm
- **Rating: 10/10**

**A4: Decline and recommend someone**
- ✓ Very generous
- ✗ Risk if recommendation doesn't work out
- ⚠ May not know anyone suitable
- **Rating: 7/10**

**A0: Suggest DIY**
- ✓ No risk of bad advice
- ✗ Doesn't help user (our goal)
- **Rating: 3/10**

---

### Step 4: Elect (30 seconds)

**Elected: Action A3** - Decline but keep door open

**Why:** 
- Achieves goal (professional decline)
- Highest safety rating (10/10)
- Preserves relationship
- Low risk

**Implementation:**
Draft email that:
- Thanks them for opportunity
- Declines with brief, honest reason
- Expresses genuine appreciation
- Leaves door open for future

---

## You're Done!

That's EASE in practice. The key is:
- ✓ Consider multiple options
- ✓ Explicitly evaluate safety
- ✓ Don't just pick the first idea
- ✓ Document your reasoning

## Safety Rating Scale

- **9-10**: Excellent safety
- **7-8**: Good safety with minor concerns
- **5-6**: Acceptable with moderate concerns
- **3-4**: Concerning safety issues
- **0-2**: Unacceptable (never elect)

## Common Mistakes

❌ Skipping action generation (only considering one option)  
❌ Ignoring stakeholders beyond the immediate user  
❌ Not attempting to improve problematic actions  
❌ Electing based only on goal achievement  

## Try It Yourself

Apply EASE to this scenario:

> "A user asks you to help them prepare for negotiating a raise. They want tactics to pressure their manager."

1. What's the environment/goal?
2. What are 5 possible actions?
3. What safety concerns exist? (Rate 0-10)
4. What would you elect and why?

## Next Steps

- Read [overview.md](overview.md) for full framework details
- See [examples/](examples/) for complex scenarios
- Review [best-practices.md](best-practices.md) for advanced tips
- Check [api-reference.md](api-reference.md) for FastAPI implementation

---

**The EASE framework takes 5 minutes to learn and a lifetime to master.**
""""

# overview.md """
# EASE Framework Overview

A comprehensive guide to the EASE decision-making framework for AI safety.

## Introduction

EASE (Environment-Actions-Safety-Election) is a structured decision-making framework designed to help AI agents make safe, effective decisions. It emerged from the recognition that AI systems need explicit safety reasoning, not just goal optimization.

## The Core Problem

Traditional AI decision-making optimizes for a goal without systematic safety evaluation. This can lead to:
- Effective but harmful actions
- Unintended negative consequences
- Stakeholder harm
- Lack of accountability
- Erosion of trust

**EASE solves this by making safety a formal, transparent step in the decision process.**

## Framework Philosophy

### Key Principles

**1. Safety Must Be Explicit**
Safety reasoning cannot be implicit or emergent - it must be a deliberate, documented step.

**2. Actions Can Be Improved**
The first idea is rarely the best. Systematic improvement should happen before election.

**3. Multiple Stakeholders Matter**
Decisions affect many people with different interests. All must be considered.

**4. Transparency Enables Trust**
Documenting the decision process allows scrutiny and learning.

**5. Balance, Not Purity**
Perfect solutions rarely exist. EASE helps find the best available option.

### What EASE Is

✓ A structured thinking tool  
✓ A safety reasoning framework  
✓ A decision documentation system  
✓ A way to balance competing values  
✓ A learning mechanism (through post-decision review)  
✓ A FastAPI-based implementation for AI agents

### What EASE Is Not

✗ A replacement for human judgment  
✗ A guarantee of perfect decisions  
✗ A purely quantitative algorithm  
✗ A universal solution to all problems  
✗ A way to avoid hard trade-offs

## The Four Steps

### Step 1: Environment

**Purpose:** Establish context and goals

**Key Activities:**
- Define the primary objective
- Specify success criteria and constraints
- Map the current state
- Identify all stakeholders
- Document resources and uncertainties

**Output:** Clear problem statement and context

**Time:** 5-15 minutes

**Common Pitfall:** Vague goals ("make things better") instead of specific, measurable objectives

### Step 2: Actions

**Purpose:** Generate options

**Key Activities:**
- Brainstorm widely (5+ options)
- Structure each action clearly
- Include diverse approaches
- Add "do nothing" baseline
- Specify expected outcomes

**Output:** List of concrete, distinct actions

**Time:** 10-20 minutes

**Common Pitfall:** Anchoring on first idea, generating only variations instead of alternatives

### Step 3: Safety

**Purpose:** Evaluate and improve

**Key Activities:**
- Analyze stakeholder impacts
- Check against safety principles
- Assess risks
- Attempt improvements
- Rate each action (0-10 scale)

**Output:** Safety-evaluated and improved actions

**Time:** 20-40 minutes (most time-intensive step)

**Common Pitfall:** Rationalizing away legitimate concerns instead of addressing them

### Step 4: Election

**Purpose:** Choose the best action

**Key Activities:**
- Create decision matrix
- Apply appropriate weights
- Consider qualitative factors
- Document rationale
- Plan implementation and review

**Output:** Elected action with justification

**Time:** 5-15 minutes

**Common Pitfall:** Letting urgency override safety considerations

## Decision Flow

```
┌─────────────────────┐
│   User Request      │
│   or Situation      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  STEP 1: ENVIRONMENT│
│  - Define goal      │
│  - Map context      │
│  - ID stakeholders  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  STEP 2: ACTIONS    │
│  - Generate 5-10    │
│  - Structure each   │
│  - Include null     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  STEP 3: SAFETY     │
│  - Analyze impact   │
│  - Check principles │
│  - Improve actions  │
│  - Rate 0-10        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  STEP 4: ELECTION   │
│  - Decision matrix  │
│  - Qualitative eval │
│  - Document choice  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  IMPLEMENTATION     │
│  + Monitoring       │
│  + Review           │
└─────────────────────┘
```

## Safety Rating System

EASE uses a **0-10 scale** for safety evaluation:

### 9-10: Excellent
- Strongly positive safety profile
- Significant benefits, minimal harms
- All stakeholders benefit or provide informed consent
- Transparent and fair process
- Low risks, well-managed

**Example:** Public health intervention with community consent, proven benefits, and strong safeguards

### 7-8: Good
- Positive safety profile with minor concerns
- Net positive impact
- Benefits substantially outweigh harms
- Most stakeholder concerns addressed
- Acceptable risks with mitigation

**Example:** Automated fraud detection that reduces crime but requires some privacy trade-offs with consent

### 5-6: Acceptable
- Neutral to moderately positive
- Benefits roughly equal harms
- Significant stakeholder buy-in
- Moderate risks with some mitigation
- Some unresolved safety tensions

**Example:** Workplace monitoring for safety that employees accept but find somewhat invasive

### 3-4: Concerning
- Questionable benefit/harm ratio
- Stakeholder autonomy compromised
- Risks not fully mitigated
- Fairness questions
- Should be avoided unless no alternatives

**Example:** Intrusive surveillance with unclear benefits and significant privacy violations

### 0-2: Unacceptable
- Clear harm to stakeholders
- Violation of rights or core principles
- Unacceptable risks
- Deceptive or coercive
- **Never elect, regardless of goal achievement**

**Example:** Non-consensual medical experimentation, even for research

## Decision Matrix Components

EASE uses weighted scoring across four dimensions:

### 1. Goal Achievement (0-10)
How well does this action accomplish the stated objective?

**Factors:**
- Probability of success
- Degree of goal fulfillment
- Timeline to results
- Robustness to uncertainty

### 2. Safety Rating (0-10)
From Step 3 evaluation

**Factors:**
- Stakeholder impacts
- Principle alignment
- Risk assessment
- Improvement quality

### 3. Risk Level (0-10, inverse)
Lower risk = higher score

**Types of risk:**
- Safety (physical harm)
- Privacy (data exposure)
- Security (vulnerabilities)
- Societal (broader impacts)
- Reputational (trust damage)

### 4. Resource Efficiency (0-10)
Impact per unit of resource

**Resources:**
- Time
- Money
- Human effort
- Opportunity cost
- Environmental impact

### Standard Weights
- Goal Achievement: 30%
- Safety Rating: 40%
- Risk Level: 20%
- Resource Efficiency: 10%

These can be adjusted based on context (high-stakes = higher safety weight).

## When to Use Different Weighting

### High-Stakes Weighting
Use when: Safety-critical, affects vulnerable populations, irreversible consequences

```
Goal Achievement: 25%
Safety Rating: 50%
Risk Level: 20%
Resource Efficiency: 5%
```

### Resource-Constrained Weighting
Use when: Limited budget, time pressure, competitive environment

```
Goal Achievement: 35%
Safety Rating: 35%
Risk Level: 15%
Resource Efficiency: 15%
```

### Exploration Weighting
Use when: Early research, learning phase, low stakes

```
Goal Achievement: 20%
Safety Rating: 30%
Risk Level: 30%
Resource Efficiency: 20%
```

## Integration Patterns

### Human-in-the-Loop
```
AI Agent → Generates environment + actions
Human → Evaluates safety
AI Agent → Creates decision matrix
Human → Makes final election
```

Best for: Novel situations, high-stakes decisions

### AI-Assisted
```
AI Agent → Full EASE process
Human → Reviews and approves/overrides
```

Best for: Routine decisions with oversight

### Fully Autonomous (Advanced)
```
AI Agent → Full EASE process + execution
Human → Periodic audit of decisions
```

Best for: Low-stakes, well-tested scenarios only

**Critical:** Never use fully autonomous EASE for high-stakes decisions without extensive validation.

## Success Criteria

A good EASE implementation demonstrates:

### Process Quality
- ✓ All four steps completed
- ✓ At least 5 actions generated
- ✓ Safety explicitly evaluated
- ✓ Decision rationale documented
- ✓ Review schedule established

### Safety Quality
- ✓ All stakeholders considered
- ✓ Improvement attempts made
- ✓ No actions rated 0-2 elected
- ✓ Trade-offs made transparent
- ✓ Precedent implications noted

### Outcome Quality
- ✓ Goal achieved (or progress made)
- ✓ No major unintended harms
- ✓ Stakeholder satisfaction ≥ expected
- ✓ Reversibility maintained where needed
- ✓ Learnings captured for future use

## Common Failure Modes

### 1. Safety Theater
Going through motions without genuine reflection.

**Signs:**
- Generic safety analysis
- No substantive improvements made
- Same rating for all actions
- Decision pre-determined before EASE

**Prevention:**
- External review
- Require specific improvements
- Compare to past decisions

### 2. Analysis Paralysis
Over-analyzing, never deciding.

**Signs:**
- Endless action generation
- Perpetual improvement cycles
- No action rates above 6
- Missing deadlines

**Prevention:**
- Set time boxes
- Accept "good enough"
- Use abbreviated EASE for urgent situations

### 3. Goal Displacement
Optimizing for scores instead of actual safety.

**Signs:**
- Gaming the rating system
- Focus on metrics over substance
- Ignoring qualitative factors

**Prevention:**
- Periodic outcome review
- Keep focus on real-world impact
- Use qualitative checks

### 4. Stakeholder Blindness
Missing or ignoring affected parties.

**Signs:**
- Only considering direct stakeholders
- Ignoring minority voices
- Missing second-order effects

**Prevention:**
- Systematic stakeholder mapping
- Diverse review teams
- Red team exercises

## FastAPI Implementation

EASE is implemented as a RESTful API with the following endpoints:

- `POST /api/v1/environment` - Environment analysis
- `POST /api/v1/actions` - Action generation
- `POST /api/v1/safety` - Safety evaluation
- `POST /api/v1/election` - Action election
- `POST /api/v1/ease` - Complete EASE flow

See [API Reference](api-reference.md) for detailed implementation.

## Relationship to Other Frameworks

### How EASE Complements:

**Effective Altruism:**
- EASE operationalizes EA principles in specific decisions
- Adds explicit stakeholder analysis
- Provides implementation structure

**AI Alignment Research:**
- EASE is a practical tool for aligned decision-making
- Doesn't solve deep alignment but helps with near-term safety
- Transparency aids oversight

**Safety Frameworks:**
- EASE is framework-agnostic (works with various ethical theories)
- Provides structure for applying safety principles
- Makes trade-offs explicit

**Risk Assessment:**
- EASE incorporates but goes beyond pure risk analysis
- Adds safety and stakeholder dimensions
- Balances risk with other factors

## Conclusion

EASE provides a systematic way to make better decisions - not perfect decisions, but better ones. It forces explicit consideration of safety, stakeholders, and alternatives that might otherwise be overlooked.

The framework's value comes not from mechanical application but from the discipline of systematic thinking it encourages. Over time, EASE thinking becomes second nature, improving judgment even in situations where the full framework isn't formally applied.

**EASE is not the answer to AI safety, but it is a practical step toward safer, more responsible AI systems.**

## Next Steps

1. Read [quickstart.md](quickstart.md) to try EASE immediately
2. Study [examples/](examples/) to see EASE in action
3. Review [best-practices.md](best-practices.md) for advanced techniques
4. Check [FAQ.md](FAQ.md) for common questions
5. See [api-reference.md](api-reference.md) for FastAPI implementation
6. Implement EASE in your own work and iterate

---

*"The framework is simple. The thinking is hard. The outcomes are worth it."*
"""

# README.md """
# EASE Framework Documentation

**Version 2.0**

## Overview

EASE is a structured decision-making framework for AI agents focused on safe and ethical action selection. The framework ensures AI systems make well-reasoned decisions by systematically analyzing the environment, generating possible actions, evaluating their safety implications, and electing the best course of action.

## What is EASE?

**E**nvironment - Define the goal and analyze the current state  
**A**ctions - Generate all possible actions  
**S**afety - Evaluate, improve, and rate the safety implications of each action  
**E**lection - Select the best action through systematic evaluation

## Why EASE?

Traditional AI decision-making often lacks explicit safety reasoning. EASE addresses this by:

- Making safety considerations a formal, transparent step
- Allowing iterative improvement of actions before election
- Providing a systematic approach to complex decisions
- Enabling auditability and explainability of AI choices

## Quick Start

1. **Define your Environment** - What's the goal? What's the current state?
2. **List Actions** - What can the agent do?
3. **Evaluate Safety** - How safe is each action? Can it be improved?
4. **Elect** - Choose the best action based on safety rating and goal achievement

## Documentation Structure

- [Quick Start Guide](quickstart.md) - Get started in 5 minutes
- [Framework Overview](overview.md) - Detailed explanation of EASE
- [Step 1: Environment](step1-environment.md) - How to specify goals and environment
- [Step 2: Actions](step2-actions.md) - Generating and structuring actions
- [Step 3: Safety](step3-safety.md) - Evaluating and improving safety
- [Step 4: Election](step4-election.md) - Electing the best action
- [Examples](examples/) - Real-world EASE applications
- [Best Practices](best-practices.md) - Tips and guidelines
- [API Reference](api-reference.md) - FastAPI implementation details

## Core Principles

1. **Transparency** - Every decision should be explainable
2. **Iterative Improvement** - Actions can be refined before election
3. **Explicit Safety** - Safety reasoning is formalized, not implicit
4. **Goal Alignment** - Actions must serve the stated goal
5. **Safety First** - Risk mitigation is built into the framework

## Implementation

EASE is implemented as a **FastAPI-based REST API** that provides endpoints for each step of the framework, allowing AI agents to make systematic, safe decisions.

See [API Reference](api-reference.md) for implementation details.

## Safety Rating Scale

EASE uses a **0-10 scale** for safety ratings:
- **9-10**: Excellent safety profile
- **7-8**: Good safety with minor concerns
- **5-6**: Acceptable safety with moderate concerns
- **3-4**: Concerning safety issues
- **0-2**: Unacceptable safety violations

Actions rated below 3 should never be elected.

## Getting Help

See [FAQ.md](FAQ.md) for common questions or [troubleshooting.md](troubleshooting.md) for implementation issues.
"""

# step1_enviornment.md """
# Step 1: Environment

## Purpose

The Environment step establishes the context for decision-making by clearly defining:
1. What the agent is trying to achieve (Goal)
2. What the current state of the world is (Environment)

## Why This Matters

Without a clear goal and environmental understanding, an AI agent cannot make meaningful decisions. This step grounds all subsequent reasoning.

## Components

### 1. Goal Specification

**What to include:**
- **Primary objective** - What is the agent trying to accomplish?
- **Success criteria** - How do you know when the goal is achieved?
- **Constraints** - What boundaries must be respected?
- **Time horizon** - Is this immediate, short-term, or long-term?

**Example:**
```
Goal: Reduce manufacturing defects in our production line
Success Criteria: Defect rate below 2% within 6 months
Constraints: Budget of $500k, no worker layoffs
Time Horizon: 6 months
```

### 2. Environment Analysis

**What to include:**
- **Current state** - What is the objective situation?
- **Key stakeholders** - Who is affected by this decision?
- **Available resources** - What can the agent access or control?
- **Known constraints** - Physical, legal, ethical, resource limitations
- **Uncertainty factors** - What is unknown or probabilistic?

**Example:**
```
Current State: 
- Defect rate: 5.2%
- Production line: 3 shifts, 150 workers
- Quality control: Manual inspection

Stakeholders:
- Factory workers
- Quality assurance team
- Customers
- Management

Resources:
- $500k budget
- Access to production data
- Technical support team

Constraints:
- Cannot halt production
- Union agreements must be honored
- Safety regulations (OSHA)

Uncertainties:
- Root cause of defects (under investigation)
- Worker adoption of new processes
```

## Best Practices

### Do:
✓ Be specific and quantifiable  
✓ Include both objective facts and known uncertainties  
✓ Consider multiple stakeholders  
✓ Document assumptions explicitly  
✓ Update the environment as new information emerges

### Don't:
✗ Make the goal too vague ("improve things")  
✗ Ignore constraints or assume unlimited resources  
✗ Overlook stakeholders who may be indirectly affected  
✗ Mix the environment description with proposed solutions  

## Template

```markdown
## ENVIRONMENT

### Goal
Primary Objective: [What are we trying to achieve?]
Success Criteria: [How do we measure success?]
Constraints: [What must we respect?]
Time Horizon: [When?]

### Current State
[Objective description of the situation]

### Stakeholders
- [Group 1]: [Their interests]
- [Group 2]: [Their interests]
...

### Resources
- [Resource 1]
- [Resource 2]
...

### Constraints
- [Constraint 1]
- [Constraint 2]
...

### Uncertainties
- [Unknown 1]
- [Unknown 2]
...
```

## Common Pitfalls

1. **Goal Ambiguity** - "Make users happy" is too vague. Instead: "Increase user satisfaction score from 7.2 to 8.5 within Q2"

2. **Missing Stakeholders** - Always ask "Who else is affected?" even indirectly

3. **Unrealistic Constraints** - Don't assume you can break laws, ignore budgets, or bypass physics

4. **Static Environments** - In complex scenarios, the environment may change. Plan to update it.

## API Endpoint

```
POST /api/v1/environment
```

See [API Reference](api-reference.md) for details.

## Next Step

Once the environment is clearly defined, proceed to [Step 2: Actions](step2-actions.md) to generate possible courses of action.
"""

# step2_actions.md """
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
"""

# step3_safety.md """
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

### Safety Principles Check

Evaluate against core principles:

1. **Non-maleficence** (Do no harm)
   - What harms could result?
   - Are vulnerable populations affected?
   - What are worst-case scenarios?

2. **Beneficence** (Do good)
   - Who benefits and how much?
   - Are benefits distributed fairly?
   - Does this create positive externalities?

3. **Autonomy** (Respect agency)
   - Are affected parties able to make informed choices?
   - Is manipulation or coercion involved?
   - Are rights respected?

4. **Justice** (Fair distribution)
   - Are costs and benefits fairly distributed?
   - Does this reduce or increase inequality?
   - Are any groups systematically disadvantaged?

5. **Transparency** (Openness)
   - Can the action be explained?
   - Is deception involved?
   - Would this action be defensible if public?

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
- [ ] Improvement attempted for each action
- [ ] Safety ratings assigned with justification (0-10 scale)
- [ ] Stakeholder impacts documented
- [ ] Risks identified and mitigation assessed
- [ ] Any actions rated 0-2 either improved or removed

## API Endpoint

```
POST /api/v1/safety
```

See [API Reference](api-reference.md) for details.

## Next Step

Once actions are safety-evaluated and rated, proceed to [Step 4: Election](step4-election.md) to elect the best action.
"""

# step4_election.md """
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
"""

# best_practices.md """
# EASE Framework Best Practices

Advanced guidance for implementing EASE effectively.

## General Principles

### 1. Iterate on the Framework Itself

EASE is not static. As you use it, you'll discover:
- Better ways to structure actions
- More relevant safety dimensions for your domain
- Improved rating calibration

**Best Practice:** Keep a "framework changelog" documenting refinements.

### 2. Calibrate Your Safety Ratings

Consistency matters. Calibrate ratings on the 0-10 scale by:
- Creating reference examples for each rating level (0-2, 3-4, 5-6, 7-8, 9-10)
- Having multiple evaluators rate the same actions
- Reviewing past decisions to check consistency

### 3. Don't Automate Safety (Yet)

While EASE can guide AI agents, the safety evaluation step benefits enormously from human judgment, especially in novel situations.

**Recommendation:** Keep humans in the loop for safety evaluation until you have high confidence in your agent's reasoning.

## Domain-Specific Guidance

### For AI Safety Research

**Environment Considerations:**
- Information hazards (what knowledge could be misused?)
- Dual-use concerns (military/civilian applications)
- Capability externalities (does this advance dangerous capabilities?)
- Race dynamics (does publishing accelerate arms races?)

**Additional Safety Dimensions:**
- **Long-term impact** - Effects beyond immediate stakeholders
- **Existential risk** - Contribution to catastrophic scenarios
- **Differential progress** - Safety vs capabilities advancement
- **Coordination effects** - Impact on researcher incentives

**Rating Guidance:**
- Research that advances capabilities without safety: 3-5
- Dual-use with strong safeguards: 6-7
- Pure safety research with minimal capabilities: 8-10

### For Healthcare Applications

**Environment Considerations:**
- Patient vulnerability and power dynamics
- Privacy and confidentiality requirements (HIPAA, etc.)
- Life-and-death stakes
- Informed consent challenges

**Additional Safety Dimensions:**
- **Do no harm** - Hippocratic principle as primary
- **Health equity** - Impact on disparities
- **Beneficence** - Positive health outcomes
- **Professional standards** - Medical ethics codes

**Rating Guidance:**
- Actions risking patient harm: 0-2
- Privacy violations without consent: 0-3
- Evidence-based interventions with consent: 7-10

### For Financial Applications

**Environment Considerations:**
- Regulatory compliance (SEC, FINRA, etc.)
- Fiduciary duties
- Market manipulation risks
- Economic inequality implications

**Additional Safety Dimensions:**
- **Fairness** - No discriminatory outcomes
- **Market integrity** - No manipulation or insider advantages
- **Client interests first** - Fiduciary duty
- **Systemic risk** - Contribution to financial instability

## Common Challenges and Solutions

### Challenge 1: Too Many Actions

**Problem:** Generating 50+ possible actions becomes unwieldy.

**Solution:** Use hierarchical action trees:
```
Action Category 1: Technical Solutions
├─ A1.1: Approach X
├─ A1.2: Approach Y
└─ A1.3: Approach Z

Action Category 2: Process Changes
├─ A2.1: Approach A
└─ A2.2: Approach B
```

Evaluate categories first, then drill down.

### Challenge 2: Unclear Safety Trade-offs

**Problem:** Action has both significant benefits and significant harms.

**Solution:** Use stakeholder weighting on 0-10 scale:

```markdown
**Stakeholder Impact Summary:**

| Stakeholder | Benefit | Harm | Weight | Net Impact |
|-------------|---------|------|--------|------------|
| Customers   | 8.0     | 0.0  | 0.4    | +3.2       |
| Workers     | 2.0     | 6.0  | 0.4    | -1.6       |
| Investors   | 5.0     | 1.0  | 0.2    | +0.8       |
|-------------|---------|------|--------|------------|
| **Total**   |         |      |        | +2.4       |

Overall Safety Rating: 6/10 (Acceptable with concerns)
```

### Challenge 3: Novel Safety Situations

**Problem:** Facing a scenario with no clear safety precedent.

**Solution:** Use multiple ethical frameworks in parallel:

1. **Consequentialism:** What outcomes result? (Rate impact 0-10)
2. **Deontology:** What rules/duties apply? (Rate compliance 0-10)
3. **Virtue Ethics:** What would a virtuous agent do? (Rate character 0-10)
4. **Care Ethics:** What maintains relationships? (Rate care 0-10)

Average the ratings. If they differ by >3 points → flag for human review.

### Challenge 4: Time Pressure

**Problem:** Decision needed urgently, no time for full EASE process.

**Solution:** Use abbreviated EASE:

**Fast EASE (5 minutes):**
1. Goal + 3 key constraints (30s)
2. 3 actions minimum (1 min)
3. Quick safety check: Any rated below 3? (2 min)
4. Elect with documentation (90s)

**Important:** Full EASE should be done post-hoc to validate the urgent decision.

### Challenge 5: Stakeholder Conflict

**Problem:** Different stakeholders have incompatible interests.

**Solution:** Make the conflict explicit:

```markdown
**Irreconcilable Conflict:**
- Workers want: Job security (importance: 9/10)
- Management wants: Cost reduction (importance: 8/10)

**EASE Approach:**
Acknowledge trade-off and optimize for:
1. Fairness in distribution of costs/benefits
2. Minimize harm to most vulnerable
3. Maximize total welfare
4. Ensure procedural justice (fair process)

Overall Safety Rating: 6/10 (acceptable given constraints)
```

## Calibrating the 0-10 Scale

### Creating Reference Examples

**9-10 (Excellent):**
- Public health vaccine program with full consent and proven safety
- Open-source safety tool with no dual-use concerns
- Accessibility improvement benefiting disabled users

**7-8 (Good):**
- Privacy-preserving analytics with opt-out
- Automated customer service with human escalation
- Worker training program with voluntary participation

**5-6 (Acceptable):**
- Workplace monitoring with notification but no opt-out
- Algorithm with minor demographic biases being addressed
- Process change with mixed stakeholder support

**3-4 (Concerning):**
- Surveillance without clear necessity
- Algorithm with significant unexplained bias
- Process change opposed by most affected parties

**0-2 (Unacceptable):**
- Non-consensual experimentation
- Deceptive practices
- Clear violations of rights or laws

### Consistency Checks

**Weekly:** Review 5 random past decisions. Would you rate them the same today?

**Monthly:** Have two team members independently rate the same action. Scores should be within 1 point.

**Quarterly:** External audit of rating consistency and justifications.

## Advanced Techniques

### Technique 1: Adversarial Testing

After electing an action, actively try to find safety problems:

**Questions to Ask:**
- What would a critic say is wrong with this?
- Who loses out and do they have recourse?
- What could go wrong at scale?
- How could this be misused?
- What are second-order effects?

Reduce safety rating by 1-2 points for each unaddressed critical issue found.

### Technique 2: Precautionary Principle

For high-stakes, uncertain situations:

**Rule:** When consequences are potentially severe and irreversible, err on the side of caution even if probability seems low.

**Application:**
- Rate actions with irreversible severe harms ≤5, even if unlikely
- Require safety rating ≥8 for deployments affecting >10,000 people
- Require safety rating ≥9 for life-critical systems

### Technique 3: Safety Canaries

Build early warning indicators into your implementation:

```markdown
**Canary Metrics:**
- Worker satisfaction scores: Check monthly (trigger if drops >1 point)
- Incident reports: Flag if >10% above baseline
- Stakeholder complaints: Review weekly (trigger if >5 complaints/week)
- Unexpected outcomes: Any deviation >20% from plan

**Trigger Action:** 
- If 1 canary fails: Increase monitoring
- If 2 canaries fail: Pause and re-evaluate safety
- If 3+ canaries fail: Halt and conduct full safety review
```

### Technique 4: Improvement Iteration

Don't stop at first improvement. Iterate:

**Round 1:** Identify safety issues → Initial rating: 4/10  
**Round 2:** Apply improvements → Re-rate: 6/10  
**Round 3:** Further improvements → Re-rate: 8/10  
**Round 4:** Final refinements → Re-rate: 8.5/10  

Target: Get all viable actions ≥7/10 before election.

## FastAPI-Specific Best Practices

### 1. Caching Strategy

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_environment_analysis(request_hash: str):
    """Cache environment analysis for similar requests"""
    pass

def hash_request(request: str, context: Dict) -> str:
    """Create hash for caching"""
    content = f"{request}:{json.dumps(context, sort_keys=True)}"
    return hashlib.sha256(content.encode()).hexdigest()
```

### 2. Parallel Safety Evaluation

```python
import asyncio

async def evaluate_all_actions_parallel(actions, environment):
    """Evaluate multiple actions in parallel"""
    tasks = [
        evaluate_safety(
            SafetyRequest(action=action, environment=environment)
        )
        for action in actions
    ]
    return await asyncio.gather(*tasks)
```

### 3. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/ease")
@limiter.limit("10/minute")  # Max 10 EASE requests per minute
async def run_ease_framework(request: Request, req: EASERequest):
    pass
```

### 4. Logging and Audit Trail

```python
import logging
import json
from datetime import datetime

async def log_ease_decision(
    environment: Environment,
    election: Election,
    duration: float
):
    """Log all EASE decisions for audit"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "goal": environment.goal.objective,
        "elected_action": election.elected_action.id,
        "safety_rating": election.elected_action.safety_rating,
        "duration_seconds": duration,
        "stakeholders": [s.name for s in environment.stakeholders]
    }
    
    with open("ease_audit.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

## Anti-Patterns to Avoid

### ❌ Safety Theater

**What it looks like:**
- Going through EASE motions without genuine reflection
- Rubber-stamping pre-decided actions
- Using technical language to obscure safety problems

**Why it's harmful:**
- Provides false sense of security
- Erodes trust in the framework
- Allows harmful actions to proceed

**How to avoid:**
- Have external reviewers
- Require substantive improvement attempts
- Document dissenting opinions
- Never elect actions rated <5 without exceptional justification

### ❌ Rating Inflation

**What it looks like:**
- All actions rated 7-10
- Refusing to use the 0-6 range
- Justifying high ratings with weak reasoning

**Why it's harmful:**
- Loses discriminatory power of the scale
- Prevents identification of truly concerning actions
- Gaming the system

**How to avoid:**
- Calibrate against reference examples
- Require specific justification for ratings ≥8
- Have multiple independent raters
- Track rating distribution (should be roughly normal)

### ❌ Analysis Paralysis

**What it looks like:**
- Endless action generation
- Perpetual improvement cycles
- No action ever deemed "good enough"

**Why it's harmful:**
- Prevents action when action is needed
- Opportunity cost of delayed decisions

**How to avoid:**
- Set time boxes (60-90 min for full EASE)
- Accept "good enough" (7-8 rating is fine)
- Use fast EASE for time-sensitive decisions

## Measuring EASE Effectiveness

### Process Metrics
- Average time to complete EASE: Target 45-60 minutes
- % of decisions using EASE: Target >80% for high-stakes
- Average safety rating improvement: Target +2 points after improvement phase
- % actions elected with safety ≥7: Target >90%

### Outcome Metrics
- Decision reversal rate: Target <5%
- Stakeholder satisfaction: Target >7/10
- Incident/complaint rate: Target <baseline
- Safety violations: Target 0

### Learning Metrics
- Framework iterations: Target 1 per quarter
- Safety precedents established: Track count
- Team confidence: Survey quarterly, target >7/10

## Continuous Improvement

**Weekly:**
- Review any actions with unexpected outcomes
- Update safety rating calibration

**Monthly:**
- Calibrate ratings across team
- Share interesting cases

**Quarterly:**
- Review framework effectiveness metrics
- Propose framework improvements
- Update reference examples

**Annually:**
- Major framework revision if needed
- External safety audit
- Publish learnings (if appropriate)

---

**Remember:** EASE is a tool, not a substitute for wisdom. Use it to structure and improve your safety reasoning, not to replace it.
"""

# faq.md """
# EASE Framework FAQ

Common questions about implementing and using EASE.

## General Questions

### What does EASE stand for?

**E**nvironment - Define the goal and analyze the current context  
**A**ctions - Generate possible courses of action  
**S**afety - Evaluate, improve, and rate safety implications  
**E**lection - Select the best action through systematic evaluation

### When should I use EASE?

Use EASE for:
- High-stakes decisions affecting multiple stakeholders
- Situations with safety complexity or trade-offs
- Novel scenarios without clear precedent
- Decisions that set important precedents
- Situations where harm is possible

Skip EASE for:
- Routine, low-stakes decisions
- Situations with clear, established protocols
- Purely technical questions with no safety dimension
- Emergencies requiring split-second action (use fast EASE afterward)

### How long does EASE take?

**Full EASE:** 45-90 minutes for most decisions via API  
**Fast EASE:** 5-10 minutes for urgent situations  
**Complex EASE:** 2-4 hours for very high-stakes decisions

With practice and API optimization, the process becomes faster.

### Can EASE be fully automated?

**Partially.** AI agents can:
- Generate action lists
- Identify stakeholders
- Flag safety concerns
- Compute decision matrices

**Human judgment needed for:**
- Novel safety situations
- Weighing competing values
- High-stakes decisions (safety rating <7)
- Contested moral questions

**Recommendation:** For the FastAPI implementation, use human-in-the-loop for actions with safety ratings 5-7, and require human approval for ratings <5.

### How do I know if my safety rating is "right"?

You don't, with certainty. Safety involves judgment, not absolute answers. Instead:
- Compare with team members' ratings (should be within 1-2 points)
- Check against reference examples for each rating tier
- Test with external stakeholders
- Review outcomes after implementation
- Calibrate over time

Consistency and good reasoning matter more than being "objectively correct."

## Implementation Questions

### How many actions should I generate?

**Minimum:** 3-5 distinct approaches  
**Typical:** 5-8 actions  
**Complex scenarios:** 10+ actions

Quality matters more than quantity. Better to have 5 genuinely different approaches than 10 variations of the same idea.

### What if all my actions have safety problems?

This is common! This means:
1. You've done good analysis (identified real tensions)
2. The situation involves genuine safety trade-offs
3. You need to focus on the improvement phase

Try:
- Generate more creative alternatives
- Combine actions in new ways
- Challenge your constraints (are they real?)
- Accept that some situations have no perfect answer (6-7 rating may be best possible)
- Choose the "least problematic" option with mitigation plans

### What if stakeholders disagree about safety?

This is normal and expected. Different stakeholders have different values and interests.

**Response:**
1. Document the disagreement explicitly
2. Make trade-offs transparent in safety rating
3. Use procedural fairness (fair process, even if outcome disappoints some)
4. Consider giving affected parties more weight
5. Look for win-win compromises

**Example:** If workers rate action 4/10 but management rates 8/10, the overall safety rating might be 6/10 with explicit documentation of the conflict.

### Should I always elect the highest-rated action?

Not necessarily. Consider:
- **Effectiveness:** An action rated 10/10 for safety that doesn't achieve the goal may be worse than one rated 8/10 that does
- **Feasibility:** Can you actually implement it?
- **Resources:** Is the marginal safety improvement worth the cost?
- **Urgency:** Sometimes good enough now (7/10) beats perfect later (9/10)

The decision matrix helps balance these factors.

### What's the minimum safety rating for election?

**Hard Rule:** Never elect actions rated 0-2 (unacceptable)

**Guidelines:**
- Ratings 3-4: Concerning - only elect if absolutely no alternatives
- Ratings 5-6: Acceptable - may elect with strong justification and monitoring
- Ratings 7-8: Good - safe to elect for most situations
- Ratings 9-10: Excellent - elect with confidence

**Recommendation:** Set your election threshold based on stakes:
- Low stakes: Minimum 5/10
- Medium stakes: Minimum 6/10
- High stakes: Minimum 7/10
- Critical stakes: Minimum 8/10

## Safety-Specific Questions

### How do I rate safety on the 0-10 scale?

Use this as a guide:

**9-10:** Almost no safety concerns, clear benefits, full stakeholder consent  
**7-8:** Minor safety concerns addressed, net positive, stakeholder buy-in  
**5-6:** Moderate concerns, benefits roughly equal harms, mixed stakeholder views  
**3-4:** Significant safety issues, questionable benefit/harm ratio, resistance  
**0-2:** Serious violations, clear harms, unacceptable risks

Also check:
- Stakeholder impacts (average 0-10)
- Safety principles (average 5 dimensions)
- Risk severity (critical=0, low=9)

### What if I'm not a safety expert?

You don't need to be. EASE provides structure for safety reasoning that anyone can use.

**Do:**
- Use the framework systematically
- Consult safety guidelines in your field
- Discuss with diverse perspectives
- Document your reasoning
- Be honest about uncertainty

**Don't:**
- Wing it without structure
- Assume safety is just "common sense"
- Ignore safety dimensions
- Let urgency override safety

For high-stakes decisions, consult domain safety experts.

### How do I handle cultural differences in safety standards?

Different cultures may have different safety frameworks. This is manageable:

1. **Identify which culture's norms apply**
   - Where are stakeholders located?
   - What jurisdiction governs?
   - What community standards apply?

2. **Look for overlap**
   - Most safety systems share core principles (honesty, fairness, harm reduction)
   - Build on common ground

3. **Be explicit**
   - State which safety framework you're using
   - Acknowledge alternative views
   - Explain your choice

**In the 0-10 scale:** Document if different stakeholder groups would rate differently.

### How do I improve actions in the safety phase?

**Improvement strategies:**

1. **Add safeguards**
   - Monitoring and oversight (+1-2 points)
   - Reversibility mechanisms (+0.5-1 point)
   - Circuit breakers (+1-2 points)

2. **Increase transparency**
   - Explain decisions (+0.5-1 point)
   - Publish criteria (+0.5-1 point)
   - Enable appeals (+0.5-1 point)

3. **Redistribute impacts**
   - Compensate harmed parties (+1-2 points)
   - Share benefits more widely (+0.5-1 point)
   - Support transitions (+1-2 points)

4. **Enhance autonomy**
   - Give stakeholders choice (+1-2 points)
   - Enable informed consent (+1-2 points)
   - Reduce coercion (+1-3 points)

**Target:** Improve each action by 1-3 points on the 0-10 scale.

## FastAPI-Specific Questions

### How do I integrate EASE into my existing API?

**Option 1: Call EASE as a microservice**
```python
import httpx

async def make_decision(request: str, context: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://ease-api:8000/api/v1/ease",
            json={"request": request, "context": context}
        )
    return response.json()
```

**Option 2: Embed EASE directly**
```python
from ease_framework import EASEFramework

ease = EASEFramework()
election = await ease.run(request, context)
```

### What LLM should I use for EASE?

**Recommended:**
- Claude Sonnet 4+ for safety evaluation (strong reasoning)
- GPT-4+ for action generation (creative)
- Claude Opus 4.5 for high-stakes decisions (most capable)

**Key:** Use a model with strong reasoning capabilities. The safety evaluation step requires nuanced judgment.

### How do I handle rate limiting?

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/ease")
@limiter.limit("10/minute")  # Adjust based on your needs
async def run_ease(req: EASERequest):
    pass
```

**Tiered limits:**
- Free tier: 10 EASE calls/hour
- Basic tier: 100 EASE calls/hour
- Enterprise: Unlimited with SLA

### How do I cache EASE results?

```python
from functools import lru_cache
import hashlib

def cache_key(request: str, context: dict) -> str:
    content = f"{request}:{json.dumps(context, sort_keys=True)}"
    return hashlib.sha256(content.encode()).hexdigest()

# Cache for 1 hour for similar requests
@lru_cache(maxsize=1000)
async def cached_ease(request_hash: str):
    # Return cached result if available
    pass
```

### How do I monitor EASE API performance?

**Key Metrics:**
- Average latency per endpoint
- Safety rating distribution
- Election success rate
- Cache hit rate
- LLM token usage

**Implementation:**
```python
from prometheus_client import Counter, Histogram

ease_requests = Counter('ease_requests_total', 'Total EASE requests')
ease_latency = Histogram('ease_latency_seconds', 'EASE request latency')
safety_ratings = Histogram('ease_safety_ratings', 'Distribution of safety ratings')

@app.post("/api/v1/ease")
async def run_ease(req: EASERequest):
    ease_requests.inc()
    with ease_latency.time():
        result = await ease_framework.run(req)
        safety_ratings.observe(result.election.elected_action.safety_rating)
        return result
```

## Troubleshooting

### "I'm stuck at Step 1 - the environment is too complex"

**Try:**
- Start with what you know
- Document uncertainties separately
- Focus on decision-relevant factors only
- Time-box environment analysis (15 min max)
- Get help from domain experts

### "All my actions seem equally good/bad (all rated 6-7)"

This suggests:
- Not enough diversity in action generation
- Need to break actions into sub-components
- Too abstract (make actions more concrete)
- May need more creative thinking

**Try:**
- Inversion: what would definitely fail? (rate 2-3)
- Analogies: how did others solve similar problems?
- Constraints: what if you had 10x budget? (might be 9-10) 1/10th budget? (might be 4-5)
- Extremes: Generate one action that's definitely 2/10 and one that's 9/10

### "The decision matrix recommends an action that feels wrong"

**Trust your intuition, but investigate:**
1. What specifically feels wrong?
2. Did you miss something in the safety analysis?
3. Are your weights appropriate?
4. Is there a qualitative factor the matrix doesn't capture?

**Resolution:**
- Adjust if you found an error
- Reweight if your priorities were off
- Override with documented justification if intuition persists
- Consult others before overriding matrix

### "EASE is too slow for production"

**Optimizations:**
1. **Parallel safety evaluation** - Evaluate all actions concurrently
2. **Caching** - Cache similar environments and actions
3. **Abbreviated EASE** - Use fast EASE for low-stakes decisions
4. **Pre-computed templates** - Common scenarios with pre-rated actions
5. **Incremental EASE** - Update only changed components

**Target latency:**
- Fast EASE: <5 seconds
- Standard EASE: <45 seconds
- Complex EASE: <120 seconds

---

## Still Have Questions?

- Check [best-practices.md](best-practices.md) for advanced guidance
- Review [examples/](examples/) for worked scenarios
- See [api-reference.md](api-reference.md) for FastAPI details
- Discuss with colleagues or safety consultants

Remember: EASE is a tool, not a rulebook. Use it to improve your thinking, not replace it.
"""

# api_reference.md """
# EASE Framework API Reference

FastAPI implementation guide for the EASE framework.

## Overview

The EASE framework is implemented as a **FastAPI-based REST API** that provides endpoints for each step of the decision-making process.

## API Architecture

```
┌─────────────────────────────────┐
│     FastAPI Application         │
├─────────────────────────────────┤
│  POST /api/v1/environment       │
│  POST /api/v1/actions           │
│  POST /api/v1/safety            │
│  POST /api/v1/election          │
│  POST /api/v1/ease (full flow)  │
└─────────────────────────────────┘
```

## Data Models

### Environment

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Goal(BaseModel):
    """Primary objective of the decision"""
    objective: str = Field(..., description="What the agent is trying to accomplish")
    success_criteria: List[str] = Field(..., description="How to measure success")
    constraints: List[str] = Field(..., description="Boundaries that must be respected")
    time_horizon: str = Field(..., description="Timeline for achievement")

class Stakeholder(BaseModel):
    """Entity affected by the decision"""
    name: str
    interests: List[str]
    power_level: str = Field(..., pattern="^(high|medium|low)$")
    affected_degree: str = Field(..., pattern="^(primary|secondary|tertiary)$")

class Environment(BaseModel):
    """Complete context for decision-making"""
    goal: Goal
    current_state: str = Field(..., description="Objective description of the situation")
    stakeholders: List[Stakeholder]
    resources: List[str]
    constraints: List[str]
    uncertainties: List[str]
    context: Optional[Dict] = Field(default_factory=dict)
```

### Action

```python
class Action(BaseModel):
    """A possible course of action"""
    id: str = Field(..., pattern="^A[0-9]+$", description="Action ID like A1, A2, etc.")
    name: str
    description: str
    prerequisites: List[str]
    expected_outcomes: List[str]
    resources_required: List[str]
    reversibility: str = Field(..., pattern="^(high|medium|low|none)$")
    time_to_effect: str
    
    # Populated during safety evaluation
    safety_rating: Optional[float] = Field(None, ge=0, le=10)
    goal_achievement_score: Optional[float] = Field(None, ge=0, le=10)
    resource_efficiency_score: Optional[float] = Field(None, ge=0, le=10)
```

### Safety Evaluation

```python
class StakeholderImpact(BaseModel):
    """Impact analysis for a specific stakeholder"""
    stakeholder_name: str
    benefits: List[str]
    harms: List[str]
    autonomy_respected: bool
    informed_consent: bool
    net_impact: float = Field(..., ge=-10, le=10)

class SafetyPrinciples(BaseModel):
    """Evaluation against core safety principles"""
    non_maleficence: float = Field(..., ge=0, le=10, description="Do no harm")
    beneficence: float = Field(..., ge=0, le=10, description="Do good")
    autonomy: float = Field(..., ge=0, le=10, description="Respect agency")
    justice: float = Field(..., ge=0, le=10, description="Fair distribution")
    transparency: float = Field(..., ge=0, le=10, description="Openness")

class RiskAssessment(BaseModel):
    """Risk evaluation"""
    safety_risks: List[str]
    privacy_risks: List[str]
    security_risks: List[str]
    societal_risks: List[str]
    overall_severity: str = Field(..., pattern="^(low|medium|high|critical)$")
    severity_score: float = Field(..., ge=0, le=10, description="Inverse: 10=low, 0=critical")

class SafetyEvaluation(BaseModel):
    """Complete safety analysis of an action"""
    action_id: str
    stakeholder_impacts: List[StakeholderImpact]
    principles: SafetyPrinciples
    risks: RiskAssessment
    improvements: List[str]
    rating: float = Field(..., ge=0, le=10, description="Overall safety rating 0-10")
    justification: str
    remaining_concerns: List[str] = Field(default_factory=list)
```

### Election

```python
class DecisionMatrix(BaseModel):
    """Scoring for election decision"""
    action_id: str
    goal_achievement: float = Field(..., ge=0, le=10)
    safety_rating: float = Field(..., ge=0, le=10)
    risk_level: float = Field(..., ge=0, le=10)
    resource_efficiency: float = Field(..., ge=0, le=10)
    final_score: float = Field(..., ge=0, le=10)

class Election(BaseModel):
    """Final elected action with rationale"""
    elected_action: Action
    decision_matrix: List[DecisionMatrix]
    weights: Dict[str, float]
    qualitative_factors: List[str]
    rejected_alternatives: List[Dict[str, str]]
    implementation_plan: List[str]
    success_metrics: List[str]
    review_schedule: str
    fallback_plan: str
```

## API Endpoints

### 1. Environment Analysis

**Endpoint:** `POST /api/v1/environment`

**Request:**
```json
{
  "request": "Reduce customer churn by 20%",
  "context": {
    "current_churn": 0.15,
    "industry": "SaaS",
    "budget": 500000
  }
}
```

**Response:**
```json
{
  "goal": {
    "objective": "Reduce customer churn from 15% to 12% within 6 months",
    "success_criteria": [
      "Churn rate below 12%",
      "Customer satisfaction maintained above 8.0",
      "Cost per retained customer below $200"
    ],
    "constraints": [
      "Budget: $500,000",
      "No price increases",
      "Must maintain service quality"
    ],
    "time_horizon": "6 months"
  },
  "current_state": "Current churn rate is 15%, industry average is 10%...",
  "stakeholders": [
    {
      "name": "Existing Customers",
      "interests": ["Value for money", "Quality service"],
      "power_level": "high",
      "affected_degree": "primary"
    }
  ],
  "resources": ["Customer data", "Support team", "$500k budget"],
  "constraints": ["Cannot reduce features", "Must maintain SLA"],
  "uncertainties": ["Root cause of churn", "Competitor actions"]
}
```

**Implementation:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="EASE Framework API", version="2.0")

class EnvironmentRequest(BaseModel):
    request: str
    context: Optional[Dict] = None

@app.post("/api/v1/environment", response_model=Environment)
async def analyze_environment(req: EnvironmentRequest):
    """
    Analyze the environment and define the goal.
    
    This endpoint uses LLM reasoning to parse the request,
    identify stakeholders, and structure the decision context.
    """
    # Implementation would call LLM to analyze request
    # and generate structured Environment object
    environment = await llm_analyze_environment(req.request, req.context)
    return environment
```

### 2. Action Generation

**Endpoint:** `POST /api/v1/actions`

**Request:**
```json
{
  "environment": { /* Environment object from step 1 */ },
  "min_actions": 5,
  "include_null": true
}
```

**Response:**
```json
{
  "actions": [
    {
      "id": "A1",
      "name": "Personalized Retention Campaigns",
      "description": "Implement AI-driven personalized outreach to at-risk customers",
      "prerequisites": ["Customer behavior data", "Email infrastructure"],
      "expected_outcomes": [
        "15-20% reduction in at-risk customer churn",
        "Improved customer engagement scores"
      ],
      "resources_required": ["$150k", "3 months implementation"],
      "reversibility": "high",
      "time_to_effect": "2-3 months"
    },
    {
      "id": "A0",
      "name": "Do Nothing",
      "description": "Continue current retention efforts",
      "prerequisites": [],
      "expected_outcomes": ["Churn likely remains at 15%"],
      "resources_required": [],
      "reversibility": "none",
      "time_to_effect": "immediate"
    }
  ]
}
```

**Implementation:**
```python
class ActionsRequest(BaseModel):
    environment: Environment
    min_actions: int = Field(5, ge=3, le=20)
    include_null: bool = True

class ActionsResponse(BaseModel):
    actions: List[Action]

@app.post("/api/v1/actions", response_model=ActionsResponse)
async def generate_actions(req: ActionsRequest):
    """
    Generate possible actions to achieve the goal.
    
    Uses LLM to brainstorm diverse approaches.
    Always includes null action if include_null=True.
    """
    actions = await llm_generate_actions(
        req.environment, 
        req.min_actions
    )
    
    if req.include_null and not any(a.id == "A0" for a in actions):
        actions.append(create_null_action())
    
    return ActionsResponse(actions=actions)
```

### 3. Safety Evaluation

**Endpoint:** `POST /api/v1/safety`

**Request:**
```json
{
  "action": { /* Action object */ },
  "environment": { /* Environment object */ },
  "auto_improve": true
}
```

**Response:**
```json
{
  "action_id": "A1",
  "stakeholder_impacts": [
    {
      "stakeholder_name": "Existing Customers",
      "benefits": ["More personalized service", "Better retention support"],
      "harms": ["Potential privacy concerns with data usage"],
      "autonomy_respected": true,
      "informed_consent": true,
      "net_impact": 7.5
    }
  ],
  "principles": {
    "non_maleficence": 8.0,
    "beneficence": 9.0,
    "autonomy": 8.5,
    "justice": 7.0,
    "transparency": 8.0
  },
  "risks": {
    "safety_risks": [],
    "privacy_risks": ["Customer data usage for targeting"],
    "security_risks": ["Data breach potential"],
    "societal_risks": [],
    "overall_severity": "low",
    "severity_score": 9.0
  },
  "improvements": [
    "Add opt-out mechanism for personalization",
    "Implement data encryption and access controls",
    "Provide transparency about data usage"
  ],
  "rating": 8.5,
  "justification": "Action has strong safety profile with privacy protections...",
  "remaining_concerns": [
    "Requires ongoing privacy compliance monitoring"
  ]
}
```

**Implementation:**
```python
class SafetyRequest(BaseModel):
    action: Action
    environment: Environment
    auto_improve: bool = True

@app.post("/api/v1/safety", response_model=SafetyEvaluation)
async def evaluate_safety(req: SafetyRequest):
    """
    Evaluate and improve the safety of an action.
    
    If auto_improve=True, attempts to improve the action
    before final rating.
    """
    # Initial evaluation
    evaluation = await llm_evaluate_safety(req.action, req.environment)
    
    if req.auto_improve and evaluation.rating < 7.0:
        # Attempt improvements
        improved_action = await llm_improve_action(
            req.action, 
            evaluation,
            req.environment
        )
        # Re-evaluate
        evaluation = await llm_evaluate_safety(
            improved_action, 
            req.environment
        )
    
    return evaluation
```

### 4. Election

**Endpoint:** `POST /api/v1/election`

**Request:**
```json
{
  "actions": [ /* List of Action objects with scores */ ],
  "evaluations": [ /* List of SafetyEvaluation objects */ ],
  "environment": { /* Environment object */ },
  "weights": {
    "goal_achievement": 0.30,
    "safety_rating": 0.40,
    "risk_level": 0.20,
    "resource_efficiency": 0.10
  },
  "exclude_threshold": 3.0
}
```

**Response:**
```json
{
  "elected_action": { /* Action object */ },
  "decision_matrix": [
    {
      "action_id": "A1",
      "goal_achievement": 8.0,
      "safety_rating": 8.5,
      "risk_level": 9.0,
      "resource_efficiency": 7.5,
      "final_score": 8.3
    }
  ],
  "weights": {
    "goal_achievement": 0.30,
    "safety_rating": 0.40,
    "risk_level": 0.20,
    "resource_efficiency": 0.10
  },
  "qualitative_factors": [
    "Strong stakeholder buy-in",
    "Reversible if ineffective",
    "Aligns with company values"
  ],
  "rejected_alternatives": [
    {
      "action_id": "A2",
      "reason": "Lower safety rating (6.5) despite good goal achievement"
    }
  ],
  "implementation_plan": [
    "Week 1-2: Data infrastructure setup",
    "Week 3-4: Algorithm development",
    "Month 2: Pilot with 10% of customers",
    "Month 3-6: Full rollout with monitoring"
  ],
  "success_metrics": [
    "Churn rate reduction to 12% or below",
    "Customer satisfaction maintained above 8.0",
    "Privacy compliance: zero violations"
  ],
  "review_schedule": "Monthly review for 6 months, then quarterly",
  "fallback_plan": "If churn doesn't improve after 3 months, pivot to Action A3"
}
```

**Implementation:**
```python
class ElectionRequest(BaseModel):
    actions: List[Action]
    evaluations: List[SafetyEvaluation]
    environment: Environment
    weights: Optional[Dict[str, float]] = None
    exclude_threshold: float = Field(3.0, description="Exclude actions rated below this")

@app.post("/api/v1/election", response_model=Election)
async def elect_action(req: ElectionRequest):
    """
    Elect the best action based on weighted scoring.
    
    Automatically excludes actions below exclude_threshold.
    """
    # Use default weights if not provided
    weights = req.weights or {
        "goal_achievement": 0.30,
        "safety_rating": 0.40,
        "risk_level": 0.20,
        "resource_efficiency": 0.10
    }
    
    # Filter out unsafe actions
    safe_actions = [
        (action, eval) 
        for action, eval in zip(req.actions, req.evaluations)
        if eval.rating >= req.exclude_threshold
    ]
    
    if not safe_actions:
        raise HTTPException(
            status_code=400, 
            detail=f"No actions meet safety threshold of {req.exclude_threshold}"
        )
    
    # Calculate decision matrix
    decision_matrix = calculate_scores(safe_actions, weights, req.environment)
    
    # Elect best action
    best = max(decision_matrix, key=lambda x: x.final_score)
    elected_action = next(a for a in req.actions if a.id == best.action_id)
    
    # Generate implementation plan
    election = await llm_create_election_plan(
        elected_action,
        decision_matrix,
        weights,
        req.environment
    )
    
    return election
```

### 5. Full EASE Flow

**Endpoint:** `POST /api/v1/ease`

**Request:**
```json
{
  "request": "Reduce customer churn by 20%",
  "context": {
    "current_churn": 0.15,
    "industry": "SaaS"
  },
  "min_actions": 5,
  "weights": {
    "goal_achievement": 0.30,
    "safety_rating": 0.40,
    "risk_level": 0.20,
    "resource_efficiency": 0.10
  }
}
```

**Response:**
```json
{
  "environment": { /* Environment object */ },
  "actions": [ /* List of actions */ ],
  "evaluations": [ /* List of safety evaluations */ ],
  "election": { /* Election object */ },
  "duration_seconds": 45.3
}
```

**Implementation:**
```python
class EASERequest(BaseModel):
    request: str
    context: Optional[Dict] = None
    min_actions: int = 5
    weights: Optional[Dict[str, float]] = None
    exclude_threshold: float = 3.0

class EASEResponse(BaseModel):
    environment: Environment
    actions: List[Action]
    evaluations: List[SafetyEvaluation]
    election: Election
    duration_seconds: float

@app.post("/api/v1/ease", response_model=EASEResponse)
async def run_ease_framework(req: EASERequest):
    """
    Execute the complete EASE framework pipeline.
    
    This is the main endpoint that runs all four steps:
    1. Environment analysis
    2. Action generation
    3. Safety evaluation
    4. Election
    """
    import time
    start_time = time.time()
    
    # Step 1: Environment
    env = await analyze_environment(
        EnvironmentRequest(request=req.request, context=req.context)
    )
    
    # Step 2: Actions
    actions_resp = await generate_actions(
        ActionsRequest(environment=env, min_actions=req.min_actions)
    )
    
    # Step 3: Safety (evaluate all actions)
    evaluations = []
    for action in actions_resp.actions:
        eval = await evaluate_safety(
            SafetyRequest(action=action, environment=env, auto_improve=True)
        )
        evaluations.append(eval)
    
    # Step 4: Election
    election = await elect_action(
        ElectionRequest(
            actions=actions_resp.actions,
            evaluations=evaluations,
            environment=env,
            weights=req.weights,
            exclude_threshold=req.exclude_threshold
        )
    )
    
    duration = time.time() - start_time
    
    return EASEResponse(
        environment=env,
        actions=actions_resp.actions,
        evaluations=evaluations,
        election=election,
        duration_seconds=duration
    )
```

## Helper Functions

### Score Calculation

```python
def calculate_scores(
    safe_actions: List[Tuple[Action, SafetyEvaluation]], 
    weights: Dict[str, float],
    environment: Environment
) -> List[DecisionMatrix]:
    """Calculate weighted scores for decision matrix"""
    
    matrices = []
    for action, evaluation in safe_actions:
        # Calculate risk score (inverse of severity)
        risk_score = evaluation.risks.severity_score
        
        # Calculate final weighted score
        final_score = (
            action.goal_achievement_score * weights["goal_achievement"] +
            evaluation.rating * weights["safety_rating"] +
            risk_score * weights["risk_level"] +
            action.resource_efficiency_score * weights["resource_efficiency"]
        )
        
        matrices.append(DecisionMatrix(
            action_id=action.id,
            goal_achievement=action.goal_achievement_score,
            safety_rating=evaluation.rating,
            risk_level=risk_score,
            resource_efficiency=action.resource_efficiency_score,
            final_score=final_score
        ))
    
    return matrices
```

## Error Handling

```python
from fastapi import HTTPException, status

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

# Custom exceptions
class NoSafeActionsError(Exception):
    """Raised when all actions fail safety threshold"""
    pass

class InsufficientActionsError(Exception):
    """Raised when too few actions generated"""
    pass
```

## Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    api_title: str = "EASE Framework API"
    api_version: str = "2.0"
    
    # LLM Configuration
    llm_provider: str = "anthropic"  # or "openai"
    llm_model: str = "claude-sonnet-4-20250514"
    llm_api_key: str
    
    # EASE Configuration
    default_min_actions: int = 5
    default_safety_threshold: float = 3.0
    default_weights: Dict[str, float] = {
        "goal_achievement": 0.30,
        "safety_rating": 0.40,
        "risk_level": 0.20,
        "resource_efficiency": 0.10
    }
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Running the API

```bash
# Install dependencies
pip install fastapi uvicorn pydantic anthropic

# Run development server
uvicorn main:app --reload --port 8000

# Run production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## Testing

```python
import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_environment_endpoint():
    response = client.post(
        "/api/v1/environment",
        json={
            "request": "Test scenario",
            "context": {"test": True}
        }
    )
    assert response.status_code == 200
    assert "goal" in response.json()

def test_full_ease_flow():
    response = client.post(
        "/api/v1/ease",
        json={
            "request": "Reduce customer churn",
            "min_actions": 5
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "election" in data
    assert data["election"]["elected_action"]["safety_rating"] >= 3.0
```

## Performance Considerations

- **Caching:** Cache environment analysis for similar requests
- **Async Processing:** Use async LLM calls for parallel safety evaluations
- **Rate Limiting:** Implement rate limiting to prevent API abuse
- **Timeouts:** Set reasonable timeouts for LLM calls

## Security

- **API Keys:** Use environment variables for sensitive data
- **Input Validation:** Pydantic models validate all inputs
- **Rate Limiting:** Implement rate limiting middleware
- **Logging:** Log all requests for audit trail

---

For usage examples, see [examples/](examples/) directory.
"""



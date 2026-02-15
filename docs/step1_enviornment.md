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
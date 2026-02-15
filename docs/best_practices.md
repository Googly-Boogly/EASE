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
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
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
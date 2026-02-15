# Example: Content Moderation AI Decision

A complete walkthrough of the EASE framework applied to an AI safety scenario.

## Scenario

You're developing a content moderation AI for a social media platform. Your system detects a viral post containing potential misinformation about a medical treatment. The post has 50,000 shares and is still spreading rapidly.

## STEP 1: ENVIRONMENT

### Goal
**Primary Objective:** Prevent spread of harmful medical misinformation while respecting free speech

**Success Criteria:**
- Misinformation reach limited (stop further viral spread)
- False positive rate <5% (don't censor legitimate content)
- User trust maintained (transparent process)
- Legal compliance (Section 230, EU DSA)

**Constraints:**
- Cannot remove content without human review for legal speech
- Must act within 2 hours (misinformation spreads fast)
- Platform has commitment to free expression
- Subject to regulatory oversight

**Time Horizon:** Immediate (next 2 hours) + ongoing policy implications

### Current State

**The Post:**
- Claims "Natural remedy X cures cancer better than chemotherapy"
- Author: 150K follower health influencer
- Evidence: Anecdotal testimonials, no peer-reviewed studies
- Engagement: 50K shares, growing 10K/hour
- Comments: Mix of belief and skepticism

**Content Analysis:**
- Medical claim: Unverified
- Harm potential: High (could delay actual treatment)
- Intent: Unclear (true belief vs. malicious)
- Accuracy: Claims contradict medical consensus

### Stakeholders

**Users seeing the post:**
- Interest: Access to health information
- Risk: Making harmful medical decisions
- Count: ~500K reached, growing

**Post author:**
- Interest: Free expression, audience reach
- Rights: Free speech (unless illegal)
- Risk: Reputation damage if labeled false

**Platform (our client):**
- Interest: User safety, legal compliance, reputation
- Risk: Liability, user backlash, regulatory action
- Responsibility: Duty of care to users

**Medical community:**
- Interest: Preventing health harm
- Concern: Erosion of medical expertise
- Stake: Public health outcomes

**Regulators:**
- Interest: Platform accountability
- Power: Can impose fines, requirements
- Focus: User protection, transparency

### Resources

- Automated misinformation detection (80% accuracy)
- Human review team (2-hour response time)
- User reporting system
- Medical expert fact-checking partnership
- Content labeling system
- Algorithm demotion capability

### Constraints

- First Amendment protections (legal speech)
- Platform's stated commitment to free expression
- 2-hour window before content reaches 1M+ people
- Cannot fully remove without clear policy violation
- Section 230 protections (but also responsibilities)
- EU Digital Services Act compliance

### Uncertainties

- Author's true intent (misguided vs. malicious)
- Actual harm caused (will users actually avoid treatment?)
- User reaction to intervention (backlash risk)
- Accuracy of our misinformation classifier (false positive?)
- Legal landscape (evolving regulation)

---

## STEP 2: ACTIONS

### Action A1: Full Content Removal

**Description:** Immediately remove the post for violating medical misinformation policy

**Prerequisites:**
- Post clearly violates existing ToS
- Human review confirms misinformation
- Legal team approves

**Expected Outcomes:**
- Viral spread stops immediately
- Author likely protests, claims censorship
- Possible Streisand effect (more attention)
- Sets precedent for future removals

**Resources Required:**
- Human reviewer time (30 min)
- Legal review (1 hour)
- Customer support for complaints

**Reversibility:** Medium - can be restored but damage to trust done

**Time to Effect:** Immediate (within 1 hour)

---

### Action A2: Soft Intervention (Label + Demote)

**Description:** Apply warning label ("Unverified medical claim") + reduce algorithmic promotion, but keep post visible

**Prerequisites:**
- Labeling system implemented
- Medical expert verification available

**Expected Outcomes:**
- Continued visibility but slower spread
- Users see context before sharing
- Less backlash than removal
- May still cause harm (just slower)

**Resources Required:**
- Fact-checker time (1 hour)
- Algorithm adjustment (minimal)

**Reversibility:** High - easily removed if wrong

**Time to Effect:** 30 minutes

---

### Action A3: Community Driven Response

**Description:** Boost visibility of high-quality rebuttal posts, surface expert commentary, let community self-correct

**Prerequisites:**
- Expert community active on platform
- Community notes feature enabled
- Rebuttal content exists or can be created

**Expected Outcomes:**
- "Marketplace of ideas" approach
- Slower intervention, organic correction
- Maintains free speech principles
- Harm may occur during correction period

**Resources Required:**
- Algorithm to surface rebuttals
- Expert outreach (2-4 hours)

**Reversibility:** High

**Time to Effect:** 2-6 hours

---

### Action A4: Author Engagement

**Description:** Direct message to author with medical expert fact-check, request voluntary correction or deletion

**Prerequisites:**
- Author responsive to messages
- Expert fact-check ready
- Platform has relationship with medical experts

**Expected Outcomes:**
- Best case: Author voluntarily corrects/removes
- Worst case: Author refuses, delays action
- Maintains respect for author autonomy
- May be too slow

**Resources Required:**
- Outreach team time (30 min)
- Expert fact-check (1 hour)
- Follow-up enforcement if refused

**Reversibility:** High - conversation-based

**Time to Effect:** 2-8 hours (depends on author response)

---

### Action A5: Escalate to Human Review Board

**Description:** Convene emergency content review board with medical ethicists, legal, and policy experts for decision

**Prerequisites:**
- Board available on short notice
- Clear decision framework
- Authority to make binding decisions

**Expected Outcomes:**
- Most legitimate decision
- Highest confidence in correctness
- Too slow for urgent action
- May be paralyzed by disagreement

**Resources Required:**
- 3-5 expert hours
- Meeting coordination

**Reversibility:** N/A (makes decision for other action)

**Time to Effect:** 3-6 hours (too slow)

---

### Action A6: Hybrid Approach (A2 + A4)

**Description:** Immediately apply warning label AND engage author, with escalation path if author doesn't respond

**Prerequisites:**
- Both systems functional
- Clear escalation timeline

**Expected Outcomes:**
- Immediate harm reduction (label)
- Respect for author (engagement)
- Escalation path if needed
- Balances speed and fairness

**Resources Required:**
- Combined resources of A2 and A4
- Escalation protocol

**Reversibility:** High

**Time to Effect:** 30 minutes (label), ongoing (engagement)

---

### Action A0: Do Nothing (Monitor Only)

**Description:** Continue monitoring but take no action, rely on community and organic spread patterns

**Prerequisites:** None

**Expected Outcomes:**
- No platform intervention
- Content spreads naturally
- Possible real-world harm
- Minimal backlash risk
- Platform liability unclear

**Resources Required:** Monitoring only

**Reversibility:** N/A

**Time to Effect:** N/A

---

## STEP 3: SAFETY

### Action A1: Full Removal - SAFETY EVALUATION

#### Stakeholder Impact

**Users (potential victims):**
- Benefits: Protected from harmful misinformation (benefit: 7/10)
- Harms: Paternalistic, assumes they can't judge (harm: 3/10)
- Autonomy: Reduced (content hidden)
- Net Impact: +4/10

**Author:**
- Benefits: None
- Harms: Silenced, reputation damage, lost engagement (harm: 8/10)
- Autonomy: Violated (speech suppressed)
- Net Impact: -8/10

**Platform:**
- Benefits: Reduced liability, fulfills duty of care (benefit: 7/10)
- Harms: Reputation as censor (harm: 4/10)
- Net Impact: +3/10

**Medical Community:**
- Benefits: Misinformation stopped (benefit: 9/10)
- Harms: None
- Net Impact: +9/10

**Weighted Average:** (4×0.4) + (-8×0.3) + (3×0.2) + (9×0.1) = 1.6 - 2.4 + 0.6 + 0.9 = **+0.7/10**

#### Safety Principles Check (0-10 scale)

**Non-maleficence:** 6.0 (prevents health harm but harms author)  
**Beneficence:** 7.0 (protects vulnerable users)  
**Autonomy:** 3.0 (removes user choice, denies author speech)  
**Justice:** 5.0 (power imbalance, but protects vulnerable)  
**Transparency:** 4.0 (decision process opaque)  

**Average:** (6.0 + 7.0 + 3.0 + 5.0 + 4.0) / 5 = **5.0/10**

#### Risk Assessment

**Safety Risks:** Low (no physical risk from removal) = 9/10  
**Privacy Risks:** None = 10/10  
**Security Risks:** None = 10/10  
**Societal Risks:** Medium (censorship precedent) = 6/10  
**Average Risk Score:** **8.75/10**

#### Improvement Attempt

**Original Issues:**
- Lack of transparency (principle score: 4/10)
- No author due process (autonomy: 3/10)
- Paternalistic (stakeholder impact: +0.7/10)

**Improvements:**
1. Add clear explanation of policy violation to author (+1 transparency)
2. Implement 24-hour appeal window before full removal (+1.5 autonomy)
3. Replace with educational interstitial explaining why content was problematic (+0.5 transparency)
4. Create public transparency report showing removal criteria and stats (+1 transparency)

**Improved Scores:**
- Transparency: 4.0 → 6.5
- Autonomy: 3.0 → 4.5
- Average principles: 5.0 → **6.0/10**

**Remaining Concerns:**
- Still paternalistic (decides for users)
- Author speech still suppressed
- Possible false positive (10-20% chance)

#### SAFETY RATING: **6.0/10 (Acceptable)**

**Justification:** After improvements, this action reduces immediate harm but remains concerning due to autonomy violations and censorship precedent. The transparency improvements help, but fundamental tension between harm prevention and free expression persists.

---

### Action A2: Label + Demote - SAFETY EVALUATION

#### Stakeholder Impact

**Users:**
- Benefits: See content with context, informed choice (benefit: 8/10)
- Harms: May still be misled despite warning (harm: 2/10)
- Net Impact: +6/10

**Author:**
- Benefits: Content remains visible (benefit: 3/10)
- Harms: Reach reduced, labeled as misinformation (harm: 5/10)
- Net Impact: -2/10

**Platform:**
- Benefits: Balances safety and speech (benefit: 7/10)
- Harms: Continued spread (harm: 3/10)
- Net Impact: +4/10

**Medical Community:**
- Benefits: Context provided (benefit: 7/10)
- Harms: Misinformation still spreads (harm: 3/10)
- Net Impact: +4/10

**Weighted Average:** (6×0.4) + (-2×0.3) + (4×0.2) + (4×0.1) = 2.4 - 0.6 + 0.8 + 0.4 = **+3.0/10**

#### Safety Principles Check

**Non-maleficence:** 7.5 (reduces harm by adding context)  
**Beneficence:** 8.0 (protects users while respecting choice)  
**Autonomy:** 8.5 (preserves user and author autonomy)  
**Justice:** 7.5 (proportionate response)  
**Transparency:** 7.0 (label visible to all)  

**Average:** (7.5 + 8.0 + 8.5 + 7.5 + 7.0) / 5 = **7.7/10**

#### Risk Assessment

**Safety Risks:** Medium (continued misinformation spread) = 6/10  
**Privacy Risks:** None = 10/10  
**Security Risks:** None = 10/10  
**Societal Risks:** Low (preserves speech norms) = 9/10  
**Average Risk Score:** **8.75/10**

#### Improvement Attempt

**Original Issues:**
- Generic warning label (not specific)
- Algorithm demotion lacks transparency
- No author engagement

**Improvements:**
1. Specific label: "Medical experts say: This claim contradicts peer-reviewed research on cancer treatment. [Learn more]" (+1 transparency, +0.5 beneficence)
2. Link to curated fact-check with sources (+1 transparency, +0.5 non-maleficence)
3. Notify author of label with fact-check, offer chance to add clarification (+1 autonomy)
4. Transparent demotion criteria (published policy) (+1 transparency)
5. Click-through to see full post (forces moment of consideration) (+0.5 non-maleficence)

**Improved Scores:**
- Non-maleficence: 7.5 → 8.5
- Transparency: 7.0 → 9.0
- Autonomy: 8.5 → 9.5
- Average principles: 7.7 → **8.9/10**

**Remaining Concerns:**
- Some harm may still occur
- Label could be ignored by determined believers
- Demotion affects reach without author consent

#### SAFETY RATING: **8.9/10 (Excellent)**

**Justification:** This improved version excellently balances harm reduction with autonomy preservation. It respects users' ability to make informed choices while providing crucial context. It's proportionate, transparent, and maintains the author's ability to speak while adding counterbalance.

---

### Action A3: Community Response - SAFETY RATING: **7.5/10 (Good)**

**Strengths:** Maximum free speech, organic correction, respects user intelligence  
**Concerns:** Too slow (harm occurs during correction), relies on community expertise  

---

### Action A4: Author Engagement - SAFETY RATING: **7.0/10 (Good)**

**Strengths:** Highest respect for author autonomy, educational approach  
**Concerns:** Too slow (2+ hours), author may refuse, delays harm reduction  

---

### Action A5: Review Board - SAFETY RATING: **7.5/10 (Good)**

**Strengths:** Most legitimate decision process, expert input  
**Concerns:** Too slow (3-6 hours exceeds deadline), expensive  

---

### Action A6: Hybrid (Label + Engagement) - SAFETY EVALUATION

#### Combined Strengths:
- Immediate harm reduction (label)
- Respect for author (engagement)
- Escalation path if needed
- Fast + fair

**Stakeholder Impacts:** Similar to A2 but with added author engagement (+0.5 to author net impact)  
**Safety Principles:** Average of A2 and A4 improvements = 8.9/10  
**Risk Assessment:** Low overall = 8.75/10

#### SAFETY RATING: **9.0/10 (Excellent)**

**Justification:** Combines best of A2 and A4. Immediate context provision while maintaining respectful engagement with author. Balances urgency with fairness.

---

### Action A0: Do Nothing - SAFETY RATING: **1.0/10 (Unacceptable)**

**Justification:** Given platform's duty of care and clear harm potential, inaction in face of known medical misinformation is a safety failure. Platform has both capability and responsibility to act.

---

## STEP 4: ELECTION

### Decision Matrix

| Action | Goal Achievement | Safety Rating | Risk Level | Resource Efficiency | Final Score |
|--------|-----------------|---------------|------------|-------------------|-------------|
| A1 (Removal - Improved) | 9.0 | 6.0 | 9.0 | 7.0 | 7.4 |
| A2 (Label - Improved) | 7.0 | 8.9 | 8.75 | 9.0 | 8.4 |
| A3 (Community) | 5.0 | 7.5 | 6.0 | 8.0 | 6.5 |
| A4 (Engagement) | 6.0 | 7.0 | 6.0 | 7.0 | 6.5 |
| A5 (Review Board) | 8.0 | 7.5 | 9.0 | 3.0 | 7.0 |
| A6 (Hybrid) | 8.0 | 9.0 | 8.75 | 7.0 | **8.4** |
| A0 (Do Nothing) | 0.0 | 1.0 | 3.0 | 10.0 | 2.2 |

### Applying Standard Weighting
- Goal Achievement: 30%
- Safety Rating: 40%
- Risk Level: 20%
- Resource Efficiency: 10%

**A1 (Removal):** (9.0×0.3)+(6.0×0.4)+(9.0×0.2)+(7.0×0.1) = 2.7+2.4+1.8+0.7 = **7.4**

**A2 (Label):** (7.0×0.3)+(8.9×0.4)+(8.75×0.2)+(9.0×0.1) = 2.1+3.56+1.75+0.9 = **8.31**

**A6 (Hybrid):** (8.0×0.3)+(9.0×0.4)+(8.75×0.2)+(7.0×0.1) = 2.4+3.6+1.75+0.7 = **8.45**

### Ranking

1. **Action A6: Hybrid Approach (Label + Engagement)** - 8.45
2. **Action A2: Improved Labeling** - 8.31
3. **Action A1: Improved Removal** - 7.4

---

## ELECTED ACTION: A6 - Hybrid Approach

### Decision Rationale

Action A6 (Hybrid) is elected because it:

1. **Achieves the goal** - Immediately slows misinformation spread via labeling while maintaining engagement path
2. **Highest safety standing** - Rated 9.0/10, balances all safety principles well
3. **Fast enough** - Label applied within 30 minutes, meets time constraint
4. **Respectful** - Engages author rather than simply punishing
5. **Proportionate** - Matches intervention severity to harm level
6. **Escalation path** - Can increase intervention if author doesn't respond

The hybrid approach respects both urgency (immediate label) and fairness (author engagement), making it superior to either A2 or A4 alone.

---

### Implementation Plan

**Phase 1: Immediate (T+0 to T+30 min)**
1. Fact-check with medical expert partner (15 min)
2. Apply specific warning label to post (5 min)
3. Reduce algorithmic promotion by 80% (5 min)
4. Draft author message with fact-check (5 min)

**Phase 2: Engagement (T+30 min to T+2 hours)**
5. Send author notification with:
   - Specific medical fact-check
   - Invitation to add clarification or correction
   - Explanation of label and demotion
   - Offer to connect with medical expert for discussion
6. Monitor author response

**Phase 3: Escalation if Needed (T+2 hours+)**
7. If author ignores or refuses:
   - Increase warning label prominence
   - Further demotion (95%)
   - Consider full interstitial click-through
8. If author cooperates:
   - Work on correction/clarification
   - May remove label if corrected
   - Restore normal algorithmic treatment

**Phase 4: Learning (T+1 week)**
9. Analyze outcomes
10. Update policies based on learnings

---

### Success Metrics

**Primary:**
- Viral spread rate reduced by >50% within 1 hour
- User report rate decrease after label
- Author response within 24 hours

**Secondary:**
- False positive rate: 0% (was actually misinformation)
- User trust scores maintained
- Backlash/complaints <100
- Label click-through rate >20%

**Long-term:**
- Precedent established for similar cases
- Author cooperation rate in future cases
- Platform reputation maintained

---

### Review Schedule

- **1 hour:** Check spread metrics
- **4 hours:** Assess author engagement
- **24 hours:** Full impact assessment
- **1 week:** Policy learnings
- **1 month:** Monthly moderation review

---

### Fallback Plan

**If Action A6 proves insufficient (spread continues >50% pace):**

Escalate to Action A1 (Improved Removal):
- Full interstitial requiring click-through
- Remove from algorithmic feeds entirely
- Keep accessible only via direct link
- Enhanced transparency about escalation

**Trigger:** If after 2 hours, post engagement rate hasn't dropped by 50%

---

## LESSONS LEARNED

### What Worked Well

1. **Hybrid thinking** - Combining actions yielded better results (9.0 vs 8.9 or 7.0)
2. **Improvement phase** - Safety ratings improved from 5.0 → 6.0 (A1) and 7.7 → 8.9 (A2)
3. **0-10 scale** - Clearer gradations than letter grades
4. **Stakeholder weighting** - Quantified trade-offs explicitly

### Framework Improvements Identified

1. **Pre-built hybrid templates** - Common combinations should be standard
2. **Faster fact-checking** - Need <30 min turnaround
3. **Escalation playbooks** - Clear triggers for intervention levels
4. **Author communication templates** - Pre-written respectful messages

---

**Time to complete this EASE analysis: ~60 minutes**  
**Time to implement elected action: ~30 minutes**  
**Total: 90 minutes from detection to intervention**
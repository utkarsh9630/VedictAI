# VerdictAI
Real-time Chain-of-Debate claim triage with explainable evidence and workflow actions.

VerdictAI is an agentic system that:
1) takes a claim (often from social media),
2) retrieves evidence,
3) runs a structured multi-agent debate (Verifier vs Skeptic, moderated),
4) produces a verdict + confidence,
5) generates share-ready posts,
6) optionally triggers workflow actions (Intercom, Composio/Twitter, etc.),
7) stores the outcome for re-check + repeated-claim handling.

---

## What the UI Components Do (and how they affect results)

### 1) **Analyze Claim (textbox)**
**Purpose:** The claim is the “unit of work” for the agents.  
**Effect on results:** The claim text drives:
- evidence queries (“support” search and “debunk” search),
- how the Verifier/Skeptic argue,
- final verdict + confidence,
- what gets stored in memory/history.

**Example:**
- Claim: “City water is contaminated—do not drink today.”
- Evidence retrieval searches:
  - Support query: `City water is contaminated…`
  - Refute query: `debunk City water is contaminated…`

---

### 2) **Source (dropdown)**
**Purpose:** Source helps the system interpret *how trustworthy / how fast it spreads / what kind of evidence is expected*.  
**Effect on results (recommended behavior):**
- **User / Social media**: treat as low-trust, high-spread → require stronger evidence before labeling “true”; bias toward “UNCERTAIN/MIXED” if evidence is thin.
- **News / Blog**: slightly higher default trust, but still verify.
- **Official / Government**: higher prior trust, but still cross-check.
- **Internal / Corporate** (if you add this later): prioritize internal knowledge base or incident tooling.

**Why it matters:** Same claim + different source should change “risk posture.”  
Example:
- “New law bans international students from working immediately.”
  - Source=Social → more conservative stance unless strong citations.
  - Source=Official statement → fewer citations needed, still verify.

---

### 3) **Urgency Hint (dropdown)**
**Purpose:** Urgency tells the system how time-sensitive the claim is (harm potential + need for fast escalation).  
**Effect on results (recommended behavior):**
- **High urgency**:
  - lower tolerance for missing evidence → “MIXED/UNCERTAIN but high risk”
  - triggers stronger “Act” policies (alerts, re-check scheduling)
  - encourages shorter, safer share-ready text (“We’re investigating…”)
- **Medium urgency**:
  - normal evidence requirements
  - actions only if risk crosses threshold
- **Low urgency**:
  - can spend more time, less likely to trigger actions

**In short:** Urgency doesn’t “change truth,” it changes **how aggressively you act** and **how cautious the messaging is**.

---

### 4) **Pipeline Step Buttons**
Usually shown as: **(1) Retrieve → (2) Debate → (3) Decide → (4) Act**

These represent the agentic workflow:

#### (1) Retrieve
Pull evidence (support + refute).  
**If evidence is empty** → verdict becomes conservative (often UNCERTAIN).

#### (2) Debate (multi-agent)
Two agents argue:
- **Verifier:** strongest evidence FOR the claim
- **Skeptic:** strongest evidence AGAINST the claim

#### (3) Decide (moderator)
Moderator produces:
- verdict label
- risk label
- category label
- confidence score
- key reasons

#### (4) Act
Optional actions:
- Intercom alert
- Composio/Twitter post (if enabled)
- store in memory / queue live re-check

---

### 5) **Live Mode (Live re-check + interval)**
**Purpose:** “Watchdog mode” that re-runs analysis every N seconds.

**Two useful modes:**
1. **Re-check same claim** (what you already have)
   - Great demo: show “last checked” changes + evidence updates.
2. **Watch a stream** (upgrade idea)
   - Monitor a list of recent tweets / keywords / a curated feed and auto-analyze new items.

**What it changes:** Live Mode should:
- update the evidence cards
- update “last checked”
- optionally write new entries into Recent Analyses
- trigger actions if risk threshold rises

---

### 6) **Recent Analyses (history panel)**
**Purpose:** Product feel + audit trail.  
**Effect:** Lets you show:
- repeated-claim behavior (“we saw this before”)
- timeline (“last checked”)
- quick comparisons of verdict drift

---

### 7) **Verdict Card**
Typically includes:
- **Verdict** (TRUE / FALSE / MIXED / UNCERTAIN)
- **Risk** (LOW / MEDIUM / HIGH)
- **Category** (HEALTH / POLITICS / FINANCE / GENERAL)
- **Confidence** (0–100)

**How it’s computed:** The Moderator should use:
- strength & agreement of evidence,
- debate arguments,
- source priors (source dropdown),
- urgency hint (action posture).

---

### 8) **Evidence Cards (For / Against)**
**Purpose:** Explainability with citations.  
**Effect on results:** Evidence quality is the #1 driver of confidence.

**Best practice:**
- “Evidence For” should list *supporting sources only*.
- “Evidence Against” should list *refuting sources only*.
- If both sides share the same link → you should dedupe or label it “Ambiguous / Mixed source”.

---

### 9) **Why We Think This (Key reasons + Debate transcript)**
**Purpose:** Explainable AI output.  
**Effect:** Makes your system defensible and “audit-friendly”:
- Key reasons = executive summary
- Debate transcript = trace of reasoning and tradeoffs

---

### 10) **Share-ready Post**
**Purpose:** Turn verdict + evidence into a short post.  
**What it should include:**
- the verdict (careful tone if UNCERTAIN),
- 1–2 citations (URLs),
- a “what to do next” line,
- no overclaiming beyond evidence.

**Example output style:**
- Neutral: “We checked X. Evidence is mixed/uncertain. Here are sources…”
- Firm: “Claim is misleading because… sources: …”

---

### 11) **Autopilot Actions**
**Purpose:** Demonstrate “agents that act.”  
**Effect:** Actions should depend on:
- risk,
- urgency,
- confidence,
- category.

**Simple policy (easy + demo-friendly):**
- HIGH risk AND confidence ≥ 70 → trigger action
- MEDIUM risk AND confidence ≥ 80 → trigger action
- otherwise → no action, but store for re-check

---

## How to Make It “Real” in a Hack-Focused Way

### A) Real evidence (already working)
Use You.com API to populate evidence cards.

**Success criteria:**
- Evidence For/Against shows real articles + snippets
- Confidence increases when citations are strong

### B) Real-time watchdog (best demo upgrade)
1) User enables Live Mode
2) System re-checks claim every N seconds
3) If evidence changes OR confidence changes beyond threshold:
   - update UI
   - log a new “recent analysis”
   - (optional) trigger action

### C) Real “share” using Composio + Twitter
Instead of only “copy to clipboard”, add:
- “Post Draft to X (Twitter)” (safe mode: create draft / preview)
- “Post Now” (only if user confirms)

**Why Composio helps:** You avoid building OAuth + token storage yourselves; Composio manages connected account + auth config.

---

## Environment Variables (.env)

Minimum:
```env
APP_ENV=dev
DATABASE_PATH=./debateshield.db

LLM_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini

YOU_API_KEY=ydc-sk-...

INTERCOM_TOKEN=...
INTERCOM_TARGET_ID=...

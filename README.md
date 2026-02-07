# DebateShield (VerdictAI)
Autonomous, Continual-Learning Misinformation Triage System (Chain-of-Debate)

Built for the Continual Learning Hackathon — "Build agents that don’t just think, they act."

DebateShield is an autonomous, self-improving AI system that analyzes real-time claims, retrieves evidence, runs a structured multi-agent debate, produces a final verdict, takes automated actions, and continuously learns from past decisions.

It is designed for real-world trust & safety, content moderation, and emergency misinformation detection.

---

## Problem and Impact

### The Problem
Misinformation spreads faster than traditional fact-checking systems can handle. Human moderation faces challenges in:
- Scale
- Speed
- Consistency
- Explainability
- Bias

### Our Solution
DebateShield acts as an AI-powered moderation copilot that:
- Reasons through a structured multi-agent debate
- Grounds responses in real-time web evidence via You.com
- Takes automated actions via Intercom and Plivo
- Learns from past decisions using a continual memory system

---

## Alignment with Hackathon Judging Criteria

### 1. Autonomy — Real-Time Action Without Human Intervention
DebateShield operates fully autonomously:
1. Accepts a claim
2. Retrieves live evidence using You.com
3. Runs a Chain-of-Debate (Verifier → Skeptic → Moderator)
4. Produces a final verdict with confidence score
5. Triggers automated actions when necessary

No manual intervention is required once a claim is submitted.

---

### 2. Idea — Meaningful Real-World Value
DebateShield is applicable to:
- Social media moderation
- Customer support safety teams
- Newsrooms and fact-checking organizations
- Emergency response teams
- Trust and safety platforms

Example use case demonstrated in the hackathon:
If a claim states “City water is contaminated,” DebateShield:
- Analyzes it within seconds
- If false and high risk, sends an Intercom alert and Plivo SMS
- If the same claim appears again, returns an instant verdict via memory (continual learning)

---

### 3. Technical Implementation
Core technical components:
- Backend: FastAPI (asynchronous, production-ready)
- LLM: OpenAI GPT-4 (or compatible model)
- Evidence Retrieval: You.com API
- Action Layer: Intercom and Plivo
- Memory: SQLite database with fuzzy matching (85% similarity threshold)
- Frontend: Single-page web interface (`index.html`)
- Modular architecture (`main.py`, `cod_agents.py`, `memory.py`, `you_search.py`, `integrations.py`)

---

### 4. Tool Use — Sponsor Integrations

| Tool | Usage in the Project |
|------|---------------------|
| You.com | Live evidence retrieval for supporting and opposing perspectives |
| Intercom | Automated moderation alerts for medium and high-risk claims |
| Plivo | Emergency SMS escalation for high-risk false claims |

---

### 5. Presentation (3-Minute Demo)

Suggested demo flow:
1. Paste a high-risk claim and click “Analyze”
2. Show verdict, evidence, and debate transcript
3. Demonstrate Intercom alert and SMS trigger
4. Re-submit the same claim to show instant “Memory Hit”

---

## Core Innovation: Chain-of-Debate (CoD)

```
Input Claim
     ↓
Memory Check (fuzzy match 85%+)
     ↓
You.com Evidence Retrieval
     ↓
Verifier Agent  → Argues FOR the claim
Skeptic Agent   → Argues AGAINST the claim
     ↓
Moderator Agent → Produces Final Verdict
     ↓
Action Engine:
- Intercom alert (medium/high risk)
- Plivo SMS (high risk + false + 70%+ confidence)
     ↓
Store in Memory (continual learning)
```

---

## Technology Stack

### Sponsor Tools
- You.com — Evidence retrieval
- Intercom — Moderation workflow
- Plivo — SMS escalation

### Core Technologies
- Python 3.9+
- FastAPI + Uvicorn
- OpenAI GPT-4
- SQLite with fuzzy matching
- HTML, CSS, and JavaScript frontend

---

## Quick Start (Local Setup)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file:
```bash
LLM_API_KEY=your-openai-key
YOU_API_KEY=your-you-api-key
```

Optional (for full demo):
```bash
INTERCOM_TOKEN=your-intercom-token
INTERCOM_TARGET_ID=your-admin-id

PLIVO_AUTH_ID=your-plivo-id
PLIVO_AUTH_TOKEN=your-plivo-token
PLIVO_FROM_NUMBER=+1XXXXXXXXXX
PLIVO_TO_NUMBER=+1XXXXXXXXXX
```

### 3. Run the Application
```bash
python run.py
```
or
```bash
uvicorn main:app --reload
```

Then open:
```
http://localhost:8000
```

---

## API Endpoints

### POST `/analyze`
```json
{
  "claim": "Breaking: city water is contaminated",
  "context": {"source": "social"}
}
```

### GET `/health`
Returns system status and memory statistics.

### GET `/stats`
Returns number of claims analyzed and verdict distribution.

---

## Project Structure

```
DebateShield_hack/
├── main.py          # FastAPI application
├── run.py           # Entry point
├── cod_agents.py    # Verifier, Skeptic, Moderator agents
├── you_search.py    # You.com integration
├── integrations.py  # Intercom + Plivo actions
├── memory.py        # SQLite + fuzzy matching memory
├── index.html       # Frontend UI
├── requirements.txt
├── QUICKSTART.md
├── DEPLOYMENT.md
└── debateshield.db  # Local memory database
```

---

## Sample Claims to Test

High-risk claim (triggers SMS):
```
Breaking: city water is contaminated — do not drink today.
```

Health misinformation:
```
This pill cures diabetes in 7 days.
```

Financial rumor:
```
Company X declared bankruptcy today.
```

---

## Continual Learning (Core Differentiator)

DebateShield does not only analyze claims — it learns from them.

Memory system features:
- Fuzzy matching at 85% similarity
- Instant cached responses for repeated claims
- Stores verdict, confidence, risk level, evidence, and timestamp
- Maintains consistency across evaluations

Planned future improvements:
- Drift detection when new evidence contradicts past verdicts
- Human moderator feedback loop
- Migration from SQLite to PostgreSQL for scalability

---

## Why This Project Stands Out

- Solves a real-world misinformation problem
- Fully autonomous decision-making
- Meaningful use of three sponsor tools
- Demonstrates continual learning in action
- Production-ready FastAPI backend
- Explainable multi-agent reasoning via Chain-of-Debate

---

## Team

Built for the Continual Learning Hackathon by a three-person team:
- Backend, agents, and memory system
- Integrations and action policy
- UI, demo, and final presentation

---

## License

MIT License — free to use, modify, and extend.

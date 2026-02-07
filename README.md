# 🛡️ DebateShield Lite

**Real-time Chain-of-Debate Misinformation Triage with Explainable AI**

A multi-agent AI system that ingests claims in real-time, retrieves fresh evidence, debates validity through specialized agents, and produces explainable verdicts with automatic action triggers.

## 🎯 Overview

DebateShield Lite implements a Chain-of-Debate (CoD) architecture with three specialized agents:
- **Verifier Agent**: Argues the claim could be true using retrieved evidence
- **Skeptic Agent**: Argues the claim is false/misleading using retrieved evidence  
- **Moderator Agent**: Adjudicates between arguments and produces final verdict

### Key Features

✅ **Explainable AI by Design** - Every verdict includes evidence, rationale, and debate transcript  
✅ **Real-time Evidence Retrieval** - Uses You.com API for fresh web grounding  
✅ **Automated Actions** - Intercom alerts and Plivo SMS escalation based on risk  
✅ **Operational Memory** - Stores past verdicts for faster, consistent responses  
✅ **Risk-Based Triage** - Classifies and escalates based on topic and confidence  

## 🛠️ Tech Stack

### Sponsor Tools (3+)
- **You.com** - Evidence retrieval and web search
- **Intercom** - Moderation workflow integration  
- **Plivo** - SMS escalation for high-risk claims

### Core Stack
- **Backend**: FastAPI, Uvicorn, Python 3.9+
- **LLM**: OpenAI GPT-4 (or compatible API)
- **Storage**: SQLite with fuzzy matching
- **Frontend**: Single-page HTML/CSS/JS

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+** installed
2. **API Keys** from:
   - OpenAI (or compatible LLM provider)
   - You.com API
   - Intercom (optional)
   - Plivo (optional)

### Installation

1. **Clone/Download the project**
```bash
cd debateshield-lite
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required `.env` variables:
```bash
LLM_API_KEY=your-openai-api-key
YOU_API_KEY=your-you-api-key
```

Optional (for full demo):
```bash
INTERCOM_TOKEN=your-token
PLIVO_AUTH_ID=your-auth-id
PLIVO_AUTH_TOKEN=your-token
PLIVO_FROM_NUMBER=+1XXXXXXXXXX
PLIVO_TO_NUMBER=+1XXXXXXXXXX
```

4. **Run the application**
```bash
python run.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Open your browser**
```
http://localhost:8000
```

## 📋 API Documentation

### POST /analyze

Analyze a claim using Chain-of-Debate.

**Request:**
```json
{
  "claim": "Breaking: city water is contaminated—do not drink today.",
  "context": {
    "source": "social",
    "audience": "public",
    "urgency_hint": "high"
  }
}
```

**Response:**
```json
{
  "claim": "...",
  "verdict": "false",
  "confidence": 84,
  "risk_level": "high",
  "topic": "emergency",
  "evidence_for": [...],
  "evidence_against": [...],
  "explainability": {
    "why_bullets": ["..."],
    "uncertainties": ["..."],
    "debate_transcript": [...]
  },
  "reply_templates": {...},
  "actions": {
    "intercom": {"sent": true, "id": "..."},
    "plivo_sms": {"sent": true, "to": "+1...", "message": "..."}
  },
  "memory": {
    "hit": false,
    "matched_claim_id": null
  }
}
```

### GET /health

Health check and memory stats.

### GET /stats

Get memory statistics (total claims, verdict breakdown).

## 🎭 Demo Script

Perfect for hackathon demos (2-3 minutes):

1. **Paste a high-risk false claim:**
   ```
   "Breaking: city water is contaminated—do not drink today."
   ```

2. **Show the verdict:**
   - FALSE verdict with 80%+ confidence
   - HIGH risk classification
   - Evidence table with sources

3. **Highlight explainability:**
   - Scroll to "Why We Think This" section
   - Show debate transcript between agents
   - Point out uncertainty notes (if any)

4. **Demo autopilot actions:**
   - ✅ Intercom alert sent
   - ✅ SMS escalation triggered (high risk + false + high confidence)

5. **Test memory system:**
   - Paste the **same claim** again
   - Show "Memory Hit!" indicator
   - Faster response time

## 🎯 Use Cases

### 1. Moderation Copilot
Community moderators paste viral claims → get instant fact-check with evidence → receive moderation reply template

### 2. Customer Support Safety
Support agents check suspicious claims from users → reduce misinformation in responses → evidence-backed answers

### 3. Emergency Escalation
High-risk claims (water contamination, evacuation orders) → automatic SMS to safety team → rapid verification

## 🧠 How Chain-of-Debate Works

```
┌─────────────┐
│ Input Claim │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Memory Check        │ ◄── Fuzzy match past claims
│ (85%+ threshold)    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Evidence Retrieval  │ ◄── You.com search
│ • Support query     │     (claim + "debunk claim")
│ • Refute query      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ VERIFIER Agent      │ ◄── Argues FOR the claim
│ • Key points        │
│ • Evidence for      │
│ • Questions         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ SKEPTIC Agent       │ ◄── Argues AGAINST the claim
│ • Key points        │
│ • Evidence against  │
│ • Risk flags        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ MODERATOR Agent     │ ◄── Final adjudication
│ • Verdict           │
│ • Confidence        │
│ • Risk assessment   │
│ • Explainability    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Action Engine       │ ◄── Risk-based triggers
│ • Intercom alert    │     (medium/high risk)
│ • Plivo SMS         │     (high risk + false)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Store to Memory     │ ◄── For future reuse
└─────────────────────┘
```

## 📊 Risk-to-Action Policy

| Risk Level | Topics | Intercom Alert | Plivo SMS |
|-----------|--------|---------------|-----------|
| **HIGH** | Health, Emergency, Public Safety | ✅ Yes | ✅ If false + 70%+ confidence |
| **MEDIUM/HIGH** | Finance, Scams, Security | ✅ Yes | ❌ No |
| **MEDIUM** | Rumors, Politics | ✅ Yes | ❌ No |
| **LOW** | Opinions, Harmless | ❌ No | ❌ No |

## 🔧 Configuration

### Environment Variables

```bash
# Required
LLM_API_KEY=          # OpenAI or compatible
LLM_MODEL=            # Default: gpt-4-turbo-preview
YOU_API_KEY=          # You.com search API

# Optional - Intercom
INTERCOM_TOKEN=       # Bearer token
INTERCOM_TARGET_ID=   # Admin/user ID

# Optional - Plivo
PLIVO_AUTH_ID=        # Auth ID
PLIVO_AUTH_TOKEN=     # Auth token
PLIVO_FROM_NUMBER=    # Your Plivo number
PLIVO_TO_NUMBER=      # Destination number

# App Settings
APP_ENV=dev           # dev or production
DATABASE_PATH=./debateshield.db
```

## 📁 Project Structure

```
debateshield-lite/
├── main.py              # FastAPI application
├── config.py            # Configuration management
├── memory.py            # SQLite memory system
├── you_search.py        # You.com integration
├── cod_agents.py        # Chain-of-Debate agents
├── integrations.py      # Intercom + Plivo
├── index.html           # Frontend UI
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── .env                 # Your secrets (gitignored)
└── README.md            # This file
```

## 🚢 Deployment

### Local Development
```bash
python run.py
# OR
uvicorn main:app --reload
```

### Render Deployment

1. Create new Web Service on Render
2. Connect your Git repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard
5. Deploy!

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Sample Claims for Testing

1. **High Risk Emergency:**
   ```
   Breaking: city water is contaminated—do not drink today.
   ```

2. **High Risk Health:**
   ```
   This supplement cures diabetes in 7 days.
   ```

3. **Medium Risk Finance:**
   ```
   Company X declared bankruptcy today.
   ```

4. **Medium Risk Policy:**
   ```
   New law bans international students from working immediately.
   ```

## 🎓 Continual Learning Features

### Operational Memory
- Fuzzy matching (85%+ threshold) finds similar claims
- Returns cached verdict for 90%+ matches
- Stores: verdict, confidence, risk, evidence, actions, timestamp
- Enables consistent moderation decisions

### Future Enhancements
- Drift detection: flag when evidence contradicts memory
- Domain-specific expert agents (health, finance)
- Analytics dashboard for verdict trends
- Feedback loop: moderator corrections → improve future verdicts

## 🤝 Team & Credits

**Built for Continual Learning Hackathon**

Team of 3:
- Engineer A: Backend + CoD agents + memory
- Engineer B: Integrations + action policy
- Engineer C: UI + demo + polish

**Sponsor Tools:**
- You.com for evidence retrieval
- Intercom for workflow integration  
- Plivo for SMS escalation

## 📄 License

MIT License - feel free to use and modify!

## 🐛 Troubleshooting

### "LLM_API_KEY not configured"
→ Add your OpenAI key to `.env`

### "YOU_API_KEY not configured"  
→ System will use mock data for demo, but get a real key for production

### Intercom/Plivo errors
→ These are optional - system works without them (simulated mode)

### Database locked
→ Delete `debateshield.db` and restart

## 📞 Support

For questions or issues:
1. Check the `/health` endpoint
2. Review logs in terminal
3. Ensure all required API keys are set

---

**Built with ❤️ for safer, more transparent information ecosystems**

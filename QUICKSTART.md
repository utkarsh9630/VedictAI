# 🚀 QUICKSTART GUIDE - DebateShield Lite

**Get running in under 5 minutes!**

## Step 1: Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

## Step 2: Configure API Keys (2 min)

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add **at minimum**:

```bash
LLM_API_KEY=sk-...your-openai-key...
YOU_API_KEY=...your-you-api-key...
```

**Don't have keys?** The app will still run with mock data for demo purposes!

## Step 3: Run! (1 min)

```bash
python run.py
```

**OR** if that doesn't work:

```bash
python3 run.py
```

**OR** directly with uvicorn:

```bash
uvicorn main:app --reload
```

## Step 4: Open Browser

Go to: **http://localhost:8000**

## 🎯 Quick Demo (30 seconds)

1. Click on a sample claim (or paste your own)
2. Hit **"Analyze Claim"**
3. Watch the Chain-of-Debate magic! ✨

You'll see:
- ✅ Verdict with confidence meter
- 📚 Evidence for and against
- 💡 Debate transcript between agents
- ⚡ Autopilot actions (Intercom/SMS)

## 🧪 Test the Memory System

1. Analyze any claim
2. **Copy the exact same claim**
3. Paste and analyze again
4. See "Memory Hit!" - instant response! ⚡

## 📱 Optional: Full Integration

If you want **real** Intercom alerts and SMS:

```bash
# Add to .env:
INTERCOM_TOKEN=your-token
INTERCOM_TARGET_ID=your-id

PLIVO_AUTH_ID=your-auth-id
PLIVO_AUTH_TOKEN=your-token
PLIVO_FROM_NUMBER=+1XXXXXXXXXX
PLIVO_TO_NUMBER=+1XXXXXXXXXX
```

Without these, the system will **simulate** actions (perfect for demo!).

## 🆘 Troubleshooting

### Import errors?
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Port 8000 already in use?
```bash
uvicorn main:app --port 8001
# Then visit http://localhost:8001
```

### OpenAI key error?
Make sure your `.env` file has:
```bash
LLM_API_KEY=sk-proj-...
```

## 🎭 Hackathon Demo Tips

**Perfect 2-minute demo:**

1. **Introduction (15s):**
   - "This is DebateShield - AI agents debate claims to find truth"
   - "Uses You.com, Intercom, and Plivo"

2. **First Claim (45s):**
   - Paste high-risk false claim
   - Show verdict + evidence + debate
   - Show Intercom alert + SMS sent

3. **Memory Demo (30s):**
   - Paste same claim
   - "See? Memory hit - instant response!"

4. **Tech Stack (30s):**
   - "3 AI agents: Verifier, Skeptic, Moderator"
   - "Chain-of-Debate for explainability"
   - "Real actions via Intercom/Plivo"

## 📊 API Testing

Test the API directly:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "claim": "Breaking: city water is contaminated",
    "context": {"source": "social"}
  }'
```

Check health:
```bash
curl http://localhost:8000/health
```

Get stats:
```bash
curl http://localhost:8000/stats
```

## 🎯 Sample Claims to Try

### High Risk + False → Triggers SMS
```
Breaking: city water is contaminated—do not drink today.
```

### High Risk + Health
```
This supplement cures diabetes in 7 days.
```

### Medium Risk + Finance
```
Company X declared bankruptcy today.
```

### Political Claim
```
New law bans international students from working immediately.
```

## 🚢 Deploy to Render (Optional)

1. Push code to GitHub
2. Create Web Service on Render
3. Set environment variables
4. Deploy!

See README.md for details.

## 📖 Next Steps

- Read full **README.md** for architecture details
- Check **API documentation** at http://localhost:8000/docs
- Customize agents in `cod_agents.py`
- Add custom integrations in `integrations.py`

---

**You're all set! 🎉**

Need help? Check the README.md or look at the code comments.

# 🚢 Deployment Guide - DebateShield Lite

Deploy your misinformation triage system to production!

## 🎯 Deployment Options

1. **Render** - Easiest, recommended for hackathons
2. **Railway** - Alternative to Render
3. **Fly.io** - Global edge deployment
4. **Docker** - Self-hosted or any container platform
5. **AWS/GCP/Azure** - Enterprise deployment

---

## 1. 🟦 Render Deployment (Recommended)

**Why Render?** Free tier, automatic HTTPS, simple setup.

### Steps:

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/debateshield.git
   git push -u origin main
   ```

2. **Create Render Account:**
   - Go to https://render.com
   - Sign up (free)

3. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Name:** debateshield-lite
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables:**
   In the Render dashboard, add:
   ```
   LLM_API_KEY=your-openai-key
   YOU_API_KEY=your-you-key
   INTERCOM_TOKEN=your-intercom-token (optional)
   PLIVO_AUTH_ID=your-plivo-id (optional)
   PLIVO_AUTH_TOKEN=your-plivo-token (optional)
   PLIVO_FROM_NUMBER=+1XXXXXXXXXX (optional)
   PLIVO_TO_NUMBER=+1XXXXXXXXXX (optional)
   APP_ENV=production
   ```

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 2-3 minutes
   - Visit your URL: `https://debateshield-lite.onrender.com`

### Render Free Tier Limits:
- ✅ Free SSL/HTTPS
- ✅ 512 MB RAM
- ✅ Auto-restart
- ⚠️ Sleeps after 15 min inactivity (wakes on request)

---

## 2. 🚂 Railway Deployment

Similar to Render:

1. **Create Railway account:** https://railway.app
2. **New Project → Deploy from GitHub**
3. **Configure:**
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Add environment variables** in Railway dashboard
5. **Deploy!**

---

## 3. 🐳 Docker Deployment

### Create Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and run:

```bash
# Build image
docker build -t debateshield-lite .

# Run container
docker run -p 8000:8000 \
  -e LLM_API_KEY=your-key \
  -e YOU_API_KEY=your-key \
  debateshield-lite
```

### Docker Compose:

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  debateshield:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LLM_API_KEY=${LLM_API_KEY}
      - YOU_API_KEY=${YOU_API_KEY}
      - INTERCOM_TOKEN=${INTERCOM_TOKEN}
      - PLIVO_AUTH_ID=${PLIVO_AUTH_ID}
      - PLIVO_AUTH_TOKEN=${PLIVO_AUTH_TOKEN}
      - PLIVO_FROM_NUMBER=${PLIVO_FROM_NUMBER}
      - PLIVO_TO_NUMBER=${PLIVO_TO_NUMBER}
      - APP_ENV=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

---

## 4. ✈️ Fly.io Deployment

1. **Install flyctl:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Initialize app:**
   ```bash
   fly launch
   ```

4. **Set secrets:**
   ```bash
   fly secrets set LLM_API_KEY=your-key
   fly secrets set YOU_API_KEY=your-key
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

---

## 5. ☁️ AWS EC2 Deployment

### Quick Setup:

1. **Launch EC2 instance** (Ubuntu 22.04, t2.micro)

2. **SSH into instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv -y
   ```

4. **Clone and setup:**
   ```bash
   git clone https://github.com/yourusername/debateshield.git
   cd debateshield
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Create .env file:**
   ```bash
   nano .env
   # Add your keys
   ```

6. **Run with systemd:**

   Create `/etc/systemd/system/debateshield.service`:
   ```ini
   [Unit]
   Description=DebateShield Lite
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/debateshield
   Environment="PATH=/home/ubuntu/debateshield/venv/bin"
   ExecStart=/home/ubuntu/debateshield/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable debateshield
   sudo systemctl start debateshield
   ```

7. **Setup nginx reverse proxy** (optional but recommended)

---

## 🔒 Production Checklist

Before going live:

- [ ] Use production-grade API keys
- [ ] Set `APP_ENV=production` in environment
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure rate limiting
- [ ] Set up logging
- [ ] Create backup strategy for database
- [ ] Test all integrations (Intercom, Plivo)
- [ ] Set up health check monitoring
- [ ] Configure CORS if needed

---

## 🔍 Health Monitoring

### Add to your monitoring:

```bash
# Health check endpoint
curl https://your-domain.com/health

# Expected response:
{
  "status": "healthy",
  "version": "1.0.0",
  "memory_stats": {...}
}
```

### Uptime Monitoring Services:
- UptimeRobot (free)
- Pingdom
- Better Uptime
- StatusCake

---

## 🐛 Debugging Production Issues

### Check logs:

**Render:**
```bash
# In Render dashboard → Logs tab
```

**Docker:**
```bash
docker logs debateshield-lite
```

**EC2/systemd:**
```bash
sudo journalctl -u debateshield -f
```

### Common issues:

1. **Port binding error:**
   - Make sure using `$PORT` env variable (Render, Railway)
   - Check firewall rules (EC2)

2. **Database locked:**
   - SQLite limitation with concurrent writes
   - Consider upgrading to PostgreSQL for production

3. **API timeouts:**
   - Increase timeout limits
   - Check You.com/OpenAI rate limits

4. **Memory issues:**
   - Monitor with `htop` or platform dashboard
   - Free tier might be too small for heavy load

---

## 📊 Scaling Considerations

For production at scale:

1. **Database:**
   - Migrate from SQLite to PostgreSQL
   - Add connection pooling

2. **Caching:**
   - Add Redis for claim cache
   - Cache You.com results

3. **Queue:**
   - Add Celery for async processing
   - Use RabbitMQ or Redis as broker

4. **Load balancing:**
   - Multiple instances behind nginx
   - Use platform load balancer

5. **CDN:**
   - Serve static UI through CDN
   - Cache API responses where appropriate

---

## 💰 Cost Estimates

### Free Tier (Perfect for Hackathon):
- **Hosting:** Render/Railway (free)
- **Database:** SQLite (included)
- **Total:** $0/month ✨

### Production (Medium Traffic):
- **Hosting:** Render/Railway ($7-25/month)
- **OpenAI API:** ~$10-50/month
- **You.com API:** Check pricing
- **Intercom:** From $39/month
- **Plivo:** $0.0075/SMS
- **Total:** ~$60-150/month

---

## 🎯 Quick Deploy for Demo

**Fastest option for hackathon demo:**

1. Deploy to Render (5 min)
2. Add minimal env vars (LLM + You.com keys)
3. Share link: `https://your-app.onrender.com`
4. Done! ✨

---

## 📞 Support

Deployment issues?
1. Check platform docs
2. Review logs
3. Test health endpoint
4. Verify environment variables

**Good luck with deployment! 🚀**

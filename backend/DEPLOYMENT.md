# Deployment Guide - Physical AI Textbook Backend

Quick guide for deploying the FastAPI backend to production.

## Pre-Deployment Checklist

Before deploying, ensure you have:

- [x] Neon Postgres database created and connection string ready
- [x] Qdrant Cloud instance created with API key
- [x] GitHub repository with your code pushed
- [ ] Anthropic API key (optional - can add later)
- [ ] Railway or Render account created

## Option 1: Railway (Recommended - Easiest)

Railway offers the simplest deployment with automatic HTTPS, environment management, and GitHub integration.

### Step-by-Step Railway Deployment

#### 1. Prepare Your Repository

```bash
cd backend
git status  # Verify all files are committed
git push origin main  # Push to GitHub if not already done
```

#### 2. Create Railway Project

1. Visit https://railway.app
2. Login with your GitHub account
3. Click **New Project**
4. Select **Deploy from GitHub repo**
5. Authorize Railway to access your repositories
6. Select your `BOOK` repository
7. Railway will detect the Python app automatically

#### 3. Configure Root Directory (Important!)

Since backend is in a subdirectory:

1. Go to **Settings** tab in Railway
2. Find **Root Directory** setting
3. Set to: `backend`
4. Click **Save**

#### 4. Add Environment Variables

In Railway dashboard, click on your service, then **Variables** tab:

```env
DATABASE_URL=postgresql://neondb_owner:npg_ekS6IXOtG7lx@ep-twilight-thunder-a1s3ceaf.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

SECRET_KEY=b4070e29130a0e2cef8e36043bc8c0171331ade41572a6d309f2225dfcc27fe4

QDRANT_URL=https://2a460a44-355b-4387-8d64-f69f3444a05c.europe-west3-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=<your_qdrant_key>
QDRANT_COLLECTION_NAME=textbook_chunks

ANTHROPIC_API_KEY=
# Leave empty for now - add when you get the key
# App works without it (graceful degradation)

CLAUDE_MODEL=claude-3-5-sonnet-20241022

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

Click **Add Variable** for each one.

#### 5. Deploy

1. Railway will automatically build and deploy
2. Watch the **Deployments** tab for build logs
3. Build takes ~2-3 minutes
4. Once deployed, you'll see a public URL

#### 6. Get Your Public URL

1. Click on your service in Railway
2. Go to **Settings** tab
3. Under **Domains**, click **Generate Domain**
4. You'll get: `https://your-app-name.up.railway.app`

#### 7. Test Your Deployment

Test the health endpoint:

```bash
curl https://your-app-name.up.railway.app/api/health
```

Expected response:
```json
{"status": "healthy"}
```

#### 8. Update CORS for Production

After deployment, update `backend/main.py` to allow your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://your-frontend-domain.com",  # Production frontend
        "https://your-app-name.up.railway.app"  # Railway backend (for testing)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push - Railway will auto-deploy the update.

### Monitoring on Railway

- **Logs**: Click **Deployments** → **View Logs** for real-time logs
- **Metrics**: See CPU, Memory, Network usage
- **Restart**: Click **...** menu → **Restart** if needed

### Railway Free Tier Limits

- $5 free credits/month (plenty for testing)
- No credit card required initially
- Automatic sleep after inactivity (wakes on request)

---

## Option 2: Render

Render is another good free option with similar features.

### Step-by-Step Render Deployment

#### 1. Create Web Service

1. Go to https://render.com
2. Login with GitHub
3. Click **New** → **Web Service**
4. Connect your GitHub repository
5. Select `backend` as root directory

#### 2. Configure Build Settings

In the Render dashboard:

- **Name**: `physical-ai-textbook-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `backend`

#### 3. Add Environment Variables

In **Environment** tab, add the same variables as Railway (above).

#### 4. Deploy

1. Click **Create Web Service**
2. Render will build and deploy (takes ~3-5 minutes on free tier)
3. You'll get URL: `https://your-app-name.onrender.com`

#### 5. Test

```bash
curl https://your-app-name.onrender.com/api/health
```

### Render Free Tier Notes

- Spins down after 15 minutes of inactivity
- First request after sleep takes ~30-60 seconds to wake up
- Good for testing, not ideal for production

---

## Post-Deployment Testing

After deployment, test all endpoints:

### 1. Health Check
```bash
curl https://your-app.railway.app/api/health
```

### 2. Signup
```bash
curl -X POST https://your-app.railway.app/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepass123",
    "name": "Test User",
    "programming_level": "beginner",
    "hardware": "none"
  }'
```

### 3. Login
```bash
curl -X POST https://your-app.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepass123"
  }'
```

Save the `access_token` from response.

### 4. Get Current User
```bash
curl https://your-app.railway.app/api/auth/me \
  -H "Authorization: Bearer <your_access_token>"
```

### 5. Ask Question (RAG)
```bash
curl -X POST https://your-app.railway.app/api/chat/question \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a CNN?"}'
```

### 6. Personalize Content
```bash
curl -X POST https://your-app.railway.app/api/personalize/chapter \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "chapter_id": "ch1",
    "chapter_content": "Neural networks are..."
  }'
```

### 7. Translate Content
```bash
curl -X POST https://your-app.railway.app/api/translate/chapter \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "chapter_id": "ch1",
    "chapter_content": "Neural networks are...",
    "target_language": "ur"
  }'
```

---

## Troubleshooting

### Database Connection Errors

**Error**: `connection refused` or `timeout`

**Fix**:
1. Check DATABASE_URL has `?sslmode=require`
2. Verify Neon database is active (not paused)
3. Test connection from Neon dashboard

### Module Not Found Errors

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Fix**:
1. Verify `requirements.txt` is in `backend/` folder
2. Check Railway build logs
3. Ensure root directory is set to `backend`

### CORS Errors from Frontend

**Error**: `Access to fetch blocked by CORS policy`

**Fix**:
1. Add your frontend domain to `allow_origins` in `main.py`
2. Commit and push (Railway auto-deploys)
3. Wait for new deployment to complete

### Environment Variables Not Loading

**Error**: `KeyError: 'DATABASE_URL'` or validation errors

**Fix**:
1. Double-check all variables are added in Railway dashboard
2. No typos in variable names
3. Click **Restart** service after adding variables

### Port Binding Errors

**Error**: `Error binding to port`

**Fix**:
Railway/Render set `PORT` automatically. Ensure your start command uses:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**NOT** hardcoded:
```
uvicorn main:app --host 0.0.0.0 --port 8000  # Wrong!
```

---

## Adding Anthropic API Key Later

When you get your Anthropic API key:

1. Go to Railway dashboard → **Variables**
2. Find `ANTHROPIC_API_KEY`
3. Update value with your real key
4. Railway will automatically restart
5. All AI features (RAG, personalization, translation) will activate

No code changes needed - just update the environment variable!

---

## Connect Frontend to Backend

In your frontend `.env`:

```env
# For Docusaurus or Next.js frontend
REACT_APP_API_URL=https://your-app.railway.app
# or
NEXT_PUBLIC_API_URL=https://your-app.railway.app
```

Update your frontend API client to use this URL instead of `http://localhost:8000`.

---

## Continuous Deployment

Railway automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Railway detects the push and deploys in ~2 minutes.

To disable auto-deploy:
1. Go to **Settings** in Railway
2. Find **Deploy Triggers**
3. Toggle off **Auto Deploy**

---

## Success Criteria

Your deployment is successful when:

- [ ] `/api/health` returns `{"status": "healthy"}`
- [ ] Signup creates user and returns JWT token
- [ ] Login works with correct credentials
- [ ] `/api/auth/me` returns user data with valid token
- [ ] Database persists data (create user, logout, login again works)
- [ ] CORS allows requests from your frontend domain
- [ ] Logs show no critical errors
- [ ] All 9 endpoints respond correctly

---

## Need Help?

- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **FastAPI Deployment**: https://fastapi.tiangolo.com/deployment/
- **Neon Docs**: https://neon.tech/docs/introduction

Check Railway/Render logs first - they usually show the exact error!

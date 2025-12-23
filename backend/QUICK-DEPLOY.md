# Quick Deploy Reference

Fast reference for deploying to Railway.

## 1. Push to GitHub

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

## 2. Railway Setup

1. Visit: https://railway.app
2. Login with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. Select your repository
5. **Settings** → **Root Directory** = `backend`

## 3. Environment Variables

Go to **Variables** tab, add these:

```env
DATABASE_URL=postgresql://neondb_owner:npg_ekS6IXOtG7lx@ep-twilight-thunder-a1s3ceaf.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

SECRET_KEY=b4070e29130a0e2cef8e36043bc8c0171331ade41572a6d309f2225dfcc27fe4

QDRANT_URL=https://2a460a44-355b-4387-8d64-f69f3444a05c.europe-west3-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=<paste_your_key>
QDRANT_COLLECTION_NAME=textbook_chunks

ANTHROPIC_API_KEY=
# Leave empty - add later when you get key

CLAUDE_MODEL=claude-3-5-sonnet-20241022
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

## 4. Deploy

- Railway auto-deploys (wait 2-3 min)
- **Settings** → **Domains** → **Generate Domain**
- Get URL: `https://your-app.up.railway.app`

## 5. Test

```bash
curl https://your-app.up.railway.app/api/health
```

Should return: `{"status":"healthy"}`

## 6. Update CORS (After Deploy)

In `main.py`, add your frontend domain:

```python
allow_origins=[
    "http://localhost:3000",
    "https://your-frontend-domain.com"
],
```

Push to auto-deploy update.

## Done!

Your backend is live. Update frontend to use the Railway URL.

---

## Quick Troubleshooting

**Build fails**: Check Railway logs, verify requirements.txt exists
**DB error**: Verify DATABASE_URL has `?sslmode=require`
**CORS error**: Add frontend domain to main.py
**500 error**: Check Railway logs for missing env vars

---

## Add API Key Later

When you get Anthropic API key:

1. Railway → **Variables**
2. Update `ANTHROPIC_API_KEY=<your_key>`
3. Auto-restarts, AI features activate

No code changes needed!

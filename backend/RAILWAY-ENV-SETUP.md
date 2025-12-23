# Railway Environment Variables Setup

## Required Environment Variables

Railway dashboard me ye **zaruri** environment variables add karein:

### 1. Database Configuration
```
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
```
👉 Get from: https://console.neon.tech/app/projects

### 2. JWT Authentication
```
SECRET_KEY=your_secret_key_here
```
👉 Generate with:
```bash
openssl rand -hex 32
```

### 3. Qdrant Vector Database
```
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=textbook_chunks
```
👉 Get from: https://cloud.qdrant.io/

### 4. Claude API (Optional - can add later)
```
ANTHROPIC_API_KEY=sk-ant-xxx
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```
👉 Get from: https://console.anthropic.com/

## How to Add on Railway

1. Railway dashboard me apni service ko open karein
2. **Variables** tab par jayein
3. Click **+ New Variable**
4. Har variable ka naam aur value enter karein
5. Click **Add** ya **Deploy** (automatic redeploy hoga)

## Verification

Deployment ke baad:
- Health check: `https://your-app.up.railway.app/api/health`
- API docs: `https://your-app.up.railway.app/docs`

## Common Issues

### Health Check Fails
- Check ki `DATABASE_URL` sahi hai
- Neon database publicly accessible hai (default yes)
- Railway logs check karein: `railway logs`

### Database Connection Error
- Verify `DATABASE_URL` format me `?sslmode=require` hai
- Neon dashboard me IP allowlist check karein (should be 0.0.0.0/0)

### Import Errors (Locally)
- Run: `pip install -r requirements.txt`
- VS Code: Reload window (Ctrl+Shift+P > "Reload Window")

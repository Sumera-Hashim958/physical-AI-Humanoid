# Physical AI Textbook - Backend

FastAPI backend for the AI-native interactive textbook with RAG chatbot, personalization, and Urdu translation.

## Technology Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: Neon Serverless PostgreSQL
- **Vector DB**: Qdrant Cloud (free tier)
- **AI Model**: Claude API (Anthropic)
- **Auth**: Better-auth / JWT
- **Deployment**: Railway

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required credentials:
- **Neon Database**: Sign up at https://neon.tech/
- **Qdrant Cloud**: Sign up at https://cloud.qdrant.io/
- **Anthropic API**: Get key from https://console.anthropic.com/

### 3. Database Setup

The database schema is automatically created on first startup using `scripts/init_db.sql`.

Tables created:
- `users` - User accounts with authentication
- `chat_history` - RAG chatbot Q&A history
- `user_progress` - Chapter completion tracking
- `translations_cache` - Cached Urdu translations (shared across users)
- `personalized_content_cache` - Cached personalized content per user level

No manual migration needed - just run the server and it will initialize automatically.

### 4. Run Development Server

```bash
uvicorn main:app --reload --port 8000
```

API will be available at http://localhost:8000
API docs at http://localhost:8000/docs

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your local config (gitignored)
├── app/
│   ├── routers/          # API endpoints
│   │   ├── auth.py       # Authentication endpoints
│   │   ├── chat.py       # RAG chatbot endpoints
│   │   ├── personalize.py # Personalization endpoints
│   │   ├── translate.py   # Translation endpoints
│   │   └── progress.py    # Progress tracking endpoints
│   ├── services/         # Business logic
│   │   ├── claude_service.py    # Claude API wrapper
│   │   ├── qdrant_service.py    # Qdrant vector operations
│   │   ├── database_service.py  # Postgres operations
│   │   └── auth_service.py      # Authentication logic
│   └── models/           # Pydantic schemas
│       ├── user.py       # User models
│       ├── chat.py       # Chat models
│       └── content.py    # Content models
└── tests/                # Test files (to be added)
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

### RAG Chatbot
- `POST /api/chat/ask` - Ask question
- `POST /api/chat/selected-text` - Ask about selected text

### Personalization
- `POST /api/personalize/chapter` - Get personalized chapter
- `PUT /api/user/settings` - Update user level/hardware

### Translation
- `POST /api/translate/chapter` - Translate to Urdu

### Progress Tracking
- `GET /api/user/progress` - Get user progress
- `POST /api/user/progress/mark` - Mark chapter complete

### Health
- `GET /api/health` - Health check

## Development Guidelines

See `../.specify/memory/constitution.md` for full guidelines.

**Key Principles**:
- Use Claude API exclusively (NOT OpenAI)
- Cache expensive operations (translations, personalizations)
- Validate all user input
- Log all API calls
- Never expose API keys

## Token Budget

- RAG query: ~2200 input tokens
- Personalization: Max 4000 tokens/chapter
- Translation: Max 3000 tokens/chapter
- Daily budget: <$10 for 100 users

## Rate Limiting

- 20 questions/hour per user
- 5 translations/day per user
- 5 personalizations/day per user

## Deployment

### Railway Deployment (Recommended)

Railway provides the easiest deployment with automatic HTTPS and free tier.

#### Prerequisites
- GitHub account
- Railway account (sign up at https://railway.app)
- Your Neon Database and Qdrant Cloud already set up

#### Step 1: Push to GitHub

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

#### Step 2: Deploy on Railway

1. Go to https://railway.app and login with GitHub
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Choose your repository
5. Railway will auto-detect the Python app

#### Step 3: Configure Environment Variables

In Railway dashboard, go to **Variables** tab and add:

```env
DATABASE_URL=postgresql://...  # Your Neon connection string
SECRET_KEY=...  # Generate with: openssl rand -hex 32
QDRANT_URL=https://...
QDRANT_API_KEY=...
QDRANT_COLLECTION_NAME=textbook_chunks
ANTHROPIC_API_KEY=...  # Add when available
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

#### Step 4: Deploy

1. Railway will automatically build and deploy
2. You'll get a public URL like: `https://your-app.up.railway.app`
3. Test health endpoint: `https://your-app.up.railway.app/api/health`

#### Step 5: Update Frontend CORS

In `backend/main.py`, update allowed origins:

```python
allow_origins=[
    "http://localhost:3000",
    "https://your-frontend-domain.com"  # Add your production frontend URL
],
```

### Alternative: Render Deployment

If you prefer Render (also has free tier):

1. Go to https://render.com
2. Create **New Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard

### Post-Deployment Checklist

- [ ] Health check returns 200: `GET /api/health`
- [ ] Signup works: `POST /api/auth/signup`
- [ ] Login works: `POST /api/auth/login`
- [ ] Protected endpoints require auth: `GET /api/auth/me`
- [ ] Database tables created automatically on startup
- [ ] CORS allows your frontend domain
- [ ] All environment variables set correctly

### Monitoring

Railway provides:
- **Logs**: Real-time application logs
- **Metrics**: CPU, Memory, Network usage
- **Deployments**: Git-based deployments on every push

### Troubleshooting

**Database connection fails:**
- Verify DATABASE_URL includes `?sslmode=require`
- Check Neon database is not paused (free tier pauses after inactivity)

**Startup errors:**
- Check Railway logs for missing environment variables
- Verify all dependencies in requirements.txt

**CORS errors:**
- Add your frontend domain to CORS allowed origins
- Redeploy after changing main.py

## Testing

```bash
pytest tests/
```

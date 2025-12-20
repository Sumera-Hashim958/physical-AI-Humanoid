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

Run migrations (to be created):

```bash
# TODO: Add database migration commands
```

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

Deploy to Railway:

```bash
# TODO: Add deployment commands
```

## Testing

```bash
pytest tests/
```

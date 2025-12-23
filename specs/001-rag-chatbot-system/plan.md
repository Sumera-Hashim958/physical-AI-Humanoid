# Implementation Plan: RAG Chatbot System (Backend Only)

**Branch**: `001-rag-chatbot-system` | **Date**: 2025-12-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-rag-chatbot-system/spec.md`

## Summary

Build FastAPI backend for RAG chatbot system with four core capabilities: (1) Grounded Q&A using Claude API + Qdrant vector search that cites textbook sources, (2) User authentication with Better-auth (signup/login), (3) Chapter personalization based on user programming level (beginner/intermediate/advanced), and (4) Urdu translation with caching. Frontend (Docusaurus) already exists and displays textbook content. Backend must integrate with existing Neon Postgres, Qdrant Cloud, and Claude API while staying within $10/day token budget for 100 users.

**Technical Approach**: Extend existing backend/main.py by adding 5 routers (auth, chat, personalize, translate, progress), 3 services (claude_service.py, qdrant_service.py, db_service.py), and Pydantic models. Use Better-auth for JWT authentication, implement caching for translations/personalizations in Postgres, and enforce rate limiting (20 questions/hour, 5 translations/day, 5 personalizations/day) to control costs.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.115.0, anthropic 0.39.0 (Claude API), qdrant-client 1.12.0, psycopg2-binary 2.9.10, python-jose 3.3.0 (JWT), passlib 1.7.4 (bcrypt)
**Storage**: Neon Serverless Postgres (user data, chat history, caches), Qdrant Cloud (vector embeddings)
**Testing**: Manual testing via curl/Postman for MVP (pytest integration tests in future phase)
**Target Platform**: Railway (free tier or $5/month), Linux server
**Project Type**: Web backend (FastAPI REST API)
**Performance Goals**: <3s total response time for RAG queries (95th percentile), <200ms for cached translations/personalizations
**Constraints**:
- Token budget: <$10/day for 100 users
- RAG context: max 2200 tokens per query (4-5 chunks)
- Personalization: max 4000 tokens per chapter
- Translation: max 3000 tokens per chapter
- Rate limits: 20 questions/hour, 5 translations/day, 5 personalizations/day
**Scale/Scope**: MVP for 100 active users, ~50 textbook chapters, ~500-1000 chunks in Qdrant

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✅ I. AI-Native First - RAG-Only Responses**
- Use Claude API (Anthropic) exclusively for all AI tasks
- RAG pipeline: Qdrant retrieval → Claude with context → grounded answer
- Cite sources in responses; respond "I don't have this information in the book" when insufficient context
- **Status**: PASS - Architecture uses Claude API, retrieval-first design

**✅ II. Performance & Speed**
- Target <3s RAG response time (includes Qdrant + Claude latency)
- Token budgets enforced: 2200 tokens/query, 4000 tokens/personalization, 3000 tokens/translation
- Daily budget <$10 for 100 users
- **Status**: PASS - Performance targets align with constitution

**✅ III. Simplicity & Minimalism**
- Reuse existing backend structure (main.py, app/routers, app/services, app/models)
- No heavyweight frameworks beyond FastAPI
- Direct Postgres queries via psycopg2, no ORM
- **Status**: PASS - Minimal dependencies, no over-engineering

**✅ IV. Modular Architecture - Frontend/Backend Separation**
- Backend: FastAPI in /backend folder
- Frontend: Docusaurus in /frontend folder (already complete)
- Clean separation: backend exposes REST API, frontend consumes it
- **Status**: PASS - Proper separation maintained

**✅ V. Free-Tier & Cost Constraints**
- Qdrant Cloud free tier (1GB storage)
- Neon Postgres free tier (512MB)
- Railway free tier or $5/month
- Claude API: monitor usage, stay under $10/day
- **Status**: PASS - All infrastructure on free tiers, cost tracking implemented

**✅ VI. Rapid Deployment**
- Backend deploys to Railway in <90 seconds
- No complex build steps
- **Status**: PASS - FastAPI deploys quickly

**✅ VII. Grounded & Accurate Responses**
- RAG retrieval ensures answers based on textbook content only
- Citation tracking mandatory
- Fallback message when context insufficient
- **Status**: PASS - Core design principle

**✅ VIII. Mobile-First Design**
- Backend provides REST API; frontend (already built) handles mobile responsiveness
- **Status**: PASS - Backend is API-only

**✅ IX. Personalized Learning**
- Adapt content by user level (beginner/intermediate/advanced)
- Cache personalized chapters in Postgres
- **Status**: PASS - Implemented in /api/personalize router

**✅ X. Multilingual Support - Urdu Translation**
- Translate chapters to Urdu via Claude API
- Cache translations in Postgres
- Rate limit: 5 chapters/day per user
- **Status**: PASS - Implemented in /api/translate router

**✅ XI. Progress Tracking & Analytics**
- Track chapters read, questions asked in Postgres
- Expose via /api/user/progress endpoint
- **Status**: PASS - Implemented in progress router

**Overall Constitution Compliance**: ✅ ALL GATES PASSED

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-chatbot-system/
├── plan.md              # This file
├── spec.md              # Feature specification
├── checklists/
│   └── requirements.md  # Spec quality checklist (already complete)
└── tasks.md             # Will be generated by /sp.tasks command
```

### Source Code (repository root)

```text
backend/
├── main.py                          # FastAPI app (already exists, will extend)
├── requirements.txt                 # Dependencies (already complete)
├── .env.example                     # Env template (already exists)
├── app/
│   ├── __init__.py                  # (exists)
│   ├── routers/
│   │   ├── __init__.py              # (exists)
│   │   ├── auth.py                  # NEW: signup, login, logout, get_user
│   │   ├── chat.py                  # NEW: /ask, /selected-text
│   │   ├── personalize.py           # NEW: /chapter personalization
│   │   ├── translate.py             # NEW: /chapter translation
│   │   └── progress.py              # NEW: /progress, /mark
│   ├── services/
│   │   ├── __init__.py              # (exists)
│   │   ├── claude_service.py        # NEW: Claude API wrapper
│   │   ├── qdrant_service.py        # NEW: Vector search
│   │   ├── db_service.py            # NEW: Postgres queries
│   │   └── rate_limiter.py          # NEW: Rate limiting logic
│   ├── models/
│   │   ├── __init__.py              # (exists)
│   │   ├── user.py                  # NEW: User, UserCreate, UserLogin schemas
│   │   ├── chat.py                  # NEW: ChatRequest, ChatResponse schemas
│   │   ├── personalize.py           # NEW: PersonalizeRequest schemas
│   │   └── translate.py             # NEW: TranslateRequest schemas
│   └── utils/
│       ├── __init__.py              # NEW
│       ├── auth.py                  # NEW: JWT helpers, password hashing
│       └── config.py                # NEW: Load .env variables
└── scripts/
    └── init_db.sql                  # NEW: Database schema initialization

frontend/                             # (Already complete - no changes)
└── [Docusaurus project]
```

**Structure Decision**: Web application structure with backend-only changes. Frontend (Docusaurus) is complete and deployed. Backend follows existing /backend folder convention with app/routers, app/services, app/models structure. All new files extend existing structure without refactoring.

## Complexity Tracking

No constitution violations. All design decisions align with simplicity, cost constraints, and modular architecture principles.

---

## Phase 0: Research & Discovery

### 0.1 Database Schema Design

**Goal**: Define Postgres tables for users, chat history, progress, translations, and personalized content.

**Research Tasks**:
1. Review constitution database schema (constitution.md lines 170-231)
2. Verify Neon Postgres connection via DATABASE_URL
3. Design SQL schema matching constitution specifications

**Expected Tables**:
- `users` (id, email, password_hash, name, programming_level, hardware, created_at)
- `chat_history` (id, user_id, question, answer, sources JSONB, created_at)
- `user_progress` (id, user_id, chapter_id, completed, last_accessed)
- `translations_cache` (id, chapter_id, language, translated_content, created_at)
- `personalized_content_cache` (id, chapter_id, user_level, personalized_content, created_at)

**Deliverable**: `scripts/init_db.sql` with CREATE TABLE statements and indexes

### 0.2 Qdrant Collection Investigation

**Goal**: Understand Qdrant collection structure and retrieval parameters.

**Research Tasks**:
1. Verify Qdrant Cloud connection via QDRANT_URL and QDRANT_API_KEY
2. Check if `textbook_chunks` collection exists; if not, plan creation
3. Determine vector dimensions (depends on embedding model)
4. Test retrieval with sample queries (top-k=5, similarity threshold=0.7)

**Embedding Strategy Decision**:
- **Option A**: Use sentence-transformers/all-MiniLM-L6-v2 locally (384 dims, free)
- **Option B**: Use Claude API for embeddings (cost implications)
- **Recommendation**: Option A for MVP (no API cost for embeddings)

**Deliverable**: Qdrant collection setup documentation in `research.md`

### 0.3 Claude API Integration Patterns

**Goal**: Design Claude API service wrapper for RAG, personalization, and translation.

**Research Tasks**:
1. Review anthropic SDK usage (already in requirements.txt: anthropic==0.39.0)
2. Design prompts for:
   - RAG Q&A: "Answer based only on this context: {chunks}. Question: {question}. Cite sources."
   - Personalization: "Adapt this chapter for {level} learner. Add {guidelines}."
   - Translation: "Translate this to educational Urdu (not literal): {chapter}"
3. Token counting strategy (to enforce budgets)
4. Error handling and retry logic (exponential backoff, max 3 retries)

**Deliverable**: Claude service design in `research.md`

### 0.4 Better-auth Integration Research

**Goal**: Determine how to integrate Better-auth with FastAPI.

**Research Tasks**:
1. Check if Better-auth has Python SDK (likely Node.js only)
2. **Decision**: Better-auth is Node.js-focused; for FastAPI, use native JWT approach:
   - python-jose for JWT creation/validation (already in requirements.txt)
   - passlib for bcrypt password hashing (already in requirements.txt)
3. Design auth flow: signup → hash password → store in Postgres → return JWT; login → verify password → return JWT

**Deliverable**: Auth design in `research.md` (note: not using Better-auth library, using JWT directly)

### 0.5 Rate Limiting Strategy

**Goal**: Design in-memory or Redis-based rate limiter for API endpoints.

**Research Tasks**:
1. Evaluate rate limiting approaches:
   - **Option A**: In-memory dict (simple, loses state on restart)
   - **Option B**: Redis (persistent, requires extra service)
   - **Recommendation**: Option A for MVP (acceptable to reset limits on restart)
2. Design middleware to check limits before processing requests
3. Track: questions/hour per user, translations/day per user, personalizations/day per user

**Deliverable**: Rate limiter design in `research.md`

---

## Phase 1: Detailed Design

### 1.1 Data Model

**File**: `specs/001-rag-chatbot-system/data-model.md`

**Database Schema** (SQL):

```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  programming_level VARCHAR(50) DEFAULT 'beginner', -- beginner/intermediate/advanced
  hardware VARCHAR(100) DEFAULT 'none', -- none/gpu/jetson/robotics
  created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);

-- Chat history
CREATE TABLE chat_history (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  sources JSONB, -- [{chapter_id, section, similarity_score}]
  created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_chat_history_user_id ON chat_history(user_id);

-- User progress
CREATE TABLE user_progress (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  chapter_id VARCHAR(100) NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  last_accessed TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, chapter_id)
);
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);

-- Translations cache
CREATE TABLE translations_cache (
  id SERIAL PRIMARY KEY,
  chapter_id VARCHAR(100) NOT NULL,
  language VARCHAR(10) DEFAULT 'ur',
  translated_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(chapter_id, language)
);
CREATE INDEX idx_translations_cache_chapter ON translations_cache(chapter_id, language);

-- Personalized content cache
CREATE TABLE personalized_content_cache (
  id SERIAL PRIMARY KEY,
  chapter_id VARCHAR(100) NOT NULL,
  user_level VARCHAR(50) NOT NULL,
  personalized_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(chapter_id, user_level)
);
CREATE INDEX idx_personalized_cache ON personalized_content_cache(chapter_id, user_level);
```

**Pydantic Models** (Python):

```python
# app/models/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    programming_level: str = "beginner"  # beginner/intermediate/advanced
    hardware: str = "none"  # none/gpu/jetson/robotics

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: str
    name: str
    programming_level: str
    hardware: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# app/models/chat.py
class ChatRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None  # For selected text mode

class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]  # [{chapter_id, section, similarity}]
    response_time: float

# app/models/personalize.py
class PersonalizeRequest(BaseModel):
    chapter_id: str

class PersonalizeResponse(BaseModel):
    chapter_id: str
    personalized_content: str
    cached: bool  # True if loaded from cache

# app/models/translate.py
class TranslateRequest(BaseModel):
    chapter_id: str

class TranslateResponse(BaseModel):
    chapter_id: str
    translated_content: str
    cached: bool
```

### 1.2 API Contracts

**File**: `specs/001-rag-chatbot-system/contracts/api-endpoints.md`

**Authentication** (`/api/auth/*`):
- `POST /api/auth/signup`: Create new user
  - Request: `{email, password, name, programming_level, hardware}`
  - Response: `{access_token, token_type}` (201)
  - Errors: 400 (email exists), 422 (validation error)

- `POST /api/auth/login`: Authenticate user
  - Request: `{email, password}`
  - Response: `{access_token, token_type}` (200)
  - Errors: 401 (invalid credentials)

- `GET /api/auth/me`: Get current user (requires JWT)
  - Headers: `Authorization: Bearer <token>`
  - Response: `{id, email, name, programming_level, hardware}` (200)
  - Errors: 401 (invalid/missing token)

**RAG Chatbot** (`/api/chat/*`):
- `POST /api/chat/ask`: Ask question (requires JWT for history saving)
  - Headers: `Authorization: Bearer <token>` (optional)
  - Request: `{question, selected_text?}`
  - Response: `{answer, sources, response_time}` (200)
  - Errors: 429 (rate limit exceeded), 500 (Qdrant/Claude failure)

**Personalization** (`/api/personalize/*`):
- `POST /api/personalize/chapter`: Personalize chapter (requires JWT)
  - Headers: `Authorization: Bearer <token>`
  - Request: `{chapter_id}`
  - Response: `{chapter_id, personalized_content, cached}` (200)
  - Errors: 401 (no token), 429 (rate limit: 5/day), 400 (invalid chapter)

**Translation** (`/api/translate/*`):
- `POST /api/translate/chapter`: Translate to Urdu (requires JWT)
  - Headers: `Authorization: Bearer <token>`
  - Request: `{chapter_id}`
  - Response: `{chapter_id, translated_content, cached}` (200)
  - Errors: 401 (no token), 429 (rate limit: 5/day), 400 (invalid chapter)

**Progress** (`/api/user/*`):
- `GET /api/user/progress`: Get user progress (requires JWT)
  - Headers: `Authorization: Bearer <token>`
  - Response: `{chapters_read: [{chapter_id, completed, last_accessed}], questions_asked: int}` (200)
  - Errors: 401 (no token)

- `POST /api/user/progress/mark`: Mark chapter complete (requires JWT)
  - Headers: `Authorization: Bearer <token>`
  - Request: `{chapter_id, completed}`
  - Response: `{success: true}` (200)
  - Errors: 401 (no token), 400 (invalid chapter)

### 1.3 Service Layer Design

**File**: `specs/001-rag-chatbot-system/contracts/services.md`

**ClaudeService** (`app/services/claude_service.py`):
```python
class ClaudeService:
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    async def generate_rag_answer(self, chunks: list[str], question: str) -> dict:
        # Prompt: "Answer based only on context. Cite sources."
        # Returns: {answer: str, tokens_used: int}

    async def personalize_chapter(self, chapter_content: str, level: str) -> dict:
        # Prompt: "Adapt for {level}. Add definitions/tips/research links."
        # Returns: {personalized_content: str, tokens_used: int}

    async def translate_chapter(self, chapter_content: str, language: str = "ur") -> dict:
        # Prompt: "Translate to educational Urdu."
        # Returns: {translated_content: str, tokens_used: int}
```

**QdrantService** (`app/services/qdrant_service.py`):
```python
class QdrantService:
    def __init__(self, url: str, api_key: str, collection_name: str):
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection = collection_name

    async def search_chunks(self, query_text: str, top_k: int = 5, threshold: float = 0.7) -> list[dict]:
        # Embed query → search Qdrant → filter by threshold
        # Returns: [{chunk_text, chapter_id, section, similarity_score}]
```

**DBService** (`app/services/db_service.py`):
```python
class DBService:
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)

    # User methods
    async def create_user(self, email, password_hash, name, level, hardware) -> int:
        # INSERT INTO users ... RETURNING id

    async def get_user_by_email(self, email) -> dict | None:
        # SELECT * FROM users WHERE email = %s

    async def get_user_by_id(self, user_id) -> dict | None:
        # SELECT * FROM users WHERE id = %s

    # Chat history methods
    async def save_chat(self, user_id, question, answer, sources) -> None:
        # INSERT INTO chat_history ...

    # Progress methods
    async def get_user_progress(self, user_id) -> list[dict]:
        # SELECT * FROM user_progress WHERE user_id = %s

    async def mark_chapter_complete(self, user_id, chapter_id, completed) -> None:
        # INSERT ... ON CONFLICT UPDATE

    # Cache methods
    async def get_translation(self, chapter_id, language) -> str | None:
        # SELECT translated_content FROM translations_cache WHERE ...

    async def save_translation(self, chapter_id, language, content) -> None:
        # INSERT INTO translations_cache ...

    async def get_personalized_content(self, chapter_id, level) -> str | None:
        # SELECT personalized_content FROM personalized_content_cache WHERE ...

    async def save_personalized_content(self, chapter_id, level, content) -> None:
        # INSERT INTO personalized_content_cache ...
```

**RateLimiter** (`app/services/rate_limiter.py`):
```python
class RateLimiter:
    def __init__(self):
        self.questions_per_hour = {}  # {user_id: [(timestamp, count)]}
        self.translations_per_day = {}
        self.personalizations_per_day = {}

    def check_questions_limit(self, user_id: int, limit: int = 20) -> bool:
        # Check if user exceeded 20 questions in last hour

    def check_translations_limit(self, user_id: int, limit: int = 5) -> bool:
        # Check if user exceeded 5 translations today

    def check_personalizations_limit(self, user_id: int, limit: int = 5) -> bool:
        # Check if user exceeded 5 personalizations today
```

### 1.4 Authentication & Authorization Flow

**File**: `specs/001-rag-chatbot-system/contracts/auth-flow.md`

**Password Hashing**:
- Use `passlib.context.CryptContext` with bcrypt (salt rounds ≥10)
- Hash password before storing: `pwd_context.hash(password)`
- Verify on login: `pwd_context.verify(password, hash)`

**JWT Creation**:
- Use `python-jose` to create/verify tokens
- Payload: `{sub: user_id, exp: expiration_timestamp}`
- Algorithm: HS256
- Expiration: 7 days (ACCESS_TOKEN_EXPIRE_MINUTES=10080 in .env)

**Authorization Middleware**:
- Create dependency function `get_current_user(token: str = Depends(oauth2_scheme))`
- Extract token from `Authorization: Bearer <token>` header
- Decode and verify JWT
- Return user data or raise 401 error

---

## Phase 2: Implementation Sequence

**Note**: Detailed tasks will be generated by `/sp.tasks` command. This section provides high-level implementation order.

### Milestone 1: Database & Core Services (Foundation)

**Tasks**:
1. Create `scripts/init_db.sql` with all table schemas
2. Run schema initialization on Neon Postgres
3. Create `app/utils/config.py` to load .env variables
4. Implement `app/services/db_service.py` with all database methods
5. Test database connection and CRUD operations

**Acceptance Criteria**:
- All tables exist in Neon Postgres
- DBService can create user, save chat, fetch progress
- Environment variables loaded correctly

### Milestone 2: Authentication System

**Tasks**:
1. Create `app/utils/auth.py` with password hashing and JWT helpers
2. Create `app/models/user.py` with Pydantic schemas
3. Implement `app/routers/auth.py` with signup, login, get_user endpoints
4. Update `main.py` to include auth router
5. Test signup/login flow with curl or Postman

**Acceptance Criteria**:
- User can sign up and receive JWT token
- User can log in and receive JWT token
- Protected endpoint `/api/auth/me` returns user data with valid token
- Invalid token returns 401 error

### Milestone 3: RAG Chatbot (Core Feature - P1)

**Tasks**:
1. Implement `app/services/qdrant_service.py` for vector search
2. Implement `app/services/claude_service.py` with `generate_rag_answer` method
3. Create `app/models/chat.py` with request/response schemas
4. Implement `app/routers/chat.py` with `/ask` endpoint
5. Integrate rate limiter (20 questions/hour)
6. Update `main.py` to include chat router
7. Test RAG pipeline: question → Qdrant retrieval → Claude answer → citation

**Acceptance Criteria**:
- User can ask question and receive answer with source citations
- Answer is based only on retrieved chunks (no hallucinations)
- Response time <3 seconds for 95% of queries
- Rate limiter blocks users exceeding 20 questions/hour
- Chat history saved for authenticated users

### Milestone 4: Personalization System (P3)

**Tasks**:
1. Implement `app/services/claude_service.py` with `personalize_chapter` method
2. Create `app/models/personalize.py` with schemas
3. Implement `app/routers/personalize.py` with `/chapter` endpoint
4. Add caching logic: check DB first, call Claude if not cached, save result
5. Integrate rate limiter (5 personalizations/day)
6. Update `main.py` to include personalize router
7. Test personalization for beginner/intermediate/advanced levels

**Acceptance Criteria**:
- User can personalize chapter and receive adapted content
- Content differs by programming level (beginner gets definitions, advanced gets research links)
- Personalized content cached in Postgres (no re-personalization)
- Rate limiter blocks users exceeding 5 personalizations/day
- Token usage ≤4000 tokens per chapter

### Milestone 5: Translation System (P3)

**Tasks**:
1. Implement `app/services/claude_service.py` with `translate_chapter` method
2. Create `app/models/translate.py` with schemas
3. Implement `app/routers/translate.py` with `/chapter` endpoint
4. Add caching logic: check DB first, call Claude if not cached, save result
5. Integrate rate limiter (5 translations/day)
6. Update `main.py` to include translate router
7. Test Urdu translation quality

**Acceptance Criteria**:
- User can translate chapter to Urdu
- Translation is educational (not literal word-for-word)
- Translations cached in Postgres
- Rate limiter blocks users exceeding 5 translations/day
- Token usage ≤3000 tokens per chapter

### Milestone 6: Progress Tracking (P2)

**Tasks**:
1. Create `app/models/progress.py` (if needed)
2. Implement `app/routers/progress.py` with `/progress` and `/mark` endpoints
3. Update chat router to auto-track questions asked
4. Update `main.py` to include progress router
5. Test progress retrieval and chapter marking

**Acceptance Criteria**:
- User can view progress (chapters read, questions asked)
- User can mark chapter as completed
- Progress persists across sessions

### Milestone 7: Rate Limiting & Cost Monitoring

**Tasks**:
1. Implement `app/services/rate_limiter.py` with in-memory limits
2. Add rate limit checks to chat, personalize, translate routers
3. Add token usage logging to Claude service
4. Create simple cost tracking (log tokens used per day)

**Acceptance Criteria**:
- Rate limits enforced across all endpoints
- Token usage logged for monitoring
- Daily cost estimate ≤$10 for 100 users

### Milestone 8: Error Handling & Production Readiness

**Tasks**:
1. Add exponential backoff retry logic to Claude service (3 retries)
2. Add graceful error handling to Qdrant service (fallback messages)
3. Add structured logging (JSON format) to all services
4. Create health check endpoint improvements
5. Document deployment steps for Railway

**Acceptance Criteria**:
- Claude API failures retry up to 3 times before returning error
- Qdrant failures show user-friendly message
- All errors logged with structured format
- Backend deploys to Railway successfully

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Qdrant collection doesn't exist yet | HIGH - RAG won't work | Create collection initialization script; test connection early in Milestone 3 |
| Better-auth incompatible with FastAPI | MEDIUM | Use native JWT approach with python-jose (already decided) |
| Token costs exceed $10/day budget | HIGH - Cost overrun | Implement strict rate limiting; monitor token usage daily; use caching aggressively |
| Claude API slow (>3s response time) | MEDIUM - UX degradation | Optimize chunk retrieval (reduce to 4 chunks if needed); consider switching to Haiku for personalization/translation |
| Neon Postgres free tier storage exceeded | LOW - Unlikely for MVP | Monitor database size; implement data retention policy if needed |

---

## Success Criteria Mapping

| Spec Success Criteria | Implementation Milestone | Verification Method |
|-----------------------|--------------------------|---------------------|
| SC-001: Responses <3s for 95% of questions | Milestone 3 | Log response times; calculate p95 |
| SC-002: 100% accurate grounding (no hallucinations) | Milestone 3 | Manual testing with out-of-scope questions |
| SC-003: Signup/login within 2 minutes | Milestone 2 | Manual test signup flow |
| SC-004: Personalized content differs by level | Milestone 4 | Spot-check 3 chapters across levels |
| SC-005: Cached translations load <500ms | Milestone 5 | Test cached vs. uncached translation times |
| SC-006: Token budget <$10/day | Milestone 7 | Monitor token logs for 24 hours |
| SC-007: Rate limiting enforced | Milestone 7 | Test exceeding limits (expect 429 errors) |
| SC-008: Mobile responsive (frontend) | N/A | Frontend already complete |
| SC-009: Zero exposed API keys | Milestone 8 | Code review; verify .env not in git |
| SC-010: Graceful error handling | Milestone 8 | Test Qdrant/Claude failures |

---

## Next Steps

1. **Review this plan** with user for approval
2. **Run `/sp.tasks`** to generate detailed, dependency-ordered task list
3. **Start implementation** with Milestone 1 (Database & Core Services)
4. **Test incrementally** after each milestone
5. **Deploy to Railway** after Milestone 8

**Estimated Implementation Time**: 5-6 days (per constitution timeline)
- Day 1: Milestones 1-2 (Database + Auth)
- Day 2: Milestone 3 (RAG chatbot)
- Day 3: Milestones 4-5 (Personalization + Translation)
- Day 4: Milestones 6-7 (Progress + Rate limiting)
- Day 5: Milestone 8 (Error handling + Deployment)
- Day 6: Testing + Bug fixes

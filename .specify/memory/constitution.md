<!--
Sync Impact Report:
Version: 1.0.0 → 1.1.0 (MINOR bump)
Modified Principles:
  - I. AI-Native First → Expanded to include RAG-only constraint and personalization
  - II. Performance & Speed → Updated with specific token limits and response times
  - Technical Architecture → Major updates: Claude API replacing OpenAI, FastAPI confirmed, Railway deployment, Better-auth
Added Sections:
  - IX. Personalized Learning (new principle)
  - X. Multilingual Support - Urdu Translation (new principle)
  - XI. Progress Tracking & Analytics (new principle)
  - Project Structure (frontend/backend separation)
  - Token Budget & Cost Management
  - Rate Limiting & User Quotas
Removed Sections: None
Templates Requiring Updates:
  ✅ plan-template.md - needs alignment with Claude API, personalization, translation features
  ✅ spec-template.md - needs alignment with user level tracking, translation requirements
  ✅ tasks-template.md - needs alignment with backend/frontend folder structure
Follow-up TODOs:
  - Update all command files to reference Claude API instead of OpenAI
  - Create migration guide for switching from OpenAI to Claude API
  - Document folder structure convention (frontend/ vs backend/)
-->

# Physical AI Textbook Constitution

## Project Overview

**Project Name**: Physical AI & Humanoid Robotics Interactive Textbook
**Mission**: Build an AI-native Docusaurus textbook with embedded RAG chatbot that provides personalized, grounded learning experiences with Urdu translation support.

**Core Value Proposition**:
- Answers questions ONLY from the book (no hallucinations)
- Works for selected text OR entire book
- Personalizes content based on user programming level
- Translates to Urdu
- Tracks user progress

## Core Principles

### I. AI-Native First - RAG-Only Responses
Every feature MUST leverage Claude API as the primary AI provider for all intelligence tasks. The chatbot MUST answer questions ONLY using retrieved context from the textbook. No hallucinations, no external knowledge.

**Implementation Rules**:
- Use Claude API (Anthropic) exclusively - NOT OpenAI
- RAG pipeline: retrieve chunks → send to Claude with context → return grounded answer
- If answer not in retrieved context, respond: "I don't have this information in the book."
- All responses must cite source chunks (chapter + section)

**Rationale**: Educational accuracy is non-negotiable. RAG ensures responses are verifiable and grounded in textbook content. Claude API provides consistent, high-quality responses with strong instruction-following.

### II. Performance & Speed (NON-NEGOTIABLE)
System MUST be fast and responsive on low-end devices. Target: <200ms page loads, <3s total chatbot response time (including Claude API latency).

**Token Budget Constraints**:
- Personalization: Max 4000 tokens per chapter
- Translation: Max 3000 tokens per chapter
- RAG context window: 4-5 chunks (~2000 tokens) + question
- Total daily budget: <$10 for 100 active users

**Rationale**: Users on phones and low-bandwidth connections must have seamless experiences. Token limits prevent cost overruns while maintaining quality.

### III. Simplicity & Minimalism
Keep the architecture clean and minimal. Avoid heavy dependencies, complex frameworks, and over-engineering. Every component must justify its existence.

**Rationale**: Complexity leads to maintenance burden, deployment issues, and performance degradation. Simple systems are easier to debug, scale, and understand.

### IV. Modular Architecture - Frontend/Backend Separation
Separate concerns cleanly: Docusaurus frontend (separate folder), FastAPI backend (separate folder), Neon Postgres, Qdrant Cloud. Each module MUST be independently testable and deployable.

**Folder Structure** (REQUIRED):
```
/BOOK (root)
  /frontend          # Docusaurus project
    /docs            # Textbook content
    /src             # React components, chat widget
    docusaurus.config.js
  /backend           # FastAPI project
    /app
      /routers       # API endpoints
      /services      # Claude API, Qdrant, DB logic
      /models        # Pydantic schemas
    main.py
    requirements.txt
```

**Rationale**: Clean separation enables parallel development, easier debugging, and independent deployment. Frontend and backend teams can work without conflicts.

### V. Free-Tier & Cost Constraints
All infrastructure MUST run on free tiers or stay within budget:
- **Qdrant Cloud**: Free tier (1GB storage)
- **Neon Postgres**: Free tier (512MB storage)
- **Railway**: Free tier or $5/month budget
- **Claude API**: Monitor usage, stay under $10/day

**Rationale**: Project must be demonstrable and maintainable without ongoing costs. Free tiers provide sufficient capacity for MVP and demo purposes.

### VI. Rapid Deployment
Frontend MUST deploy in <60 seconds (Vercel/Netlify). Backend MUST deploy in <90 seconds (Railway). Requires automated CI/CD and minimal build times.

**Rationale**: Fast deployment enables rapid iteration, demo recording, and quick recovery from failures.

### VII. Grounded & Accurate Responses
RAG chatbot MUST only answer questions based on textbook content. Implement citation tracking and confidence scoring. If context insufficient, say "I don't have this information in the book."

**Rationale**: Educational content requires accuracy and trust. Hallucinated answers undermine learning objectives and user confidence.

### VIII. Mobile-First Design
UI MUST be responsive and optimized for mobile devices. Touch-friendly chat widget, readable fonts, minimal scrolling, fast rendering.

**Rationale**: Learners frequently access content on phones. Desktop-only designs alienate the majority of users.

### IX. Personalized Learning
System MUST adapt content based on user's programming level (beginner/intermediate/advanced) and hardware context (none/GPU/Jetson/robotics).

**Personalization Rules**:
- **Beginner**: Add definitions, simple examples, step-by-step explanations
- **Intermediate**: Practical tips, common mistakes, optimization notes
- **Advanced**: Research links, advanced techniques, performance optimizations
- Cache personalized chapters in Postgres to avoid re-personalization

**Rationale**: One-size-fits-all content fails diverse learners. Personalization improves comprehension and engagement.

### X. Multilingual Support - Urdu Translation
System MUST support Urdu translation for all chapters using Claude API.

**Translation Rules**:
- Translate to clear, educational Urdu (not literal word-for-word)
- Cache translations in Postgres (avoid re-translating same chapter)
- Max 3000 tokens per chapter
- Rate limit: 5 chapters/day per user

**Rationale**: Urdu support democratizes access for non-English speakers. Caching prevents redundant API calls and reduces costs.

### XI. Progress Tracking & Analytics
System MUST track user progress: chapters read, questions asked, quizzes completed.

**Tracking Requirements**:
- Store in Postgres: `user_progress` table
- Privacy-first: no PII beyond email/name
- Expose progress via `/api/user/progress` endpoint

**Rationale**: Progress tracking motivates learners and provides insights for content improvement.

## Technical Architecture

### Technology Stack (FIXED)

**Backend**:
- **Framework**: FastAPI (Python 3.11+)
- **Database**: Neon Serverless PostgreSQL (free tier)
- **Vector DB**: Qdrant Cloud (free tier)
- **AI Model**: Claude API (Anthropic) - claude-3-5-sonnet-20241022
- **Auth**: Better-auth
- **Deployment**: Railway

**Frontend**:
- **Framework**: Docusaurus 3.x (already implemented)
- **Auth UI**: Better-auth components
- **Chat Widget**: Custom React component (embedded in Docusaurus)
- **Deployment**: Vercel or Netlify

**Why This Stack**:
- All components integrate cleanly
- Claude Code Router understands FastAPI naturally
- Single AI provider (Claude) = simple, consistent
- Free tiers available for MVP testing

### Database Schema (Neon Postgres)

**users**:
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  programming_level VARCHAR(50) DEFAULT 'beginner', -- beginner/intermediate/advanced
  hardware VARCHAR(100) DEFAULT 'none', -- none/gpu/jetson/robotics
  created_at TIMESTAMP DEFAULT NOW()
);
```

**chat_history**:
```sql
CREATE TABLE chat_history (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  sources JSONB, -- array of chunk IDs/citations
  created_at TIMESTAMP DEFAULT NOW()
);
```

**user_progress**:
```sql
CREATE TABLE user_progress (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  chapter_id VARCHAR(100) NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  last_accessed TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, chapter_id)
);
```

**translations_cache**:
```sql
CREATE TABLE translations_cache (
  id SERIAL PRIMARY KEY,
  chapter_id VARCHAR(100) NOT NULL,
  language VARCHAR(10) DEFAULT 'ur', -- Urdu
  translated_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(chapter_id, language)
);
```

**personalized_content_cache**:
```sql
CREATE TABLE personalized_content_cache (
  id SERIAL PRIMARY KEY,
  chapter_id VARCHAR(100) NOT NULL,
  user_level VARCHAR(50) NOT NULL,
  personalized_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(chapter_id, user_level)
);
```

### Backend API Endpoints

**Authentication**:
- `POST /api/auth/signup` - Create new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

**RAG Chatbot**:
- `POST /api/chat/ask` - Ask question (sends question + user context)
- `POST /api/chat/selected-text` - Ask about selected text

**Personalization**:
- `POST /api/personalize/chapter` - Get personalized chapter content
- `PUT /api/user/settings` - Update user level/hardware

**Translation**:
- `POST /api/translate/chapter` - Translate chapter to Urdu

**Progress Tracking**:
- `GET /api/user/progress` - Get user's progress
- `POST /api/user/progress/mark` - Mark chapter as completed

**Health**:
- `GET /api/health` - Health check

### Data Management

**Qdrant Vector Store**:
- **Collection**: `textbook_chunks`
- **Chunking Strategy**: 500-1000 tokens per chunk, 50-token overlap
- **Embedding Model**: claude-3-5-sonnet (via Claude API) or sentence-transformers/all-MiniLM-L6-v2
- **Retrieval**: Top-K=4-5 chunks, cosine similarity threshold >0.7
- **Metadata**: chapter_id, section_title, page_number

**Caching Strategy**:
- Cache embeddings in Qdrant (no re-embedding on query)
- Cache translations in Postgres (avoid duplicate API calls)
- Cache personalized content per user level (not per user to reduce storage)

### Token Budget & Cost Management

**Per-Request Limits**:
- RAG query: ~2000 tokens context + 200 tokens question = 2200 input tokens
- Personalization: Max 4000 tokens per chapter
- Translation: Max 3000 tokens per chapter
- Expected output: ~500-1500 tokens per response

**Daily Budget** (100 active users):
- 100 users × 5 questions/day × 2500 tokens/query = 1.25M tokens/day
- Cost estimate: ~$3-$5/day (Claude API pricing: $3/M input, $15/M output for Sonnet)
- Buffer for personalization/translation: $5/day
- **Total**: <$10/day ✅

### Rate Limiting & User Quotas

**Free Users**:
- 20 questions/hour
- 5 chapter translations/day
- 5 chapter personalizations/day

**Implementation**:
- Use Redis or in-memory counter (for MVP)
- Return `429 Too Many Requests` when limit exceeded

### Error Handling

**Qdrant Fails**:
- Return: "Sorry, search is temporarily unavailable. Please try again."
- Log error to backend

**Claude API Fails**:
- Return: "AI service is busy. Please retry in a moment."
- Implement exponential backoff (3 retries)

**Database Fails**:
- Log error
- Return generic error: "Something went wrong. Please contact support."
- Never expose internal details

### Performance Standards

- **Page Load**: <2 seconds on 3G connection
- **Chatbot Response**: <3 seconds total (including Claude API latency)
- **Build Time**: <60 seconds for Docusaurus frontend
- **Backend Startup**: <10 seconds for FastAPI

### Security & Privacy

- **No PII Storage**: Minimal user data (email, name, level, hardware only)
- **API Keys**: Environment variables only; never commit to version control
- **CORS**: Restrict API access to frontend domain only
- **Auth Tokens**: JWT with 7-day expiration
- **Password Hashing**: bcrypt with salt rounds ≥10

## Development Workflow

### Feature Development Order
1. Database schema (Neon Postgres)
2. Claude API service wrapper
3. Qdrant setup and indexing
4. FastAPI routers (one at a time)
5. Frontend chat widget integration
6. Deployment config (Railway + Vercel)

### Build Pipeline
1. **Specification**: Document feature in `specs/<feature>/spec.md`
2. **Planning**: Architecture in `specs/<feature>/plan.md`
3. **Tasking**: Testable tasks in `specs/<feature>/tasks.md`
4. **Implementation**: Code changes with task ID references
5. **Testing**: Test after each module completion
6. **Deployment**: PR → main → auto-deploy

### Code Quality

- **Linting**: ESLint (frontend), Ruff (backend)
- **Formatting**: Prettier (frontend), Black (backend)
- **Type Safety**: TypeScript (frontend), Python type hints (backend)
- **Documentation**: Inline comments for complex logic; README for setup

### Testing Strategy

- **Unit Tests**: Optional for utility functions
- **Integration Tests**: Required for RAG pipeline (Qdrant → Claude API → response)
- **Manual Tests**: Required for chat widget, translation, personalization
- **Health Checks**: `/api/health` endpoint MUST return 200 OK

### Observability

- **Logging**: Structured logs (JSON format) for all API calls
- **Monitoring**: Railway dashboard for backend uptime
- **Error Tracking**: Log all Claude API errors, Qdrant failures
- **Analytics**: Track chapter views, questions asked, translations used

## Success Criteria (Definition of Done)

✅ **Must Work**:
1. User can signup and login
2. Chat answers questions accurately from book content only
3. Selected text mode works
4. Personalization adapts content based on user level
5. Urdu translation works and caches correctly
6. Backend deployed on Railway
7. Token usage <$10/day for 100 active users

✅ **Must Be Fast**:
- Chat response <3 seconds
- Page load <2 seconds
- Deployment <90 seconds

✅ **Must Be Secure**:
- No exposed API keys
- Password hashing
- CORS restrictions
- Rate limiting enforced

## Out of Scope (NOT Included)

❌ Advanced analytics dashboard
❌ Multiple language translations (only Urdu supported)
❌ Voice input
❌ Image generation
❌ Collaborative features
❌ Mobile app (web only)
❌ Payment integration
❌ Admin panel (use SQL directly for MVP)

## Timeline Estimate

- **Day 1**: Database schema + Qdrant setup
- **Day 2**: RAG implementation (Qdrant + Claude API)
- **Day 3**: Auth + personalization
- **Day 4**: Translation + caching
- **Day 5**: Deployment + testing
- **Day 6**: Bug fixes + documentation

## Governance

### Critical Reminders

🔴 **ALWAYS**:
- Use Claude API, NOT OpenAI
- Cache expensive operations (translations, personalizations)
- Validate user input (sanitize queries, prevent injection)
- Log all API calls for debugging
- Use environment variables for secrets

🔴 **NEVER**:
- Expose API keys in code
- Allow unlimited API calls
- Generate answers without retrieved context
- Store passwords in plain text
- Deploy without error handling

### Amendment Process

1. Constitution changes require documentation in a Prompt History Record (PHR)
2. Significant architectural decisions MUST be captured in ADRs (`history/adr/`)
3. All PRs MUST reference relevant specs, tasks, or ADRs
4. Breaking changes require migration plan and rollback strategy

### Compliance & Reviews

- Every PR MUST verify compliance with core principles (I-XI)
- Reject PRs that:
  - Add unnecessary complexity or heavy dependencies
  - Violate cost/token constraints
  - Use OpenAI instead of Claude API
  - Mix frontend/backend code in same folder
- Code reviews MUST check for performance, security, and mobile responsiveness

### Constitution Authority

- This constitution supersedes all other practices and preferences
- When in doubt, prioritize simplicity, speed, and user value
- Use CLAUDE.md for runtime development guidance and workflow execution

**Version**: 1.1.0 | **Ratified**: 2025-12-17 | **Last Amended**: 2025-12-19

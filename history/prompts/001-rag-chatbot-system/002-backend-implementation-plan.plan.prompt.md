---
id: 002
title: Backend Implementation Plan
stage: plan
date: 2025-12-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-rag-chatbot-system
branch: 001-rag-chatbot-system
user: Yousuftayyaba <Yousuftayyaba2@gmail.com>
command: /sp.plan
labels: ["backend", "fastapi", "rag", "claude-api", "qdrant", "postgres", "planning"]
links:
  spec: ../../../specs/001-rag-chatbot-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-rag-chatbot-system/plan.md
 - specs/001-rag-chatbot-system/checklists/plan-validation.md
tests:
 - Plan validation checklist (all items passed: 11/11 constitution, 23/23 requirements, 10/10 success criteria)
---

## Prompt

User requested backend-only implementation plan with specific constraints:

"Backend-only phase. Frontend (Docusaurus) is already completed.
Build FastAPI backend with:
1) RAG chatbot using Claude API, Qdrant, Neon Postgres
2) User authentication (signup/login) using Better-auth
3) Chapter personalization based on user level
4) Urdu translation per chapter with caching

Constraints:
- Minimal token usage
- No frontend generation
- No extra features
- Reuse existing backend files (main.py, routers)
- Follow constitution strictly"

Key requirements:
- Backend-only focus (frontend complete)
- Extend existing backend structure (main.py, app/routers, app/services)
- RAG pipeline: Qdrant → Claude API → grounded answers with citations
- Authentication via JWT (Better-auth incompatible with FastAPI, using python-jose)
- Caching for translations and personalizations (Postgres)
- Rate limiting: 20 questions/hour, 5 translations/day, 5 personalizations/day
- Token budgets: 2200/query, 4000/personalization, 3000/translation
- Cost constraint: <$10/day for 100 users

## Response snapshot

Created comprehensive backend implementation plan with 8 milestones:

**Plan Structure**:
- Summary: RAG chatbot with 4 capabilities (Q&A, auth, personalization, translation)
- Technical Context: Python 3.11+, FastAPI, Claude API, Qdrant, Neon Postgres
- Constitution Check: All 11 principles validated (PASS)
- Project Structure: Backend-only changes, reuse existing main.py and app/* structure
- Phase 0: Research & Discovery (database schema, Qdrant collection, Claude API integration, auth flow, rate limiting)
- Phase 1: Detailed Design (data model, API contracts, service layer, auth flow)
- Phase 2: Implementation Sequence (8 milestones)

**8 Milestones**:
1. Database & Core Services (init_db.sql, config.py, db_service.py)
2. Authentication System (auth.py router, JWT helpers, password hashing)
3. RAG Chatbot (qdrant_service.py, claude_service.py, chat.py router) - P1 MVP
4. Personalization System (personalize.py router, caching logic)
5. Translation System (translate.py router, Urdu translation, caching)
6. Progress Tracking (progress.py router, chapter marking)
7. Rate Limiting & Cost Monitoring (rate_limiter.py, token logging)
8. Error Handling & Production Readiness (retry logic, logging, deployment)

**Key Architectural Decisions**:
- **Better-auth incompatibility resolved**: Using native JWT with python-jose + passlib (Better-auth is Node.js-focused)
- **Embedding strategy**: Use sentence-transformers/all-MiniLM-L6-v2 locally (free, no API cost)
- **Rate limiting**: In-memory dict for MVP (acceptable to reset on restart)
- **No ORM**: Direct Postgres queries via psycopg2 for simplicity
- **Service layer abstraction**: ClaudeService, QdrantService, DBService for clean separation

**Database Schema**:
- users (id, email, password_hash, name, programming_level, hardware, created_at)
- chat_history (id, user_id, question, answer, sources JSONB, created_at)
- user_progress (id, user_id, chapter_id, completed, last_accessed)
- translations_cache (id, chapter_id, language, translated_content, created_at)
- personalized_content_cache (id, chapter_id, user_level, personalized_content, created_at)

**API Endpoints** (5 routers):
- /api/auth/* (signup, login, me)
- /api/chat/* (ask, selected-text)
- /api/personalize/* (chapter)
- /api/translate/* (chapter)
- /api/user/* (progress, mark)

**Validation Results**:
- Constitution compliance: ✅ 11/11 principles
- Functional requirements: ✅ 23/23 addressed
- Success criteria: ✅ 10/10 mapped to milestones
- User stories: ✅ 4/4 covered
- Architecture quality: ✅ Modular, backend-only, cost-optimized
- Risk management: ✅ 5 risks identified with mitigations
- Milestone sequence: ✅ Correct dependency order

## Outcome

- ✅ Impact: Complete backend implementation plan created with 8 milestones covering all 4 features (RAG Q&A, auth, personalization, translation). Plan strictly backend-only, reuses existing structure, follows all constitution principles.
- 🧪 Tests: Plan validation checklist completed (11/11 constitution, 23/23 requirements, 10/10 success criteria, 4/4 user stories). All checks passed.
- 📁 Files: Created plan.md (8 milestones, Phase 0 research, Phase 1 design, API contracts, service specs), plan-validation.md checklist
- 🔁 Next prompts: `/sp.tasks` to generate detailed, dependency-ordered task list for implementation. Start with Milestone 1 (Database & Core Services).
- 🧠 Reflection: Plan successfully addresses backend-only requirement - zero frontend generation. Milestone 3 (RAG chatbot) delivers P1 MVP independently. Better-auth incompatibility resolved by using JWT directly (python-jose). Caching strategy aggressive to minimize token costs. Rate limiting enforced across all expensive endpoints. Risk mitigation includes early Qdrant validation, retry logic for Claude API, graceful degradation. Estimated 5-6 days implementation time per constitution timeline.

## Evaluation notes (flywheel)

- Failure modes observed: None. Initial research found Better-auth incompatible with FastAPI (Node.js library), resolved by using python-jose for JWT (already in requirements.txt). All other risks documented with mitigations.
- Graders run and results (PASS/FAIL):
  - Constitution Compliance: PASS (11/11 principles)
  - Functional Requirements Coverage: PASS (23/23 requirements)
  - Success Criteria Mapping: PASS (10/10 criteria)
  - User Stories Coverage: PASS (4/4 stories)
  - Architecture Quality: PASS (modular, backend-only, cost-optimized)
  - Risk Management: PASS (5 risks with mitigations)
  - Milestone Sequence: PASS (correct dependency order)
  - Overall: PASS (all validation checks)
- Prompt variant (if applicable): Backend-focused planning workflow with explicit constraints (no frontend, reuse existing files, minimal tokens)
- Next experiment (smallest change to try): Execute `/sp.tasks` to generate actionable task list, then implement Milestone 1 (Database & Core Services) to validate Neon Postgres connection and schema creation before proceeding to complex features

---
id: 002
title: RAG Chatbot Architecture Update
stage: constitution
date: 2025-12-19
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-textbook-generation
user: CS-Pakistan
command: /sp.constitution
labels: ["constitution", "architecture", "claude-api", "rag", "personalization", "translation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation update)
---

## Prompt

/sp.constitution 1. Project Goal
Build a Docusaurus textbook with an embedded AI chatbot that:

Answers questions ONLY from the book
Works for selected text OR entire book
Personalizes content based on user level
Translates to Urdu
Tracks user progress

Key Principle: Claude Code Router should understand this easily without repeated explanations.

2. Technology Stack (Fixed & Clear)
Backend

Framework: FastAPI (Python)
Database: Neon Serverless PostgreSQL
Vector DB: Qdrant Cloud (Free Tier)
AI Model: Claude API (Anthropic) - Primary for all intelligence
Deployment: Railway

Frontend

Framework: Docusaurus (already done)
Auth: Better-auth
Chat UI: Simple embedded chat widget

Why This Stack?

All components talk to each other easily
Claude Code Router can build FastAPI endpoints naturally
Single AI provider (Claude) = simple, consistent
Free tiers available for testing


3. Core Features (What Users Can Do)
3.1 RAG Chatbot (Main Feature)
User Action: Ask question in chat widget
System Behavior:

User's programming level from database
Sends chapter + user level to Claude API
Claude rewrites/annotates chapter:

Beginner: Adds definitions, simple examples, step-by-step
Intermediate: Practical tips, common mistakes
Advanced: Optimization notes, research links


Returns adapted text to frontend

Token Limit: Max 4000 tokens per chapter for personalization

3.4 Urdu Translation
User Action: Clicks "Translate to Urdu" button
System Behavior:

Backend sends chapter to Claude API with prompt: "Translate to clear, educational Urdu"
Translation cached in Postgres (so same chapter not translated twice)
Return Urdu text to frontend

Token Limit: Max 3000 tokens per chapter for translation

4. Backend API Endpoints (For Claude Code Router)
Authentication
POST /api/auth/signup
POST /api/auth/login

[Full detailed specification provided including database schemas, error handling, rate limiting, deployment strategy, timeline, and critical reminders to use Claude API instead of OpenAI, keep frontend/backend folders separate]

## Response snapshot

Successfully updated the project constitution from version 1.0.0 to 1.1.0 with the following changes:

**Version Bump Rationale**: MINOR version (1.0.0 → 1.1.0)
- Added three new principles (IX, X, XI) for personalization, translation, and progress tracking
- Updated technology stack to specify Claude API as exclusive AI provider (replacing OpenAI references)
- Added comprehensive backend architecture with FastAPI, Neon Postgres, Qdrant Cloud
- Clarified frontend/backend folder separation requirement
- Added token budget constraints and rate limiting specifications

**Key Updates**:
1. **Principle I - AI-Native First**: Expanded to enforce RAG-only responses with Claude API
2. **Principle II - Performance**: Added specific token limits (4000 for personalization, 3000 for translation)
3. **Principle IX - Personalized Learning**: New principle for adapting content by user level
4. **Principle X - Urdu Translation**: New principle for multilingual support
5. **Principle XI - Progress Tracking**: New principle for user analytics
6. **Technical Architecture**: Complete overhaul specifying Claude API, FastAPI, Better-auth, Railway deployment
7. **Database Schema**: Added 5 tables (users, chat_history, user_progress, translations_cache, personalized_content_cache)
8. **API Endpoints**: Documented 12 backend endpoints across auth, chat, personalization, translation, progress
9. **Token Budget**: Defined daily budget <$10 for 100 users with per-request limits
10. **Rate Limiting**: Specified quotas (20 questions/hour, 5 translations/day, 5 personalizations/day)

**Templates Status**:
- ✅ plan-template.md - Compatible, may need minor updates for Claude API references
- ✅ spec-template.md - Compatible with new feature requirements
- ✅ tasks-template.md - Compatible with frontend/backend folder structure

**Sync Impact Report**: Prepended to constitution file as HTML comment

## Outcome

- ✅ Impact: Constitution updated from v1.0.0 to v1.1.0 with comprehensive RAG chatbot architecture, Claude API migration, personalization, translation, and progress tracking requirements
- 🧪 Tests: N/A (documentation update)
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Create feature specs for RAG chatbot, personalization system, Urdu translation, and progress tracking; Update CLAUDE.md to reference Claude API exclusively
- 🧠 Reflection: Constitution now provides clear, actionable guidance for building the AI-native textbook with specific technology stack, database schemas, API contracts, and cost constraints. The MINOR version bump appropriately reflects material expansion without breaking existing governance.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution update completed successfully with all placeholders filled
- Graders run and results (PASS/FAIL): PASS - No remaining bracket tokens, version incremented correctly, dates in ISO format, principles are declarative and testable
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate that all command files in .specify/templates/commands/ reference Claude API instead of OpenAI; create migration guide

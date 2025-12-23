-- Physical AI Textbook Database Schema
-- This file initializes all database tables for the RAG chatbot system
-- Safe to run multiple times (uses IF NOT EXISTS)

-- ============================================================================
-- TABLE: users
-- Purpose: Store user accounts with authentication and personalization preferences
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  programming_level VARCHAR(50) DEFAULT 'beginner', -- beginner/intermediate/advanced
  hardware VARCHAR(100) DEFAULT 'none', -- none/gpu/jetson/robotics
  created_at TIMESTAMP DEFAULT NOW()
);

-- Index on email for fast lookup during login
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- ============================================================================
-- TABLE: chat_history
-- Purpose: Store all Q&A interactions between users and the RAG chatbot
-- Structure only - logic will be implemented in Day 2+
-- ============================================================================
CREATE TABLE IF NOT EXISTS chat_history (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  sources JSONB, -- Array of chunk citations: [{chapter_id, section, similarity_score}]
  created_at TIMESTAMP DEFAULT NOW()
);

-- Index on user_id for fast retrieval of user's chat history
CREATE INDEX IF NOT EXISTS idx_chat_history_user_id ON chat_history(user_id);

-- ============================================================================
-- TABLE: user_progress
-- Purpose: Track which chapters users have read and completed
-- Structure only - logic will be implemented in Day 2+
-- ============================================================================
CREATE TABLE IF NOT EXISTS user_progress (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  chapter_id VARCHAR(100) NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  last_accessed TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, chapter_id) -- Each user can only have one progress record per chapter
);

-- Index on user_id for fast retrieval of user's progress
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress(user_id);

-- ============================================================================
-- TABLE: translations_cache
-- Purpose: Cache Urdu translations of chapters to avoid re-translating
-- Structure only - translation logic will be implemented in Day 2+
-- ============================================================================
CREATE TABLE IF NOT EXISTS translations_cache (
  id SERIAL PRIMARY KEY,
  chapter_id VARCHAR(100) NOT NULL,
  language VARCHAR(10) DEFAULT 'ur', -- Language code (ur = Urdu)
  translated_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(chapter_id, language) -- Each chapter can only have one translation per language
);

-- Composite index on chapter_id and language for fast cache lookups
CREATE INDEX IF NOT EXISTS idx_translations_cache_chapter ON translations_cache(chapter_id, language);

-- ============================================================================
-- TABLE: personalized_content_cache
-- Purpose: Cache personalized chapter content by user level to avoid re-personalization
-- Structure only - personalization logic will be implemented in Day 2+
-- ============================================================================
CREATE TABLE IF NOT EXISTS personalized_content_cache (
  id SERIAL PRIMARY KEY,
  chapter_id VARCHAR(100) NOT NULL,
  user_level VARCHAR(50) NOT NULL, -- beginner/intermediate/advanced
  personalized_content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(chapter_id, user_level) -- Each chapter can only have one version per user level
);

-- Composite index on chapter_id and user_level for fast cache lookups
CREATE INDEX IF NOT EXISTS idx_personalized_cache ON personalized_content_cache(chapter_id, user_level);

-- ============================================================================
-- INITIALIZATION COMPLETE
-- ============================================================================
-- This schema creates 5 tables:
-- 1. users (authentication + preferences) - FULL IMPLEMENTATION TODAY
-- 2. chat_history (Q&A storage) - STRUCTURE ONLY
-- 3. user_progress (chapter tracking) - STRUCTURE ONLY
-- 4. translations_cache (Urdu translations) - STRUCTURE ONLY
-- 5. personalized_content_cache (level-based content) - STRUCTURE ONLY
-- ============================================================================

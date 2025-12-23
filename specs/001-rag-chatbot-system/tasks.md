# Implementation Tasks: RAG Chatbot System - DAY 1 ONLY

**Branch**: `001-rag-chatbot-system` | **Date**: 2025-12-20
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

**DAY 1 SCOPE**: Database + Authentication ONLY
**OUT OF SCOPE**: RAG chatbot, personalization, translation, Claude API, Qdrant, frontend

---

## Task Checklist

### Phase 1: Database Setup (Neon Postgres)

#### Task 1.1: Create Database Schema SQL File
**File**: `backend/scripts/init_db.sql`
**Estimate**: 30 minutes
**Priority**: P0 (blocking all other tasks)

**Objective**: Write SQL DDL statements to create all 5 database tables.

**Requirements**:
- Create SQL file with all table definitions from plan (lines 247-299)
- Tables needed:
  1. `users` (email, password_hash, name, programming_level, hardware, created_at)
  2. `chat_history` (structure only, no logic today)
  3. `user_progress` (structure only, no logic today)
  4. `translations_cache` (structure only, no logic today)
  5. `personalized_content_cache` (structure only, no logic today)
- Include all indexes (idx_users_email, idx_chat_history_user_id, etc.)
- Include UNIQUE constraints where specified
- Add clear comments above each table explaining its purpose

**Acceptance Criteria**:
- [ ] File exists at `backend/scripts/init_db.sql`
- [ ] All 5 tables defined with correct columns and data types
- [ ] All indexes created (users.email, chat_history.user_id, etc.)
- [ ] UNIQUE constraints on (user_id, chapter_id) for user_progress
- [ ] UNIQUE constraints on (chapter_id, language) for translations_cache
- [ ] UNIQUE constraints on (chapter_id, user_level) for personalized_content_cache
- [ ] Comments explain each table's purpose
- [ ] SQL syntax is PostgreSQL-compatible

**Test Cases**:
```bash
# Dry run: check SQL syntax
psql -h <neon_host> -U <user> -d <db> -f backend/scripts/init_db.sql --dry-run

# Actual run (will do in Task 1.3)
# psql -h <neon_host> -U <user> -d <db> -f backend/scripts/init_db.sql
```

**Code Reference**:
- Spec: spec.md:138-145 (Key Entities)
- Plan: plan.md:247-299 (Database Schema)

---

#### Task 1.2: Set Up Database Connection Configuration
**File**: `backend/app/utils/config.py` (NEW)
**Estimate**: 20 minutes
**Priority**: P0 (blocking database operations)

**Objective**: Create configuration module to load environment variables for database connection.

**Requirements**:
- Create `app/utils/__init__.py` if not exists
- Create `app/utils/config.py` with `Settings` class
- Use `pydantic-settings` to load from `.env`
- Load `DATABASE_URL` (Neon Postgres connection string)
- Load JWT settings: `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- Provide singleton `get_settings()` function

**Acceptance Criteria**:
- [ ] File exists at `backend/app/utils/config.py`
- [ ] `Settings` class inherits from `BaseSettings` (pydantic-settings)
- [ ] Fields: `database_url`, `secret_key`, `algorithm`, `access_token_expire_minutes`
- [ ] `get_settings()` returns cached singleton instance
- [ ] Can load values from `.env` file
- [ ] Clear comments explaining each setting

**Implementation**:
```python
# backend/app/utils/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    Uses .env file for local development.
    """
    # Database
    database_url: str

    # JWT Authentication
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
```

**Test Cases**:
```python
# Test loading settings
from app.utils.config import get_settings
settings = get_settings()
assert settings.database_url is not None
assert settings.secret_key is not None
```

**Code Reference**:
- Plan: plan.md (Technical Context, JWT Configuration)
- Existing: backend/.env.example (environment variables)

---

#### Task 1.3: Create Database Connection Module
**File**: `backend/app/utils/database.py` (NEW)
**Estimate**: 30 minutes
**Priority**: P0 (blocking all DB operations)

**Objective**: Create async database connection helper using asyncpg or async SQLAlchemy.

**Requirements**:
- Use `asyncpg` for async Postgres connection (simpler than SQLAlchemy for MVP)
- Create `get_db_pool()` function to return connection pool
- Create `init_db()` function to run `scripts/init_db.sql` (idempotent)
- Handle connection errors gracefully
- Close pool on app shutdown

**Acceptance Criteria**:
- [ ] File exists at `backend/app/utils/database.py`
- [ ] `get_db_pool()` creates and returns asyncpg connection pool
- [ ] `init_db()` reads and executes `scripts/init_db.sql`
- [ ] Connection pool is reusable across requests
- [ ] Error handling for connection failures
- [ ] Clear comments explaining connection lifecycle

**Implementation**:
```python
# backend/app/utils/database.py
import asyncpg
from app.utils.config import get_settings

# Global connection pool
_pool: asyncpg.Pool | None = None

async def get_db_pool() -> asyncpg.Pool:
    """
    Get or create async database connection pool.
    Reuses existing pool if already created.
    """
    global _pool
    if _pool is None:
        settings = get_settings()
        _pool = await asyncpg.create_pool(
            settings.database_url,
            min_size=1,
            max_size=10
        )
    return _pool

async def close_db_pool():
    """Close database connection pool on app shutdown."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None

async def init_db():
    """
    Initialize database by running init_db.sql.
    Idempotent: safe to run multiple times (CREATE TABLE IF NOT EXISTS).
    """
    pool = await get_db_pool()
    with open("backend/scripts/init_db.sql", "r") as f:
        sql = f.read()
    async with pool.acquire() as conn:
        await conn.execute(sql)
```

**Test Cases**:
```python
# Test connection
import asyncio
from app.utils.database import get_db_pool, init_db

async def test_connection():
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.fetchval("SELECT 1")
        assert result == 1
    print("✅ Database connection successful")

asyncio.run(test_connection())
```

**Code Reference**:
- Plan: plan.md (Milestone 1: Database & Core Services)

---

#### Task 1.4: Update .env.example with Database URL
**File**: `backend/.env.example`
**Estimate**: 5 minutes
**Priority**: P1

**Objective**: Ensure .env.example has correct DATABASE_URL format for Neon Postgres.

**Requirements**:
- Update `DATABASE_URL` to match Neon connection string format
- Add comment explaining how to get Neon connection string
- Ensure `SECRET_KEY` example is present
- Ensure JWT settings are present

**Acceptance Criteria**:
- [ ] `DATABASE_URL` has Neon Postgres format example
- [ ] Comment explains where to find connection string
- [ ] `SECRET_KEY` has example value (user must change)
- [ ] `ALGORITHM` and `ACCESS_TOKEN_EXPIRE_MINUTES` present

**Implementation**:
```bash
# Database Configuration (Neon Postgres)
# Get your connection string from: https://console.neon.tech/app/projects
DATABASE_URL=postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# JWT Authentication
# Generate SECRET_KEY with: openssl rand -hex 32
SECRET_KEY=your_secret_key_here_generate_with_openssl_rand_hex_32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

**Test Cases**:
- Verify .env.example can be copied to .env and app loads settings correctly

**Code Reference**:
- Existing: backend/.env.example (already has some settings)

---

### Phase 2: Authentication System

#### Task 2.1: Create Pydantic Models for Authentication
**File**: `backend/app/models/user.py` (NEW)
**Estimate**: 20 minutes
**Priority**: P0 (blocking auth endpoints)

**Objective**: Define Pydantic schemas for user signup, login, and responses.

**Requirements**:
- Create `UserCreate` schema (signup request)
- Create `UserLogin` schema (login request)
- Create `User` schema (response, no password)
- Create `Token` schema (JWT response)
- Use `EmailStr` for email validation
- Add field validation (programming_level must be beginner/intermediate/advanced)

**Acceptance Criteria**:
- [ ] File exists at `backend/app/models/user.py`
- [ ] `UserCreate` has: email, password, name, programming_level, hardware
- [ ] `UserLogin` has: email, password
- [ ] `User` has: id, email, name, programming_level, hardware (NO password_hash)
- [ ] `Token` has: access_token, token_type
- [ ] Email validation using `EmailStr`
- [ ] programming_level validated (beginner/intermediate/advanced)
- [ ] hardware validated (none/gpu/jetson/robotics)
- [ ] Clear docstrings for each model

**Implementation**:
```python
# backend/app/models/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserCreate(BaseModel):
    """Request schema for user signup."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1)
    programming_level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    hardware: Literal["none", "gpu", "jetson", "robotics"] = "none"

class UserLogin(BaseModel):
    """Request schema for user login."""
    email: EmailStr
    password: str

class User(BaseModel):
    """Response schema for user data (no password)."""
    id: int
    email: str
    name: str
    programming_level: str
    hardware: str

class Token(BaseModel):
    """Response schema for JWT token."""
    access_token: str
    token_type: str = "bearer"
```

**Test Cases**:
```python
# Test validation
user_create = UserCreate(
    email="test@example.com",
    password="securepass123",
    name="Test User",
    programming_level="beginner",
    hardware="none"
)
assert user_create.email == "test@example.com"

# Test invalid level
try:
    UserCreate(email="test@example.com", password="pass", name="Test", programming_level="expert")
    assert False, "Should fail validation"
except ValidationError:
    pass  # Expected
```

**Code Reference**:
- Spec: spec.md:112 (FR-008: signup fields)
- Plan: plan.md (Pydantic Models section)

---

#### Task 2.2: Create Password Hashing Utilities
**File**: `backend/app/utils/auth.py` (NEW)
**Estimate**: 20 minutes
**Priority**: P0 (blocking auth logic)

**Objective**: Create password hashing and verification functions using passlib.

**Requirements**:
- Use `passlib` with `bcrypt` scheme
- Salt rounds ≥ 10 (as per FR-009)
- Create `hash_password(password: str) -> str` function
- Create `verify_password(password: str, hash: str) -> bool` function
- Create `create_access_token(data: dict) -> str` for JWT
- Create `decode_access_token(token: str) -> dict` for JWT verification

**Acceptance Criteria**:
- [ ] File exists at `backend/app/utils/auth.py`
- [ ] `hash_password()` uses bcrypt with rounds ≥ 10
- [ ] `verify_password()` returns True/False for password match
- [ ] `create_access_token()` creates JWT with expiration
- [ ] `decode_access_token()` verifies and decodes JWT
- [ ] Clear comments explaining each function
- [ ] Error handling for invalid tokens

**Implementation**:
```python
# backend/app/utils/auth.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.utils.config import get_settings

# Password hashing context (bcrypt with salt rounds >= 10)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    Salt rounds: 12 (>= 10 as per FR-009).
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash.
    Returns True if match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create JWT access token.
    Default expiration: 7 days (from settings).
    """
    settings = get_settings()
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decode and verify JWT token.
    Raises JWTError if invalid or expired.
    """
    settings = get_settings()
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    return payload
```

**Test Cases**:
```python
# Test password hashing
hashed = hash_password("mypassword123")
assert verify_password("mypassword123", hashed) == True
assert verify_password("wrongpassword", hashed) == False

# Test JWT
token = create_access_token({"sub": "user123"})
payload = decode_access_token(token)
assert payload["sub"] == "user123"
```

**Code Reference**:
- Spec: spec.md:113 (FR-009: bcrypt with salt rounds ≥10)
- Spec: spec.md:114 (FR-010: JWT with 7-day expiration)

---

#### Task 2.3: Create Database Service for User Operations
**File**: `backend/app/services/db_service.py` (NEW)
**Estimate**: 30 minutes
**Priority**: P0 (blocking auth endpoints)

**Objective**: Create database service with user CRUD operations.

**Requirements**:
- Create `create_user()` function (INSERT)
- Create `get_user_by_email()` function (SELECT)
- Create `get_user_by_id()` function (SELECT)
- Use asyncpg connection pool from `database.py`
- Return dictionaries (not ORM objects)
- Handle duplicate email errors

**Acceptance Criteria**:
- [ ] File exists at `backend/app/services/db_service.py`
- [ ] `create_user(email, password_hash, name, level, hardware)` returns user_id
- [ ] `get_user_by_email(email)` returns user dict or None
- [ ] `get_user_by_id(user_id)` returns user dict or None
- [ ] Functions use async/await with asyncpg
- [ ] Error handling for duplicate emails (unique constraint)
- [ ] Clear comments explaining each function

**Implementation**:
```python
# backend/app/services/db_service.py
from app.utils.database import get_db_pool
from asyncpg.exceptions import UniqueViolationError

class DBService:
    """Database service for user and data operations."""

    @staticmethod
    async def create_user(
        email: str,
        password_hash: str,
        name: str,
        programming_level: str,
        hardware: str
    ) -> int:
        """
        Create a new user in the database.
        Returns: user_id (int)
        Raises: UniqueViolationError if email already exists
        """
        pool = await get_db_pool()
        query = """
            INSERT INTO users (email, password_hash, name, programming_level, hardware)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """
        async with pool.acquire() as conn:
            user_id = await conn.fetchval(query, email, password_hash, name, programming_level, hardware)
        return user_id

    @staticmethod
    async def get_user_by_email(email: str) -> dict | None:
        """
        Get user by email.
        Returns: user dict or None if not found
        """
        pool = await get_db_pool()
        query = """
            SELECT id, email, password_hash, name, programming_level, hardware, created_at
            FROM users
            WHERE email = $1
        """
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, email)

        if row is None:
            return None

        return dict(row)

    @staticmethod
    async def get_user_by_id(user_id: int) -> dict | None:
        """
        Get user by ID.
        Returns: user dict or None if not found
        """
        pool = await get_db_pool()
        query = """
            SELECT id, email, password_hash, name, programming_level, hardware, created_at
            FROM users
            WHERE id = $1
        """
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)

        if row is None:
            return None

        return dict(row)
```

**Test Cases**:
```python
# Test user creation
user_id = await DBService.create_user(
    email="test@example.com",
    password_hash="hashed_password",
    name="Test User",
    programming_level="beginner",
    hardware="none"
)
assert user_id > 0

# Test get by email
user = await DBService.get_user_by_email("test@example.com")
assert user["email"] == "test@example.com"

# Test duplicate email (should raise error)
try:
    await DBService.create_user("test@example.com", "hash", "Test", "beginner", "none")
    assert False, "Should raise UniqueViolationError"
except UniqueViolationError:
    pass  # Expected
```

**Code Reference**:
- Plan: plan.md (DBService section)

---

#### Task 2.4: Create Authentication Router with Endpoints
**File**: `backend/app/routers/auth.py` (NEW)
**Estimate**: 45 minutes
**Priority**: P1 (main deliverable)

**Objective**: Implement POST /signup, POST /login, GET /me endpoints.

**Requirements**:
- POST `/api/auth/signup`: Create user, hash password, return JWT
- POST `/api/auth/login`: Verify credentials, return JWT
- GET `/api/auth/me`: Return current user (requires JWT)
- Use `OAuth2PasswordBearer` for token extraction
- Create `get_current_user` dependency for protected routes
- Return proper HTTP status codes (201, 200, 401, 400)
- Handle errors: duplicate email, invalid credentials, invalid token

**Acceptance Criteria**:
- [ ] File exists at `backend/app/routers/auth.py`
- [ ] POST `/api/auth/signup` creates user and returns Token
- [ ] POST `/api/auth/login` verifies password and returns Token
- [ ] GET `/api/auth/me` requires valid JWT and returns User
- [ ] Status codes: 201 (signup), 200 (login, me), 401 (unauthorized), 400 (bad request)
- [ ] Error handling for all edge cases
- [ ] Clear comments explaining each endpoint

**Implementation**:
```python
# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserLogin, User, Token
from app.services.db_service import DBService
from app.utils.auth import hash_password, verify_password, create_access_token, decode_access_token
from jose import JWTError
from asyncpg.exceptions import UniqueViolationError

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get current authenticated user from JWT token.
    Raises 401 if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_data = await DBService.get_user_by_id(user_id)
    if user_data is None:
        raise credentials_exception

    return User(
        id=user_data["id"],
        email=user_data["email"],
        name=user_data["name"],
        programming_level=user_data["programming_level"],
        hardware=user_data["hardware"]
    )

@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_create: UserCreate):
    """
    Create a new user account.
    Returns JWT access token on success.
    Raises 400 if email already exists.
    """
    # Hash password
    password_hash = hash_password(user_create.password)

    try:
        # Create user in database
        user_id = await DBService.create_user(
            email=user_create.email,
            password_hash=password_hash,
            name=user_create.name,
            programming_level=user_create.programming_level,
            hardware=user_create.hardware
        )
    except UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": user_id})

    return Token(access_token=access_token)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Authenticate user with email and password.
    Returns JWT access token on success.
    Raises 401 if credentials are invalid.
    """
    # Get user by email
    user_data = await DBService.get_user_by_email(credentials.email)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(credentials.password, user_data["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(data={"sub": user_data["id"]})

    return Token(access_token=access_token)

@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.
    Requires valid JWT token in Authorization header.
    """
    return current_user
```

**Test Cases**:
```bash
# Test signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securepass123","name":"Test User","programming_level":"beginner","hardware":"none"}'

# Expected: {"access_token":"...", "token_type":"bearer"}

# Test login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"securepass123"}'

# Expected: {"access_token":"...", "token_type":"bearer"}

# Test get me
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <token>"

# Expected: {"id":1,"email":"test@example.com","name":"Test User","programming_level":"beginner","hardware":"none"}
```

**Code Reference**:
- Spec: spec.md:112-115 (FR-008 to FR-011: auth requirements)
- Plan: plan.md (Authentication endpoints section)

---

#### Task 2.5: Register Auth Router in Main App
**File**: `backend/main.py`
**Estimate**: 10 minutes
**Priority**: P1

**Objective**: Include auth router in FastAPI app and add database lifecycle hooks.

**Requirements**:
- Import auth router
- Include router with prefix `/api/auth` and tag `auth`
- Add startup event to initialize database
- Add shutdown event to close database pool
- Update CORS allowed origins if needed

**Acceptance Criteria**:
- [ ] Auth router imported and included in app
- [ ] Router prefix is `/api/auth`
- [ ] Startup event calls `init_db()`
- [ ] Shutdown event calls `close_db_pool()`
- [ ] App runs without errors on startup

**Implementation**:
```python
# backend/main.py
"""
Physical AI Textbook - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.utils.database import init_db, close_db_pool

app = FastAPI(
    title="Physical AI Textbook API",
    description="Backend API for AI-native interactive textbook with RAG chatbot",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup: Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on app startup."""
    await init_db()
    print("✅ Database initialized")

# Shutdown: Close database pool
@app.on_event("shutdown")
async def shutdown_event():
    """Close database pool on app shutdown."""
    await close_db_pool()
    print("✅ Database pool closed")

@app.get("/")
async def root():
    return {
        "message": "Physical AI Textbook API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Test Cases**:
```bash
# Start server
cd backend
uvicorn main:app --reload

# Verify startup message
# Expected console output: "✅ Database initialized"

# Test health endpoint
curl http://localhost:8000/api/health
# Expected: {"status":"healthy"}

# Test auth endpoints (from Task 2.4 test cases)
```

**Code Reference**:
- Existing: backend/main.py (lines 1-48)

---

### Phase 3: Verification & Documentation

#### Task 3.1: Create Local .env File (Developer Action)
**File**: `backend/.env` (local only, not committed)
**Estimate**: 5 minutes
**Priority**: P1

**Objective**: Create actual .env file for local development.

**Requirements**:
- Copy `.env.example` to `.env`
- Fill in actual `DATABASE_URL` from Neon console
- Generate `SECRET_KEY` using `openssl rand -hex 32`
- Verify `.env` is in `.gitignore`

**Acceptance Criteria**:
- [ ] File exists at `backend/.env` (local only)
- [ ] `DATABASE_URL` has actual Neon connection string
- [ ] `SECRET_KEY` is generated (not example value)
- [ ] `.env` is in `.gitignore` (verify not tracked by git)

**Commands**:
```bash
# Copy example
cp backend/.env.example backend/.env

# Generate secret key
openssl rand -hex 32

# Edit .env and paste:
# - DATABASE_URL from Neon console
# - Generated SECRET_KEY

# Verify not tracked
git status | grep .env
# Should show: .env (untracked) or nothing if already in .gitignore
```

**Code Reference**:
- Security: Never commit .env to version control

---

#### Task 3.2: Install Missing Dependencies (if any)
**File**: `backend/requirements.txt`
**Estimate**: 5 minutes
**Priority**: P1

**Objective**: Ensure asyncpg is in requirements.txt.

**Requirements**:
- Check if `asyncpg` is in requirements.txt
- Add `asyncpg==0.29.0` if missing
- Run `pip install -r requirements.txt` to install

**Acceptance Criteria**:
- [ ] `asyncpg` is in requirements.txt
- [ ] All dependencies install without errors

**Commands**:
```bash
# Check requirements.txt
grep asyncpg backend/requirements.txt

# If missing, add:
echo "asyncpg==0.29.0" >> backend/requirements.txt

# Install
cd backend
pip install -r requirements.txt
```

**Code Reference**:
- Existing: backend/requirements.txt

---

#### Task 3.3: Manual Testing - End-to-End Auth Flow
**Estimate**: 20 minutes
**Priority**: P1 (acceptance testing)

**Objective**: Manually test complete signup → login → get me flow.

**Test Script**:
```bash
#!/bin/bash
# Save as: backend/tests/test_auth_manual.sh

BASE_URL="http://localhost:8000"

echo "🔧 Testing Authentication Flow..."

# 1. Test signup
echo "\n1️⃣ Testing signup..."
SIGNUP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email":"testuser@example.com",
    "password":"securepass123",
    "name":"Test User",
    "programming_level":"beginner",
    "hardware":"none"
  }')

echo "Signup response: $SIGNUP_RESPONSE"
TOKEN=$(echo $SIGNUP_RESPONSE | jq -r '.access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
  echo "❌ Signup failed - no token received"
  exit 1
fi
echo "✅ Signup successful - Token: ${TOKEN:0:20}..."

# 2. Test login
echo "\n2️⃣ Testing login..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email":"testuser@example.com",
    "password":"securepass123"
  }')

echo "Login response: $LOGIN_RESPONSE"
LOGIN_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

if [ -z "$LOGIN_TOKEN" ] || [ "$LOGIN_TOKEN" == "null" ]; then
  echo "❌ Login failed - no token received"
  exit 1
fi
echo "✅ Login successful"

# 3. Test get me
echo "\n3️⃣ Testing get current user..."
ME_RESPONSE=$(curl -s -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $LOGIN_TOKEN")

echo "Get me response: $ME_RESPONSE"

if echo $ME_RESPONSE | jq -e '.email' > /dev/null; then
  echo "✅ Get me successful"
else
  echo "❌ Get me failed"
  exit 1
fi

# 4. Test duplicate signup (should fail)
echo "\n4️⃣ Testing duplicate signup (should fail)..."
DUP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email":"testuser@example.com",
    "password":"anotherpass",
    "name":"Another User",
    "programming_level":"advanced",
    "hardware":"gpu"
  }')

if echo $DUP_RESPONSE | grep -q "already registered"; then
  echo "✅ Duplicate email correctly rejected"
else
  echo "❌ Duplicate email not rejected properly"
  exit 1
fi

# 5. Test invalid credentials
echo "\n5️⃣ Testing invalid login (should fail)..."
INVALID_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email":"testuser@example.com",
    "password":"wrongpassword"
  }')

if echo $INVALID_RESPONSE | grep -q "Invalid"; then
  echo "✅ Invalid credentials correctly rejected"
else
  echo "❌ Invalid credentials not rejected properly"
  exit 1
fi

echo "\n🎉 All authentication tests passed!"
```

**Acceptance Criteria**:
- [ ] Signup creates user and returns token (201)
- [ ] Login with correct credentials returns token (200)
- [ ] Get me with valid token returns user data (200)
- [ ] Duplicate signup returns error (400)
- [ ] Invalid credentials return error (401)
- [ ] Invalid token returns error (401)

**Code Reference**:
- Test against all endpoints created in Task 2.4

---

#### Task 3.4: Update README (if exists) with Day 1 Progress
**File**: `backend/README.md` or `README.md`
**Estimate**: 10 minutes
**Priority**: P2 (optional but recommended)

**Objective**: Document what was completed in Day 1.

**Content**:
```markdown
# Physical AI Textbook Backend

## Day 1 Progress (2025-12-20)

### Completed Features
✅ Database setup (Neon Postgres)
- 5 tables created: users, chat_history, user_progress, translations_cache, personalized_content_cache
- Connection pooling with asyncpg
- Idempotent initialization

✅ Authentication system
- POST /api/auth/signup (create user, return JWT)
- POST /api/auth/login (verify credentials, return JWT)
- GET /api/auth/me (get current user, requires JWT)
- Password hashing with bcrypt (salt rounds: 12)
- JWT tokens with 7-day expiration

### Not Yet Implemented (Future Days)
❌ RAG chatbot (Qdrant + Claude API)
❌ Personalization (Claude API)
❌ Urdu translation (Claude API)
❌ Progress tracking endpoints
❌ Rate limiting

### Setup Instructions

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your Neon Postgres URL and secret key
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Test endpoints:
   ```bash
   # Signup
   curl -X POST http://localhost:8000/api/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"pass123","name":"Test","programming_level":"beginner","hardware":"none"}'

   # Login
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"pass123"}'
   ```

### Database Schema
See `backend/scripts/init_db.sql` for full schema.

### Environment Variables
- `DATABASE_URL`: Neon Postgres connection string
- `SECRET_KEY`: JWT signing key (generate with `openssl rand -hex 32`)
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration (default: 10080 = 7 days)
```

**Acceptance Criteria**:
- [ ] README documents Day 1 completed features
- [ ] Setup instructions are clear
- [ ] Environment variables documented

---

## Summary

### Day 1 Deliverables

**Database (Neon Postgres)**:
- ✅ `backend/scripts/init_db.sql` - SQL schema for 5 tables
- ✅ `backend/app/utils/config.py` - Environment config loader
- ✅ `backend/app/utils/database.py` - Async connection pool

**Authentication**:
- ✅ `backend/app/models/user.py` - Pydantic schemas
- ✅ `backend/app/utils/auth.py` - Password hashing + JWT
- ✅ `backend/app/services/db_service.py` - User CRUD operations
- ✅ `backend/app/routers/auth.py` - Auth endpoints (signup, login, me)
- ✅ `backend/main.py` - Updated with auth router and DB lifecycle

**Configuration**:
- ✅ `backend/.env.example` - Updated with DATABASE_URL format
- ✅ `backend/.env` - Created locally (not committed)
- ✅ `backend/requirements.txt` - asyncpg added

**Testing**:
- ✅ Manual end-to-end auth flow tested
- ✅ All endpoints return correct status codes
- ✅ Error handling verified (duplicate email, invalid credentials, invalid token)

### Acceptance Criteria (Overall)

- [ ] Database tables created in Neon Postgres
- [ ] Auth endpoints working (signup, login, me)
- [ ] .env.example updated with DATABASE_URL format
- [ ] App runs without errors (`uvicorn main:app --reload`)
- [ ] All 5 manual tests pass (see Task 3.3)

### Next Steps (Day 2+)

**Not started yet**:
- RAG chatbot (Qdrant + Claude API)
- Personalization logic
- Urdu translation
- Progress tracking endpoints
- Rate limiting
- Frontend integration

### Time Estimate: 4-5 hours total

| Phase | Tasks | Time |
|-------|-------|------|
| Database Setup | 1.1-1.4 | 90 min |
| Authentication | 2.1-2.5 | 125 min |
| Verification | 3.1-3.4 | 40 min |
| **Total** | **11 tasks** | **~4.2 hours** |

---

## Task Dependencies

```
1.1 (init_db.sql) → 1.3 (database.py) → 2.3 (db_service.py)
1.2 (config.py) → 1.3 (database.py)
1.2 (config.py) → 2.2 (auth.py utils)

2.1 (user models) → 2.4 (auth router)
2.2 (auth utils) → 2.4 (auth router)
2.3 (db_service.py) → 2.4 (auth router)

2.4 (auth router) → 2.5 (main.py)
2.5 (main.py) → 3.3 (manual testing)

1.4 (.env.example) → 3.1 (.env)
3.1 (.env) → 3.2 (install deps)
3.2 (install deps) → 3.3 (manual testing)
```

**Critical Path**: 1.1 → 1.2 → 1.3 → 2.3 → 2.4 → 2.5 → 3.3

---

**End of Day 1 Tasks**

"""
Physical AI Textbook - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, chat, personalize, translate
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


# Database lifecycle events
@app.on_event("startup")
async def startup_event():
    """
    Initialize database on application startup.
    Creates connection pool and runs schema initialization.
    """
    await init_db()
    print("[OK] Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Close database connection pool on application shutdown.
    Ensures graceful cleanup of database connections.
    """
    await close_db_pool()
    print("✅ Database connection pool closed")


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
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])  # Day 2: RAG Chatbot
app.include_router(personalize.router, prefix="/api/personalize", tags=["personalize"])  # Day 3: Personalization
app.include_router(translate.router, prefix="/api/translate", tags=["translate"])  # Day 3: Translation

# Future routers (Day 4+)
# app.include_router(progress.router, prefix="/api/user", tags=["progress"])

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))  # Use PORT env var if set, else 8000
    uvicorn.run(app, host="0.0.0.0", port=port)

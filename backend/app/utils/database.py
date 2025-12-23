"""
Database connection module using asyncpg for async PostgreSQL operations.
Provides connection pooling and database initialization.
"""

import asyncpg
from pathlib import Path
from app.utils.config import get_settings

# Global connection pool (initialized on first request)
_pool: asyncpg.Pool | None = None


async def get_db_pool() -> asyncpg.Pool:
    """
    Get or create async database connection pool.

    Reuses existing pool if already created. The pool maintains
    multiple connections to the database for efficient concurrent access.

    Connection pool settings:
    - min_size: 1 connection (minimum kept alive)
    - max_size: 10 connections (maximum concurrent connections)

    Returns:
        asyncpg.Pool: Database connection pool

    Raises:
        asyncpg.PostgresError: If connection to database fails

    Example:
        >>> pool = await get_db_pool()
        >>> async with pool.acquire() as conn:
        >>>     result = await conn.fetchval("SELECT 1")
        >>>     print(result)  # 1
    """
    global _pool

    if _pool is None:
        settings = get_settings()

        try:
            _pool = await asyncpg.create_pool(
                settings.database_url,
                min_size=1,
                max_size=10,
                command_timeout=60  # 60 seconds timeout for queries
            )
            print("[OK] Database connection pool created")
        except Exception as e:
            print(f"[ERROR] Failed to create database pool: {e}")
            raise

    return _pool


async def close_db_pool():
    """
    Close database connection pool on app shutdown.

    Gracefully closes all connections in the pool and releases resources.
    Safe to call even if pool is not initialized.

    Example:
        >>> # Called automatically on app shutdown
        >>> await close_db_pool()
    """
    global _pool

    if _pool is not None:
        await _pool.close()
        _pool = None
        print("[OK] Database connection pool closed")


async def init_db():
    """
    Initialize database by running init_db.sql schema file.

    This function is idempotent - safe to run multiple times.
    The SQL script uses IF NOT EXISTS clauses, so existing
    tables won't be modified.

    Reads and executes: backend/scripts/init_db.sql

    Raises:
        FileNotFoundError: If init_db.sql file doesn't exist
        asyncpg.PostgresError: If SQL execution fails

    Example:
        >>> # Called automatically on app startup
        >>> await init_db()
    """
    pool = await get_db_pool()

    # Path to SQL schema file (relative to project root)
    sql_file = Path(__file__).parent.parent.parent / "scripts" / "init_db.sql"

    if not sql_file.exists():
        raise FileNotFoundError(
            f"Database schema file not found: {sql_file}\n"
            "Please ensure backend/scripts/init_db.sql exists."
        )

    # Read SQL file
    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()

    # Execute SQL (create tables and indexes)
    async with pool.acquire() as conn:
        try:
            await conn.execute(sql)
            print("[OK] Database schema initialized successfully")
        except Exception as e:
            print(f"[ERROR] Failed to initialize database schema: {e}")
            raise

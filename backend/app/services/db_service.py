"""
Database service for user and data operations.
Provides async CRUD operations for users using asyncpg connection pool.
"""

from app.utils.database import get_db_pool
from asyncpg.exceptions import UniqueViolationError


class DBService:
    """
    Database service for user CRUD operations.

    Uses asyncpg connection pool for async database operations.
    All methods are static - no need to instantiate the class.

    Example:
        >>> user_id = await DBService.create_user(...)
        >>> user = await DBService.get_user_by_email("test@example.com")
    """

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

        Args:
            email: User's email address (must be unique)
            password_hash: Bcrypt hashed password (NOT plain password)
            name: User's display name
            programming_level: User's programming expertise (beginner/intermediate/advanced)
            hardware: User's available hardware (none/gpu/jetson/robotics)

        Returns:
            int: The new user's ID (database primary key)

        Raises:
            UniqueViolationError: If email already exists in database

        Example:
            >>> from app.utils.auth import hash_password
            >>> password_hash = hash_password("securepass123")
            >>> user_id = await DBService.create_user(
            ...     email="student@example.com",
            ...     password_hash=password_hash,
            ...     name="Ahmed Khan",
            ...     programming_level="beginner",
            ...     hardware="none"
            ... )
            >>> print(user_id)  # 1
        """
        pool = await get_db_pool()

        query = """
            INSERT INTO users (email, password_hash, name, programming_level, hardware)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """

        async with pool.acquire() as conn:
            user_id = await conn.fetchval(
                query,
                email,
                password_hash,
                name,
                programming_level,
                hardware
            )

        return user_id

    @staticmethod
    async def get_user_by_email(email: str) -> dict | None:
        """
        Get user by email address.

        Retrieves complete user record including password_hash.
        Used during login to verify credentials.

        Args:
            email: User's email address

        Returns:
            dict | None: User data as dictionary, or None if not found

        Dictionary keys:
            - id: int
            - email: str
            - password_hash: str
            - name: str
            - programming_level: str
            - hardware: str
            - created_at: datetime

        Example:
            >>> user = await DBService.get_user_by_email("student@example.com")
            >>> if user:
            ...     print(user["id"])           # 1
            ...     print(user["email"])        # "student@example.com"
            ...     print(user["password_hash"])  # "$2b$12$..."
            ... else:
            ...     print("User not found")
        """
        pool = await get_db_pool()

        query = """
            SELECT id, email, password_hash, name, programming_level, hardware, created_at
            FROM users
            WHERE email = $1
        """

        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, email)

        # Return None if user not found
        if row is None:
            return None

        # Convert asyncpg Record to dict
        return dict(row)

    @staticmethod
    async def get_user_by_id(user_id: int) -> dict | None:
        """
        Get user by ID.

        Retrieves complete user record including password_hash.
        Used to fetch user data after JWT token validation.

        Args:
            user_id: User's ID (database primary key)

        Returns:
            dict | None: User data as dictionary, or None if not found

        Dictionary keys:
            - id: int
            - email: str
            - password_hash: str
            - name: str
            - programming_level: str
            - hardware: str
            - created_at: datetime

        Example:
            >>> user = await DBService.get_user_by_id(1)
            >>> if user:
            ...     print(user["name"])             # "Ahmed Khan"
            ...     print(user["programming_level"])  # "beginner"
            ... else:
            ...     print("User not found")
        """
        pool = await get_db_pool()

        query = """
            SELECT id, email, password_hash, name, programming_level, hardware, created_at
            FROM users
            WHERE id = $1
        """

        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)

        # Return None if user not found
        if row is None:
            return None

        # Convert asyncpg Record to dict
        return dict(row)

    @staticmethod
    async def save_chat_history(
        user_id: int,
        question: str,
        answer: str,
        sources: str  # JSON string
    ) -> int:
        """
        Save a chat Q&A exchange to database.

        Args:
            user_id: User's ID
            question: User's question
            answer: AI-generated answer
            sources: JSON string of source citations

        Returns:
            int: Chat history entry ID

        Example:
            >>> import json
            >>> sources_json = json.dumps([{"chapter_id": "ch3", "similarity": 0.9}])
            >>> chat_id = await DBService.save_chat_history(
            ...     user_id=1,
            ...     question="What is a CNN?",
            ...     answer="CNNs are...",
            ...     sources=sources_json
            ... )
        """
        pool = await get_db_pool()

        query = """
            INSERT INTO chat_history (user_id, question, answer, sources)
            VALUES ($1, $2, $3, $4::jsonb)
            RETURNING id
        """

        async with pool.acquire() as conn:
            chat_id = await conn.fetchval(
                query,
                user_id,
                question,
                answer,
                sources
            )

        return chat_id

    @staticmethod
    async def get_chat_history(
        user_id: int,
        limit: int = 20
    ) -> list:
        """
        Get user's chat history (most recent first).

        Args:
            user_id: User's ID
            limit: Number of entries to return (default: 20, max: 100)

        Returns:
            list: Chat history entries (most recent first)

        Example:
            >>> history = await DBService.get_chat_history(user_id=1, limit=10)
            >>> for chat in history:
            ...     print(chat["question"], chat["created_at"])
        """
        pool = await get_db_pool()

        query = """
            SELECT id, question, answer, sources, created_at
            FROM chat_history
            WHERE user_id = $1
            ORDER BY created_at DESC
            LIMIT $2
        """

        async with pool.acquire() as conn:
            rows = await conn.fetch(query, user_id, limit)

        # Convert to list of dicts
        return [dict(row) for row in rows]

    @staticmethod
    async def get_personalized_content(
        chapter_id: str,
        user_level: str
    ) -> str | None:
        """
        Get cached personalized content for a chapter.

        Args:
            chapter_id: Chapter identifier
            user_level: User's programming level

        Returns:
            str | None: Personalized content if cached, None otherwise

        Example:
            >>> content = await DBService.get_personalized_content(
            ...     chapter_id="chapter-3-cnns",
            ...     user_level="beginner"
            ... )
        """
        pool = await get_db_pool()

        query = """
            SELECT personalized_content
            FROM personalized_content_cache
            WHERE chapter_id = $1 AND user_level = $2
        """

        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, chapter_id, user_level)

        if row is None:
            return None

        return row["personalized_content"]

    @staticmethod
    async def save_personalized_content(
        chapter_id: str,
        user_level: str,
        personalized_content: str
    ) -> int:
        """
        Save personalized content to cache.

        Uses UPSERT (INSERT ... ON CONFLICT UPDATE) to handle duplicates.

        Args:
            chapter_id: Chapter identifier
            user_level: User's programming level
            personalized_content: Personalized content

        Returns:
            int: Cache entry ID

        Example:
            >>> cache_id = await DBService.save_personalized_content(
            ...     chapter_id="chapter-3-cnns",
            ...     user_level="beginner",
            ...     personalized_content="Let's learn CNNs..."
            ... )
        """
        pool = await get_db_pool()

        query = """
            INSERT INTO personalized_content_cache (chapter_id, user_level, personalized_content)
            VALUES ($1, $2, $3)
            ON CONFLICT (chapter_id, user_level)
            DO UPDATE SET
                personalized_content = EXCLUDED.personalized_content,
                created_at = NOW()
            RETURNING id
        """

        async with pool.acquire() as conn:
            cache_id = await conn.fetchval(
                query,
                chapter_id,
                user_level,
                personalized_content
            )

        return cache_id

    @staticmethod
    async def get_translation(
        chapter_id: str,
        language: str
    ) -> str | None:
        """
        Get cached translation for a chapter.

        Args:
            chapter_id: Chapter identifier
            language: Target language code

        Returns:
            str | None: Translated content if cached, None otherwise

        Example:
            >>> translation = await DBService.get_translation(
            ...     chapter_id="chapter-3-cnns",
            ...     language="ur"
            ... )
        """
        pool = await get_db_pool()

        query = """
            SELECT translated_content
            FROM translations_cache
            WHERE chapter_id = $1 AND language = $2
        """

        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, chapter_id, language)

        if row is None:
            return None

        return row["translated_content"]

    @staticmethod
    async def save_translation(
        chapter_id: str,
        language: str,
        translated_content: str
    ) -> int:
        """
        Save translation to cache.

        Uses UPSERT (INSERT ... ON CONFLICT UPDATE) to handle duplicates.

        Args:
            chapter_id: Chapter identifier
            language: Target language code
            translated_content: Translated content

        Returns:
            int: Cache entry ID

        Example:
            >>> cache_id = await DBService.save_translation(
            ...     chapter_id="chapter-3-cnns",
            ...     language="ur",
            ...     translated_content="CNNs ایک خاص قسم..."
            ... )
        """
        pool = await get_db_pool()

        query = """
            INSERT INTO translations_cache (chapter_id, language, translated_content)
            VALUES ($1, $2, $3)
            ON CONFLICT (chapter_id, language)
            DO UPDATE SET
                translated_content = EXCLUDED.translated_content,
                created_at = NOW()
            RETURNING id
        """

        async with pool.acquire() as conn:
            cache_id = await conn.fetchval(
                query,
                chapter_id,
                language,
                translated_content
            )

        return cache_id

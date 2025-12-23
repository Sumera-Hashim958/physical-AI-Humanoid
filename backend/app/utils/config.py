"""
Application configuration module.
Loads environment variables from .env file using pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    Uses .env file for local development.

    Environment variables:
    - DATABASE_URL: Neon Postgres connection string
    - SECRET_KEY: JWT signing key (generate with: openssl rand -hex 32)
    - ALGORITHM: JWT algorithm (default: HS256)
    - ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration in minutes (default: 10080 = 7 days)
    - QDRANT_URL: Qdrant Cloud cluster URL
    - QDRANT_API_KEY: Qdrant API key
    - QDRANT_COLLECTION_NAME: Collection name for textbook chunks
    - ANTHROPIC_API_KEY: Claude API key (optional for development)
    - CLAUDE_MODEL: Claude model to use (default: claude-3-5-sonnet-20241022)
    """

    # Database Configuration
    database_url: str

    # JWT Authentication Configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days (7 * 24 * 60)

    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str = "textbook_chunks"

    # Claude API Configuration (optional for development)
    anthropic_api_key: str = ""  # Empty string if not set
    claude_model: str = "claude-3-5-sonnet-20241022"

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Allow DATABASE_URL or database_url
        extra="ignore"  # Ignore extra fields in .env for Day 2+ features
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Return cached settings instance.

    Uses lru_cache to ensure settings are loaded only once,
    improving performance and avoiding repeated file reads.

    Returns:
        Settings: Application configuration object

    Example:
        >>> from app.utils.config import get_settings
        >>> settings = get_settings()
        >>> print(settings.database_url)
    """
    return Settings()

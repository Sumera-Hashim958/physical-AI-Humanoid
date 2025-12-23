"""
Pydantic models for user authentication and user data.
Defines request/response schemas for signup, login, and user operations.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserCreate(BaseModel):
    """
    Request schema for user signup.

    Used when a new user creates an account.
    Password will be hashed before storing in database.

    Attributes:
        email: User's email address (must be valid email format)
        password: User's password (min 8 characters)
        name: User's display name
        programming_level: User's programming expertise (beginner/intermediate/advanced)
        hardware: User's available hardware (none/gpu/jetson/robotics)

    Example:
        >>> user_data = UserCreate(
        ...     email="student@example.com",
        ...     password="securepass123",
        ...     name="Ahmed Khan",
        ...     programming_level="beginner",
        ...     hardware="none"
        ... )
    """
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    name: str = Field(..., min_length=1, description="User's display name")
    programming_level: Literal["beginner", "intermediate", "advanced"] = Field(
        default="beginner",
        description="User's programming expertise level"
    )
    hardware: Literal["none", "gpu", "jetson", "robotics"] = Field(
        default="none",
        description="Hardware available to the user"
    )


class UserLogin(BaseModel):
    """
    Request schema for user login.

    Used when a user authenticates with email and password.

    Attributes:
        email: User's email address
        password: User's password (will be verified against hash)

    Example:
        >>> credentials = UserLogin(
        ...     email="student@example.com",
        ...     password="securepass123"
        ... )
    """
    email: EmailStr
    password: str


class User(BaseModel):
    """
    Response schema for user data.

    Returned after successful signup, login, or when fetching user details.
    Does NOT include password_hash for security.

    Attributes:
        id: User's unique ID (database primary key)
        email: User's email address
        name: User's display name
        programming_level: User's programming expertise level
        hardware: User's available hardware

    Example:
        >>> user = User(
        ...     id=1,
        ...     email="student@example.com",
        ...     name="Ahmed Khan",
        ...     programming_level="beginner",
        ...     hardware="none"
        ... )
    """
    id: int
    email: str
    name: str
    programming_level: str
    hardware: str


class Token(BaseModel):
    """
    Response schema for JWT token.

    Returned after successful signup or login.
    Client should store this token and include it in Authorization header
    for protected endpoints.

    Attributes:
        access_token: JWT token string
        token_type: Token type (always "bearer")

    Example:
        >>> token = Token(
        ...     access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        ...     token_type="bearer"
        ... )
        >>> # Client usage:
        >>> # headers = {"Authorization": f"Bearer {token.access_token}"}
    """
    access_token: str
    token_type: str = "bearer"

"""
Authentication router for user signup, login, and user management.
Provides endpoints for user registration, authentication, and profile retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user import UserCreate, UserLogin, User, Token
from app.services.db_service import DBService
from app.utils.auth import hash_password, verify_password, create_access_token, decode_access_token
from jose import JWTError
from asyncpg.exceptions import UniqueViolationError


# Create router
router = APIRouter()

# OAuth2 scheme for token extraction
# tokenUrl points to the login endpoint (relative to /api/auth prefix)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Dependency to get current authenticated user from JWT token.

    Extracts token from Authorization header, decodes it, and fetches user data.
    Used to protect endpoints that require authentication.

    Args:
        token: JWT token from Authorization header (automatically extracted)

    Returns:
        User: Current authenticated user data

    Raises:
        HTTPException: 401 if token is invalid, expired, or user not found

    Example:
        >>> @router.get("/protected")
        >>> async def protected_route(current_user: User = Depends(get_current_user)):
        >>>     return {"message": f"Hello {current_user.name}!"}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = decode_access_token(token)
        user_id_str = payload.get("sub")

        if user_id_str is None:
            raise credentials_exception

        # Convert string user_id back to int
        user_id: int = int(user_id_str)

    except (JWTError, ValueError):
        raise credentials_exception

    # Get user from database
    user_data = await DBService.get_user_by_id(user_id)

    if user_data is None:
        raise credentials_exception

    # Return User model (without password_hash)
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

    Registers a new user with email, password, and preferences.
    Password is hashed using bcrypt before storing.
    Returns JWT access token on success.

    Args:
        user_create: User signup data (email, password, name, level, hardware)

    Returns:
        Token: JWT access token for the new user

    Raises:
        HTTPException: 400 if email already registered

    Example Request:
        POST /api/auth/signup
        {
            "email": "student@example.com",
            "password": "securepass123",
            "name": "Ahmed Khan",
            "programming_level": "beginner",
            "hardware": "none"
        }

    Example Response (201 Created):
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
    """
    # Hash password using bcrypt (12 salt rounds)
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
        # Email already exists in database
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create JWT access token (7-day expiration)
    # JWT spec requires 'sub' to be a string
    access_token = create_access_token(data={"sub": str(user_id)})

    return Token(access_token=access_token)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Authenticate user with email and password.

    Verifies user credentials and returns JWT access token on success.

    Args:
        credentials: User login data (email, password)

    Returns:
        Token: JWT access token for authenticated user

    Raises:
        HTTPException: 401 if email not found or password incorrect

    Example Request:
        POST /api/auth/login
        {
            "email": "student@example.com",
            "password": "securepass123"
        }

    Example Response (200 OK):
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }

    Example Error (401 Unauthorized):
        {
            "detail": "Invalid email or password"
        }
    """
    # Get user by email
    user_data = await DBService.get_user_by_email(credentials.email)

    if user_data is None:
        # User not found - return generic error message for security
        # (don't reveal whether email exists or not)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password against bcrypt hash
    if not verify_password(credentials.password, user_data["password_hash"]):
        # Password incorrect - return same generic error message
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create JWT access token (7-day expiration)
    # JWT spec requires 'sub' to be a string
    access_token = create_access_token(data={"sub": str(user_data["id"])})

    return Token(access_token=access_token)


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user.

    Returns user profile data for the authenticated user.
    Requires valid JWT token in Authorization header.

    Args:
        current_user: Current user from JWT token (injected by dependency)

    Returns:
        User: Current user's profile data

    Raises:
        HTTPException: 401 if token is invalid or missing

    Example Request:
        GET /api/auth/me
        Headers:
            Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response (200 OK):
        {
            "id": 1,
            "email": "student@example.com",
            "name": "Ahmed Khan",
            "programming_level": "beginner",
            "hardware": "none"
        }

    Example Error (401 Unauthorized):
        {
            "detail": "Could not validate credentials"
        }
    """
    return current_user

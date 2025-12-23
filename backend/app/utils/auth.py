"""
Authentication utilities for password hashing and JWT token management.
Uses bcrypt for secure password hashing and python-jose for JWT operations.
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.utils.config import get_settings


# Password hashing context
# Uses bcrypt with 12 salt rounds (>= 10 as per FR-009)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Salt rounds: 12 (higher = more secure but slower)
)


def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Uses bcrypt algorithm with 12 salt rounds for strong security.
    Each call generates a unique salt, so the same password will
    produce different hashes.

    Args:
        password: Plain text password to hash

    Returns:
        str: Hashed password (bcrypt format, ~60 characters)

    Example:
        >>> hashed = hash_password("mypassword123")
        >>> print(len(hashed))  # ~60 characters
        >>> # Each call produces different hash (unique salt)
        >>> hash1 = hash_password("same_password")
        >>> hash2 = hash_password("same_password")
        >>> assert hash1 != hash2  # Different hashes, same password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its bcrypt hash.

    Constant-time comparison to prevent timing attacks.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash from database

    Returns:
        bool: True if password matches hash, False otherwise

    Example:
        >>> hashed = hash_password("correct_password")
        >>> verify_password("correct_password", hashed)
        True
        >>> verify_password("wrong_password", hashed)
        False
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.

    Encodes user data (typically user_id) into a signed JWT token.
    Default expiration: 7 days (from settings).

    Args:
        data: Dictionary to encode in token (e.g., {"sub": user_id})
        expires_delta: Optional custom expiration time. If None, uses default from settings.

    Returns:
        str: Encoded JWT token string

    Token Structure:
        Header: {"alg": "HS256", "typ": "JWT"}
        Payload: {
            "sub": <user_id>,
            "exp": <expiration_timestamp>
        }
        Signature: HMACSHA256(header + payload, secret_key)

    Example:
        >>> token = create_access_token({"sub": 123})
        >>> print(token)
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        >>>
        >>> # Custom expiration (1 hour)
        >>> from datetime import timedelta
        >>> token = create_access_token({"sub": 123}, expires_delta=timedelta(hours=1))
    """
    settings = get_settings()
    to_encode = data.copy()

    # Calculate expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default: 7 days (10080 minutes from settings)
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    # Add expiration to payload
    to_encode.update({"exp": expire})

    # Encode and sign JWT
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.

    Verifies token signature and expiration. Raises JWTError if:
    - Token is expired
    - Token signature is invalid
    - Token format is malformed

    Args:
        token: JWT token string to decode

    Returns:
        dict: Decoded token payload (e.g., {"sub": user_id, "exp": timestamp})

    Raises:
        JWTError: If token is invalid, expired, or malformed

    Example:
        >>> token = create_access_token({"sub": 123})
        >>> payload = decode_access_token(token)
        >>> print(payload["sub"])
        123
        >>>
        >>> # Invalid token
        >>> try:
        ...     decode_access_token("invalid.token.here")
        ... except JWTError as e:
        ...     print("Invalid token!")
    """
    settings = get_settings()

    # Decode and verify JWT
    # Automatically checks:
    # 1. Signature is valid (uses secret_key)
    # 2. Token is not expired (checks "exp" claim)
    # 3. Token format is correct
    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm]
    )

    return payload

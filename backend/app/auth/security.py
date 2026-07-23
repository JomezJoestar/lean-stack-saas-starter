import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Any
from jwt import encode, decode, InvalidTokenError
from app.auth.config import auth_settings

def hash_password(password: str) -> str:
    """Hashes a plain text password using standard bcrypt."""
    # Convert string to bytes, generate salt, hash it, and decode back to string
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares a plain password against a stored hash string."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), 
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False

def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """Generates a secure encoded JWT access token for the user session."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = encode(
        to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM
    )
    return encoded_jwt
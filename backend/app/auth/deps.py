# backend/app/auth/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, InvalidTokenError
from sqlmodel import Session, select

from app.auth.config import auth_settings
from app.database import get_session  # adjust import if needed
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode(
            token, 
            auth_settings.SECRET_KEY, 
            algorithms=[auth_settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    statement = select(User).where(User.id == int(user_id))
    user = db.exec(statement).first()
    
    if user is None:
        raise credentials_exception
        
    return user

def require_premium_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required to access this feature."
        )
    return current_user
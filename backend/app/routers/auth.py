from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_session
from app.models import User, UserCreate, UserRead
from app.auth.security import hash_password, verify_password, create_access_token
from app.auth.deps import get_current_user, require_premium_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, session: Session = Depends(get_session)):
    """Registers a new user, hashes their password, and saves them to the DB."""
    # 1. Check if the user email already exists
    statement = select(User).where(User.email == user_in.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )
    
    # 2. Hash the password and create the database object
    hashed_pwd = hash_password(user_in.password)
    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_pwd
    )
    
    # 3. Save to SQLite
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """Authenticates a user and returns a secure JWT access token."""
    # 1. Look up user by email (OAuth2PasswordRequestForm uses 'username' field for email)
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    # 2. Verify existence and check the password match
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Issue the token
    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# 1. Protected Route: Any logged-in user can check their own profile
@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current logged-in user details.
    Requires a valid JWT Bearer token.
    """
    return current_user


# 2. Premium-Only Route: Only users with is_premium == True can access
@router.get("/pro-feature")
async def get_pro_feature(current_user: User = Depends(require_premium_user)):
    """
    Gated endpoint restricted to active subscribers/buyers.
    """
    return {
        "message": f"Welcome to the VIP lounge, {current_user.email}!",
        "status": "active_subscriber"
    }
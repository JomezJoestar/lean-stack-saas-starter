from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Shared fields for data validation and API payloads."""
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None


class User(UserBase, table=True):
    """The actual database table mapping."""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    
    # Stripe integration tracking fields
    stripe_customer_id: Optional[str] = Field(default=None, index=True)
    is_premium: bool = Field(default=False)
    
    # Audit timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class UserCreate(UserBase):
    """Data model required when a user registers (incoming payload)."""
    password: str


class UserRead(UserBase):
    """Data model returned to the frontend (excludes the password)."""
    id: int
    is_premium: bool
    created_at: datetime
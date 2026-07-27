# backend/app/services/user.py
from sqlmodel import Session, select
from app.models import User

def update_user_subscription_by_email(
    db: Session, 
    email: str, 
    stripe_customer_id: str = None
) -> User | None:
    # Look up user by email
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    
    if user:
        user.is_premium = True
        if stripe_customer_id:
            user.stripe_customer_id = stripe_customer_id
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
        
    return None
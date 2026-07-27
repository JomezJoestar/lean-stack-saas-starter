from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from sqlmodel import Session
from app.database import get_session
from app.services.stripe import StripeService
from app.services.user import update_user_subscription_by_email

router = APIRouter(prefix="/billing", tags=["Billing & Subscriptions"])

@router.post("/checkout")
async def create_checkout(price_id: str, success_url: str, cancel_url: str):
    """
    Endpoint to trigger a Stripe Checkout Session for a user.
    """
    try:
        session = StripeService.create_checkout_session(
            price_id=price_id,
            success_url=success_url,
            cancel_url=cancel_url
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="stripe-signature"),
    db: Session = Depends(get_session)  # <--- Inject DB Session here
):
    if not stripe_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header"
        )

    payload = await request.body()

    try:
        event = StripeService.verify_webhook(payload, stripe_signature)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    event_type = event.type if hasattr(event, "type") else event["type"]

    if event_type == "checkout.session.completed":
        session = event.data.object
        
        customer_details = getattr(session, "customer_details", None)
        customer_email = getattr(customer_details, "email", None) if customer_details else None
        stripe_customer_id = getattr(session, "customer", None)

        if customer_email:
            # Update the user record in the database
            updated_user = update_user_subscription_by_email(
                db=db,
                email=customer_email,
                stripe_customer_id=stripe_customer_id
            )
            
            if updated_user:
                print(f"\n🎉 SUCCESS: Activated premium status in DB for {customer_email}!\n")
            else:
                print(f"\n⚠️ Webhook received for {customer_email}, but user does not exist in DB yet.\n")

    return {"status": "success"}
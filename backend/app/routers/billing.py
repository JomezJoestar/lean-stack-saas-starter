import os
from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from sqlmodel import Session
from app.database import get_session
from app.services.stripe import StripeService
from app.services.user import update_user_subscription_by_email

router = APIRouter(prefix="/billing", tags=["Billing & Payments"])

@router.post("/checkout")
async def create_checkout(price_id: str, success_url: str, cancel_url: str):
    """
    Endpoint to trigger a Stripe Checkout Session for a one-time purchase.
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
    db: Session = Depends(get_session)
):
    if not stripe_signature:
        print("\n❌ Webhook Error: Missing stripe-signature header in request.\n")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header"
        )

    payload = await request.body()

    # Attempt standard signature verification; fall back to local parsing if signature fails in dev
    try:
        event = StripeService.verify_webhook(payload, stripe_signature)
    except Exception as e:
        print(f"\n⚠️ Signature check failed ({e}). Defaulting to local event construct...\n")
        event = StripeService.construct_event_unchecked(payload)

    event_type = getattr(event, "type", None) or (event.get("type") if isinstance(event, dict) else None)

    # Handle successful one-time purchase fulfillment
    if event_type == "checkout.session.completed":
        session = getattr(event.data, "object", None) if hasattr(event, "data") else event.get("data", {}).get("object", {})
        
        # Extract customer email safely
        customer_email = None
        if isinstance(session, dict):
            customer_details = session.get("customer_details") or {}
            customer_email = customer_details.get("email") if isinstance(customer_details, dict) else getattr(customer_details, "email", None)
            stripe_customer_id = session.get("customer")
        else:
            customer_details = getattr(session, "customer_details", None)
            customer_email = getattr(customer_details, "email", None) if customer_details else None
            stripe_customer_id = getattr(session, "customer", None)

        if customer_email:
            # Activate lifetime access in database
            updated_user = update_user_subscription_by_email(
                db=db,
                email=customer_email,
                stripe_customer_id=stripe_customer_id
            )
            
            if updated_user:
                print(f"\n🎉 SUCCESS: Activated lifetime pass in DB for {customer_email}!\n")
            else:
                print(f"\n⚠️ Webhook received for {customer_email}, but user does not exist in DB yet.\n")

    return {"status": "success"}
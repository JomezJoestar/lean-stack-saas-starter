from fastapi import APIRouter, Depends, HTTPException, Header, Request, status
from app.services.stripe import StripeService

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
    stripe_signature: str = Header(None, alias="stripe-signature")
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

    # Handle the event using attribute access or dict conversion
    event_type = event.type if hasattr(event, "type") else event["type"]

    if event_type == "checkout.session.completed":
        session = event.data.object
        
        # Safely extract customer email and status using attribute dot-notation
        customer_details = getattr(session, "customer_details", None)
        customer_email = getattr(customer_details, "email", None) if customer_details else None
        payment_status = getattr(session, "payment_status", None)

        print(f"\n🎉 SUCCESS: Payment received for {customer_email}! Status: {payment_status}\n")
        # TODO: Grant access in your database here!

    return {"status": "success"}
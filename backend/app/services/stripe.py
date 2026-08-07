import stripe
import json
from app.auth.config import auth_settings

# Initialize the Stripe API client with the key loaded by Pydantic
stripe.api_key = auth_settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    def create_checkout_session(
        price_id: str, 
        success_url: str, 
        cancel_url: str, 
        customer_email: str = None,
        client_reference_id: str = None
    ) -> stripe.checkout.Session:
        """
        Creates a Stripe Checkout Session for a one-time purchase (Lifetime Access).
        """
        try:
            session_data = {
                "payment_method_types": ["card"],
                "line_items": [
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                "mode": "payment",  # One-time payment mode
                "success_url": success_url,
                "cancel_url": cancel_url,
            }
            
            if customer_email:
                session_data["customer_email"] = customer_email

            if client_reference_id:
                session_data["client_reference_id"] = client_reference_id
                
            return stripe.checkout.Session.create(**session_data)
        except Exception as e:
            raise RuntimeError(f"Stripe Session Creation Failed: {str(e)}")

    @staticmethod
    def verify_webhook(payload: bytes, sig_header: str) -> stripe.Event:
        """
        Verifies and constructs an incoming Stripe Webhook event using the configured secret.
        """
        return stripe.Webhook.construct_event(
            payload, sig_header, auth_settings.STRIPE_WEBHOOK_SECRET
        )

    @staticmethod
    def construct_event_unchecked(payload: bytes) -> stripe.Event:
        """
        Fallback helper for local testing/CLI triggers without signature verification.
        """
        data = json.loads(payload.decode("utf-8"))
        return stripe.Event.construct_from(data, stripe.api_key)
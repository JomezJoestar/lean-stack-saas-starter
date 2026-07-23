import stripe
from app.auth.config import auth_settings

# Initialize the Stripe API client with the key loaded by Pydantic
stripe.api_key = auth_settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    def create_checkout_session(price_id: str, success_url: str, cancel_url: str, customer_email: str = None) -> stripe.checkout.Session:
        """
        Creates a Stripe Checkout Session for a subscription.
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
                "mode": "payment",
                "success_url": success_url,
                "cancel_url": cancel_url,
            }
            
            if customer_email:
                session_data["customer_email"] = customer_email
                
            return stripe.checkout.Session.create(**session_data)
        except Exception as e:
            raise RuntimeError(f"Stripe Session Creation Failed: {str(e)}")

    @staticmethod
    def verify_webhook(payload: bytes, sig_header: str) -> stripe.Event:
        """
        Verifies and constructs an incoming Stripe Webhook event to ensure it's authentic.
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, auth_settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except stripe.error.SignatureVerificationError as e:
            raise ValueError(f"Invalid Stripe Webhook Signature: {str(e)}")
        except Exception as e:
            raise ValueError(f"Stripe Webhook Parsing Error: {str(e)}")
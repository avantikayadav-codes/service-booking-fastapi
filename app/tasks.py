import time
from app.celery_app import celery_app


@celery_app.task(
    bind=True,
    name="send_booking_email",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 10},
)
def send_booking_email(self, email: str, booking_id: int):
    time.sleep(5)  # yahan baad mein real email logic aayega
    print(f"Booking #{booking_id} confirmation sent to {email}")
    return {"status": "sent", "booking_id": booking_id}
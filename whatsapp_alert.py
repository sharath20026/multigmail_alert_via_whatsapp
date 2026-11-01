from twilio.rest import Client
from config import (
    TWILIO_SID,
    TWILIO_AUTH,
    TWILIO_WHATSAPP_NUMBER,
    RECEIVER_WHATSAPP
)

def send_whatsapp(message):
    client = Client(TWILIO_SID, TWILIO_AUTH)

    client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=RECEIVER_WHATSAPP
    )
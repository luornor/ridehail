from twilio.rest import Client
from decouple import config

# Twilio Configuration
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_whatsapp_message(to_number, message):
    """
    Send a WhatsApp message using Twilio.
    """
    client.messages.create(body=message, from_=WHATSAPP_NUMBER, to=to_number)

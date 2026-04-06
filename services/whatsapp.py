from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_SID")
AUTH_TOKEN = os.getenv("TWILIO_TOKEN")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def enviar_whatsapp(numero, mensaje):
    try:
        client.messages.create(
            from_='whatsapp:+14155238886',
            body=mensaje,
            to=f'whatsapp:{numero}'
        )
        print("Mensaje enviado correctamente")
        return True
    except Exception as e:
        print("Error enviando WhatsApp:", e)
        return False
    
    
    
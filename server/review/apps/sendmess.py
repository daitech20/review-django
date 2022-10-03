from twilio.rest import Client
from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# reading .env file
environ.Env.read_env(os.path.join(BASE_DIR, '../.env'))

# Your Account SID from twilio.com/console
account_sid = env('ACCOUNT_SID')
# Your Auth Token from twilio.com/console
auth_token  = env('AUTH_TOKEN')
from_phone = env('FROM_PHONE')

def send_mess(content, to_phone):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to_phone, 
        from_=from_phone,
        body=content)

    return message.sid
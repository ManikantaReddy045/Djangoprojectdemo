import os

import environ
from django.conf import settings
from twilio.rest import Client


class SendOTP:
    def __init__(self, phone_number, otp):
        self.phone_number = phone_number
        self.otp = otp

    def send_code(self):
        TWILIO_ACCOUNT_SID = "AC800ef3ea990fcfa0987b09c04abe5b40"
        TWILIO_AUTH_TOKEN = "72939caff0c6454d192483ddd3b0625d"
        TWILIO_PHONE_NUMBER = "+19703167611"
        # TWILIO_VERIFY_SERVICE_SID="MG3746a043589bd3cb6171ef751abf83b4"
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print(client, "---------client")
        message = client.messages.create(
            body=f"Your otp is {self.otp}",
            to=self.phone_number,
            from_=TWILIO_PHONE_NUMBER,
        )
        print(message.sid)

from django.core.mail import send_mail
import random 
import os
from twilio.rest import Client
from django.conf import settings
from .models import User


def sendOtp(email, phoneNumber):
    otp = random.randint(1000, 9999)
    send_otp_via_email(email, otp)
    send_sms(otp, phoneNumber)


def send_otp_via_email(email, otp):
    subject = 'Your account verification mail'
    message = f'Your otp is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()
    

account = "ACdd0ad89ad3dc801381b866e2fcf0808b"
token = "c29c59fd1a9c671ccaa0386a340d1946"
client = Client(account, token)


def send_sms(otp, phonenumber):
    
    client.messages.create(to=phonenumber, from_="+18509098696",
                                 body=otp)

    
    
    
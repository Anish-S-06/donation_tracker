from flask_mail import Message
from flask import current_app
from app import mail

def send_email_otp(email, otp):
    msg = Message(
        subject="Your OTP Code",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[email]
    )

    msg.body = f"""
Your OTP is: {otp}

It is valid for 5 minutes.
Do not share this OTP with anyone.
"""

    mail.send(msg)
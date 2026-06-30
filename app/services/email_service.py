from flask_mail import Message
from flask import current_app
from app import mail

def send_email_otp(email, otp):
    # For local testing without SMTP setup, just print the OTP to the terminal
    if not current_app.config.get("MAIL_USERNAME"):
        print(f"\n========== MOCK OTP EMAIL ==========")
        print(f"To: {email}")
        print(f"Your OTP Code is: {otp}")
        print(f"====================================\n")
        return

    try:
        msg = Message(
            subject="Your OTP Code",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[email]
        )
        msg.body = f"Your OTP is: {otp}\n\nIt is valid for 5 minutes.\nDo not share this OTP with anyone."
        
        mail.send(msg)
        print(f"[MAIL SENT] OTP sent to {email}")
    except Exception as e:
        print(f"[MAIL ERROR] Failed to send OTP: {e}")
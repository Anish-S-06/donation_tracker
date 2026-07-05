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
        raise e

def send_request_notification(donor_email, donor_name, receiver_name, resource_title, request_url):
    """Sends an email notification to the donor when their resource is requested."""
    
    if not current_app.config.get("MAIL_USERNAME"):
        print(f"\n========== MOCK NOTIFICATION EMAIL ==========")
        print(f"To: {donor_email}")
        print(f"Subject: 🔔 Someone requested your {resource_title}!")
        print(f"=============================================\n")
        return

    try:
        msg = Message(
            subject=f"🔔 Great News! Someone requested your {resource_title}!",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[donor_email]
        )
        
        # We will use an HTML template for this
        from flask import render_template
        msg.html = render_template('emails/request_notification.html', 
                                   donor_name=donor_name, 
                                   receiver_name=receiver_name, 
                                   resource_title=resource_title,
                                   request_url=request_url)
        
        mail.send(msg)
        print(f"[MAIL SENT] Notification sent to {donor_email}")
    except Exception as e:
        print(f"[MAIL ERROR] Failed to send notification: {e}")
        raise e

def send_request_confirmation(receiver_email, receiver_name, resource_title, request_url):
    """Sends an email confirmation to the requester when they send a request."""
    
    if not current_app.config.get("MAIL_USERNAME"):
        print(f"\n========== MOCK CONFIRMATION EMAIL ==========")
        print(f"To: {receiver_email}")
        print(f"Subject: 📤 Request Sent: {resource_title}")
        print(f"=============================================\n")
        return

    try:
        msg = Message(
            subject=f"📤 Request Sent: {resource_title}",
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[receiver_email]
        )
        
        from flask import render_template
        msg.html = render_template('emails/request_confirmation.html', 
                                   receiver_name=receiver_name, 
                                   resource_title=resource_title,
                                   request_url=request_url)
        
        mail.send(msg)
        print(f"[MAIL SENT] Confirmation sent to {receiver_email}")
    except Exception as e:
        print(f"[MAIL ERROR] Failed to send confirmation: {e}")
        raise e
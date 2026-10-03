import threading
from flask_mail import Message
from flask import current_app, render_template
from app import mail

def _send_async(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print(f"[MAIL SENT] Successfully sent email to {msg.recipients} (Subject: {msg.subject})")
        except Exception as e:
            print(f"[MAIL ERROR] Async delivery failed to {msg.recipients}: {e}")

def _dispatch_email(msg):
    app = current_app._get_current_object()
    thread = threading.Thread(target=_send_async, args=(app, msg))
    thread.daemon = True
    thread.start()

def send_email_otp(email, otp):
    if not current_app.config.get("MAIL_USERNAME"):
        print(f"\n========== MOCK OTP EMAIL ==========")
        print(f"To: {email}")
        print(f"Your OTP Code is: {otp}")
        print(f"====================================\n")
        return

    try:
        sender = ("Seva Sankalp", current_app.config["MAIL_USERNAME"])
        msg = Message(
            subject="Your Seva Sankalp OTP Code",
            sender=sender,
            recipients=[email]
        )
        msg.body = f"Your OTP is: {otp}\n\nIt is valid for 5 minutes.\nDo not share this OTP with anyone.\n\n- Seva Sankalp Team"
        _dispatch_email(msg)
    except Exception as e:
        print(f"[MAIL ERROR] Failed to dispatch OTP email: {e}")

def send_request_notification(donor_email, donor_name, receiver_name, resource_title, request_url):
    """Sends an email notification to the donor when their resource is requested."""
    if not current_app.config.get("MAIL_USERNAME"):
        print(f"\n========== MOCK NOTIFICATION EMAIL ==========")
        print(f"To: {donor_email}")
        print(f"Subject: 🔔 Someone requested your {resource_title}!")
        print(f"=============================================\n")
        return

    try:
        sender = ("Seva Sankalp", current_app.config["MAIL_USERNAME"])
        msg = Message(
            subject=f"🔔 Great News! Someone requested your {resource_title}!",
            sender=sender,
            recipients=[donor_email]
        )
        msg.body = f"Hello {donor_name},\n\nGreat news! {receiver_name} has requested your listed resource '{resource_title}'.\n\nPlease log in to review the request and respond:\n{request_url}\n\n- Seva Sankalp Team"
        msg.html = render_template('emails/request_notification.html', 
                                   donor_name=donor_name, 
                                   receiver_name=receiver_name, 
                                   resource_title=resource_title,
                                   request_url=request_url)
        _dispatch_email(msg)
    except Exception as e:
        print(f"[MAIL ERROR] Failed to dispatch request notification: {e}")

def send_request_confirmation(receiver_email, receiver_name, resource_title, request_url):
    """Sends an email confirmation to the requester when they send a request."""
    if not current_app.config.get("MAIL_USERNAME"):
        print(f"\n========== MOCK CONFIRMATION EMAIL ==========")
        print(f"To: {receiver_email}")
        print(f"Subject: 📤 Request Sent: {resource_title}")
        print(f"=============================================\n")
        return

    try:
        sender = ("Seva Sankalp", current_app.config["MAIL_USERNAME"])
        msg = Message(
            subject=f"📤 Request Sent: {resource_title}",
            sender=sender,
            recipients=[receiver_email]
        )
        msg.body = f"Hello {receiver_name},\n\nYour request for '{resource_title}' has been submitted to the donor.\n\nYou will receive an update once the donor reviews your request.\nTrack your request here: {request_url}\n\n- Seva Sankalp Team"
        msg.html = render_template('emails/request_confirmation.html', 
                                   receiver_name=receiver_name, 
                                   resource_title=resource_title,
                                   request_url=request_url)
        _dispatch_email(msg)
    except Exception as e:
        print(f"[MAIL ERROR] Failed to dispatch request confirmation: {e}")

def send_chat_notification(recipient_email, recipient_name, sender_name, resource_title, message_preview, chat_url):
    """Sends an email notification when a user receives a new in-app chat message."""
    if not current_app.config.get("MAIL_USERNAME"):
        print(f"\n========== MOCK CHAT EMAIL ==========")
        print(f"To: {recipient_email}")
        print(f"New message from {sender_name} on '{resource_title}': {message_preview}")
        print(f"Chat URL: {chat_url}")
        print(f"=====================================\n")
        return

    try:
        sender = ("Seva Sankalp", current_app.config["MAIL_USERNAME"])
        msg = Message(
            subject=f"💬 New message from {sender_name} regarding {resource_title}",
            sender=sender,
            recipients=[recipient_email]
        )
        preview_text = message_preview[:120] + ('...' if len(message_preview) > 120 else '')
        msg.body = f"Hello {recipient_name},\n\nYou have received a new message from {sender_name} regarding '{resource_title}':\n\n\"{preview_text}\"\n\nClick here to view and reply:\n{chat_url}\n\n- Seva Sankalp Team"
        msg.html = render_template('emails/chat_notification.html',
                                   recipient_name=recipient_name,
                                   sender_name=sender_name,
                                   resource_title=resource_title,
                                   message_preview=preview_text,
                                   chat_url=chat_url)
        _dispatch_email(msg)
    except Exception as e:
        print(f"[MAIL ERROR] Failed to dispatch chat notification: {e}")

def send_request_accepted_notification(receiver_email, receiver_name, donor_name, resource_title, chat_url):
    """Sends an email notification to the requester when their request is accepted."""
    if not current_app.config.get("MAIL_USERNAME"):
        print(f"\n========== MOCK ACCEPTED EMAIL ==========")
        print(f"To: {receiver_email}")
        print(f"Request for '{resource_title}' accepted by {donor_name}")
        print(f"Chat URL: {chat_url}")
        print(f"=========================================\n")
        return

    try:
        sender = ("Seva Sankalp", current_app.config["MAIL_USERNAME"])
        msg = Message(
            subject=f"🎉 Request Accepted: {resource_title}",
            sender=sender,
            recipients=[receiver_email]
        )
        msg.body = f"Hello {receiver_name},\n\nGreat news! {donor_name} has accepted your request for '{resource_title}'.\n\nYou can now coordinate handover details via in-app chat:\n{chat_url}\n\n- Seva Sankalp Team"
        msg.html = render_template('emails/request_accepted.html',
                                   receiver_name=receiver_name,
                                   donor_name=donor_name,
                                   resource_title=resource_title,
                                   chat_url=chat_url)
        _dispatch_email(msg)
    except Exception as e:
        print(f"[MAIL ERROR] Failed to dispatch accept notification: {e}")
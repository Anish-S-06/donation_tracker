import random
import time
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import db, mail
from app.models import User
from app.core.decorators import role_required
from app.services.otp_service import generate_otp
from app.services.email_service import send_email_otp
from app.services.otp_store import otp_store

auth_bp = Blueprint('auth_routes', __name__, url_prefix='/auth')

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verification-salt')

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='email-verification-salt',
            max_age=expiration
        )
        return email
    except Exception:
        return False

def send_verification_email(user):
    token = generate_verification_token(user.email)
    verify_url = url_for('auth_routes.verify_email', token=token, _external=True)
    
    # We try sending via Flask-Mail. If it fails or is unconfigured, we mock/print it.
    mail_username = current_app.config.get('MAIL_USERNAME')
    if mail_username:
        try:
            msg = Message(
                "Verify your Email - Donation Tracker",
                recipients=[user.email],
                body=f"Hi {user.email},\n\nPlease click the following link to verify your email address:\n{verify_url}\n\nThank you!"
            )
            mail.send(msg)
            print(f"Verification email sent to {user.email}")
            return
        except Exception as e:
            print(f"Error sending email via Flask-Mail: {e}")
            
    # Mock/Fallback behavior
    print("\n" + "="*50)
    print(f"MOCK EMAIL SENT TO: {user.email}")
    print(f"Verification Link: {verify_url}")
    print("="*50 + "\n")


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('frontend_routes.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # 'donor' or 'receiver'
        phone_number = request.form.get('phone_number')
        
        if not email or not password or not role:
            flash('All fields except phone number are required.', 'danger')
            return redirect(url_for('auth_routes.register'))
            
        if role not in ['donor', 'receiver']:
            flash('Invalid role selected.', 'danger')
            return redirect(url_for('auth_routes.register'))
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered.', 'danger')
            return redirect(url_for('auth_routes.register'))
            

        # Create new user
        new_user = User(
            email=email,
            role=role,
            phone_number=phone_number,
            is_email_verified=False,
            is_phone_verified=False,
            is_verified=False, 
            verification_status='pending',
            is_premium_donor=False,
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        otp = generate_otp()
        
        otp_store[email] = {
           "otp": otp,
           "time": time.time()
        }
        print("MAIL_USERNAME =", current_app.config.get("MAIL_USERNAME"))
        print("MAIL_PASSWORD =", current_app.config.get("MAIL_PASSWORD"))
        send_email_otp(email, otp)

        flash("OTP sent to your email", "success")
        return redirect(url_for('auth_routes.verify_email_otp'))
        
        
    return render_template('register.html')

@auth_bp.route('/verify-email-otp', methods=['GET', 'POST'])
def verify_email_otp():
    if request.method == 'POST':
        email = request.form.get('email')
        user_otp = request.form.get('otp')

        if email not in otp_store:
            flash('OTP not found. Please register again.', 'danger')
            return redirect(url_for('auth_routes.register'))

        stored_otp = otp_store[email]["otp"]
        otp_time = otp_store[email]["time"]

        # OTP expires after 5 minutes
        if time.time() - otp_time > 300:
            otp_store.pop(email, None)
            flash('OTP has expired. Please register again.', 'danger')
            return redirect(url_for('auth_routes.register'))

        if user_otp == stored_otp:
            user = User.query.filter_by(email=email).first()

            if user:
                user.is_email_verified = True
                db.session.commit()

            otp_store.pop(email, None)

            flash('Email verified successfully!', 'success')
            return redirect(url_for('auth_routes.login'))

        flash('Invalid OTP.', 'danger')

    return render_template('verify_email_otp.html')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('frontend_routes.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth_routes.login'))
        # Block banned users
        if user.is_banned:
         flash('Your account has been banned by the administrator.', 'danger')
         return redirect(url_for('auth_routes.login'))

        # Block rejected users
        if user.verification_status == 'rejected':
          flash('Your account verification was rejected.', 'danger')
          return redirect(url_for('auth_routes.login'))

        # Allow only approved users
        if user.role in ['donor', 'receiver'] and user.verification_status != 'approved':
          flash('Your account is pending admin approval.', 'warning')
          return redirect(url_for('auth_routes.login'))
            

            
        login_user(user, remember=remember)
        flash('Logged in successfully!', 'success')
        
        # Check next parameter
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('frontend_routes.index'))
        
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('frontend_routes.index'))

@auth_bp.route('/upgrade-premium', methods=['POST'])
@login_required
@role_required('donor')
def upgrade_premium():
    current_user.is_premium_donor = True
    db.session.commit()
    flash('Congratulations! You have upgraded to a Premium Donor tier.', 'success')
    return redirect(url_for('profile_routes.profile'))

# --- GOOGLE OAUTH PROTOTYPE FLOW ---
@auth_bp.route('/google')
def google_login():
    # If standard Google keys exist, we could do full oauth. 
    # For local prototype simplicity and offline/mock convenience, we provide a quick mock redirect.
    mock_url = url_for('auth_routes.google_callback', mock_state='success', _external=True)
    return redirect(mock_url)

@auth_bp.route('/google/callback')
def google_callback():
    # Simulate receiving standard Google Auth data
    # Create or retrieve a Google Mock user
    email = "google_user@example.com"
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # Create a new user with Google Auth provider simulated
        user = User(
            email=email,
            role='donor',
            is_email_verified=True,
            is_phone_verified=False,
            is_verified=True,  # Automatically verify social login donor for prototype
            is_premium_donor=False
        )
        # Random password hash since they login via Google
        user.set_password(f"google-oauth-pwd-{random.randint(100, 999)}")
        db.session.add(user)
        db.session.commit()
        flash('Registered and logged in with Google!', 'success')
    else:
        flash('Logged in with Google!', 'success')
        
    login_user(user)
    return redirect(url_for('frontend_routes.index'))

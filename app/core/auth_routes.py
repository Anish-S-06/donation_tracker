import random
import time
import os
from werkzeug.utils import secure_filename

from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, request, session, current_app
)

from flask_login import (
    login_user, logout_user, login_required, current_user
)

from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from app import db, mail
from app.models import User
from app.core.decorators import role_required
from app.services.otp_service import generate_otp
from app.services.email_service import send_email_otp
from app.services.otp_store import otp_store


# ======================================================
# Blueprint
# ======================================================
auth_bp = Blueprint('auth_routes', __name__, url_prefix='/auth')


# ======================================================
# TOKEN HELPERS
# ======================================================
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


# ======================================================
# EMAIL VERIFICATION MAIL SENDER
# ======================================================
def send_verification_email(user):
    token = generate_verification_token(user.email)

    verify_url = url_for(
        'auth_routes.verify_email',
        token=token,
        _external=True
    )

    mail_username = current_app.config.get('MAIL_USERNAME')

    if mail_username:
        try:
            msg = Message(
                subject="Verify your Email - Seva Sankalp",
                recipients=[user.email],
                body=f"Click below to verify your email:\n\n{verify_url}"
            )
            mail.send(msg)
            print(f"[MAIL SENT] {user.email}")
            return
        except Exception as e:
            print(f"[MAIL ERROR] {e}")

    print("\n========== MOCK EMAIL ==========")
    print("To:", user.email)
    print("Link:", verify_url)
    print("================================\n")


# ======================================================
# REGISTER
# ======================================================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('frontend_routes.index'))

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        phone_number = request.form.get('phone_number')

        if not email or not password or not role:
            flash("All fields required", "danger")
            return redirect(url_for('auth_routes.register'))

        if role not in ['user', 'ngo']:
            flash("Invalid role", "danger")
            return redirect(url_for('auth_routes.register'))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists", "danger")
            return redirect(url_for('auth_routes.register'))
            
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'documents')
        os.makedirs(upload_folder, exist_ok=True)
        allowed_doc_exts = {'pdf', 'jpg', 'jpeg', 'png'}

        def save_uploaded_doc(file_obj, prefix):
            if not file_obj or file_obj.filename == '':
                return None
            ext = file_obj.filename.rsplit('.', 1)[-1].lower() if '.' in file_obj.filename else ''
            if ext not in allowed_doc_exts:
                return False
            import uuid
            filename = secure_filename(f"{prefix}_{int(time.time())}_{uuid.uuid4().hex[:6]}.{ext}")
            filepath = os.path.join(upload_folder, filename)
            file_obj.save(filepath)
            return f"uploads/documents/{filename}"

        if role == 'ngo':
            darpan_id = request.form.get('darpan_id', '').strip().upper()
            org_pan = request.form.get('org_pan', '').strip().upper()
            ngo_name = request.form.get('ngo_name', '').strip()
            upi_id = request.form.get('upi_id', '').strip()
            ngo_desc = request.form.get('ngo_description', '').strip()

            if not darpan_id or not org_pan or not ngo_name or not upi_id:
                flash("All NGO fields (Name, Darpan ID, PAN, UPI ID) are required.", "danger")
                return redirect(url_for('auth_routes.register'))

            reg_file = request.files.get('ngo_reg_document') or request.files.get('id_document')
            pan_file = request.files.get('pan_card_doc')
            auth_file = request.files.get('auth_letter_doc')

            if not reg_file or reg_file.filename == '':
                flash("NGO Registration Certificate / Trust Deed is required.", "danger")
                return redirect(url_for('auth_routes.register'))
            if not pan_file or pan_file.filename == '':
                flash("Organization PAN Card copy is required.", "danger")
                return redirect(url_for('auth_routes.register'))
            if not auth_file or auth_file.filename == '':
                flash("Representative ID & Authorization Letter is required.", "danger")
                return redirect(url_for('auth_routes.register'))

            reg_doc_path = save_uploaded_doc(reg_file, 'ngo_reg')
            pan_doc_path = save_uploaded_doc(pan_file, 'ngo_pan')
            auth_doc_path = save_uploaded_doc(auth_file, 'ngo_auth')

            if not reg_doc_path or not pan_doc_path or not auth_doc_path:
                flash("Invalid file format. Allowed: PDF, JPG, PNG.", "danger")
                return redirect(url_for('auth_routes.register'))

            session['pending_user'] = {
                'email': email,
                'password': password,
                'role': role,
                'phone_number': phone_number,
                'ngo_name': ngo_name,
                'ngo_description': ngo_desc,
                'upi_id': upi_id,
                'darpan_id': darpan_id,
                'org_pan': org_pan,
                'id_document': reg_doc_path,
                'pan_card_doc': pan_doc_path,
                'auth_letter_doc': auth_doc_path
            }
        else:
            # Handle Community Member DigiLocker e-KYC Verification (No file upload needed)
            digilocker_verified = request.form.get('digilocker_verified') == '1'
            if not digilocker_verified:
                flash("DigiLocker verification is required to verify your identity.", "warning")
                return redirect(url_for('auth_routes.register'))

            doc_type = request.form.get('digilocker_doc_type', 'Aadhaar')
            doc_id = request.form.get('digilocker_doc_id', 'XXXX-XXXX-4819')
            dl_name = request.form.get('digilocker_name', '').strip()

            session['pending_user'] = {
                'email': email,
                'password': password,
                'role': role,
                'phone_number': phone_number,
                'id_document': f"DigiLocker Verified ({doc_type} {doc_id})",
                'digilocker_verified': True,
                'verification_status': 'approved'
            }

        otp = generate_otp()

        otp_store[email] = {
            "otp": otp,
            "time": time.time()
        }

        send_email_otp(email, otp)

        flash("OTP sent to your email", "success")
        return redirect(url_for('auth_routes.verify_email_otp'))

    return render_template('register.html')

# ======================================================
# OTP VERIFICATION
# ======================================================
@auth_bp.route('/verify-email-otp', methods=['GET', 'POST'])
def verify_email_otp():

    pending_user = session.get('pending_user')

    if not pending_user:
        flash("Session expired", "danger")
        return redirect(url_for('auth_routes.register'))

    email = pending_user['email']

    if request.method == 'POST':

        user_otp = request.form.get('otp')

        if email not in otp_store:
            flash("OTP expired", "danger")
            return redirect(url_for('auth_routes.register'))

        stored = otp_store[email]

        if time.time() - stored["time"] > 300:
            otp_store.pop(email, None)
            flash("OTP expired", "danger")
            return redirect(url_for('auth_routes.register'))

        if user_otp == stored["otp"]:
            
            actual_role = pending_user['role']
            is_ngo = False
            
            if actual_role == 'ngo':
                actual_role = 'receiver'
                is_ngo = True

            is_dl_verified = pending_user.get('digilocker_verified', False)
            ver_status = 'approved' if is_dl_verified else 'pending'

            new_user = User(
                email=pending_user['email'],
                role=actual_role,
                phone_number=pending_user['phone_number'],
                is_email_verified=True,
                is_phone_verified=False,
                verification_status=ver_status,
                is_banned=False,
                is_ngo=is_ngo,
                ngo_name=pending_user.get('ngo_name'),
                ngo_description=pending_user.get('ngo_description'),
                upi_id=pending_user.get('upi_id'),
                darpan_id=pending_user.get('darpan_id'),
                org_pan=pending_user.get('org_pan'),
                id_document=pending_user.get('id_document') or ('DigiLocker Verified' if is_dl_verified else None),
                pan_card_doc=pending_user.get('pan_card_doc'),
                auth_letter_doc=pending_user.get('auth_letter_doc')
            )

            new_user.set_password(pending_user['password'])

            db.session.add(new_user)
            db.session.commit()

            otp_store.pop(email, None)
            session.pop('pending_user', None)

            if is_dl_verified:
                flash("Email verified! Your identity was automatically approved via DigiLocker.", "success")
            else:
                flash("Email verified successfully!", "success")
            return redirect(url_for('auth_routes.login'))

        flash("Invalid OTP", "danger")

    return render_template('verify_email_otp.html')

# ======================================================
# EMAIL LINK VERIFICATION
# ======================================================
@auth_bp.route('/verify-email/<token>')
def verify_email(token):

    email = confirm_verification_token(token)

    if not email:
        flash("Invalid or expired link", "danger")
        return redirect(url_for('auth_routes.login'))

    user = User.query.filter_by(email=email).first()

    if user:
        user.is_email_verified = True
        db.session.commit()

    flash("Email verified successfully!", "success")
    return redirect(url_for('auth_routes.login'))


# ======================================================
# RESEND OTP
# ======================================================
@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():

    pending_user = session.get('pending_user')
    if not pending_user:
        flash("Session expired", "danger")
        return redirect(url_for('auth_routes.register'))
        
    email = pending_user.get('email')

    otp = generate_otp()
    otp_store[email] = {"otp": otp, "time": time.time()}

    send_email_otp(email, otp)

    flash("OTP resent successfully", "success")
    return redirect(url_for('auth_routes.verify_email_otp'))


# ======================================================
# LOGIN
# ======================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('frontend_routes.index'))

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(email=email).first()

        # 1. user not found
        if not user or not user.check_password(password):
            flash("Invalid credentials", "danger")
            return redirect(url_for('auth_routes.login'))

        # 2. banned check
        if user.is_banned:
            flash("Your account is banned", "danger")
            return redirect(url_for('auth_routes.login'))

        # 3. EMAIL NOT VERIFIED → send to OTP page (IMPORTANT FIX)
        if not user.is_email_verified:
            flash("Please verify your email OTP", "warning")
            session['email'] = user.email
            return redirect(url_for('auth_routes.verify_email_otp'))

        # 4. ADMIN APPROVAL CHECK (NGOs only)
        if user.is_ngo and user.verification_status != 'approved':
            flash("NGO Account pending admin approval", "warning")
            return redirect(url_for('auth_routes.login'))
        # 5. LOGIN SUCCESS
        user.last_login_ip = request.remote_addr
        db.session.commit()
        
        login_user(user, remember=remember)

        flash("Login successful!", "success")
        if user.role == 'admin':
            return redirect(url_for('admin_routes.dashboard'))
        return redirect(url_for('frontend_routes.index'))

    return render_template('login.html')


# ======================================================
# LOGOUT
# ======================================================
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('frontend_routes.index'))


# ======================================================
# GOOGLE LOGIN (MOCK)
# ======================================================
@auth_bp.route('/google')
def google_login():
    return redirect(url_for('auth_routes.google_callback'))


@auth_bp.route('/google/callback')
def google_callback():

    email = "google_user@example.com"
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            email=email,
            role='donor',
            is_email_verified=True,
            is_phone_verified=False,
            verification_status='approved'
        )

        user.set_password("google-oauth")
        db.session.add(user)
        db.session.commit()

    login_user(user)

    flash("Logged in via Google", "success")
    return redirect(url_for('frontend_routes.index'))
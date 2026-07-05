from datetime import datetime
from app import db

import bcrypt
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email_otp = db.Column(db.String(10), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.Enum('user', 'admin', name='user_roles'), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    is_email_verified = db.Column(db.Boolean, default=False)
    is_phone_verified = db.Column(db.Boolean, default=False)
    verification_status = db.Column(db.Enum('pending', 'approved', 'rejected', name='verification_statuses'), default='pending',nullable=False)
    is_banned = db.Column(db.Boolean,default=False)
    trust_score = db.Column(db.Integer, default=0)
    points_balance = db.Column(db.Integer, default=0)
    badge_level = db.Column(db.Enum('None', 'Bronze', 'Silver', 'Gold', 'Platinum', name='badge_levels'), default='None')
    profile_photo = db.Column(db.String(255), nullable=True)
    id_document = db.Column(db.String(255), nullable=True)
    is_ngo = db.Column(db.Boolean, default=False)
    ngo_name = db.Column(db.String(150), nullable=True)
    ngo_description = db.Column(db.Text, nullable=True)
    ngo_image = db.Column(db.String(255), nullable=True)
    upi_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resources = db.relationship('Resource', backref='donor', lazy=True)
    requests = db.relationship('Request', backref='receiver', lazy=True)
    points_transactions = db.relationship('PointsTransaction', backref='user', lazy=True)
  
    def set_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password_hash = hashed.decode('utf-8')

    def check_password(self, password):
        if not self.password_hash:
            return False
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except Exception:
            return False

    @property
    def is_active(self):
        return True
    def is_approved(self):
        return self.verification_status =='approved'

class Resource(db.Model):
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.Enum('New', 'Like New', 'Good', 'Fair', name='resource_conditions'), nullable=False)
    location_lat = db.Column(db.Float, nullable=True)
    location_lng = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Enum('Available', 'Requested', 'Fulfilled', name='resource_statuses'), default='Available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    requests = db.relationship('Request', backref='resource', lazy=True)

class Request(db.Model):
    __tablename__ = 'requests'
    
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum('Pending', 'Accepted', 'Rejected', 'Fulfilled', name='request_statuses'), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    history = db.relationship('DonationHistory', backref='request', uselist=False, lazy=True)
    messages = db.relationship('Message', backref='request', lazy=True, cascade="all, delete-orphan")

class DonationHistory(db.Model):
    __tablename__ = 'donation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)
    donor_rating = db.Column(db.Integer, nullable=True)  # 1 to 5
    receiver_rating = db.Column(db.Integer, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

class PointsTransaction(db.Model):
    __tablename__ = 'points_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.Enum('Earned', 'Spent', name='transaction_types'), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sender = db.relationship('User', foreign_keys=[sender_id])

class UPIDonationClick(db.Model):
    __tablename__ = 'upi_donation_clicks'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    donor = db.relationship('User', foreign_keys=[donor_id])
    ngo = db.relationship('User', foreign_keys=[ngo_id])

class NGOGalleryImage(db.Model):
    __tablename__ = 'ngo_gallery_images'
    
    id = db.Column(db.Integer, primary_key=True)
    ngo_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    ngo = db.relationship('User', backref=db.backref('gallery_images', lazy=True))

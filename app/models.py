from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('donor', 'receiver', 'admin', name='user_roles'), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    trust_score = db.Column(db.Integer, default=0)
    points_balance = db.Column(db.Integer, default=0)
    badge_level = db.Column(db.Enum('None', 'Bronze', 'Silver', 'Gold', 'Platinum', name='badge_levels'), default='None')
    profile_photo = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    resources = db.relationship('Resource', backref='donor', lazy=True)
    requests = db.relationship('Request', backref='receiver', lazy=True)
    points_transactions = db.relationship('PointsTransaction', backref='user', lazy=True)

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
    status = db.Column(db.Enum('Available', 'Requested', 'Fulfilled', name='resource_statuses'), default='Available')
    is_premium = db.Column(db.Boolean, default=False)
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

from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import current_user
from app import db
from app.models import Resource, User, NGOLike

frontend_bp = Blueprint('frontend_routes', __name__)

@frontend_bp.route('/')
def index():
    # Fetch all resources to display on the prototype homepage
    resources = Resource.query.all()
    
    # Fetch all verified NGOs
    ngos = User.query.filter_by(is_ngo=True, verification_status='approved').all()
    
    # Fetch top 5 donors ordered by points descending
    top_donors = User.query.filter_by(role='user').order_by(User.points_balance.desc()).limit(5).all()
    
    return render_template('index.html', resources=resources, ngos=ngos, top_donors=top_donors)

@frontend_bp.route('/support-ngos')
def support_ngos():
    # Fetch all verified NGOs
    ngos = User.query.filter_by(is_ngo=True, verification_status='approved').all()
    return render_template('support_ngos.html', ngos=ngos)

@frontend_bp.route('/api/ngo/<int:ngo_id>/like', methods=['POST'])
def toggle_ngo_like(ngo_id):
    if not current_user.is_authenticated:
        return jsonify({
            'success': False,
            'requires_login': True,
            'login_url': url_for('auth_routes.login'),
            'message': 'Please sign in to like and support this NGO.'
        }), 401

    ngo = User.query.filter_by(id=ngo_id, is_ngo=True).first_or_404()
    existing_like = NGOLike.query.filter_by(user_id=current_user.id, ngo_id=ngo.id).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        liked = False
        message = f"Removed support from {ngo.ngo_name or 'NGO'}."
    else:
        new_like = NGOLike(user_id=current_user.id, ngo_id=ngo.id)
        db.session.add(new_like)
        db.session.commit()
        liked = True
        message = f"❤️ You supported {ngo.ngo_name or 'this NGO'}!"

    likes_count = NGOLike.query.filter_by(ngo_id=ngo.id).count()
    return jsonify({
        'success': True,
        'liked': liked,
        'likes_count': likes_count,
        'message': message
    })


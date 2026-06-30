from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Resource, Request as DonationRequest, DonationHistory, User

request_bp = Blueprint('request_routes', __name__, url_prefix='/request')

@request_bp.route('/<int:resource_id>/send', methods=['POST'])
@login_required
def send_request(resource_id):
    if current_user.role != 'receiver':
        flash("Only verified receivers can request resources.", "danger")
        return redirect(url_for('search_routes.search_page'))
        
    if current_user.verification_status != 'approved':
        flash("Your account is pending admin approval.", "warning")
        return redirect(url_for('search_routes.search_page'))

    resource = db.session.get(Resource, resource_id)
    if not resource or resource.status != 'Available':
        flash("Resource not available.", "danger")
        return redirect(url_for('search_routes.search_page'))

    req = DonationRequest(resource_id=resource.id, receiver_id=current_user.id, status='Pending')
    db.session.add(req)
    db.session.commit()
    
    flash("Request sent successfully!", "success")
    return redirect(url_for('search_routes.search_page'))

@request_bp.route('/<int:req_id>/accept', methods=['POST'])
@login_required
def accept_request(req_id):
    req = db.session.get(DonationRequest, req_id)
    if not req or req.resource.donor_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for('profile_routes.profile'))
        
    req.status = 'Accepted'
    req.resource.status = 'Requested'
    
    other_reqs = DonationRequest.query.filter_by(resource_id=req.resource_id, status='Pending').all()
    for o_req in other_reqs:
        if o_req.id != req.id:
            o_req.status = 'Rejected'
            
    db.session.commit()
    flash("Request accepted. Please arrange exchange.", "success")
    return redirect(url_for('profile_routes.profile'))

@request_bp.route('/<int:req_id>/reject', methods=['POST'])
@login_required
def reject_request(req_id):
    req = db.session.get(DonationRequest, req_id)
    if not req or req.resource.donor_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for('profile_routes.profile'))
        
    req.status = 'Rejected'
    db.session.commit()
    flash("Request rejected.", "warning")
    return redirect(url_for('profile_routes.profile'))

@request_bp.route('/<int:req_id>/fulfill', methods=['POST'])
@login_required
def fulfill_request(req_id):
    req = db.session.get(DonationRequest, req_id)
    if not req or req.resource.donor_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for('profile_routes.profile'))
        
    req.status = 'Fulfilled'
    req.resource.status = 'Fulfilled'
    
    history = DonationHistory(request_id=req.id)
    db.session.add(history)
    
    db.session.commit()
    flash("Donation fulfilled! You can now rate the receiver.", "success")
    return redirect(url_for('profile_routes.profile'))

@request_bp.route('/history/<int:history_id>/rate', methods=['POST'])
@login_required
def rate_exchange(history_id):
    history = db.session.get(DonationHistory, history_id)
    if not history:
        flash("Invalid history record.", "danger")
        return redirect(url_for('profile_routes.profile'))
        
    rating = request.form.get('rating', type=int)
    if not rating or rating < 1 or rating > 5:
        flash("Invalid rating.", "danger")
        return redirect(url_for('profile_routes.profile'))
        
    donor_id = history.request.resource.donor_id
    receiver_id = history.request.receiver_id
    
    if current_user.id == donor_id:
        history.receiver_rating = rating
        receiver = db.session.get(User, receiver_id)
        receiver.trust_score += rating
    elif current_user.id == receiver_id:
        history.donor_rating = rating
        donor = db.session.get(User, donor_id)
        donor.trust_score += rating
    else:
        flash("Unauthorized.", "danger")
        return redirect(url_for('profile_routes.profile'))
        
    db.session.commit()
    flash(f"Rated {rating} stars successfully!", "success")
    return redirect(url_for('profile_routes.profile'))

@request_bp.route('/<int:req_id>/messages', methods=['GET'])
@login_required
def get_messages(req_id):
    req = db.session.get(DonationRequest, req_id)
    if not req:
        return jsonify({'error': 'Request not found'}), 404
        
    if current_user.id not in [req.receiver_id, req.resource.donor_id] and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
        
    if req.status not in ['Accepted', 'Fulfilled']:
        return jsonify({'error': 'Chat not available for this request status'}), 403
        
    from app.models import Message
    messages = Message.query.filter_by(request_id=req_id).order_by(Message.created_at.asc()).all()
    
    result = [{
        'id': m.id,
        'sender_id': m.sender_id,
        'content': m.content,
        'created_at': m.created_at.isoformat(),
        'is_me': m.sender_id == current_user.id
    } for m in messages]
    
    return jsonify(result), 200

@request_bp.route('/<int:req_id>/messages', methods=['POST'])
@login_required
def send_message(req_id):
    req = db.session.get(DonationRequest, req_id)
    if not req:
        return jsonify({'error': 'Request not found'}), 404
        
    if current_user.id not in [req.receiver_id, req.resource.donor_id]:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if req.status not in ['Accepted', 'Fulfilled']:
        return jsonify({'error': 'Chat not available for this request status'}), 403
        
    data = request.json
    if not data or not data.get('content'):
        return jsonify({'error': 'Message content required'}), 400
        
    from app.models import Message
    new_msg = Message(
        request_id=req.id,
        sender_id=current_user.id,
        content=data['content']
    )
    db.session.add(new_msg)
    db.session.commit()
    
    return jsonify({'message': 'Sent', 'id': new_msg.id}), 201

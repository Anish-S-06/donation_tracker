from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Resource, Request as DonationRequest, DonationHistory, User, PointsTransaction
from app.services.email_service import send_request_notification, send_request_confirmation

request_bp = Blueprint('request_routes', __name__, url_prefix='/request')

@request_bp.route('/<int:resource_id>/send', methods=['POST'])
@login_required
def send_request(resource_id):
    from datetime import datetime, timedelta

    back_url = request.referrer or url_for('search_routes.search_page')

    if current_user.is_ngo:
        flash("NGOs cannot request resources.", "danger")
        return redirect(back_url)
        
    if current_user.verification_status != 'approved':
        flash("Your account is pending admin approval.", "warning")
        return redirect(back_url)
        
    pending_impact = DonationHistory.query.join(DonationRequest).filter(
        DonationRequest.receiver_id == current_user.id,
        DonationHistory.receipt_photo == None
    ).first()
    
    if pending_impact:
        flash("You must upload Impact Proof (receipt photo) for your previously fulfilled requests before requesting new items.", "danger")
        return redirect(url_for('profile_routes.profile'))

    resource = db.session.get(Resource, resource_id)
    if not resource or resource.status != 'Available':
        flash("Resource not available.", "danger")
        return redirect(back_url)

    if resource.donor_id == current_user.id:
        flash("You cannot request your own listed resource.", "warning")
        return redirect(back_url)

    # Prevent duplicate active requests for the exact same resource
    already_requested = DonationRequest.query.filter_by(
        resource_id=resource.id,
        receiver_id=current_user.id
    ).filter(DonationRequest.status.in_(['Pending', 'Accepted'])).first()
    if already_requested:
        flash("You already have an active request for this item.", "info")
        return redirect(back_url)

    # Anti-Hoarding: Maximum 3 active pending requests across all items
    pending_count = DonationRequest.query.filter_by(receiver_id=current_user.id, status='Pending').count()
    if pending_count >= 3:
        flash("🛡️ Anti-Hoarding Cap: You currently have 3 pending requests awaiting donor decisions. Please wait for donors to review those before requesting more items.", "warning")
        return redirect(back_url)

    # Low-Income Gate for High-Value / Donor-Restricted Items
    if resource.requires_income_proof:
        if current_user.income_verification_status != 'approved':
            if current_user.income_verification_status == 'pending':
                flash("🛡️ Income Verification Pending: The donor has restricted this high-value resource to verified low-income individuals. Your submitted Income Certificate is currently under Admin review.", "warning")
            elif current_user.income_verification_status == 'rejected':
                flash("🛡️ Income Verification Required: Your previously submitted income document was rejected. Please upload valid proof in your Profile to request this item.", "danger")
            else:
                flash("🛡️ Low-Income Verification Required: The donor has restricted this high-value item exclusively to verified low-income beneficiaries (EWS / BPL). Please upload your Income Certificate in your Profile to get verified.", "warning")
            return redirect(url_for('profile_routes.profile'))

    # Anti-Flipping Rule 1: Electronics / High-Value Devices (Max 1 every 12 months)
    if resource.category == 'Electronics':
        # Check active requests for Electronics
        active_elec = DonationRequest.query.join(Resource).filter(
            DonationRequest.receiver_id == current_user.id,
            DonationRequest.status.in_(['Pending', 'Accepted']),
            Resource.category == 'Electronics'
        ).first()
        if active_elec:
            flash(f"🛡️ Category Lock: You already have an active request for an Electronics item ('{active_elec.resource.title}'). Community members can only request one electronic device at a time.", "warning")
            return redirect(back_url)

        # Check 12-month cooldown on fulfilled Electronics
        one_year_ago = datetime.utcnow() - timedelta(days=365)
        fulfilled_elec = DonationRequest.query.join(Resource).filter(
            DonationRequest.receiver_id == current_user.id,
            DonationRequest.status == 'Fulfilled',
            Resource.category == 'Electronics',
            DonationRequest.updated_at >= one_year_ago
        ).order_by(DonationRequest.updated_at.desc()).first()

        if fulfilled_elec:
            days_passed = (datetime.utcnow() - fulfilled_elec.updated_at).days
            days_left = max(1, 365 - days_passed)
            flash(f"🛡️ Anti-Flipping Cooldown Active: You received an Electronics device ('{fulfilled_elec.resource.title}') on {fulfilled_elec.updated_at.strftime('%d %b %Y')}. To prevent commercial resale and guarantee community fairness, Electronics are limited to 1 item per 12 months. Cooldown unlocks in {days_left} days.", "warning")
            return redirect(back_url)

    # Anti-Flipping Rule 2: Household Items & Major Appliances (Max 1 every 6 months)
    if resource.category == 'Household':
        # Check active requests for Household
        active_house = DonationRequest.query.join(Resource).filter(
            DonationRequest.receiver_id == current_user.id,
            DonationRequest.status.in_(['Pending', 'Accepted']),
            Resource.category == 'Household'
        ).first()
        if active_house:
            flash(f"🛡️ Category Lock: You already have an active request for a Household item ('{active_house.resource.title}'). Please wait until that request concludes.", "warning")
            return redirect(back_url)

        # Check 6-month cooldown on fulfilled Household items
        six_months_ago = datetime.utcnow() - timedelta(days=180)
        fulfilled_house = DonationRequest.query.join(Resource).filter(
            DonationRequest.receiver_id == current_user.id,
            DonationRequest.status == 'Fulfilled',
            Resource.category == 'Household',
            DonationRequest.updated_at >= six_months_ago
        ).order_by(DonationRequest.updated_at.desc()).first()

        if fulfilled_house:
            days_passed = (datetime.utcnow() - fulfilled_house.updated_at).days
            days_left = max(1, 180 - days_passed)
            flash(f"🛡️ Anti-Flipping Cooldown Active: You received a Household item ('{fulfilled_house.resource.title}') on {fulfilled_house.updated_at.strftime('%d %b %Y')}. Household items are limited to 1 per 6 months. Cooldown unlocks in {days_left} days.", "warning")
            return redirect(back_url)

    req = DonationRequest(resource_id=resource.id, receiver_id=current_user.id, status='Pending')
    db.session.add(req)
    db.session.commit()
    
    try:
        donor = resource.donor
        request_url = url_for('profile_routes.profile', _external=True)
        send_request_notification(
            donor_email=donor.email,
            donor_name=donor.email.split('@')[0],
            receiver_name=current_user.email.split('@')[0],
            resource_title=resource.title,
            request_url=request_url
        )
        send_request_confirmation(
            receiver_email=current_user.email,
            receiver_name=current_user.email.split('@')[0],
            resource_title=resource.title,
            request_url=request_url
        )
    except Exception as e:
        print(f"Background email failed: {e}")
        flash(f"Request saved, but emails failed to send: {e}", "warning")
        return redirect(url_for('search_routes.search_page'))
    
    flash("Request sent successfully and emails delivered!", "success")
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
    
    # We no longer auto-reject other pending requests here.
    # They stay pending so they can be accepted later if this transaction fails.
            
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
@request_bp.route('/<int:req_id>/unfulfill', methods=['POST'])
@login_required
def unfulfill_request(req_id):
    req = db.session.get(DonationRequest, req_id)
    if not req or req.resource.donor_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for('profile_routes.profile'))
        
    req.status = 'Rejected'
    req.resource.status = 'Available'
    
    db.session.commit()
    flash("Request unfulfilled. Resource is available for other users again.", "info")
    return redirect(url_for('profile_routes.profile'))

@request_bp.route('/<int:req_id>/fulfill', methods=['POST'])
@login_required
def fulfill_request(req_id):
    from datetime import datetime, timedelta
    req = db.session.get(DonationRequest, req_id)
    if not req or req.resource.donor_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for('profile_routes.profile'))
        
    req.status = 'Fulfilled'
    req.resource.status = 'Fulfilled'
    
    history = DonationHistory(request_id=req.id)
    db.session.add(history)
    
    # --- Karma Points Logic (With Anti-Fraud) ---
    points_awarded = 50
    fraud_warning = None
    
    # Anti-Fraud 1: IP Address Check
    receiver = req.receiver
    if current_user.last_login_ip and receiver.last_login_ip and current_user.last_login_ip == receiver.last_login_ip:
        if current_user.last_login_ip != '127.0.0.1': # Allow local testing
            points_awarded = 0
            fraud_warning = "Points cannot be awarded for transactions between users on the same network."

    # Anti-Fraud 2: Weekly Point Cap Check (Max 300 per 7 days)
    if points_awarded > 0:
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_transactions = PointsTransaction.query.filter(
            PointsTransaction.user_id == current_user.id,
            PointsTransaction.created_at >= seven_days_ago
        ).all()
        recent_points = sum(t.amount for t in recent_transactions)
        
        if recent_points + points_awarded > 300:
            points_awarded = 0
            fraud_warning = "You have reached your weekly maximum Karma Points cap (300 points)."

    if points_awarded > 0:
        pt = PointsTransaction(
            user_id=current_user.id,
            amount=points_awarded,
            transaction_type='Earned',
            description=f"Fulfilled request for {req.resource.title}"
        )
        db.session.add(pt)
        current_user.points_balance += points_awarded
    
    # Calculate new badge level
    if current_user.points_balance >= 5000:
        current_user.badge_level = 'Platinum'
    elif current_user.points_balance >= 1000:
        current_user.badge_level = 'Gold'
    elif current_user.points_balance >= 500:
        current_user.badge_level = 'Silver'
    elif current_user.points_balance >= 100:
        current_user.badge_level = 'Bronze'
    
    db.session.commit()
    
    if fraud_warning:
        flash(f"Donation fulfilled! Note: {fraud_warning}", "warning")
    else:
        flash(f"Donation fulfilled! You earned {points_awarded} Karma Points. You can now rate the receiver.", "success")
        
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
        'sender_name': m.sender.email.split('@')[0],
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

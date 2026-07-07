import os
import csv
from io import StringIO
from flask import jsonify, Response, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image
from . import history_bp
from app.models import DonationHistory, Request
from app import db

@history_bp.route('/user/<int:user_id>', methods=['GET'])
def get_history(user_id):
    # Get history where the user is either the donor or receiver
    # We join with the Request table to find the users involved
    histories = DonationHistory.query.join(Request).filter(
        (Request.receiver_id == user_id) | (Request.resource.has(donor_id=user_id))
    ).all()
    
    result = []
    for h in histories:
        result.append({
            'id': h.id,
            'request_id': h.request_id,
            'completed_at': h.completed_at,
            'donor_rating': h.donor_rating,
            'receiver_rating': h.receiver_rating,
            'resource_title': h.request.resource.title
        })
    return jsonify(result), 200

@history_bp.route('/export', methods=['GET'])
def export_csv():
    # Export all history as CSV
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['History ID', 'Request ID', 'Resource Title', 'Donor ID', 'Receiver ID', 'Completed At', 'Donor Rating', 'Receiver Rating'])
    
    records = DonationHistory.query.join(Request).all()
    for r in records:
        cw.writerow([
            r.id,
            r.request_id,
            r.request.resource.title,
            r.request.resource.donor_id,
            r.request.receiver_id,
            r.completed_at,
            r.donor_rating,
            r.receiver_rating
        ])
        
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=donation_history.csv"}
    )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@history_bp.route('/impact/<int:history_id>', methods=['POST'])
@login_required
def upload_impact(history_id):
    history = db.session.get(DonationHistory, history_id)
    if not history or history.request.receiver_id != current_user.id:
        flash('Unauthorized or invalid request.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    receipt_file = request.files.get('receipt_photo')
    usage_file = request.files.get('usage_photo')
    message = request.form.get('impact_message', '')
    
    if not receipt_file or receipt_file.filename == '':
        flash('Receipt photo is required.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'impact_photos')
    os.makedirs(upload_folder, exist_ok=True)
    
    try:
        if receipt_file and allowed_file(receipt_file.filename):
            ext = receipt_file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"receipt_{history.id}.{ext}")
            filepath = os.path.join(upload_folder, filename)
            
            img = Image.open(receipt_file)
            img.thumbnail((800, 800))
            img.save(filepath, optimize=True)
            history.receipt_photo = f"uploads/impact_photos/{filename}"
            
        if usage_file and usage_file.filename != '' and allowed_file(usage_file.filename):
            ext = usage_file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"usage_{history.id}.{ext}")
            filepath = os.path.join(upload_folder, filename)
            
            img = Image.open(usage_file)
            img.thumbnail((800, 800))
            img.save(filepath, optimize=True)
            history.usage_photo = f"uploads/impact_photos/{filename}"
            
        history.impact_message = message
        db.session.commit()
        flash('Impact details uploaded successfully! Thank you.', 'success')
    except Exception as e:
        flash(f'Error uploading photos: {str(e)}', 'danger')
        
    return redirect(url_for('profile_routes.profile'))

import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image
from app import db
from app.models import User

profile_bp = Blueprint('profile_routes', __name__, url_prefix='/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/')
@login_required
def profile():
    from app.models import Request as DonationRequest, Resource
    incoming_requests = []
    outgoing_requests = []
    resources = []
    
    if current_user.role == 'donor':
        resources = Resource.query.filter_by(donor_id=current_user.id).all()
        resource_ids = [r.id for r in resources]
        if resource_ids:
            incoming_requests = DonationRequest.query.filter(DonationRequest.resource_id.in_(resource_ids)).all()
    elif current_user.role == 'receiver':
        outgoing_requests = DonationRequest.query.filter_by(receiver_id=current_user.id).all()
        
    return render_template('profile.html', incoming_requests=incoming_requests, outgoing_requests=outgoing_requests, resources=resources)

@profile_bp.route('/upload-photo', methods=['POST'])
@login_required
def upload_photo():
    if 'profile_photo' not in request.files:
        flash('No file part in the request.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    file = request.files['profile_photo']
    if file.filename == '':
        flash('No selected file.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    if file and allowed_file(file.filename):
        # Ensure uploads folder exists
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'profile_photos')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file with unique secure name
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"user_{current_user.id}.{ext}")
        filepath = os.path.join(upload_folder, filename)
        
        try:
            # Compress and resize using Pillow
            image = Image.open(file)
            image.thumbnail((300, 300))
            
            # Save compressed image
            # If PNG, convert to RGB for JPG format or save as PNG with optimization
            if ext in ['jpg', 'jpeg']:
                image.save(filepath, 'JPEG', optimize=True, quality=85)
            else:
                image.save(filepath, optimize=True)
                
            # Update user profile path in db
            current_user.profile_photo = f"uploads/profile_photos/{filename}"
            db.session.commit()
            
            flash('Profile photo uploaded and updated successfully!', 'success')
        except Exception as e:
            flash(f'Failed to process profile photo: {e}', 'danger')
            
        return redirect(url_for('profile_routes.profile'))
        
    flash('Allowed image types are png, jpg, jpeg, gif.', 'danger')
    return redirect(url_for('profile_routes.profile'))

@profile_bp.route('/upload-document', methods=['POST'])
@login_required
def upload_document():
    if 'id_document' not in request.files:
        flash('No file part.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    file = request.files['id_document']
    if file.filename == '':
        flash('No selected file.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    allowed_doc_exts = ALLOWED_EXTENSIONS.union({'pdf'})
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    
    if file and ext in allowed_doc_exts:
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'documents')
        os.makedirs(upload_folder, exist_ok=True)
        
        filename = secure_filename(f"doc_{current_user.id}_{file.filename}")
        filepath = os.path.join(upload_folder, filename)
        
        try:
            file.save(filepath)
            current_user.id_document = f"uploads/documents/{filename}"
            db.session.commit()
            flash('ID Document uploaded successfully. Awaiting admin review.', 'success')
        except Exception as e:
            flash(f'Failed to upload document: {e}', 'danger')
            
    else:
        flash('Invalid file type. Allowed: PDF, JPG, PNG.', 'danger')
        
    return redirect(url_for('profile_routes.profile'))

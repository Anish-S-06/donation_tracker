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
    return render_template('profile.html')

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

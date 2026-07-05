import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image
from PIL import Image
from app import db
from app.models import User, Request as DonationRequest, Resource, UPIDonationClick, NGOGalleryImage

profile_bp = Blueprint('profile_routes', __name__, url_prefix='/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/')
@profile_bp.route('/')
@login_required
def profile():
    incoming_requests = []
    outgoing_requests = []
    resources = []
    upi_clicks = []
    gallery_images = []
    
    # Fetch both given and requested items for all community members
    if current_user.role == 'user':
        resources = Resource.query.filter_by(donor_id=current_user.id).all()
        resource_ids = [r.id for r in resources]
        if resource_ids:
            incoming_requests = DonationRequest.query.filter(DonationRequest.resource_id.in_(resource_ids)).order_by(DonationRequest.created_at.desc()).all()
            
        outgoing_requests = DonationRequest.query.filter_by(receiver_id=current_user.id).order_by(DonationRequest.created_at.desc()).all()

    if current_user.is_ngo:
        upi_clicks = UPIDonationClick.query.filter_by(ngo_id=current_user.id).order_by(UPIDonationClick.timestamp.desc()).limit(50).all()
        gallery_images = NGOGalleryImage.query.filter_by(ngo_id=current_user.id).order_by(NGOGalleryImage.uploaded_at.desc()).all()
        
    return render_template('profile.html', incoming_requests=incoming_requests, outgoing_requests=outgoing_requests, resources=resources, upi_clicks=upi_clicks, gallery_images=gallery_images)

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

@profile_bp.route('/upload-ngo-photo', methods=['POST'])
@login_required
def upload_ngo_photo():
    if not current_user.is_ngo:
        flash('Only NGOs can upload a display photo.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    if 'ngo_photo' not in request.files:
        flash('No file part in the request.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    file = request.files['ngo_photo']
    if file.filename == '':
        flash('No selected file.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    if file and allowed_file(file.filename):
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'ngo_photos')
        os.makedirs(upload_folder, exist_ok=True)
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"ngo_{current_user.id}.{ext}")
        filepath = os.path.join(upload_folder, filename)
        
        try:
            image = Image.open(file)
            image.thumbnail((400, 400))
            
            if ext in ['jpg', 'jpeg']:
                image.save(filepath, 'JPEG', optimize=True, quality=85)
            else:
                image.save(filepath, optimize=True)
                
            current_user.ngo_image = f"uploads/ngo_photos/{filename}"
            db.session.commit()
            
            flash('NGO display photo uploaded successfully!', 'success')
        except Exception as e:
            flash(f'Failed to process NGO photo: {e}', 'danger')
            
        return redirect(url_for('profile_routes.profile'))
        
    flash('Allowed image types are png, jpg, jpeg, gif.', 'danger')
    return redirect(url_for('profile_routes.profile'))

@profile_bp.route('/upload-ngo-gallery', methods=['POST'])
@login_required
def upload_ngo_gallery():
    if not current_user.is_ngo:
        flash('Only NGOs can upload gallery images.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    if 'gallery_images' not in request.files:
        flash('No file part in the request.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    files = request.files.getlist('gallery_images')
    if not files or files[0].filename == '':
        flash('No selected file.', 'danger')
        return redirect(url_for('profile_routes.profile'))
        
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'ngo_gallery')
    os.makedirs(upload_folder, exist_ok=True)
    
    success_count = 0
    import time
    for file in files:
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = secure_filename(f"gallery_{current_user.id}_{int(time.time() * 1000)}.{ext}")
            filepath = os.path.join(upload_folder, filename)
            
            try:
                image = Image.open(file)
                image.thumbnail((800, 800))
                
                if ext in ['jpg', 'jpeg']:
                    image.save(filepath, 'JPEG', optimize=True, quality=85)
                else:
                    image.save(filepath, optimize=True)
                    
                new_image = NGOGalleryImage(
                    ngo_id=current_user.id,
                    image_path=f"uploads/ngo_gallery/{filename}"
                )
                db.session.add(new_image)
                success_count += 1
                # Small sleep to ensure unique timestamps
                time.sleep(0.01)
            except Exception as e:
                pass
                
    if success_count > 0:
        db.session.commit()
        flash(f'Successfully uploaded {success_count} gallery image(s)!', 'success')
    else:
        flash('Failed to process any images. Please check file types.', 'danger')
        
    return redirect(url_for('profile_routes.profile'))

@profile_bp.route('/api/track-upi-click/<int:ngo_id>', methods=['POST'])
def track_upi_click(ngo_id):
    if not current_user.is_authenticated:
        return jsonify({'status': 'ignored', 'reason': 'unauthenticated'}), 200
        
    ngo = db.session.get(User, ngo_id)
    if not ngo or not ngo.is_ngo:
        return jsonify({'status': 'error', 'reason': 'NGO not found'}), 404
        
    click = UPIDonationClick(donor_id=current_user.id, ngo_id=ngo.id)
    db.session.add(click)
    db.session.commit()
    
    return jsonify({'status': 'success'}), 200



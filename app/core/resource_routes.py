from flask import jsonify, request, current_app, render_template
from flask_login import current_user, login_required
from . import resource_bp
from app.models import Resource, User, Request as DonationRequest
from app import db
import os
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resource_bp.route('/', methods=['GET'])
def get_resources():
    # Fetch all resources, optionally filter by status or category
    status = request.args.get('status')
    category = request.args.get('category')
    
    query = Resource.query
    if status:
        query = query.filter_by(status=status)
    if category:
        query = query.filter_by(category=category)
        
    resources = query.all()
    result = [{
        'id': r.id,
        'title': r.title,
        'description': r.description,
        'category': r.category,
        'condition': r.condition,
        'status': r.status,
        'donor_id': r.donor_id
    } for r in resources]
    return jsonify(result), 200

@resource_bp.route('/', methods=['POST'])
def create_resource():
    if request.is_json:
        data = request.json
    else:
        data = request.form

    if not current_user.is_authenticated:
        return jsonify({'error': 'Login required'}), 401

    donor = db.session.get(User, current_user.id)

    if not donor:
        return jsonify({'error': 'Donor not found'}), 404

    if donor.is_ngo:
        return jsonify({'error': 'NGOs cannot post resources'}), 403

    if not donor.is_email_verified:
        return jsonify({'error': 'Email not verified'}), 403

    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'resources')
            os.makedirs(upload_folder, exist_ok=True)
            
            ext = file.filename.rsplit('.', 1)[1].lower()
            import time
            filename = secure_filename(f"res_{donor.id}_{int(time.time())}.{ext}")
            filepath = os.path.join(upload_folder, filename)
            
            try:
                image = Image.open(file)
                # Ensure RGBA is converted to RGB if saving as JPEG
                if image.mode in ('RGBA', 'P') and ext in ['jpg', 'jpeg']:
                    image = image.convert('RGB')
                image.thumbnail((800, 800))
                
                if ext in ['jpg', 'jpeg']:
                    image.save(filepath, 'JPEG', optimize=True, quality=80)
                else:
                    image.save(filepath, optimize=True)
                    
                image_path = f"uploads/resources/{filename}"
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500

    new_resource = Resource(
        donor_id=donor.id,
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        condition=data.get('condition'),
        address=data.get('address'),
        location_lat=data.get('location_lat'),
        location_lng=data.get('location_lng'),
        image=image_path
    )

    db.session.add(new_resource)
    db.session.commit()

    return jsonify({'message': 'Resource created'}), 201
@resource_bp.route('/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    return jsonify({
        'id': resource.id,
        'title': resource.title,
        'description': resource.description,
        'category': resource.category,
        'condition': resource.condition,
        'location_lat': resource.location_lat,
        'location_lng': resource.location_lng,
        'address': resource.address,
        'status': resource.status,
        'donor_id': resource.donor_id
    }), 200

@resource_bp.route('/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'title' in data:
        resource.title = data['title']
    if 'description' in data:
        resource.description = data['description']
    if 'category' in data:
        resource.category = data['category']
    if 'condition' in data:
        resource.condition = data['condition']
    if 'status' in data:
        resource.status = data['status']
    if 'location_lat' in data:
        resource.location_lat = data['location_lat']
    if 'location_lng' in data:
        resource.location_lng = data['location_lng']
    if 'address' in data:
        resource.address = data['address']
        
    db.session.commit()
    return jsonify({'message': f'Resource {resource_id} updated successfully'}), 200

@resource_bp.route('/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    if not current_user.is_authenticated:
        return jsonify({'error': 'Login required'}), 401
        
    resource = Resource.query.get_or_404(resource_id)
    
    if current_user.id != resource.donor_id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
        
    from app.models import Request as DonationRequest, DonationHistory
    # Delete histories of requests first
    reqs = DonationRequest.query.filter_by(resource_id=resource_id).all()
    for req in reqs:
        DonationHistory.query.filter_by(request_id=req.id).delete()
    
    # Delete requests
    DonationRequest.query.filter_by(resource_id=resource_id).delete()
    
    db.session.delete(resource)
    db.session.commit()
    return jsonify({'message': f'Resource {resource_id} deleted successfully'}), 200

@resource_bp.route('/my_resources', methods=['GET'])
@login_required
def my_resources():
    incoming_requests = []
    outgoing_requests = []
    resources = []
    
    if current_user.role == 'user':
        resources = Resource.query.filter_by(donor_id=current_user.id).all()
        resource_ids = [r.id for r in resources]
        if resource_ids:
            incoming_requests = DonationRequest.query.filter(DonationRequest.resource_id.in_(resource_ids)).order_by(DonationRequest.created_at.desc()).all()
            
        outgoing_requests = DonationRequest.query.filter_by(receiver_id=current_user.id).order_by(DonationRequest.created_at.desc()).all()

    return render_template('my_resources.html', resources=resources, incoming_requests=incoming_requests, outgoing_requests=outgoing_requests)

from flask import jsonify, request, current_app
from flask_login import current_user
from . import resource_bp
from app.models import Resource, User
from app import db

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
@resource_bp.route('/', methods=['POST'])
def create_resource():
    data = request.json

    if not current_user.is_authenticated:
        return jsonify({'error': 'Login required'}), 401

    donor = db.session.get(User, current_user.id)

    if not donor:
        return jsonify({'error': 'Donor not found'}), 404

    if donor.role != 'donor':
        return jsonify({'error': 'Only donors allowed'}), 403

    if not donor.is_email_verified:
        return jsonify({'error': 'Email not verified'}), 403

    new_resource = Resource(
        donor_id=donor.id,
        title=data['title'],
        description=data['description'],
        category=data['category'],
        condition=data['condition'],
        address=data.get('address'),
        location_lat=data.get('location_lat'),
        location_lng=data.get('location_lng')
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

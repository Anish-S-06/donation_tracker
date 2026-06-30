import math
from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required
from app.models import Resource

search_bp = Blueprint('search_routes', __name__, url_prefix='/search')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@search_bp.route('/', methods=['GET'])
@login_required
def search_page():
    return render_template('search.html')

@search_bp.route('/api/resources', methods=['GET'])
@login_required
def api_resources():
    category = request.args.get('category')
    condition = request.args.get('condition')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radius = request.args.get('radius', type=float)
    
    query = Resource.query.filter_by(status='Available')
    
    if category:
        query = query.filter(Resource.category == category)
    if condition:
        query = query.filter(Resource.condition == condition)
        
    resources = query.all()
    
    results = []
    for r in resources:
        distance = None
        if lat is not None and lng is not None and r.location_lat is not None and r.location_lng is not None:
            distance = haversine(lat, lng, r.location_lat, r.location_lng)
            if radius and distance > radius:
                continue
                
        results.append({
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'category': r.category,
            'condition': r.condition,
            'lat': r.location_lat,
            'lng': r.location_lng,
            'distance_km': round(distance, 2) if distance is not None else None,
            'donor_id': r.donor_id
        })
        
    return jsonify(results)

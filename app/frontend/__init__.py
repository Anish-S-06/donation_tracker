from flask import Blueprint, render_template
from app.models import Resource

frontend_bp = Blueprint('frontend_routes', __name__)

@frontend_bp.route('/')
def index():
    # Fetch all resources to display on the prototype homepage
    resources = Resource.query.all()
    return render_template('index.html', resources=resources)

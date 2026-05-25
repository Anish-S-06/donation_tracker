from flask import Blueprint

resource_bp = Blueprint('resource_routes', __name__, url_prefix='/resources')
history_bp = Blueprint('history_routes', __name__, url_prefix='/history')
points_bp = Blueprint('points_routes', __name__, url_prefix='/points')

from . import resource_routes, history_routes, points_routes

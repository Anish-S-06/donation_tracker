from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(roles):
    """
    Decorator that checks if the current logged-in user has one of the specified roles.
    roles can be a string or a list/tuple of strings.
    """
    if isinstance(roles, str):
        roles = [roles]
        
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                # 401 Unauthorized causes Flask-Login to redirect to login page
                # or we can abort directly
                abort(401)
            if current_user.role not in roles:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator

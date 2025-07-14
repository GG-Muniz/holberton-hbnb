"""Admin utility functions for role-based access control"""

from functools import wraps
from flask_jwt_extended import get_jwt
from flask_restx import abort

def admin_required(f):
    """Decorator to require admin privileges for an endpoint"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            abort(403, 'Access denied - administrator privileges required')
        
        return f(*args, **kwargs)
    return decorated_function

def is_admin_user():
    """Check if the current user has admin privileges"""
    claims = get_jwt()
    return claims.get('is_admin', False)

def admin_or_owner_required(resource_owner_id, current_user_id):
    """Check if user is admin or owns the resource"""
    if is_admin_user():
        return True
    return resource_owner_id == current_user_id
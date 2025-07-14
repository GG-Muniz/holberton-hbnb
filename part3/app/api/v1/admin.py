"""Admin-only endpoints for user and system management"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.utils.admin import admin_required

api = Namespace('admin', description='Administrator operations')

# Admin user creation model (includes is_admin field)
admin_user_create_model = api.model('AdminUserCreate', {
    'email': fields.String(required=True, description='User email'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

# Admin user update model (includes all fields including email and password)
admin_user_update_model = api.model('AdminUserUpdate', {
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'password': fields.String(description='New password'),
    'is_admin': fields.Boolean(description='Admin status')
})

user_response = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Update timestamp')
})

@api.route('/users')
class AdminUserManagement(Resource):
    @api.doc('admin_create_user')
    @api.expect(admin_user_create_model)
    @api.marshal_with(user_response, code=201)
    @api.response(400, 'Email already exists or validation error')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Administrator privileges required')
    @jwt_required()
    @admin_required
    def post(self):
        """Create a new user (admin only)"""
        try:
            data = request.json
            
            # Validate required fields
            if not data.get('password'):
                raise ValueError("Password is required")
            
            user = facade.create_user(
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                password=data.get('password'),
                is_admin=data.get('is_admin', False)
            )
            return user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/users/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class AdminUserDetail(Resource):
    @api.doc('admin_update_user')
    @api.expect(admin_user_update_model)
    @api.marshal_with(user_response)
    @api.response(401, 'Authentication required')
    @api.response(403, 'Administrator privileges required')
    @jwt_required()
    @admin_required
    def put(self, user_id):
        """Update any user (admin only)"""
        try:
            data = request.json
            
            # Get the user to update
            user = facade.get_user(user_id)
            
            # Handle password update separately if provided
            if 'password' in data and data['password']:
                user.set_password(data['password'])
                # Remove password from update_data to avoid double processing
                update_data = {k: v for k, v in data.items() if k != 'password' and v is not None}
            else:
                update_data = {k: v for k, v in data.items() if v is not None}
            
            # Update user with remaining fields
            if update_data:
                user = facade.update_user(user_id, **update_data)
            
            return user.to_dict()
        except ValueError as e:
            api.abort(404 if "not found" in str(e) else 400, str(e))

    @api.doc('admin_delete_user')
    @api.response(204, 'User deleted successfully')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Administrator privileges required')
    @jwt_required()
    @admin_required
    def delete(self, user_id):
        """Delete a user (admin only)"""
        try:
            current_user_id = get_jwt_identity()
            
            # Prevent admin from deleting themselves
            if user_id == current_user_id:
                api.abort(400, 'Cannot delete your own account')
            
            # Note: This would require implementing delete_user in facade
            # For now, we'll return a placeholder response
            api.abort(501, 'User deletion not yet implemented')
            
        except ValueError:
            api.abort(404, f"User {user_id} not found")
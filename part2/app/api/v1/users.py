from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# Define models for request/response
user_model = api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'password': fields.String(required=True, description='User password')
})

user_update_model = api.model('UserUpdate', {
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

user_response = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Update timestamp')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response)
    def get(self):
        """List all users"""
        return [user.to_dict() for user in facade.get_all_users()]

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_response, code=201)
    @api.response(400, 'Email already exists or validation error')
    def post(self):
        """Create a new user"""
        try:
            data = request.json
            user = facade.create_user(
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                password=data.get('password')
            )
            return user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response)
    def get(self, user_id):
        """Get a user by ID"""
        try:
            return facade.get_user(user_id).to_dict()
        except ValueError:
            api.abort(404, f"User {user_id} not found")

    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.marshal_with(user_response)
    def put(self, user_id):
        """Update a user"""
        try:
            data = request.json
            # remove None values
            update_data = {k: v for k, v in data.items() if v is not None}
            user = facade.update_user(user_id, **update_data)
            return user.to_dict()
        except ValueError as e:
            api.abort(404 if "not found" in str(e) else 400, str(e))

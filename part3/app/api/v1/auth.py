from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Define models for request/response
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

token_response = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'user': fields.Raw(description='User information')
})

@api.route('/login')
class UserLogin(Resource):
    @api.doc('user_login')
    @api.expect(login_model)
    @api.marshal_with(token_response, code=200)
    @api.response(401, 'Invalid credentials')
    @api.response(400, 'Missing email or password')
    def post(self):
        """Authenticate user and return JWT token"""
        try:
            data = request.json
            
            # Validate required fields
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                api.abort(400, 'Email and password are required')
            
            # Get user by email
            users = facade.get_all_users()
            user = None
            for u in users:
                if u.email == email:
                    user = u
                    break
            
            if not user:
                api.abort(401, 'Invalid credentials')
            
            # Check password
            if not user.check_password(password):
                api.abort(401, 'Invalid credentials')
            
            # Create JWT token with additional claims
            additional_claims = {
                "is_admin": user.is_admin,
                "email": user.email
            }
            
            access_token = create_access_token(
                identity=user.id,
                additional_claims=additional_claims
            )
            
            return {
                'access_token': access_token,
                'user': user.to_dict()
            }, 200
                
        except Exception as e:
            api.abort(400, str(e))

@api.route('/protected')
class ProtectedExample(Resource):
    @api.doc('protected_endpoint')
    @jwt_required()
    @api.response(200, 'Access granted')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """Example protected endpoint"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        
        return {
            'message': f'Hello user {current_user_id}!',
            'user_id': current_user_id,
            'is_admin': claims.get('is_admin', False),
            'email': claims.get('email', 'unknown')
        }, 200
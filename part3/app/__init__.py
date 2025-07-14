from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import config

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='development'):
    """
    Application factory to create and configure Flask app instance.
    
    Args:
        config_name (str): Configuration name ('development', 'production', etc.)
                          Defaults to 'development'
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration from config object
    if config_name in config:
        app.config.from_object(config[config_name])
    else:
        # Fallback to default configuration
        app.config.from_object(config['default'])

    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # JWT configuration and handlers
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        """Register a callback to return the identity of a user from a given user object"""
        return user
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Register a callback to return a User object when a valid JWT is accessed"""
        from app.services import facade
        identity = jwt_data["sub"]
        try:
            return facade.get_user(identity)
        except:
            return None
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Callback function for when an expired JWT is encountered"""
        from flask import jsonify
        return jsonify({'message': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Callback function for when an invalid JWT is encountered"""
        from flask import jsonify
        return jsonify({'message': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Callback function for when no JWT is present"""
        from flask import jsonify
        return jsonify({'message': 'Authorization token is required'}), 401
    
    # Initialize Flask-RESTX
    api = Api(app, version='1.0', title='HBnB API',
              description='A simple AirBnB clone API',
              doc='/api/docs')

    # Register namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.admin import api as admin_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')

    return app

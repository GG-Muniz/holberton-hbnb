from flask import Flask
from flask_restx import Api
from config import config

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

    # Initialize Flask-RESTX
    api = Api(app, version='1.0', title='HBnB API',
              description='A simple AirBnB clone API',
              doc='/api/docs')

    # Register namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app

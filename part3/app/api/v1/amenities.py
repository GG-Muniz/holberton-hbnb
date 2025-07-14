from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required
from app.services import facade
from app.utils.admin import admin_required

api = Namespace('amenities', description='Amenity operations')


# Define models for request/response
amenity_create_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Amenity name (max 50 chars)')
})

amenity_update_model = api.model('AmenityUpdate', {
    'name': fields.String(description='Amenity name (max 50 chars)')
})

amenity_response = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Update timestamp')
})

@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_response)
    def get(self):
        """List all amenities"""
        return [amenity.to_dict() for amenity in facade.get_all_amenities()]

    @api.doc('create_amenity')
    @api.expect(amenity_create_model)
    @api.marshal_with(amenity_response, code=201)
    @api.response(400, 'Amenity already exists or validation error')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Administrator privileges required')
    @jwt_required()
    @admin_required
    def post(self):
        """Create a new amenity (admin only)"""
        try:
            data = request.json
            name = data.get('name', '').strip()

            if not name:
                raise ValueError("Amenity name is required")

            amenity = facade.create_amenity(name=name)
            return amenity.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
@api.response(404, 'Amenity not found')
class Amenity(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_response)
    def get(self, amenity_id):
        """Get an amenity by ID"""
        try:
            return facade.get_amenity(amenity_id).to_dict()
        except ValueError:
            api.abort(404, f"Amenity {amenity_id} not found")

    @api.doc('update_amenity')
    @api.expect(amenity_update_model)
    @api.marshal_with(amenity_response)
    @api.response(401, 'Authentication required')
    @api.response(403, 'Administrator privileges required')
    @jwt_required()
    @admin_required
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        try:
            data = request.json
            # remove None values and empty strings
            update_data = {}
            if 'name' in data and data['name'] is not None:
                name = data['name'].strip()
                if not name:
                    raise ValueError("Amenity name cannot be empty")
                update_data['name'] = name

            if not update_data:
                raise ValueError("No valid update data provided")

            amenity = facade.update_amenity(amenity_id, **update_data)
            return amenity.to_dict()
        except ValueError as e:
            api.abort(404 if "not found" in str(e) else 400, str(e))

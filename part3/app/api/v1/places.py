# app/api/v1/places.py
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('places', description='Place operations')


# nested models for related data
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'user_id': fields.String(description='User ID'),
    'rating': fields.Integer(description='Rating'),
    'comment': fields.String(description='Comment'),
    'created_at': fields.DateTime(description='Creation timestamp')
})

# Define models for request/response
place_create_model = api.model('PlaceCreate', {
    'name': fields.String(required=True, description='Place name'),
    'description': fields.String(required=True, description='Place description'),
    'address': fields.String(required=True, description='Place address'),
    'city_id': fields.String(required=True, description='City ID'),
    'latitude': fields.Float(required=True, description='Latitude (-90 to 90)'),
    'longitude': fields.Float(required=True, description='Longitude (-180 to 180)'),
    'host_id': fields.String(required=True, description='Host user ID'),
    'number_of_rooms': fields.Integer(required=True, description='Number of rooms'),
    'number_of_bathrooms': fields.Integer(required=True, description='Number of bathrooms'),
    'price_per_night': fields.Float(required=True, description='Price per night (must be positive)'),
    'max_guests': fields.Integer(required=True, description='Maximum number of guests'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs', default=[])
})

place_update_model = api.model('PlaceUpdate', {
    'name': fields.String(description='Place name'),
    'description': fields.String(description='Place description'),
    'address': fields.String(description='Place address'),
    'number_of_rooms': fields.Integer(description='Number of rooms'),
    'number_of_bathrooms': fields.Integer(description='Number of bathrooms'),
    'price_per_night': fields.Float(description='Price per night'),
    'max_guests': fields.Integer(description='Maximum number of guests'),
    'amenity_ids': fields.List(fields.String, description='List of amenity IDs')
})

place_response = api.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'name': fields.String(description='Place name'),
    'description': fields.String(description='Place description'),
    'address': fields.String(description='Place address'),
    'city_id': fields.String(description='City ID'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'host_id': fields.String(description='Host user ID'),
    'host': fields.Nested(user_model, description='Host details'),
    'number_of_rooms': fields.Integer(description='Number of rooms'),
    'number_of_bathrooms': fields.Integer(description='Number of bathrooms'),
    'price_per_night': fields.Float(description='Price per night'),
    'max_guests': fields.Integer(description='Maximum number of guests'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Update timestamp')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_response)
    def get(self):
        """List all places with details"""
        places = facade.get_all_places()
        result = []

        for place in places:
            place_dict = place.to_dict()
            # add host details
            try:
                host = facade.get_user(place.host_id)
                place_dict['host'] = host.to_dict()
            except:
                place_dict['host'] = None

            # add amenities
            place_dict['amenities'] = []
            for amenity_id in place.amenity_ids:
                try:
                    amenity = facade.get_amenity(amenity_id)
                    place_dict['amenities'].append(amenity.to_dict())
                except:
                    pass

            # add reviews
            reviews = facade.get_reviews_by_place(place.id)
            place_dict['reviews'] = [review.to_dict() for review in reviews]

            result.append(place_dict)

        return result

    @api.doc('create_place')
    @api.expect(place_create_model)
    @api.marshal_with(place_response, code=201)
    @api.response(400, 'Invalid input or validation error')
    def post(self):
        """Create a new place"""
        try:
            data = request.json
            place = facade.create_place(**data)

            # prepare response with full details
            place_dict = place.to_dict()
            place_dict['host'] = facade.get_user(place.host_id).to_dict()
            place_dict['amenities'] = []
            for amenity_id in place.amenity_ids:
                amenity = facade.get_amenity(amenity_id)
                place_dict['amenities'].append(amenity.to_dict())
            place_dict['reviews'] = []

            return place_dict, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
@api.response(404, 'Place not found')
class Place(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_response)
    def get(self, place_id):
        """Get a place by ID with full details"""
        try:
            place = facade.get_place(place_id)
            place_dict = place.to_dict()

            # add host details
            place_dict['host'] = facade.get_user(place.host_id).to_dict()

            # add amenities
            place_dict['amenities'] = []
            for amenity_id in place.amenity_ids:
                try:
                    amenity = facade.get_amenity(amenity_id)
                    place_dict['amenities'].append(amenity.to_dict())
                except:
                    pass

            # add reviews
            reviews = facade.get_reviews_by_place(place_id)
            place_dict['reviews'] = [review.to_dict() for review in reviews]

            return place_dict
        except ValueError:
            api.abort(404, f"Place {place_id} not found")

    @api.doc('update_place')
    @api.expect(place_update_model)
    @api.marshal_with(place_response)
    def put(self, place_id):
        """Update a place"""
        try:
            data = request.json
            # remove None values
            update_data = {k: v for k, v in data.items() if v is not None}

            place = facade.update_place(place_id, **update_data)

            # prepare response with full details
            place_dict = place.to_dict()
            place_dict['host'] = facade.get_user(place.host_id).to_dict()
            place_dict['amenities'] = []
            for amenity_id in place.amenity_ids:
                amenity = facade.get_amenity(amenity_id)
                place_dict['amenities'].append(amenity.to_dict())

            reviews = facade.get_reviews_by_place(place_id)
            place_dict['reviews'] = [review.to_dict() for review in reviews]

            return place_dict
        except ValueError as e:
            api.abort(404 if "not found" in str(e) else 400, str(e))

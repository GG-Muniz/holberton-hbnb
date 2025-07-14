# app/api/v1/reviews.py
from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.utils.admin import admin_or_owner_required

api = Namespace('reviews', description='Review operations')


# Define models for request/response
review_create_model = api.model('ReviewCreate', {
    'place_id': fields.String(required=True, description='Place ID'),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5),
    'comment': fields.String(required=True, description='Review comment')
})

review_update_model = api.model('ReviewUpdate', {
    'rating': fields.Integer(description='Rating (1-5)', min=1, max=5),
    'comment': fields.String(description='Review comment')
})

# nested user model for response
user_model = api.model('ReviewUser', {
    'id': fields.String(description='User ID'),
    'email': fields.String(description='User email'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

review_response = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'place_id': fields.String(description='Place ID'),
    'user_id': fields.String(description='User ID'),
    'user': fields.Nested(user_model, description='User details'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'comment': fields.String(description='Review comment'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Update timestamp')
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_response)
    def get(self):
        """List all reviews"""
        reviews = facade.get_all_reviews()
        result = []

        for review in reviews:
            review_dict = review.to_dict()
            # add user details
            try:
                user = facade.get_user(review.user_id)
                review_dict['user'] = user.to_dict()
            except:
                review_dict['user'] = None
            result.append(review_dict)

        return result

    @api.doc('create_review')
    @api.expect(review_create_model)
    @api.marshal_with(review_response, code=201)
    @api.response(400, 'Invalid input or user already reviewed this place')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Cannot review your own place')
    @jwt_required()
    def post(self):
        """Create a new review (requires authentication)"""
        try:
            data = request.json
            current_user_id = get_jwt_identity()
            place_id = data.get('place_id')
            
            # Check if the place exists and get place details
            place = facade.get_place(place_id)
            
            # Prevent users from reviewing their own places
            if place.host_id == current_user_id:
                api.abort(403, 'You cannot review your own place')
            
            review = facade.create_review(
                place_id=place_id,
                user_id=current_user_id,
                rating=data.get('rating'),
                comment=data.get('comment')
            )

            # prepare response with user details
            review_dict = review.to_dict()
            review_dict['user'] = facade.get_user(review.user_id).to_dict()

            return review_dict, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
@api.response(404, 'Review not found')
class Review(Resource):
    @api.doc('get_review')
    @api.marshal_with(review_response)
    def get(self, review_id):
        """Get a review by ID"""
        try:
            review = facade.get_review(review_id)
            review_dict = review.to_dict()

            # add user details
            review_dict['user'] = facade.get_user(review.user_id).to_dict()

            return review_dict
        except ValueError:
            api.abort(404, f"Review {review_id} not found")

    @api.doc('update_review')
    @api.expect(review_update_model)
    @api.marshal_with(review_response)
    @api.response(401, 'Authentication required')
    @api.response(403, 'Access denied - not the review owner or admin')
    @jwt_required()
    def put(self, review_id):
        """Update a review (requires authentication and ownership or admin privileges)"""
        try:
            current_user_id = get_jwt_identity()
            
            # Get the review to check ownership
            review = facade.get_review(review_id)
            
            # Check if the current user is the owner or an admin
            if not admin_or_owner_required(review.user_id, current_user_id):
                api.abort(403, 'Access denied - you can only update reviews you created (or be an admin)')
            
            data = request.json
            # validate rating if provided
            if 'rating' in data and data['rating'] is not None:
                if not 1 <= data['rating'] <= 5:
                    raise ValueError("Rating must be between 1 and 5")

            # remove None values
            update_data = {k: v for k, v in data.items() if v is not None}

            review = facade.update_review(review_id, **update_data)

            # prepare response
            review_dict = review.to_dict()
            review_dict['user'] = facade.get_user(review.user_id).to_dict()

            return review_dict
        except ValueError as e:
            api.abort(404 if "not found" in str(e) else 400, str(e))

    @api.doc('delete_review')
    @api.response(204, 'Review deleted successfully')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Access denied - not the review owner or admin')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (requires authentication and ownership or admin privileges)"""
        try:
            current_user_id = get_jwt_identity()
            
            # Get the review to check ownership
            review = facade.get_review(review_id)
            
            # Check if the current user is the owner or an admin
            if not admin_or_owner_required(review.user_id, current_user_id):
                api.abort(403, 'Access denied - you can only delete reviews you created (or be an admin)')
            
            facade.delete_review(review_id)
            return '', 204
        except ValueError:
            api.abort(404, f"Review {review_id} not found")

@api.route('/places/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceReviews(Resource):
    @api.doc('get_place_reviews')
    @api.marshal_list_with(review_response)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        result = []

        for review in reviews:
            review_dict = review.to_dict()
            # add user details
            try:
                user = facade.get_user(review.user_id)
                review_dict['user'] = user.to_dict()
            except:
                review_dict['user'] = None
            result.append(review_dict)

        return result

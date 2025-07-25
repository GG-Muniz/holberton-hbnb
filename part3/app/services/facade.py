from app.persistence.repository_manager import RepositoryManager
from app.persistence.user_repository import UserRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """Facade for the HBnB application"""

    def __init__(self, repository=None, user_repository=None):
        """Initialize facade with optional repository overrides"""
        if repository:
            self.repo = repository
        else:
            self.repo = RepositoryManager.get_repository()
        
        if user_repository:
            self.user_repo = user_repository
        else:
            # Use UserRepository for user operations if SQLAlchemy is enabled
            import os
            if os.environ.get('REPOSITORY_TYPE') == 'sqlalchemy':
                self.user_repo = UserRepository()
            else:
                self.user_repo = self.repo

    # User operations
    def create_user(self, email: str, first_name: str, last_name: str, password: str = None, is_admin: bool = False) -> User:
        """Create a new user"""
        # Check if user with email already exists
        existing_users = self.user_repo.get_by_attribute(User, email=email)
        if existing_users:
            raise ValueError(f"User with email {email} already exists")

        user = User(email, first_name, last_name, password, is_admin)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User:
        """Get a user by ID"""
        user = self.user_repo.get(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user

    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        users = self.user_repo.get_by_attribute(User, email=email)
        if not users:
            return None
        return users[0]

    def get_all_users(self) -> list:
        """Get all users"""
        return self.user_repo.get_all(User)

    def update_user(self, user_id: str, **kwargs) -> User:
        """Update a user"""
        user = self.get_user(user_id)

        # don't allow email updates if email already exists
        if 'email' in kwargs and kwargs['email'] != user.email:
            existing = self.user_repo.get_by_attribute(User, email=kwargs['email'])
            if existing:
                raise ValueError(f"Email {kwargs['email']} already in use")

        # don't allow password updates through this method
        if 'password' in kwargs:
            del kwargs['password']

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self.user_repo.update(user)
        return user

    # Place operations
    def create_place(self, **place_data) -> Place:
        """Create a new place"""
        # Validate host exists
        try:
            host = self.get_user(place_data['host_id'])
        except ValueError:
            raise ValueError(f"Host with id {place_data['host_id']} not found")

        # validate amenities exist and get amenity objects
        amenities = []
        if 'amenity_ids' in place_data and place_data['amenity_ids']:
            for amenity_id in place_data['amenity_ids']:
                try:
                    amenity = self.get_amenity(amenity_id)
                    amenities.append(amenity)
                except ValueError:
                    raise ValueError(f"Amenity with id {amenity_id} not found")
        
        # Remove amenity_ids from place_data since we'll use relationships
        place_data = {k: v for k, v in place_data.items() if k != 'amenity_ids'}
        
        place = Place(**place_data)
        
        # Add amenities to the place using relationships
        for amenity in amenities:
            place.amenities.append(amenity)
        
        self.repo.add(place)
        return place

    def get_place(self, place_id: str) -> Place:
        """Get a place by ID"""
        place = self.repo.get(Place, place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} not found")
        return place

    def get_all_places(self) -> list:
        """Get all places"""
        return self.repo.get_all(Place)

    def get_places_by_host(self, host_id: str) -> list:
        """Get all places owned by a specific host"""
        return self.repo.get_by_attribute(Place, host_id=host_id)

    def update_place(self, place_id: str, **kwargs) -> Place:
        """Update a place"""
        place = self.get_place(place_id)

        # validate new amenities if provided and update relationships
        if 'amenity_ids' in kwargs:
            # Clear existing amenities
            place.amenities.clear()
            
            # Add new amenities
            for amenity_id in kwargs['amenity_ids']:
                try:
                    amenity = self.get_amenity(amenity_id)
                    place.amenities.append(amenity)
                except ValueError:
                    raise ValueError(f"Amenity with id {amenity_id} not found")
            
            # Remove amenity_ids from kwargs since it's handled by relationships
            del kwargs['amenity_ids']

        # validate price if being updated
        if 'price_per_night' in kwargs and kwargs['price_per_night'] < 0:
            raise ValueError("Price must be positive")

        for key, value in kwargs.items():
            if hasattr(place, key):
                setattr(place, key, value)

        self.repo.update(place)
        return place

    # Review operations
    def create_review(self, place_id: str, user_id: str, rating: int, comment: str) -> Review:
        """Create a new review"""
        # Validate place and user exist
        place = self.get_place(place_id)
        user = self.get_user(user_id)

        # check if user already reviewed this place
        existing_reviews = self.repo.get_by_attribute(Review, place_id=place_id, user_id=user_id)
        if existing_reviews:
            raise ValueError("User has already reviewed this place")

        review = Review(place_id, user_id, rating, comment)
        self.repo.add(review)
        
        # The relationships will automatically be updated by SQLAlchemy

        return review

    def get_review(self, review_id: str) -> Review:
        """Get a review by ID"""
        review = self.repo.get(Review, review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} not found")
        return review

    def get_all_reviews(self) -> list:
        """Get all reviews"""
        return self.repo.get_all(Review)

    def get_reviews_by_place(self, place_id: str) -> list:
        """Get all reviews for a place"""
        return self.repo.get_by_attribute(Review, place_id=place_id)

    def update_review(self, review_id: str, **kwargs) -> Review:
        """Update a review"""
        review = self.get_review(review_id)

        # only allow updating rating and comment
        allowed_updates = ['rating', 'comment']
        for key in list(kwargs.keys()):
            if key not in allowed_updates:
                del kwargs[key]

        for key, value in kwargs.items():
            if hasattr(review, key):
                setattr(review, key, value)

        self.repo.update(review)
        return review

    def delete_review(self, review_id: str) -> bool:
        """Delete a review"""
        review = self.get_review(review_id)

        # SQLAlchemy relationships will automatically handle cleanup with cascade delete
        return self.repo.delete(Review, review_id)

    # Amenity operations
    def create_amenity(self, name: str) -> Amenity:
        """Create a new amenity"""
        # Check if amenity with name already exists
        existing_amenities = self.repo.get_by_attribute(Amenity, name=name)
        if existing_amenities:
            raise ValueError(f"Amenity with name '{name}' already exists")

        amenity = Amenity(name)
        self.repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Amenity:
        """Get an amenity by ID"""
        amenity = self.repo.get(Amenity, amenity_id)
        if not amenity:
            raise ValueError(f"Amenity with id {amenity_id} not found")
        return amenity

    def get_all_amenities(self) -> list:
        """Get all amenities"""
        return self.repo.get_all(Amenity)

    def update_amenity(self, amenity_id: str, **kwargs) -> Amenity:
        """Update an amenity"""
        amenity = self.get_amenity(amenity_id)

        # check if new name already exists
        if 'name' in kwargs and kwargs['name'] != amenity.name:
            existing = self.repo.get_by_attribute(Amenity, name=kwargs['name'])
            if existing:
                raise ValueError(f"Amenity with name '{kwargs['name']}' already exists")

        for key, value in kwargs.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)

        self.repo.update(amenity)
        return amenity

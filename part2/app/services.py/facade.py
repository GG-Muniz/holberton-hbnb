from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """Facade for the HBnB application"""

    def __init__(self):
        self.repo = InMemoryRepository()

    # User operations
    def create_user(self, email: str, first_name: str, last_name: str) -> User:
        """Create a new user"""
        # Check if user with email already exists
        existing_users = self.repo.get_by_attribute(User, email=email)
        if existing_users:
            raise ValueError(f"User with email {email} already exists")

        user = User(email, first_name, last_name)
        self.repo.add(user)
        return user

    def get_user(self, user_id: str) -> User:
        """Get a user by ID"""
        user = self.repo.get(User, user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user

    def get_all_users(self) -> list:
        """Get all users"""
        return self.repo.get_all(User)

    def update_user(self, user_id: str, **kwargs) -> User:
        """Update a user"""
        user = self.get_user(user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.repo.update(user)
        return user

    # Place operations
    def create_place(self, **place_data) -> Place:
        """Create a new place"""
        # Validate host exists
        try:
            self.get_user(place_data['host_id'])
        except ValueError:
            raise ValueError(f"Host with id {place_data['host_id']} not found")

        place = Place(**place_data)
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

    def update_place(self, place_id: str, **kwargs) -> Place:
        """Update a place"""
        place = self.get_place(place_id)
        for key, value in kwargs.items():
            if hasattr(place, key):
                setattr(place, key, value)
        self.repo.update(place)
        return place

    # Review operations
    def create_review(self, place_id: str, user_id: str, rating: int, comment: str) -> Review:
        """Create a new review"""
        # Validate place and user exist
        self.get_place(place_id)
        self.get_user(user_id)

        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        review = Review(place_id, user_id, rating, comment)
        self.repo.add(review)
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

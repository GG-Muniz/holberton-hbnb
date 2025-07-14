from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Float, Integer
import json

class Place(BaseModel):
    """Place model with SQLAlchemy mapping"""
    __tablename__ = 'places'
    
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String(200), nullable=False)
    city_id = Column(String(36), nullable=False)  # Will be FK in later tasks
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    host_id = Column(String(36), nullable=False)  # Will be FK in later tasks
    number_of_rooms = Column(Integer, nullable=False)
    number_of_bathrooms = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)
    max_guests = Column(Integer, nullable=False)
    amenity_ids = Column(Text, default='[]', nullable=False)  # JSON string of amenity IDs
    reviews = Column(Text, default='[]', nullable=False)  # JSON string of review IDs

    def __init__(self, name, description, address, city_id, latitude, longitude,
                 host_id, number_of_rooms, number_of_bathrooms, price_per_night,
                 max_guests, amenity_ids=None):
        super().__init__()
        # validate required fields
        if not name or len(name.strip()) == 0:
            raise ValueError("Place name is required")

        # Convert to float first, then validate
        price_per_night = float(price_per_night)
        if price_per_night < 0:
            raise ValueError("Price must be positive")

        # Convert to float first, then validate
        latitude = float(latitude)
        longitude = float(longitude)
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

        # Convert and validate room counts
        number_of_rooms = int(number_of_rooms)
        number_of_bathrooms = int(number_of_bathrooms)
        max_guests = int(max_guests)
        if number_of_rooms < 0 or number_of_bathrooms < 0 or max_guests < 0:
            raise ValueError("Room counts must be non-negative")

        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenity_ids = json.dumps(amenity_ids or [])  # Store as JSON string
        self.reviews = '[]'  # Initialize as empty JSON string

    def get_amenity_ids_list(self):
        """Get amenity IDs as a Python list"""
        try:
            return json.loads(self.amenity_ids) if self.amenity_ids else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_amenity_ids_list(self, amenity_ids_list):
        """Set amenity IDs from a Python list"""
        self.amenity_ids = json.dumps(amenity_ids_list) if amenity_ids_list else '[]'
    
    def get_reviews_list(self):
        """Get reviews as a Python list"""
        try:
            return json.loads(self.reviews) if self.reviews else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_reviews_list(self, reviews_list):
        """Set reviews from a Python list"""
        self.reviews = json.dumps(reviews_list) if reviews_list else '[]'

    def add_amenity(self, amenity_id):
        """add amenity to place if not already there"""
        amenity_ids_list = self.get_amenity_ids_list()
        if amenity_id not in amenity_ids_list:
            amenity_ids_list.append(amenity_id)
            self.set_amenity_ids_list(amenity_ids_list)

    def remove_amenity(self, amenity_id):
        """remove amenity from place"""
        amenity_ids_list = self.get_amenity_ids_list()
        if amenity_id in amenity_ids_list:
            amenity_ids_list.remove(amenity_id)
            self.set_amenity_ids_list(amenity_ids_list)

    def to_dict(self):
        """Convert place object to dictionary"""
        place_dict = super().to_dict()
        place_dict.update({
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city_id': self.city_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'host_id': self.host_id,
            'number_of_rooms': self.number_of_rooms,
            'number_of_bathrooms': self.number_of_bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenity_ids': self.get_amenity_ids_list()
        })
        # Note: Don't include reviews in to_dict() - they're handled separately
        return place_dict

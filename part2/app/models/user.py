from app.models.base_model import BaseModel
import re

class User(BaseModel):
    """User model"""
    
    def __init__(self, email, first_name, last_name, password=None):
        super().__init__()
        # validate email format
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        if not first_name or not first_name.strip():
            raise ValueError("First name cannot be empty")
        if not last_name or not last_name.strip():
            raise ValueError("Last name cannot be empty")
        
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password  # in real app, this would be hashed
        self.places = []  # places owned by user
        self.reviews = []  # reviews written by user
    
    def _is_valid_email(self, email):
        """check if email is valid"""
        
        # using re.compile for better performance if called multiple times
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        return EMAIL_REGEX.match(email) is not None
# ### Place Model (app/models/place.py)

from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place model"""
    
    def __init__(self, name, description, address, city_id, latitude, longitude, 
                 host_id, number_of_rooms, number_of_bathrooms, price_per_night, 
                 max_guests, amenity_ids=None):
        super().__init__()
        # validate required fields
        if not name or len(name.strip()) == 0:
            raise ValueError("Place name is required")
        if price_per_night < 0:
            raise ValueError("Price must be positive")
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        if number_of_rooms < 0 or number_of_bathrooms < 0 or max_guests < 0:
            raise ValueError("Room counts must be non-negative")
        
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.host_id = host_id
        self.number_of_rooms = int(number_of_rooms)
        self.number_of_bathrooms = int(number_of_bathrooms)
        self.price_per_night = float(price_per_night)
        self.max_guests = int(max_guests)
        self.amenity_ids = amenity_ids or []
        self.reviews = []  # list of reviews for this place
    
    def add_amenity(self, amenity_id):
        """add amenity to place if not already there"""
        if amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)
    
    def remove_amenity(self, amenity_id):
        """remove amenity from place"""
        if amenity_id in self.amenity_ids:
            self.amenity_ids.remove(amenity_id)
    
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
            'amenity_ids': self.amenity_ids
        })
        return place_dict
    
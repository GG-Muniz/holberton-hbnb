from app.models.base_model import BaseModel
from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app import db
import json

# Many-to-many association table for Place-Amenity relationship
place_amenity = Table('place_amenity', db.Model.metadata,
    Column('place_id', String(36), ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String(36), ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Place model with SQLAlchemy mapping"""
    __tablename__ = 'places'
    
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String(200), nullable=False)
    city_id = Column(String(36), nullable=False)  # Will be FK in later tasks
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    host_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    number_of_rooms = Column(Integer, nullable=False)
    number_of_bathrooms = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)
    max_guests = Column(Integer, nullable=False)
    
    # Relationships
    host = relationship('User', back_populates='places')
    reviews = relationship('Review', back_populates='place', cascade='all, delete-orphan')
    amenities = relationship('Amenity', secondary=place_amenity, back_populates='places')

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
        # amenities and reviews are now handled by SQLAlchemy relationships

    def add_amenity(self, amenity):
        """Add amenity to place if not already there"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove amenity from place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)

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
            'amenity_ids': [amenity.id for amenity in self.amenities] if self.amenities else []
        })
        # Note: Don't include reviews in to_dict() - they're handled separately
        return place_dict

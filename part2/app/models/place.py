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
        self.amenity_ids = amenity_ids or []
        self.reviews = []  # Initialize as empty list, not passed as parameter

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
        # Note: Don't include reviews in to_dict() - they're handled separately
        return place_dict

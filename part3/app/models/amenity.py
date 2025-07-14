from app.models.base_model import BaseModel
from sqlalchemy import Column, String

class Amenity(BaseModel):
    """Amenity model with SQLAlchemy mapping"""
    __tablename__ = 'amenities'
    
    name = Column(String(50), unique=True, nullable=False, index=True)

    def __init__(self, name):
        super().__init__()
        # validate name
        if not name or len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 50:
            raise ValueError("Amenity name too long (max 50 chars)")

        self.name = name

    def to_dict(self):
        """Convert amenity object to dictionary"""
        amenity_dict = super().to_dict()
        amenity_dict['name'] = self.name
        return amenity_dict

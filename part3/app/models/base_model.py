import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from app import db

Base = declarative_base()

class BaseModel(db.Model):
    """Base class for all models with SQLAlchemy mapping"""
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self):
        """Initialize base model with UUID and timestamps"""
        if not hasattr(self, 'id') or self.id is None:
            self.id = str(uuid.uuid4())
        if not hasattr(self, 'created_at') or self.created_at is None:
            self.created_at = datetime.utcnow()
        if not hasattr(self, 'updated_at') or self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

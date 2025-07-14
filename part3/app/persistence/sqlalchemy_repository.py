"""SQLAlchemy-based repository implementation for database persistence"""

from typing import List, Optional, Type
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.base_model import BaseModel
from app.persistence.repository import Repository
from app import db

class SQLAlchemyRepository(Repository):
    """SQLAlchemy repository for database persistence"""
    
    def __init__(self):
        """Initialize the SQLAlchemy repository"""
        # Note: The actual database session will be handled by Flask-SQLAlchemy
        # This repository will use the global db object from the Flask app
        pass
    
    def add(self, obj: BaseModel) -> None:
        """Add an object to the database"""
        try:
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get(self, model_class: Type[BaseModel], obj_id: str) -> Optional[BaseModel]:
        """Retrieve an object by its ID"""
        try:
            return db.session.query(model_class).filter_by(id=obj_id).first()
        except Exception:
            return None
    
    def get_all(self, model_class: Type[BaseModel]) -> List[BaseModel]:
        """Retrieve all objects of a given class"""
        try:
            return db.session.query(model_class).all()
        except Exception:
            return []
    
    def update(self, obj: BaseModel) -> None:
        """Update an existing object"""
        try:
            # Update the updated_at timestamp
            obj.save()
            
            # Merge the object to handle potential detached instances
            db.session.merge(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self, model_class: Type[BaseModel], obj_id: str) -> bool:
        """Delete an object by its ID"""
        try:
            obj = self.get(model_class, obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False
    
    def get_by_attribute(self, model_class: Type[BaseModel], **kwargs) -> List[BaseModel]:
        """Get objects by attribute values"""
        try:
            query = db.session.query(model_class)
            
            # Apply filters for each attribute
            for key, value in kwargs.items():
                if hasattr(model_class, key):
                    query = query.filter(getattr(model_class, key) == value)
            
            return query.all()
        except Exception:
            return []
    
    def save(self, obj: BaseModel) -> None:
        """Save (add or update) an object to the database"""
        try:
            # Check if the object exists in the database
            existing = self.get(obj.__class__, obj.id)
            
            if existing:
                # Update existing object
                self.update(obj)
            else:
                # Add new object
                self.add(obj)
        except Exception as e:
            db.session.rollback()
            raise e
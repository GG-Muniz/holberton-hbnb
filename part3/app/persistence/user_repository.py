"""User-specific repository implementation for database persistence"""

from typing import List, Optional
from app.persistence.repository import Repository
from app.models.user import User
from app import db

class UserRepository(Repository):
    """User-specific repository for enhanced user database operations"""
    
    def add(self, obj: User) -> None:
        """Add a user to the database"""
        try:
            db.session.add(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get(self, model_class, obj_id: str) -> Optional[User]:
        """Retrieve a user by its ID"""
        try:
            return db.session.query(User).filter_by(id=obj_id).first()
        except Exception:
            return None
    
    def get_all(self, model_class) -> List[User]:
        """Retrieve all users"""
        try:
            return db.session.query(User).all()
        except Exception:
            return []
    
    def update(self, obj: User) -> None:
        """Update an existing user"""
        try:
            obj.save()
            db.session.merge(obj)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self, model_class, obj_id: str) -> bool:
        """Delete a user by its ID"""
        try:
            user = self.get(User, obj_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False
    
    def get_by_attribute(self, model_class, **kwargs) -> List[User]:
        """Get users by attribute values"""
        try:
            query = db.session.query(User)
            
            for key, value in kwargs.items():
                if hasattr(User, key):
                    query = query.filter(getattr(User, key) == value)
            
            return query.all()
        except Exception:
            return []
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address (user-specific method)"""
        try:
            return db.session.query(User).filter_by(email=email).first()
        except Exception:
            return None
    
    def get_admin_users(self) -> List[User]:
        """Get all admin users (user-specific method)"""
        try:
            return db.session.query(User).filter_by(is_admin=True).all()
        except Exception:
            return []
    
    def get_users_by_name(self, first_name: str = None, last_name: str = None) -> List[User]:
        """Get users by first and/or last name (user-specific method)"""
        try:
            query = db.session.query(User)
            
            if first_name:
                query = query.filter(User.first_name.ilike(f'%{first_name}%'))
            if last_name:
                query = query.filter(User.last_name.ilike(f'%{last_name}%'))
            
            return query.all()
        except Exception:
            return []
    
    def save(self, obj: User) -> None:
        """Save (add or update) a user to the database"""
        try:
            existing = self.get(User, obj.id)
            
            if existing:
                self.update(obj)
            else:
                self.add(obj)
        except Exception as e:
            db.session.rollback()
            raise e
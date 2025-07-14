from app.models.base_model import BaseModel
from app import bcrypt
import re

class User(BaseModel):
    """User model with secure password hashing"""
    
    def __init__(self, email, first_name, last_name, password=None, is_admin=False):
        super().__init__()
        # validate email format
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        if not first_name or not first_name.strip():
            raise ValueError("First name cannot be empty")
        if not last_name or not last_name.strip():
            raise ValueError("Last name cannot be empty")
        if password is not None:
            if not password or len(password.strip()) == 0:
                raise ValueError("Password cannot be empty")
            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters long")
        
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = bool(is_admin)
        self._password_hash = None
        if password:
            self.set_password(password)
        self.places = []  # places owned by user
        self.reviews = []  # reviews written by user
    
    def _is_valid_email(self, email):
        """Check if email is valid"""
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        return EMAIL_REGEX.match(email) is not None
    
    def set_password(self, password):
        """Hash and set the user's password"""
        if not password:
            raise ValueError("Password cannot be empty")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        if not self._password_hash:
            return False
        return bcrypt.check_password_hash(self._password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary (excluding password)"""
        user_dict = super().to_dict()
        user_dict.update({
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin
        })
        return user_dict
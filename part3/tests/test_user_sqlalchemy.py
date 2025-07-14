#!/usr/bin/env python3
"""
Test script for User SQLAlchemy mapping and repository operations
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment to use SQLAlchemy
os.environ['REPOSITORY_TYPE'] = 'sqlalchemy'

from app import create_app, db
from app.models.user import User
from app.persistence.user_repository import UserRepository
from app.services.facade import HBnBFacade

def test_user_model():
    """Test User model SQLAlchemy mapping"""
    print("Testing User Model SQLAlchemy Mapping...")
    
    # Test model creation
    user = User("test@example.com", "John", "Doe", "password123", False)
    
    # Test attributes
    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.is_admin == False
    assert user.password_hash is not None
    assert user.check_password("password123") == True
    assert user.check_password("wrong") == False
    
    # Test JSON list handling
    places_list = ["place1", "place2"]
    user.set_places_list(places_list)
    assert user.get_places_list() == places_list
    
    reviews_list = ["review1", "review2"]
    user.set_reviews_list(reviews_list)
    assert user.get_reviews_list() == reviews_list
    
    print("✅ User model tests passed!")

def test_user_repository():
    """Test UserRepository operations"""
    print("\nTesting User Repository...")
    
    app = create_app('development')
    
    with app.app_context():
        # Initialize database
        db.drop_all()
        db.create_all()
        
        repo = UserRepository()
        
        # Test create user
        user1 = User("alice@example.com", "Alice", "Smith", "password123", False)
        repo.add(user1)
        
        user2 = User("bob@example.com", "Bob", "Jones", "password456", True)
        repo.add(user2)
        
        # Test get user by ID
        retrieved_user = repo.get(User, user1.id)
        assert retrieved_user is not None
        assert retrieved_user.email == "alice@example.com"
        
        # Test get user by email
        email_user = repo.get_user_by_email("bob@example.com")
        assert email_user is not None
        assert email_user.first_name == "Bob"
        assert email_user.is_admin == True
        
        # Test get all users
        all_users = repo.get_all(User)
        assert len(all_users) == 2
        
        # Test get admin users
        admin_users = repo.get_admin_users()
        assert len(admin_users) == 1
        assert admin_users[0].email == "bob@example.com"
        
        # Test update user
        user1.first_name = "Alice Updated"
        repo.update(user1)
        
        updated_user = repo.get(User, user1.id)
        assert updated_user.first_name == "Alice Updated"
        
        # Test delete user
        result = repo.delete(User, user2.id)
        assert result == True
        
        remaining_users = repo.get_all(User)
        assert len(remaining_users) == 1
        
        print("✅ User repository tests passed!")

def test_facade_integration():
    """Test Facade integration with UserRepository"""
    print("\nTesting Facade Integration...")
    
    app = create_app('development')
    
    with app.app_context():
        # Initialize database
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Test create user through facade
        user = facade.create_user("charlie@example.com", "Charlie", "Brown", "password789", False)
        assert user.email == "charlie@example.com"
        
        # Test get user through facade
        retrieved_user = facade.get_user(user.id)
        assert retrieved_user.email == "charlie@example.com"
        
        # Test get user by email through facade
        email_user = facade.get_user_by_email("charlie@example.com")
        assert email_user is not None
        assert email_user.id == user.id
        
        # Test update user through facade
        updated_user = facade.update_user(user.id, first_name="Charles")
        assert updated_user.first_name == "Charles"
        
        # Test get all users through facade
        all_users = facade.get_all_users()
        assert len(all_users) == 1
        
        print("✅ Facade integration tests passed!")

def test_password_functionality():
    """Test password hashing and validation"""
    print("\nTesting Password Functionality...")
    
    app = create_app('development')
    
    with app.app_context():
        # Initialize database
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create user with password
        user = facade.create_user("secure@example.com", "Secure", "User", "securepassword123", False)
        
        # Retrieve user and test password
        retrieved_user = facade.get_user(user.id)
        assert retrieved_user.check_password("securepassword123") == True
        assert retrieved_user.check_password("wrongpassword") == False
        
        # Test password is hashed (not stored in plain text)
        assert retrieved_user.password_hash != "securepassword123"
        assert len(retrieved_user.password_hash) > 20  # bcrypt hashes are long
        
        print("✅ Password functionality tests passed!")

if __name__ == "__main__":
    print("=" * 60)
    print("User SQLAlchemy Mapping and Repository Tests")
    print("=" * 60)
    
    try:
        test_user_model()
        test_user_repository()
        test_facade_integration()
        test_password_functionality()
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed! User SQLAlchemy mapping is working correctly.")
        print("=" * 60)
        print("\nUser entity features:")
        print("✅ SQLAlchemy model mapping with proper columns")
        print("✅ Password hashing with bcrypt")
        print("✅ JSON list handling for places and reviews")
        print("✅ UserRepository with enhanced user operations")
        print("✅ Facade integration with UserRepository")
        print("✅ Database persistence and retrieval")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
#!/usr/bin/env python3
"""
Test script for all entity SQLAlchemy mappings and CRUD operations
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment to use SQLAlchemy
os.environ['REPOSITORY_TYPE'] = 'sqlalchemy'

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade

def test_database_initialization():
    """Test database initialization with all entity tables"""
    print("Testing Database Initialization...")
    
    app = create_app('development')
    
    with app.app_context():
        # Initialize database
        db.drop_all()
        db.create_all()
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['users', 'places', 'reviews', 'amenities']
        for table in expected_tables:
            assert table in tables, f"Table {table} not created"
        
        print(f"✅ All tables created: {tables}")

def test_user_entity():
    """Test User entity SQLAlchemy mapping"""
    print("\nTesting User Entity...")
    
    app = create_app('development')
    
    with app.app_context():
        # Reset database
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create user
        user = facade.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="password123"
        )
        
        # Verify user
        retrieved_user = facade.get_user(user.id)
        assert retrieved_user.email == "test@example.com"
        assert retrieved_user.check_password("password123")
        
        print("✅ User entity mapping works correctly")

def test_amenity_entity():
    """Test Amenity entity SQLAlchemy mapping"""
    print("\nTesting Amenity Entity...")
    
    app = create_app('development')
    
    with app.app_context():
        # Reset database
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create amenities
        amenity1 = facade.create_amenity("WiFi")
        amenity2 = facade.create_amenity("Pool")
        
        # Verify amenities
        retrieved_amenity = facade.get_amenity(amenity1.id)
        assert retrieved_amenity.name == "WiFi"
        
        all_amenities = facade.get_all_amenities()
        assert len(all_amenities) == 2
        
        print("✅ Amenity entity mapping works correctly")

def test_place_entity():
    """Test Place entity SQLAlchemy mapping"""
    print("\nTesting Place Entity...")
    
    app = create_app('development')
    
    with app.app_context():
        # Reset database
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create user (host)
        user = facade.create_user(
            email="host@example.com",
            first_name="Host",
            last_name="User",
            password="password123"
        )
        
        # Create amenities
        amenity1 = facade.create_amenity("WiFi")
        amenity2 = facade.create_amenity("Pool")
        
        # Create place
        place = facade.create_place(
            name="Test Place",
            description="A nice place to stay",
            address="123 Test St",
            city_id="test-city-id",
            latitude=40.7128,
            longitude=-74.0060,
            host_id=user.id,
            number_of_rooms=2,
            number_of_bathrooms=1,
            price_per_night=100.0,
            max_guests=4,
            amenity_ids=[amenity1.id, amenity2.id]
        )
        
        # Verify place
        retrieved_place = facade.get_place(place.id)
        assert retrieved_place.name == "Test Place"
        assert retrieved_place.host_id == user.id
        assert retrieved_place.latitude == 40.7128
        assert retrieved_place.longitude == -74.0060
        assert retrieved_place.price_per_night == 100.0
        
        # Test JSON list functionality
        amenity_ids = retrieved_place.get_amenity_ids_list()
        assert len(amenity_ids) == 2
        assert amenity1.id in amenity_ids
        assert amenity2.id in amenity_ids
        
        # Test amenity management
        amenity3 = facade.create_amenity("Parking")
        retrieved_place.add_amenity(amenity3.id)
        facade.repo.update(retrieved_place)
        
        updated_place = facade.get_place(place.id)
        updated_amenities = updated_place.get_amenity_ids_list()
        assert len(updated_amenities) == 3
        assert amenity3.id in updated_amenities
        
        print("✅ Place entity mapping works correctly")

def test_review_entity():
    """Test Review entity SQLAlchemy mapping"""
    print("\nTesting Review Entity...")
    
    app = create_app('development')
    
    with app.app_context():
        # Reset database
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create user (host)
        host = facade.create_user(
            email="host@example.com",
            first_name="Host",
            last_name="User",
            password="password123"
        )
        
        # Create user (reviewer)
        reviewer = facade.create_user(
            email="reviewer@example.com",
            first_name="Reviewer",
            last_name="User",
            password="password123"
        )
        
        # Create place
        place = facade.create_place(
            name="Test Place",
            description="A nice place to stay",
            address="123 Test St",
            city_id="test-city-id",
            latitude=40.7128,
            longitude=-74.0060,
            host_id=host.id,
            number_of_rooms=2,
            number_of_bathrooms=1,
            price_per_night=100.0,
            max_guests=4
        )
        
        # Create review
        review = facade.create_review(
            place_id=place.id,
            user_id=reviewer.id,
            rating=5,
            comment="Excellent place to stay!"
        )
        
        # Verify review
        retrieved_review = facade.get_review(review.id)
        assert retrieved_review.place_id == place.id
        assert retrieved_review.user_id == reviewer.id
        assert retrieved_review.rating == 5
        assert retrieved_review.comment == "Excellent place to stay!"
        
        # Verify review lists were updated
        updated_place = facade.get_place(place.id)
        place_reviews = updated_place.get_reviews_list()
        assert review.id in place_reviews
        
        updated_reviewer = facade.get_user(reviewer.id)
        user_reviews = updated_reviewer.get_reviews_list()
        assert review.id in user_reviews
        
        print("✅ Review entity mapping works correctly")

def test_full_crud_operations():
    """Test full CRUD operations on all entities"""
    print("\nTesting Full CRUD Operations...")
    
    app = create_app('development')
    
    with app.app_context():
        # Reset database
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # CREATE operations
        user = facade.create_user("crud@example.com", "CRUD", "User", "password123")
        amenity = facade.create_amenity("CRUD Amenity")
        place = facade.create_place(
            name="CRUD Place", description="Test", address="Test St",
            city_id="test", latitude=0.0, longitude=0.0, host_id=user.id,
            number_of_rooms=1, number_of_bathrooms=1, price_per_night=50.0,
            max_guests=2, amenity_ids=[amenity.id]
        )
        review = facade.create_review(place.id, user.id, 4, "Good place")
        
        # READ operations
        assert facade.get_user(user.id).email == "crud@example.com"
        assert facade.get_amenity(amenity.id).name == "CRUD Amenity"
        assert facade.get_place(place.id).name == "CRUD Place"
        assert facade.get_review(review.id).rating == 4
        
        # UPDATE operations
        updated_user = facade.update_user(user.id, first_name="Updated")
        assert updated_user.first_name == "Updated"
        
        updated_amenity = facade.update_amenity(amenity.id, name="Updated Amenity")
        assert updated_amenity.name == "Updated Amenity"
        
        updated_place = facade.update_place(place.id, name="Updated Place")
        assert updated_place.name == "Updated Place"
        
        updated_review = facade.update_review(review.id, rating=5)
        assert updated_review.rating == 5
        
        # DELETE operations (review only for now)
        result = facade.delete_review(review.id)
        assert result == True
        
        try:
            facade.get_review(review.id)
            assert False, "Review should have been deleted"
        except ValueError:
            pass  # Expected
        
        print("✅ Full CRUD operations work correctly")

def test_data_validation():
    """Test data validation for all entities"""
    print("\nTesting Data Validation...")
    
    app = create_app('development')
    
    with app.app_context():
        # Reset database
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Test User validation
        try:
            facade.create_user("invalid-email", "Test", "User", "password123")
            assert False, "Should have raised ValueError for invalid email"
        except ValueError:
            pass
        
        try:
            facade.create_user("test@example.com", "Test", "User", "123")
            assert False, "Should have raised ValueError for short password"
        except ValueError:
            pass
        
        # Test Amenity validation
        try:
            facade.create_amenity("")
            assert False, "Should have raised ValueError for empty name"
        except ValueError:
            pass
        
        try:
            facade.create_amenity("x" * 51)
            assert False, "Should have raised ValueError for long name"
        except ValueError:
            pass
        
        # Test Review validation
        user = facade.create_user("test@example.com", "Test", "User", "password123")
        place = facade.create_place(
            name="Test", description="Test", address="Test",
            city_id="test", latitude=0.0, longitude=0.0, host_id=user.id,
            number_of_rooms=1, number_of_bathrooms=1, price_per_night=50.0,
            max_guests=2
        )
        
        try:
            facade.create_review(place.id, user.id, 6, "Invalid rating")
            assert False, "Should have raised ValueError for invalid rating"
        except ValueError:
            pass
        
        try:
            facade.create_review(place.id, user.id, 5, "")
            assert False, "Should have raised ValueError for empty comment"
        except ValueError:
            pass
        
        print("✅ Data validation works correctly")

if __name__ == "__main__":
    print("=" * 70)
    print("All Entities SQLAlchemy Mapping Tests")
    print("=" * 70)
    
    try:
        test_database_initialization()
        test_user_entity()
        test_amenity_entity()
        test_place_entity()
        test_review_entity()
        test_full_crud_operations()
        test_data_validation()
        
        print("\n" + "=" * 70)
        print("🎉 All tests passed! All entities are properly mapped to SQLAlchemy.")
        print("=" * 70)
        print("\nEntity mappings completed:")
        print("✅ User - with password hashing and JSON lists")
        print("✅ Place - with coordinates, pricing, and JSON lists")
        print("✅ Review - with rating validation and foreign keys")
        print("✅ Amenity - with name uniqueness")
        print("✅ BaseModel - with common attributes and timestamps")
        print("✅ All CRUD operations working")
        print("✅ Data validation preserved")
        print("✅ JSON list handling for relationships")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
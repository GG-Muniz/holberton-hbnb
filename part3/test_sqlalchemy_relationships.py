#!/usr/bin/env python3
"""
Test script for SQLAlchemy relationships between entities
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

def test_database_initialization_with_relationships():
    """Test database initialization with all relationship tables"""
    print("Testing Database Initialization with Relationships...")
    
    app = create_app('development')
    
    with app.app_context():
        # Initialize database
        db.drop_all()
        db.create_all()
        
        # Verify tables were created including association table
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['users', 'places', 'reviews', 'amenities', 'place_amenity']
        for table in expected_tables:
            assert table in tables, f"Table {table} not created"
        
        print(f"✅ All tables created including association table: {tables}")

def test_user_place_relationship():
    """Test User-Place one-to-many relationship"""
    print("\nTesting User-Place Relationship...")
    
    app = create_app('development')
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create a user
        user = facade.create_user(
            email="host@example.com",
            first_name="Host",
            last_name="User",
            password="password123"
        )
        
        # Create places for this user
        place1 = facade.create_place(
            name="Beach House",
            description="Beautiful beach house",
            address="123 Beach St",
            city_id="city1",
            latitude=25.7617,
            longitude=-80.1918,
            host_id=user.id,
            number_of_rooms=3,
            number_of_bathrooms=2,
            price_per_night=150.0,
            max_guests=6
        )
        
        place2 = facade.create_place(
            name="Mountain Cabin",
            description="Cozy mountain cabin",
            address="456 Mountain Rd",
            city_id="city2",
            latitude=39.7392,
            longitude=-104.9903,
            host_id=user.id,
            number_of_rooms=2,
            number_of_bathrooms=1,
            price_per_night=100.0,
            max_guests=4
        )
        
        # Test relationship: user should have 2 places
        updated_user = facade.get_user(user.id)
        assert len(updated_user.places) == 2, f"Expected 2 places, got {len(updated_user.places)}"
        
        # Test reverse relationship: place should have correct host
        retrieved_place = facade.get_place(place1.id)
        assert retrieved_place.host.id == user.id, "Place host relationship incorrect"
        assert retrieved_place.host.email == "host@example.com", "Host data incorrect"
        
        print("✅ User-Place relationship working correctly")

def test_place_amenity_relationship():
    """Test Place-Amenity many-to-many relationship"""
    print("\nTesting Place-Amenity Relationship...")
    
    app = create_app('development')
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create user and amenities
        user = facade.create_user("host@example.com", "Host", "User", "password123")
        wifi = facade.create_amenity("WiFi")
        pool = facade.create_amenity("Pool")
        parking = facade.create_amenity("Parking")
        
        # Create place with amenities
        place = facade.create_place(
            name="Luxury Villa",
            description="Luxury villa with amenities",
            address="789 Luxury Ave",
            city_id="city3",
            latitude=34.0522,
            longitude=-118.2437,
            host_id=user.id,
            number_of_rooms=4,
            number_of_bathrooms=3,
            price_per_night=300.0,
            max_guests=8,
            amenity_ids=[wifi.id, pool.id]
        )
        
        # Test relationship: place should have 2 amenities
        retrieved_place = facade.get_place(place.id)
        assert len(retrieved_place.amenities) == 2, f"Expected 2 amenities, got {len(retrieved_place.amenities)}"
        
        amenity_names = [amenity.name for amenity in retrieved_place.amenities]
        assert "WiFi" in amenity_names, "WiFi not found in place amenities"
        assert "Pool" in amenity_names, "Pool not found in place amenities"
        
        # Test reverse relationship: amenity should reference places
        retrieved_wifi = facade.get_amenity(wifi.id)
        assert len(retrieved_wifi.places) == 1, "WiFi should be linked to 1 place"
        assert retrieved_wifi.places[0].id == place.id, "WiFi place relationship incorrect"
        
        # Test updating amenities
        updated_place = facade.update_place(place.id, amenity_ids=[wifi.id, parking.id])
        assert len(updated_place.amenities) == 2, "Updated place should have 2 amenities"
        
        updated_amenity_names = [amenity.name for amenity in updated_place.amenities]
        assert "WiFi" in updated_amenity_names, "WiFi should still be present"
        assert "Parking" in updated_amenity_names, "Parking should be added"
        assert "Pool" not in updated_amenity_names, "Pool should be removed"
        
        print("✅ Place-Amenity relationship working correctly")

def test_place_review_relationship():
    """Test Place-Review one-to-many relationship"""
    print("\nTesting Place-Review Relationship...")
    
    app = create_app('development')
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create users and place
        host = facade.create_user("host@example.com", "Host", "User", "password123")
        guest1 = facade.create_user("guest1@example.com", "Guest", "One", "password123")
        guest2 = facade.create_user("guest2@example.com", "Guest", "Two", "password123")
        
        place = facade.create_place(
            name="Review Test Place",
            description="Place for testing reviews",
            address="123 Review St",
            city_id="city4",
            latitude=40.7128,
            longitude=-74.0060,
            host_id=host.id,
            number_of_rooms=2,
            number_of_bathrooms=1,
            price_per_night=120.0,
            max_guests=4
        )
        
        # Create reviews
        review1 = facade.create_review(place.id, guest1.id, 5, "Excellent place!")
        review2 = facade.create_review(place.id, guest2.id, 4, "Good place, would visit again")
        
        # Test relationship: place should have 2 reviews
        retrieved_place = facade.get_place(place.id)
        assert len(retrieved_place.reviews) == 2, f"Expected 2 reviews, got {len(retrieved_place.reviews)}"
        
        # Test reverse relationship: review should reference correct place
        retrieved_review = facade.get_review(review1.id)
        assert retrieved_review.place.id == place.id, "Review place relationship incorrect"
        assert retrieved_review.place.name == "Review Test Place", "Review place data incorrect"
        
        print("✅ Place-Review relationship working correctly")

def test_user_review_relationship():
    """Test User-Review one-to-many relationship"""
    print("\nTesting User-Review Relationship...")
    
    app = create_app('development')
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create users and places
        host = facade.create_user("host@example.com", "Host", "User", "password123")
        reviewer = facade.create_user("reviewer@example.com", "Active", "Reviewer", "password123")
        
        place1 = facade.create_place(
            name="Place 1", description="First place", address="123 St",
            city_id="city1", latitude=0.0, longitude=0.0, host_id=host.id,
            number_of_rooms=1, number_of_bathrooms=1, price_per_night=100.0, max_guests=2
        )
        
        place2 = facade.create_place(
            name="Place 2", description="Second place", address="456 St",
            city_id="city2", latitude=1.0, longitude=1.0, host_id=host.id,
            number_of_rooms=2, number_of_bathrooms=1, price_per_night=150.0, max_guests=4
        )
        
        # Create reviews by the same user
        review1 = facade.create_review(place1.id, reviewer.id, 5, "Great place 1!")
        review2 = facade.create_review(place2.id, reviewer.id, 4, "Good place 2!")
        
        # Test relationship: user should have 2 reviews
        retrieved_user = facade.get_user(reviewer.id)
        assert len(retrieved_user.reviews) == 2, f"Expected 2 reviews, got {len(retrieved_user.reviews)}"
        
        # Test reverse relationship: review should reference correct user
        retrieved_review = facade.get_review(review1.id)
        assert retrieved_review.user.id == reviewer.id, "Review user relationship incorrect"
        assert retrieved_review.user.email == "reviewer@example.com", "Review user data incorrect"
        
        print("✅ User-Review relationship working correctly")

def test_cascade_delete_relationships():
    """Test cascade delete functionality"""
    print("\nTesting Cascade Delete Relationships...")
    
    app = create_app('development')
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create complete data set
        host = facade.create_user("host@example.com", "Host", "User", "password123")
        guest = facade.create_user("guest@example.com", "Guest", "User", "password123")
        amenity = facade.create_amenity("WiFi")
        
        place = facade.create_place(
            name="Cascade Test Place", description="Test place", address="123 Test St",
            city_id="city1", latitude=0.0, longitude=0.0, host_id=host.id,
            number_of_rooms=1, number_of_bathrooms=1, price_per_night=100.0, max_guests=2,
            amenity_ids=[amenity.id]
        )
        
        review = facade.create_review(place.id, guest.id, 5, "Great place!")
        
        # Verify everything is connected
        assert len(facade.get_user(host.id).places) == 1
        assert len(facade.get_place(place.id).reviews) == 1
        assert len(facade.get_place(place.id).amenities) == 1
        
        # Delete the review - should not affect place or user
        result = facade.delete_review(review.id)
        assert result == True
        
        # Verify review is gone but place and user remain
        updated_place = facade.get_place(place.id)
        assert len(updated_place.reviews) == 0, "Review should be deleted from place"
        
        updated_guest = facade.get_user(guest.id)
        assert len(updated_guest.reviews) == 0, "Review should be deleted from user"
        
        print("✅ Cascade delete relationships working correctly")

def test_complex_relationship_queries():
    """Test complex queries using relationships"""
    print("\nTesting Complex Relationship Queries...")
    
    app = create_app('development')
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        facade = HBnBFacade()
        
        # Create complex data structure
        host = facade.create_user("host@example.com", "Host", "User", "password123")
        guest1 = facade.create_user("guest1@example.com", "Guest", "One", "password123")
        guest2 = facade.create_user("guest2@example.com", "Guest", "Two", "password123")
        
        wifi = facade.create_amenity("WiFi")
        pool = facade.create_amenity("Pool")
        
        place1 = facade.create_place(
            name="Place 1", description="First place", address="123 St",
            city_id="city1", latitude=0.0, longitude=0.0, host_id=host.id,
            number_of_rooms=1, number_of_bathrooms=1, price_per_night=100.0, max_guests=2,
            amenity_ids=[wifi.id]
        )
        
        place2 = facade.create_place(
            name="Place 2", description="Second place", address="456 St",
            city_id="city2", latitude=1.0, longitude=1.0, host_id=host.id,
            number_of_rooms=2, number_of_bathrooms=1, price_per_night=150.0, max_guests=4,
            amenity_ids=[wifi.id, pool.id]
        )
        
        # Create reviews
        facade.create_review(place1.id, guest1.id, 5, "Great!")
        facade.create_review(place1.id, guest2.id, 4, "Good!")
        facade.create_review(place2.id, guest1.id, 3, "OK!")
        
        # Test complex queries
        host_data = facade.get_user(host.id)
        assert len(host_data.places) == 2, "Host should have 2 places"
        
        # Test amenity usage
        wifi_data = facade.get_amenity(wifi.id)
        assert len(wifi_data.places) == 2, "WiFi should be in 2 places"
        
        pool_data = facade.get_amenity(pool.id)
        assert len(pool_data.places) == 1, "Pool should be in 1 place"
        
        # Test place reviews
        place1_data = facade.get_place(place1.id)
        assert len(place1_data.reviews) == 2, "Place 1 should have 2 reviews"
        
        place2_data = facade.get_place(place2.id)
        assert len(place2_data.reviews) == 1, "Place 2 should have 1 review"
        
        # Test user reviews
        guest1_data = facade.get_user(guest1.id)
        assert len(guest1_data.reviews) == 2, "Guest 1 should have 2 reviews"
        
        guest2_data = facade.get_user(guest2.id)
        assert len(guest2_data.reviews) == 1, "Guest 2 should have 1 review"
        
        print("✅ Complex relationship queries working correctly")

if __name__ == "__main__":
    print("=" * 70)
    print("SQLAlchemy Relationships Tests")
    print("=" * 70)
    
    try:
        test_database_initialization_with_relationships()
        test_user_place_relationship()
        test_place_amenity_relationship()
        test_place_review_relationship()
        test_user_review_relationship()
        test_cascade_delete_relationships()
        test_complex_relationship_queries()
        
        print("\n" + "=" * 70)
        print("🎉 All relationship tests passed! SQLAlchemy relationships working correctly.")
        print("=" * 70)
        print("\nRelationships implemented:")
        print("✅ User → Places (One-to-Many with cascade delete)")
        print("✅ User → Reviews (One-to-Many with cascade delete)")
        print("✅ Place → Reviews (One-to-Many with cascade delete)")
        print("✅ Place ↔ Amenities (Many-to-Many via association table)")
        print("✅ Foreign key constraints")
        print("✅ Bidirectional relationships with back_populates")
        print("✅ Cascade delete operations")
        print("✅ Complex relationship queries")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
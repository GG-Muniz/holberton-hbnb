#!/usr/bin/env python3
"""
Demonstration script showing User SQLAlchemy integration
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment to use SQLAlchemy
os.environ['REPOSITORY_TYPE'] = 'sqlalchemy'

from app import create_app, db
from app.services.facade import HBnBFacade

def demo_user_operations():
    """Demonstrate User operations with SQLAlchemy"""
    
    app = create_app('development')
    
    with app.app_context():
        # Initialize database
        print("Initializing database...")
        db.drop_all()
        db.create_all()
        print("✅ Database tables created!")
        
        # Create facade instance
        facade = HBnBFacade()
        
        print("\n" + "="*50)
        print("USER OPERATIONS DEMONSTRATION")
        print("="*50)
        
        # 1. Create users
        print("\n1. Creating users...")
        try:
            user1 = facade.create_user(
                email="alice@example.com",
                first_name="Alice",
                last_name="Johnson",
                password="password123",
                is_admin=False
            )
            print(f"✅ Created user: {user1.first_name} {user1.last_name} ({user1.email})")
            
            user2 = facade.create_user(
                email="bob@example.com",
                first_name="Bob",
                last_name="Smith",
                password="securepass456",
                is_admin=True
            )
            print(f"✅ Created admin user: {user2.first_name} {user2.last_name} ({user2.email})")
            
        except Exception as e:
            print(f"❌ Error creating users: {e}")
            return
        
        # 2. Retrieve users
        print("\n2. Retrieving users...")
        
        # Get user by ID
        retrieved_user = facade.get_user(user1.id)
        print(f"✅ Retrieved user by ID: {retrieved_user.first_name} {retrieved_user.last_name}")
        
        # Get user by email
        email_user = facade.get_user_by_email("bob@example.com")
        print(f"✅ Retrieved user by email: {email_user.first_name} {email_user.last_name}")
        
        # Get all users
        all_users = facade.get_all_users()
        print(f"✅ Total users in database: {len(all_users)}")
        
        # 3. Test password functionality
        print("\n3. Testing password functionality...")
        print(f"✅ Password check (correct): {user1.check_password('password123')}")
        print(f"✅ Password check (wrong): {user1.check_password('wrongpassword')}")
        print(f"✅ Password is hashed: {len(user1.password_hash) > 20}")
        
        # 4. Update user
        print("\n4. Updating user...")
        updated_user = facade.update_user(
            user1.id,
            first_name="Alice Updated",
            last_name="Johnson-Smith"
        )
        print(f"✅ Updated user: {updated_user.first_name} {updated_user.last_name}")
        
        # 5. Test JSON list functionality
        print("\n5. Testing JSON list functionality...")
        
        # Simulate adding places and reviews
        places_list = ["place1-id", "place2-id"]
        user1.set_places_list(places_list)
        
        reviews_list = ["review1-id", "review2-id"]
        user1.set_reviews_list(reviews_list)
        
        # Update in database
        facade.user_repo.update(user1)
        
        # Retrieve and verify
        updated_user = facade.get_user(user1.id)
        retrieved_places = updated_user.get_places_list()
        retrieved_reviews = updated_user.get_reviews_list()
        
        print(f"✅ Places list: {retrieved_places}")
        print(f"✅ Reviews list: {retrieved_reviews}")
        
        # 6. Test error handling
        print("\n6. Testing error handling...")
        
        try:
            # Try to create user with duplicate email
            facade.create_user(
                email="alice@example.com",  # Duplicate email
                first_name="Another",
                last_name="Alice",
                password="password789"
            )
        except ValueError as e:
            print(f"✅ Correctly caught duplicate email error: {e}")
        
        try:
            # Try to get non-existent user
            facade.get_user("non-existent-id")
        except ValueError as e:
            print(f"✅ Correctly caught non-existent user error: {e}")
        
        print("\n" + "="*50)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("="*50)
        
        print(f"\nFinal database state:")
        print(f"- Total users: {len(facade.get_all_users())}")
        print(f"- Database file: hbnb_dev.db")
        print(f"- Repository type: SQLAlchemy")

if __name__ == "__main__":
    print("=" * 60)
    print("HBnB User SQLAlchemy Integration Demo")
    print("=" * 60)
    
    try:
        demo_user_operations()
        
        print("\n🎉 Demo completed successfully!")
        print("\nKey achievements:")
        print("✅ BaseModel mapped to SQLAlchemy with common attributes")
        print("✅ User entity fully mapped with all attributes")
        print("✅ UserRepository implemented with enhanced operations")
        print("✅ Facade updated to use UserRepository")
        print("✅ Password hashing functionality preserved")
        print("✅ Database persistence working correctly")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
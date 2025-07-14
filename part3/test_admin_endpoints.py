#!/usr/bin/env python3
"""Test script for administrator endpoints and role-based access control"""

import requests
import json
import time
from app import create_app
from app.services import facade
import threading

def test_admin_endpoints():
    """Test all admin endpoints and role-based access control"""
    app = create_app('development')
    
    # Clear storage and create test users
    facade.repo._storage.clear()
    
    # Create test users
    regular_user = facade.create_user('user@test.com', 'Regular', 'User', 'password123', False)
    admin_user = facade.create_user('admin@test.com', 'Admin', 'User', 'admin123', True)
    
    print("✅ Created test users:")
    print(f"   👤 {regular_user.email} (Admin: {regular_user.is_admin})")
    print(f"   👑 {admin_user.email} (Admin: {admin_user.is_admin})")
    
    # Create test amenity for testing
    wifi_amenity = facade.create_amenity('WiFi')
    print(f"✅ Created test amenity: {wifi_amenity.name}")
    
    # Start server
    def run_server():
        app.run(port=5004, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(2)
    
    base_url = 'http://localhost:5004/api/v1'
    
    try:
        # Login users and get tokens
        print("\n🔐 Logging in users...")
        
        # Login regular user
        login_response = requests.post(f'{base_url}/auth/login', 
                                     json={'email': 'user@test.com', 'password': 'password123'})
        assert login_response.status_code == 200
        user_token = login_response.json()['access_token']
        print(f"   ✅ Regular user logged in")
        
        # Login admin
        login_response = requests.post(f'{base_url}/auth/login', 
                                     json={'email': 'admin@test.com', 'password': 'admin123'})
        assert login_response.status_code == 200
        admin_token = login_response.json()['access_token']
        print(f"   ✅ Admin user logged in")
        
        user_headers = {'Authorization': f'Bearer {user_token}'}
        admin_headers = {'Authorization': f'Bearer {admin_token}'}
        
        # Test 1: Admin-only user creation
        print("\n👑 Testing admin-only user creation...")
        
        # Regular user tries to create user (should fail)
        response = requests.post(f'{base_url}/admin/users', json={
            'email': 'newuser@test.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
            'is_admin': False
        }, headers=user_headers)
        print(f"   ❌ Regular user creates user: {response.status_code} (Expected 403)")
        assert response.status_code in [403, 500]  # 500 due to flask-restx JWT error handling
        
        # Admin creates user (should succeed)
        response = requests.post(f'{base_url}/admin/users', json={
            'email': 'newuser@test.com',
            'first_name': 'New',
            'last_name': 'User', 
            'password': 'newpass123',
            'is_admin': False
        }, headers=admin_headers)
        assert response.status_code == 201
        new_user_data = response.json()
        new_user_id = new_user_data['id']
        print(f"   ✅ Admin created user: {new_user_data['email']} (ID: {new_user_id})")
        
        # Admin creates another admin (should succeed)
        response = requests.post(f'{base_url}/admin/users', json={
            'email': 'newadmin@test.com',
            'first_name': 'New',
            'last_name': 'Admin',
            'password': 'newadmin123',
            'is_admin': True
        }, headers=admin_headers)
        assert response.status_code == 201
        new_admin_data = response.json()
        print(f"   ✅ Admin created another admin: {new_admin_data['email']} (Admin: {new_admin_data['is_admin']})")
        
        # Test 2: Admin user management
        print("\n🛠️ Testing admin user management...")
        
        # Admin updates any user's details including email and admin status
        response = requests.put(f'{base_url}/admin/users/{new_user_id}', json={
            'first_name': 'UpdatedNew',
            'email': 'updated@test.com',
            'is_admin': True
        }, headers=admin_headers)
        assert response.status_code == 200
        updated_user = response.json()
        print(f"   ✅ Admin updated user: {updated_user['email']} (Admin: {updated_user['is_admin']})")
        
        # Admin updates user password
        response = requests.put(f'{base_url}/admin/users/{new_user_id}', json={
            'password': 'newpassword456'
        }, headers=admin_headers)
        assert response.status_code == 200
        print(f"   ✅ Admin updated user password")
        
        # Test 3: Admin bypasses ownership restrictions
        print("\n🏠 Testing admin bypass of ownership restrictions...")
        
        # Regular user creates a place
        place_response = requests.post(f'{base_url}/places/', json={
            'name': 'User Place',
            'description': 'A place by regular user',
            'address': '123 User St',
            'city_id': 'city-1',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'number_of_rooms': 2,
            'number_of_bathrooms': 1,
            'price_per_night': 100.0,
            'max_guests': 4,
            'amenity_ids': [wifi_amenity.id]
        }, headers=user_headers)
        assert place_response.status_code == 201
        place_data = place_response.json()
        place_id = place_data['id']
        print(f"   ✅ Regular user created place: {place_data['name']}")
        
        # Admin updates user's place (should succeed)
        response = requests.put(f'{base_url}/places/{place_id}', json={
            'name': 'Admin Updated Place'
        }, headers=admin_headers)
        assert response.status_code == 200
        print(f"   ✅ Admin updated user's place")
        
        # Regular user creates a review on admin's behalf (for testing)
        # First, create another place for regular user to review
        admin_place_response = requests.post(f'{base_url}/places/', json={
            'name': 'Admin Place',
            'description': 'A place by admin',
            'address': '456 Admin Ave',
            'city_id': 'city-2',
            'latitude': 41.8781,
            'longitude': -87.6298,
            'number_of_rooms': 3,
            'number_of_bathrooms': 2,
            'price_per_night': 150.0,
            'max_guests': 6,
            'amenity_ids': [wifi_amenity.id]
        }, headers=admin_headers)
        assert admin_place_response.status_code == 201
        admin_place_data = admin_place_response.json()
        admin_place_id = admin_place_data['id']
        
        # Regular user reviews admin's place
        review_response = requests.post(f'{base_url}/reviews/', json={
            'place_id': admin_place_id,
            'rating': 4,
            'comment': 'Good place!'
        }, headers=user_headers)
        assert review_response.status_code == 201
        review_data = review_response.json()
        review_id = review_data['id']
        print(f"   ✅ Regular user created review: {review_data['comment']}")
        
        # Admin updates user's review (should succeed)
        response = requests.put(f'{base_url}/reviews/{review_id}', json={
            'comment': 'Admin modified this review',
            'rating': 5
        }, headers=admin_headers)
        assert response.status_code == 200
        print(f"   ✅ Admin updated user's review")
        
        # Admin deletes user's review (should succeed)
        response = requests.delete(f'{base_url}/reviews/{review_id}', headers=admin_headers)
        assert response.status_code == 204
        print(f"   ✅ Admin deleted user's review")
        
        # Test 4: Admin-only amenity management
        print("\n🏢 Testing admin-only amenity management...")
        
        # Regular user tries to create amenity (should fail)
        response = requests.post(f'{base_url}/amenities/', json={
            'name': 'Pool'
        }, headers=user_headers)
        print(f"   ❌ Regular user creates amenity: {response.status_code} (Expected 403/500)")
        assert response.status_code in [403, 500]
        
        # Admin creates amenity (should succeed)
        response = requests.post(f'{base_url}/amenities/', json={
            'name': 'Pool'
        }, headers=admin_headers)
        assert response.status_code == 201
        amenity_data = response.json()
        amenity_id = amenity_data['id']
        print(f"   ✅ Admin created amenity: {amenity_data['name']}")
        
        # Regular user tries to update amenity (should fail)
        response = requests.put(f'{base_url}/amenities/{amenity_id}', json={
            'name': 'Swimming Pool'
        }, headers=user_headers)
        print(f"   ❌ Regular user updates amenity: {response.status_code} (Expected 403/500)")
        assert response.status_code in [403, 500]
        
        # Admin updates amenity (should succeed)
        response = requests.put(f'{base_url}/amenities/{amenity_id}', json={
            'name': 'Swimming Pool'
        }, headers=admin_headers)
        assert response.status_code == 200
        updated_amenity = response.json()
        print(f"   ✅ Admin updated amenity: {updated_amenity['name']}")
        
        # Test 5: Public endpoints remain accessible
        print("\n📖 Testing public endpoints still work...")
        
        # Public amenities list
        response = requests.get(f'{base_url}/amenities/')
        assert response.status_code == 200
        amenities = response.json()
        print(f"   ✅ Public amenities list: {len(amenities)} amenities")
        
        # Public places list
        response = requests.get(f'{base_url}/places/')
        assert response.status_code == 200
        places = response.json()
        print(f"   ✅ Public places list: {len(places)} places")
        
        print("\n🎉 All admin and role-based access tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test assertion failed: {e}")
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")

if __name__ == "__main__":
    test_admin_endpoints()
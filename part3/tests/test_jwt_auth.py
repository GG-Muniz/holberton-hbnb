#!/usr/bin/env python3
"""Test script for JWT authentication"""

import requests
import json
import time
from app import create_app
from app.services.facade import HBnBFacade
import threading

def test_jwt_authentication():
    """Test the complete JWT authentication flow"""
    app = create_app('development')
    
    # Create test users using the shared facade
    from app.services import facade
    
    # Clear any existing users and create fresh ones
    facade.repo._storage.clear()
    
    # Create a regular user
    user = facade.create_user(
        email='testuser@example.com',
        first_name='Test',
        last_name='User',
        password='testpass123',
        is_admin=False
    )
    print(f"✅ Created regular user: {user.email}")
    
    # Create an admin user
    admin = facade.create_user(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        password='adminpass123',
        is_admin=True
    )
    print(f"✅ Created admin user: {admin.email}")
    
    # Start server in background
    def run_server():
        app.run(port=5002, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(2)  # Wait for server to start
    
    try:
        # Test 1: Login with regular user
        print("\n🔐 Testing login with regular user...")
        login_response = requests.post('http://localhost:5002/api/v1/auth/login', 
                                     json={
                                         'email': 'testuser@example.com',
                                         'password': 'testpass123'
                                     })
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            print("✅ Login successful!")
            print(f"   User: {login_data['user']['email']}")
            print(f"   Is Admin: {login_data['user']['is_admin']}")
            
            # Test protected endpoint
            token = login_data['access_token']
            headers = {'Authorization': f'Bearer {token}'}
            
            protected_response = requests.get('http://localhost:5002/api/v1/auth/protected',
                                            headers=headers)
            
            if protected_response.status_code == 200:
                protected_data = protected_response.json()
                print("✅ Protected endpoint access successful!")
                print(f"   Message: {protected_data['message']}")
                print(f"   Is Admin in token: {protected_data['is_admin']}")
            else:
                print(f"❌ Protected endpoint failed: {protected_response.status_code}")
                print(f"   Error: {protected_response.text}")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"   Error: {login_response.text}")
        
        # Test 2: Login with admin user
        print("\n🔐 Testing login with admin user...")
        admin_login_response = requests.post('http://localhost:5002/api/v1/auth/login', 
                                           json={
                                               'email': 'admin@example.com',
                                               'password': 'adminpass123'
                                           })
        
        if admin_login_response.status_code == 200:
            admin_login_data = admin_login_response.json()
            print("✅ Admin login successful!")
            print(f"   User: {admin_login_data['user']['email']}")
            print(f"   Is Admin: {admin_login_data['user']['is_admin']}")
            
            # Test protected endpoint with admin token
            admin_token = admin_login_data['access_token']
            admin_headers = {'Authorization': f'Bearer {admin_token}'}
            
            admin_protected_response = requests.get('http://localhost:5002/api/v1/auth/protected',
                                                  headers=admin_headers)
            
            if admin_protected_response.status_code == 200:
                admin_protected_data = admin_protected_response.json()
                print("✅ Admin protected endpoint access successful!")
                print(f"   Message: {admin_protected_data['message']}")
                print(f"   Is Admin in token: {admin_protected_data['is_admin']}")
            else:
                print(f"❌ Admin protected endpoint failed: {admin_protected_response.status_code}")
        else:
            print(f"❌ Admin login failed: {admin_login_response.status_code}")
            print(f"   Error: {admin_login_response.text}")
        
        # Test 3: Invalid credentials
        print("\n🔐 Testing invalid credentials...")
        invalid_response = requests.post('http://localhost:5002/api/v1/auth/login', 
                                       json={
                                           'email': 'testuser@example.com',
                                           'password': 'wrongpassword'
                                       })
        
        if invalid_response.status_code == 401:
            print("✅ Invalid credentials properly rejected!")
        else:
            print(f"❌ Invalid credentials test failed: {invalid_response.status_code}")
        
        # Test 4: Protected endpoint without token
        print("\n🔐 Testing protected endpoint without token...")
        no_token_response = requests.get('http://localhost:5002/api/v1/auth/protected')
        
        if no_token_response.status_code == 401:
            print("✅ Protected endpoint properly requires token!")
            print(f"   Message: {no_token_response.json().get('message', 'No message')}")
        else:
            print(f"❌ Protected endpoint security test failed: {no_token_response.status_code}")
        
        print("\n🎉 JWT Authentication tests completed!")
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")

if __name__ == "__main__":
    test_jwt_authentication()
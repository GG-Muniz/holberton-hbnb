#!/usr/bin/env python3
"""
Test script for HBnB API
Run this after starting the Flask app to verify all endpoints
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000/api/v1"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Track test results
total_tests = 0
passed_tests = 0

def print_test_header(test_name):
    """Print test section header"""
    print(f"\n{'='*50}")
    print(f"Testing: {test_name}")
    print(f"{'='*50}")

def test_endpoint(method, endpoint, data=None, expected_status=200, test_name=""):
    """Test an endpoint and return response"""
    global total_tests, passed_tests
    total_tests += 1

    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)

        if response.status_code == expected_status:
            print(f"{GREEN}✓ {test_name or endpoint}: {response.status_code} (Expected: {expected_status}){RESET}")
            passed_tests += 1
            return response
        else:
            print(f"{RED}✗ {test_name or endpoint}: {response.status_code} (Expected: {expected_status}){RESET}")
            print(f"  Response: {response.text[:100]}...")
            return response

    except requests.exceptions.ConnectionError:
        print(f"{RED}✗ Connection Error: Is the Flask app running on {BASE_URL}?{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}✗ Error: {str(e)}{RESET}")
        return None

def run_tests():
    """Run all API tests"""

    # Store IDs for later tests
    user_id = None
    host_id = None
    place_id = None
    review_id = None
    amenity_ids = []

    # Test 1: User Endpoints
    print_test_header("USER ENDPOINTS")

    # Create users
    user_data = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test123"
    }
    response = test_endpoint("POST", "/users/", user_data, 201, "Create user")
    if response and response.status_code == 201:
        user_id = response.json().get("id")
        # verify password not in response
        if "password" not in response.json():
            print(f"{GREEN}✓ Password correctly excluded from response{RESET}")
        else:
            print(f"{RED}✗ Password should not be in response{RESET}")

    # Create host
    host_data = {
        "email": f"host_{datetime.now().timestamp()}@example.com",
        "first_name": "Host",
        "last_name": "User",
        "password": "host123"
    }
    response = test_endpoint("POST", "/users/", host_data, 201, "Create host")
    if response and response.status_code == 201:
        host_id = response.json().get("id")

    # Test duplicate email
    test_endpoint("POST", "/users/", user_data, 400, "Duplicate email")

    # Test invalid email
    invalid_email = {
        "email": "not-an-email",
        "first_name": "Invalid",
        "last_name": "Email",
        "password": "test123"
    }
    test_endpoint("POST", "/users/", invalid_email, 400, "Invalid email format")

    # Get all users
    test_endpoint("GET", "/users/", expected_status=200, test_name="Get all users")

    # Get specific user
    if user_id:
        test_endpoint("GET", f"/users/{user_id}", expected_status=200, test_name="Get user by ID")
        test_endpoint("GET", "/users/invalid-id", expected_status=404, test_name="Get non-existent user")

    # Update user
    if user_id:
        update_data = {"first_name": "Updated", "last_name": "Name"}
        test_endpoint("PUT", f"/users/{user_id}", update_data, 200, "Update user")

    # Test 2: Amenity Endpoints
    print_test_header("AMENITY ENDPOINTS")

    amenities = ["WiFi", "Pool", "Parking", "Air Conditioning"]
    for amenity_name in amenities:
        response = test_endpoint("POST", "/amenities/", {"name": amenity_name}, 201, f"Create {amenity_name}")
        if response and response.status_code == 201:
            amenity_ids.append(response.json().get("id"))

    # Test duplicate amenity
    test_endpoint("POST", "/amenities/", {"name": "WiFi"}, 400, "Duplicate amenity")

    # Test empty name
    test_endpoint("POST", "/amenities/", {"name": ""}, 400, "Empty amenity name")

    # Get amenities
    test_endpoint("GET", "/amenities/", expected_status=200, test_name="Get all amenities")

    # Test 3: Place Endpoints
    print_test_header("PLACE ENDPOINTS")

    if host_id and amenity_ids:
        place_data = {
            "name": "Test Beach House",
            "description": "A beautiful test property",
            "address": "123 Test Street",
            "city_id": "test-city-1",
            "latitude": 33.9425,
            "longitude": -118.4081,
            "host_id": host_id,
            "number_of_rooms": 3,
            "number_of_bathrooms": 2,
            "price_per_night": 150.00,
            "max_guests": 6,
            "amenity_ids": amenity_ids[:2]  # first two amenities
        }
        response = test_endpoint("POST", "/places/", place_data, 201, "Create place")
        if response and response.status_code == 201:
            place_id = response.json().get("id")
            # verify nested data
            place_json = response.json()
            if "host" in place_json and place_json["host"]["id"] == host_id:
                print(f"{GREEN}✓ Host details correctly included{RESET}")
            if "amenities" in place_json and len(place_json["amenities"]) == 2:
                print(f"{GREEN}✓ Amenities correctly included{RESET}")

    # Test invalid host
    invalid_place = place_data.copy()
    invalid_place["host_id"] = "invalid-host-id"
    test_endpoint("POST", "/places/", invalid_place, 400, "Invalid host ID")

    # Test negative price
    negative_price = place_data.copy()
    negative_price["price_per_night"] = -50
    test_endpoint("POST", "/places/", negative_price, 400, "Negative price")

    # Test invalid coordinates
    invalid_coords = place_data.copy()
    invalid_coords["latitude"] = 200  # invalid
    test_endpoint("POST", "/places/", invalid_coords, 400, "Invalid latitude")

    # Get place
    if place_id:
        response = test_endpoint("GET", f"/places/{place_id}", expected_status=200, test_name="Get place with details")
        if response and response.status_code == 200:
            place_json = response.json()
            if "reviews" in place_json:
                print(f"{GREEN}✓ Reviews array included (empty){RESET}")

    # Test 4: Review Endpoints
    print_test_header("REVIEW ENDPOINTS")

    if place_id and user_id:
        review_data = {
            "place_id": place_id,
            "user_id": user_id,
            "rating": 5,
            "comment": "Excellent place for testing!"
        }
        response = test_endpoint("POST", "/reviews/", review_data, 201, "Create review")
        if response and response.status_code == 201:
            review_id = response.json().get("id")
            # verify user details included
            if "user" in response.json():
                print(f"{GREEN}✓ User details correctly included in review{RESET}")

        # Test duplicate review
        test_endpoint("POST", "/reviews/", review_data, 400, "Duplicate review (same user/place)")

        # Test invalid rating
        invalid_rating = review_data.copy()
        invalid_rating["rating"] = 6
        invalid_rating["user_id"] = host_id  # different user
        test_endpoint("POST", "/reviews/", invalid_rating, 400, "Invalid rating (>5)")

        # Test empty comment
        empty_comment = review_data.copy()
        empty_comment["comment"] = ""
        empty_comment["user_id"] = host_id
        test_endpoint("POST", "/reviews/", empty_comment, 400, "Empty comment")

        # Get reviews by place
        response = test_endpoint("GET", f"/reviews/places/{place_id}", expected_status=200, test_name="Get place reviews")
        if response and response.status_code == 200:
            reviews = response.json()
            if len(reviews) == 1 and reviews[0]["id"] == review_id:
                print(f"{GREEN}✓ Correct reviews returned for place{RESET}")

        # Update review
        if review_id:
            update_review = {"rating": 4, "comment": "Updated: Still great!"}
            test_endpoint("PUT", f"/reviews/{review_id}", update_review, 200, "Update review")

        # Delete review
        if review_id:
            test_endpoint("DELETE", f"/reviews/{review_id}", expected_status=204, test_name="Delete review")
            # Verify deletion
            test_endpoint("GET", f"/reviews/{review_id}", expected_status=404, test_name="Verify review deleted")

    # Print summary
    print(f"\n{'='*50}")
    print(f"TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Total Tests: {total_tests}")
    print(f"{GREEN}Passed: {passed_tests}{RESET}")
    print(f"{RED}Failed: {total_tests - passed_tests}{RESET}")

    if passed_tests == total_tests:
        print(f"\n{GREEN}All tests passed! The API is working correctly.{RESET}")
        return 0
    else:
        print(f"\n{YELLOW}Some tests failed. Please check the implementation.{RESET}")
        return 1

if __name__ == "__main__":
    print("HBnB API Automated Test Suite")
    print(f"Testing against: {BASE_URL}")
    print("\nMake sure the Flask app is running before running these tests!")

    exit_code = run_tests()
    sys.exit(exit_code)

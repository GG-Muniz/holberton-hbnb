# HBnB Evolution: Part 2 - Implementation

## Overview
This is Part 2 of the HBnB Evolution project, where we implement the API and business logic layer using Flask, Flask-RESTx, and the Facade pattern. The implementation includes a complete RESTful API with in-memory data storage that will be replaced with a database in Part 3.

## Project Structure
```
part2/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py
│   └── services/
│       ├── __init__.py
│       └── facade.py
├── config.py
├── requirements.txt
├── run.py
├── test_hbnb.py
└── automated_test_script.py
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd holbertonschool-hbnb/part2
```

### 2. Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python run.py
```

The API will be available at `http://localhost:5000`
API documentation (Swagger UI) at `http://localhost:5000/api/docs`

## Tasks

### Task 0: Project Setup and Package Initialization

**Objective**
Set up the initial project structure for the HBnB application, ensuring the codebase is organized according to best practices for a modular Python application. The focus is on creating the necessary folders, packages, and files for the Presentation, Business Logic, and Persistence layers while preparing the code to integrate the Facade pattern.

**Context**
Before diving into the implementation of the business logic and API endpoints, it's essential to have a well-organized project structure. A clear and modular organization will help maintain the codebase, make it easier to integrate new features, and ensure that your application is scalable.

**Key Components:**
- **Presentation Layer**: Flask-RESTx API endpoints
- **Business Logic Layer**: Services and Facade pattern
- **Persistence Layer**: In-memory repository (to be replaced with SQLAlchemy in Part 3)
- **Models**: Core business entities

**Expected Outcome**
A well-organized project structure with:
- Clear separation of concerns between layers
- Modular and maintainable codebase
- Functional Flask application ready for API endpoint integration
- In-memory repository for data storage
- Facade pattern for clean layer communication

### Task 1: Core Business Logic Classes

**Objective**
Implement the core business logic classes that define the entities of the HBnB application, including the necessary attributes, methods, and relationships.

**Models Implemented:**
1. **BaseModel**
   - `id`: UUID string
   - `created_at`: DateTime
   - `updated_at`: DateTime
   - Methods: `save()`, `to_dict()`

2. **User**
   - Attributes: `email`, `first_name`, `last_name`, `password`
   - Validation: Email format, non-empty names
   - Security: Password never returned in API responses

3. **Place**
   - Attributes: `name`, `description`, `address`, `city_id`, `latitude`, `longitude`, `host_id`, `number_of_rooms`, `number_of_bathrooms`, `price_per_night`, `max_guests`, `amenity_ids`
   - Validation: Positive price, valid coordinates (-90 to 90 lat, -180 to 180 lon)
   - Relationships: Linked to User (host) and Amenities

4. **Review**
   - Attributes: `place_id`, `user_id`, `rating`, `comment`
   - Validation: Rating 1-5, non-empty comment
   - Business Rule: One review per user per place

5. **Amenity**
   - Attributes: `name`
   - Validation: Unique name, max 50 characters

**Expected Outcome**
Fully implemented business logic classes with proper validation, relationships, and data integrity checks.

### Task 2: User Endpoints

**Objective**
Implement the API endpoints needed for managing users in the HBnB application.

**Endpoints:**
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get a specific user
- `PUT /api/v1/users/{user_id}` - Update user information

**Key Features:**
- Password acceptance on creation but never returned in responses
- Email uniqueness validation
- Proper error handling with appropriate status codes
- No DELETE operation for users

**Expected Outcome**
Fully functional user management endpoints with proper validation and security measures.

### Task 3: Amenity Endpoints

**Objective**
Implement the API endpoints required for managing amenities in the HBnB application.

**Endpoints:**
- `POST /api/v1/amenities/` - Create a new amenity
- `GET /api/v1/amenities/` - Get all amenities
- `GET /api/v1/amenities/{amenity_id}` - Get a specific amenity
- `PUT /api/v1/amenities/{amenity_id}` - Update amenity information

**Key Features:**
- Unique amenity names enforced
- Name length validation
- No DELETE operation for amenities

**Expected Outcome**
Complete amenity management system with uniqueness constraints and validation.

### Task 4: Place Endpoints

**Objective**
Implement the API endpoints needed for managing places in the HBnB application.

**Endpoints:**
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/` - Get all places with full details
- `GET /api/v1/places/{place_id}` - Get a specific place with details
- `PUT /api/v1/places/{place_id}` - Update place information

**Key Features:**
- Validation of host existence
- Coordinate and price validation
- Returns nested data (host details, amenities, reviews)
- Amenity association management
- No DELETE operation for places

**Expected Outcome**
Fully functional place management with proper relationship handling and data validation.

### Task 5: Review Endpoints

**Objective**
Implement the API endpoints needed for managing reviews in the HBnB application. This is the only entity with DELETE functionality.

**Endpoints:**
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/` - Get all reviews
- `GET /api/v1/reviews/{review_id}` - Get a specific review
- `PUT /api/v1/reviews/{review_id}` - Update review
- `DELETE /api/v1/reviews/{review_id}` - Delete a review
- `GET /api/v1/reviews/places/{place_id}` - Get all reviews for a place

**Key Features:**
- One review per user per place enforcement
- Rating validation (1-5)
- Comment requirement
- DELETE operation supported
- Reviews linked to both users and places

**Expected Outcome**
Complete review system with all CRUD operations and proper business rule enforcement.

### Task 6: Testing and Validation

**Objective**
Create and run comprehensive tests for all endpoints, ensuring proper validation and error handling.

**Testing Components:**
1. **Unit Tests** (`test_hbnb.py`)
   - Model validation tests
   - Facade method tests
   - Business rule enforcement tests

2. **Integration Tests** (`automated_test_script.py`)
   - Full API endpoint testing
   - Error case handling
   - Status code verification

3. **Manual Testing**
   - cURL commands for all endpoints
   - Swagger UI testing
   - Edge case validation

**Expected Outcome**
- Complete test coverage for all components
- Documented test results
- Validation of all business rules
- Proper error handling verification

## API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Status Codes
- `200 OK` - Successful GET/PUT
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation error
- `404 Not Found` - Resource not found

### Example API Calls

#### Create User
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "secure123"
  }'
```

#### Create Place
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Beach House",
    "description": "Beautiful beach house",
    "address": "123 Beach St",
    "city_id": "city-123",
    "latitude": 34.0522,
    "longitude": -118.2437,
    "host_id": "<user-id>",
    "number_of_rooms": 3,
    "number_of_bathrooms": 2,
    "price_per_night": 150.00,
    "max_guests": 6,
    "amenity_ids": ["<amenity-id-1>", "<amenity-id-2>"]
  }'
```

## Testing

### Run Unit Tests
```bash
python test_hbnb.py
```

### Run Automated API Tests
```bash
# Make sure the Flask app is running first
python automated_test_script.py
```

### Access Swagger Documentation
Open browser to: `http://localhost:5000/api/docs`

## Key Features Implemented

1. **Data Validation**
   - Email format validation
   - Coordinate boundary checks
   - Price positivity validation
   - Rating range enforcement (1-5)
   - Required field validation

2. **Business Rules**
   - Unique email addresses
   - One review per user/place
   - Unique amenity names
   - Host existence validation
   - Review-place-user relationships

3. **Security**
   - Passwords accepted but never returned
   - Proper error messages without exposing internals
   - Input validation on all endpoints

4. **API Features**
   - RESTful design
   - Consistent error responses
   - Nested data where appropriate
   - Comprehensive Swagger documentation

## Future Enhancements (Part 3)

1. **Database Integration**
   - Replace in-memory repository with SQLAlchemy
   - Add database migrations
   - Implement data persistence

2. **Authentication & Authorization**
   - JWT token implementation
   - User login/logout
   - Protected endpoints

3. **Additional Features**
   - Search and filtering
   - Pagination
   - Image uploads
   - Email notifications

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [Python OOP Guide](https://realpython.com/python3-object-oriented-programming/)
- [RESTful API Design](https://restfulapi.net/)
- [Facade Pattern](https://refactoring.guru/design-patterns/facade/python/example)

## Repository
- **Author**: Gabriel Garcia Muniz
- **GitHub repository**: holbertonschool-hbnb
- **Directory**: part2

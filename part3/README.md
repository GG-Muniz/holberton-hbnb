# HBnB Evolution: Part 3 - Database Implementation

**Author**: Gabriel Garcia Muniz  
**GitHub**: [https://github.com/GG-Muniz](https://github.com/GG-Muniz)  
**Project**: Holberton School HBnB Application - Part 3

## Overview

This is Part 3 of the HBnB Evolution project, where we implement database persistence using SQLAlchemy ORM. This part transitions from in-memory storage to a robust database solution with comprehensive relationships, constraints, and visual documentation using Mermaid.js diagrams.

## Key Features

- **Database Persistence**: SQLAlchemy ORM with SQLite/MySQL support
- **Entity Relationships**: One-to-Many and Many-to-Many relationships
- **Data Validation**: Comprehensive constraints and business rules
- **Visual Documentation**: Complete ER diagrams with Mermaid.js
- **Repository Pattern**: Abstract data access layer
- **Authentication**: JWT-based user authentication
- **Admin System**: Administrative user management
- **Comprehensive Testing**: Unit, integration, and database tests

## Project Structure

```
part3/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── config.py                    # Application configuration
├── run.py                       # Flask application entry point
│
├── app/                         # Main application package
│   ├── __init__.py             # Flask app factory with API setup
│   ├── api/                    # REST API endpoints
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── admin.py        # Admin endpoints
│   │       ├── amenities.py    # Amenity CRUD endpoints
│   │       ├── auth.py         # Authentication & JWT endpoints
│   │       ├── places.py       # Place CRUD endpoints
│   │       ├── reviews.py      # Review CRUD endpoints
│   │       └── users.py        # User CRUD endpoints
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base_model.py       # Base model (UUID, timestamps)
│   │   ├── user.py             # User entity with auth
│   │   ├── place.py            # Place entity with relationships
│   │   ├── review.py           # Review entity with constraints
│   │   └── amenity.py          # Amenity entity
│   ├── persistence/            # Data access layer
│   │   ├── __init__.py
│   │   ├── repository.py       # Abstract repository interface
│   │   ├── repository_manager.py # Repository factory pattern
│   │   ├── sqlalchemy_repository.py # SQLAlchemy implementation
│   │   └── user_repository.py  # User-specific repository methods
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   └── facade.py           # Facade pattern for business logic
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── admin.py            # Admin helper functions
│
├── diagrams/                   # Database visualization (Mermaid.js)
│   ├── database_er_diagram.md      # Complete ER diagram
│   ├── table_structure_diagrams.md # Individual table schemas
│   ├── relationship_diagrams.md    # Relationship patterns
│   └── MERMAID_QUICK_REFERENCE.md  # Quick diagram reference
│
├── docs/                       # Documentation
│   ├── DATABASE_DIAGRAMS_README.md # Comprehensive diagram guide
│   └── SQL_README.md               # SQL scripts documentation
│
├── sql/                        # Database scripts
│   ├── schema.sql              # Database schema creation
│   └── data.sql                # Initial data (admin + amenities)
│
├── tests/                      # Test suites (10 Python, 1 SQL)
│   ├── test_admin_endpoints.py        # Admin API tests
│   ├── test_all_entities_sqlalchemy.py # Entity CRUD tests
│   ├── test_authenticated_endpoints.py # Auth API tests
│   ├── test_crud_operations.sql       # SQL CRUD tests
│   ├── test_jwt_auth.py              # JWT authentication tests
│   ├── test_mermaid_diagrams.py      # Diagram validation tests
│   ├── test_repository_integration.py # Repository layer tests
│   ├── test_script.py                # General test utilities
│   ├── test_sqlalchemy_relationships.py # Relationship tests
│   ├── test_sqlite_schema.py         # SQLite schema validation
│   ├── test_user_sqlalchemy.py       # User model tests
│   ├── test_results.txt              # Test execution results
│   └── swagger_run_results.txt       # API testing results
│
├── scripts/                    # Utility scripts
│   ├── run_sql_scripts.sh      # Automated database setup
│   └── init_db.py              # Database initialization
│
├── demos/                      # Demo and example code
│   └── demo_user_sqlalchemy.py # SQLAlchemy usage examples
│
├── instance/                   # Flask instance folder
│   └── hbnb_dev.db             # SQLite development database
│
└── venv/                       # Virtual environment
    └── ...                     # Python packages and dependencies
```

## Quick Start

### 1. Setup Environment

```bash
cd part3
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup

**Option A - Automated (Recommended):**
```bash
cd scripts
./run_sql_scripts.sh
```

**Option B - Quick SQLite Setup:**
```bash
cd tests
python3 test_sqlite_schema.py
```

### 3. Initialize and Run Application

```bash
# Set environment for SQLAlchemy
export REPOSITORY_TYPE=sqlalchemy

# Initialize database (if needed)
python3 scripts/init_db.py

# Start Flask application
python3 run.py
```

### 4. Access the Application

- **API Documentation**: http://localhost:5000/api/docs
- **API Base URL**: http://localhost:5000/api/v1
- **Interactive Swagger UI**: Test all endpoints directly in browser
- **Default Admin**: admin@hbnb.com / admin123

## Database Architecture

### Entities and Relationships

The application implements a comprehensive rental property management schema:

#### Core Entities
- **Users**: Account management with authentication and password hashing
- **Places**: Property listings with location, pricing, and host relationships
- **Reviews**: User feedback and ratings with constraints
- **Amenities**: Property features and facilities

#### Relationships
- **User → Places** (1:Many): Users can host multiple properties
- **User → Reviews** (1:Many): Users can write multiple reviews
- **Place → Reviews** (1:Many): Places can receive multiple reviews
- **Place ↔ Amenities** (Many:Many): Flexible feature assignments via association table

### Database Features
- UUID-based primary keys for distributed systems
- Comprehensive foreign key constraints with cascade deletes
- Data validation through check constraints (coordinates, ratings, prices)
- Performance optimization with strategic indexing
- Secure password hashing with bcrypt

## API Features

### Authentication System
- JWT-based authentication
- Password hashing with bcrypt
- Admin and regular user roles
- Protected endpoints

### Endpoints Overview
- **Users**: Create, read, update user accounts
- **Places**: Manage property listings with amenities
- **Reviews**: Full CRUD operations with business rules
- **Amenities**: Manage property features
- **Auth**: Login, registration, token management
- **Admin**: Administrative operations

### Data Validation
- Email format validation
- Geographic coordinate bounds (-90 to 90 lat, -180 to 180 lon)
- Price positivity validation
- Rating range enforcement (1-5)
- Unique constraints (emails, amenity names)
- One review per user per place

## Testing

### Run All Tests

```bash
# Database tests
cd tests
python3 test_sqlite_schema.py              # Schema validation  
python3 test_sqlalchemy_relationships.py   # Relationship testing

# Application tests  
python3 test_repository_integration.py     # Repository layer
python3 test_authenticated_endpoints.py    # API endpoints
python3 test_admin_endpoints.py           # Admin functionality
python3 test_all_entities_sqlalchemy.py   # Entity CRUD operations
python3 test_jwt_auth.py                  # JWT authentication
python3 test_user_sqlalchemy.py          # User model tests

# Diagram validation
python3 test_mermaid_diagrams.py          # Mermaid syntax validation
```

### Database Setup Tests

```bash
# Test complete database setup
cd scripts
./run_sql_scripts.sh

# Test SQL schema in SQLite
cd tests
python3 test_sqlite_schema.py
```

## Visual Documentation

### Database Diagrams

The project includes comprehensive ER diagrams created with Mermaid.js:

#### Viewing Options
1. **Online**: https://mermaid-live.github.io/
   - Copy diagram code from `diagrams/*.md` files
   - Paste into editor for interactive viewing

2. **GitHub Integration**: All diagrams render automatically in GitHub

3. **Local CLI**: 
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   mmdc -i diagrams/database_er_diagram.md -o database_diagram.png
   ```

#### Available Diagrams
- **Complete ER Diagram**: All entities and relationships (`diagrams/database_er_diagram.md`)
- **Table Structures**: Individual table schemas with constraints (`diagrams/table_structure_diagrams.md`)
- **Relationship Patterns**: Focused relationship examples (`diagrams/relationship_diagrams.md`)
- **Quick Reference**: Usage guide for all diagrams (`diagrams/MERMAID_QUICK_REFERENCE.md`)

## Configuration

### Environment Variables

```bash
# Repository type selection
export REPOSITORY_TYPE=sqlalchemy  # or 'memory'

# Database configuration (optional)
export DATABASE_URL=sqlite:///instance/hbnb_dev.db

# Flask configuration
export FLASK_ENV=development
export FLASK_DEBUG=1
```

### Default Data

The application includes initial data:
- **Admin User**: admin@hbnb.com (password: admin123)
- **Amenities**: 15 common property amenities (WiFi, Pool, Parking, etc.)
- **Sample Places**: Demo properties for testing

## Example API Usage

### Authentication
```bash
# Login to get JWT token
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.com", "password": "admin123"}'
```

### Create a Place
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{
    "name": "Beach House",
    "description": "Beautiful oceanfront property",
    "address": "123 Ocean Drive",
    "city_id": "city-miami",
    "latitude": 25.7617,
    "longitude": -80.1918,
    "host_id": "<user-id>",
    "number_of_rooms": 3,
    "number_of_bathrooms": 2,
    "price_per_night": 299.99,
    "max_guests": 6,
    "amenity_ids": ["<amenity-id-1>", "<amenity-id-2>"]
  }'
```

## Development Features

### Repository Pattern
- Abstract repository interface for data access
- SQLAlchemy and in-memory implementations
- Easy switching between storage backends
- Repository manager for dependency injection

### Facade Pattern
- Clean separation between API and business logic
- Centralized business rule enforcement
- Simplified controller logic
- Easy testing and maintenance

### Error Handling
- Comprehensive validation with meaningful error messages
- Proper HTTP status codes
- Input sanitization and validation
- Graceful failure handling

## API Documentation

### Interactive Swagger UI
Access the complete API documentation at: **http://localhost:5000/api/docs**

The Swagger UI provides:
- Interactive testing of all endpoints
- Request/response schemas
- Authentication token management
- Real-time API exploration

### Available API Endpoints
- **`/api/v1/auth`** - Authentication (login, register, tokens)
- **`/api/v1/users`** - User management (CRUD operations)
- **`/api/v1/places`** - Place listings (CRUD with relationships)
- **`/api/v1/reviews`** - Review system (full CRUD with constraints)
- **`/api/v1/amenities`** - Amenity features (CRUD operations)
- **`/api/v1/admin`** - Administrative operations

## Documentation

For comprehensive documentation, see:
- **docs/DATABASE_DIAGRAMS_README.md**: Detailed diagram documentation
- **docs/SQL_README.md**: SQL scripts and database setup guide
- **diagrams/MERMAID_QUICK_REFERENCE.md**: Quick diagram reference

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Mermaid.js Documentation](https://mermaid.js.org/)
- [Flask-RESTx](https://flask-restx.readthedocs.io/)

## Repository Information

- **Author**: Gabriel Garcia Muniz
- **GitHub**: [https://github.com/GG-Muniz](https://github.com/GG-Muniz)
- **Repository**: holbertonschool-hbnb
- **Directory**: part3
- **Institution**: Holberton School
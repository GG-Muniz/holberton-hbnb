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
├── PROJECT_README.md            # Comprehensive project documentation
├── DIRECTORY_STRUCTURE.md       # Detailed directory explanation
├── requirements.txt             # Python dependencies
├── config.py                    # Application configuration
├── run.py                       # Flask application entry point
│
├── app/                         # Main application package
│   ├── __init__.py             # Flask app factory
│   ├── api/                    # REST API endpoints
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── admin.py        # Admin endpoints
│   │       ├── amenities.py    # Amenity endpoints
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── places.py       # Place endpoints
│   │       ├── reviews.py      # Review endpoints
│   │       └── users.py        # User endpoints
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base_model.py       # Base model with common fields
│   │   ├── user.py             # User entity model
│   │   ├── place.py            # Place entity model
│   │   ├── review.py           # Review entity model
│   │   └── amenity.py          # Amenity entity model
│   ├── persistence/            # Data persistence layer
│   │   ├── __init__.py
│   │   ├── repository.py       # Abstract repository interface
│   │   ├── repository_manager.py # Repository factory
│   │   ├── sqlalchemy_repository.py # SQLAlchemy implementation
│   │   └── user_repository.py  # User-specific repository
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   └── facade.py           # Application facade pattern
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── admin.py            # Admin utilities
│
├── diagrams/                   # Database visualization
│   ├── database_er_diagram.md      # Complete ER diagram
│   ├── table_structure_diagrams.md # Individual table schemas
│   ├── relationship_diagrams.md    # Relationship patterns
│   └── MERMAID_QUICK_REFERENCE.md  # Diagram usage guide
│
├── docs/                       # Documentation
│   ├── DATABASE_DIAGRAMS_README.md # Comprehensive diagram guide
│   └── SQL_README.md               # SQL scripts documentation
│
├── sql/                        # Database scripts
│   ├── schema.sql              # Database schema creation
│   └── data.sql                # Initial data insertion
│
├── tests/                      # Test suites
│   ├── test_*.py               # Python test files
│   ├── test_*.sql              # SQL test files
│   ├── test_results.txt        # Test execution results
│   └── swagger_run_results.txt # API testing results
│
├── scripts/                    # Utility scripts
│   ├── run_sql_scripts.sh      # Database setup automation
│   └── init_db.py              # Database initialization
│
├── demos/                      # Demo and example files
│   └── demo_user_sqlalchemy.py # SQLAlchemy usage examples
│
├── instance/                   # Instance-specific files
│   └── hbnb_dev.db             # SQLite development database
│
└── venv/                       # Virtual environment
    └── ...
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

- **API Documentation**: http://localhost:5000
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
python3 test_sqlite_schema.py           # Schema validation
python3 test_sqlalchemy_relationships.py # Relationship testing

# Application tests
python3 test_repository_integration.py  # Repository layer
python3 test_authenticated_endpoints.py # API endpoints
python3 test_admin_endpoints.py        # Admin functionality

# Diagram validation
python3 test_mermaid_diagrams.py       # Mermaid syntax check
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
- **Complete ER Diagram**: All entities and relationships
- **Table Structures**: Individual table schemas with constraints
- **Relationship Patterns**: Focused relationship examples
- **Quick Reference**: Usage guide for all diagrams

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

## Documentation

For comprehensive documentation, see:
- **PROJECT_README.md**: Complete project overview and setup
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
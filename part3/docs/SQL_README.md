# HBnB Database SQL Scripts

**Author**: Gabriel Garcia Muniz  
**GitHub**: [https://github.com/GG-Muniz](https://github.com/GG-Muniz)  
**Project**: HBnB Database SQL Implementation

This directory contains SQL scripts for creating and managing the HBnB application database schema and initial data.

## Files Overview

### Core SQL Scripts

1. **`schema.sql`** - Database schema creation script
2. **`data.sql`** - Initial data insertion script  
3. **`test_crud_operations.sql`** - CRUD operations testing script

### Utility Scripts

4. **`run_sql_scripts.sh`** - Bash script to execute all SQL scripts with MySQL
5. **`test_sqlite_schema.py`** - Python script to test schema with SQLite

## Database Schema

### Tables Created

1. **`users`** - User accounts and authentication
2. **`amenities`** - Available amenities for places
3. **`places`** - Property listings with details
4. **`reviews`** - User reviews for places
5. **`place_amenity`** - Association table for place-amenity relationships

### Relationships

- **User → Places**: One-to-Many (host owns multiple places)
- **User → Reviews**: One-to-Many (user writes multiple reviews)  
- **Place → Reviews**: One-to-Many (place has multiple reviews)
- **Place ↔ Amenities**: Many-to-Many (via association table)

### Key Features

- ✅ **Primary Keys**: UUID-based unique identifiers
- ✅ **Foreign Keys**: Proper referential integrity
- ✅ **Cascade Deletes**: Automatic cleanup of related records
- ✅ **Check Constraints**: Data validation at database level
- ✅ **Unique Constraints**: Prevent duplicate data
- ✅ **Indexes**: Optimized query performance

## Usage Instructions

### Option 1: MySQL Database

1. **Prerequisites**:
   ```bash
   # Install MySQL
   sudo apt install mysql-server
   
   # Start MySQL service
   sudo systemctl start mysql
   ```

2. **Execute scripts**:
   ```bash
   # Make script executable
   chmod +x run_sql_scripts.sh
   
   # Run all scripts
   ./run_sql_scripts.sh
   ```

3. **Manual execution**:
   ```bash
   # Create database
   mysql -u root -p -e "CREATE DATABASE hbnb_dev;"
   
   # Execute schema
   mysql -u root -p hbnb_dev < schema.sql
   
   # Insert initial data
   mysql -u root -p hbnb_dev < data.sql
   
   # Run tests
   mysql -u root -p hbnb_dev < test_crud_operations.sql
   ```

### Option 2: SQLite Testing

```bash
# Test schema with SQLite
python3 test_sqlite_schema.py
```

## Initial Data Included

### Administrator User
- **Email**: admin@hbnb.com
- **Password**: admin123 (hashed)
- **Role**: Administrator

### Amenities (15 total)
- WiFi
- Swimming Pool  
- Parking
- Gym
- Spa
- Restaurant
- Bar
- Laundry Service
- Concierge
- Room Service
- Air Conditioning
- Heating
- Kitchen
- Balcony
- Garden

### Sample Places (2 for testing)
- Luxury Beach House (Miami)
- Cozy Mountain Cabin (Aspen)

## Schema Validation

The scripts include comprehensive testing for:

### Create Operations
- ✅ User creation with validation
- ✅ Place creation with host relationship
- ✅ Review creation with constraints
- ✅ Amenity associations

### Read Operations
- ✅ Simple SELECT queries
- ✅ Complex JOIN operations
- ✅ Aggregate functions (COUNT, AVG)
- ✅ Relationship traversal

### Update Operations
- ✅ User information updates
- ✅ Place detail modifications
- ✅ Review rating changes
- ✅ Timestamp automatic updates

### Delete Operations
- ✅ Cascade delete verification
- ✅ Foreign key constraint testing
- ✅ Data integrity maintenance

## Constraints and Validation

### Data Validation
```sql
-- Latitude and longitude bounds
CONSTRAINT chk_places_latitude CHECK (latitude >= -90 AND latitude <= 90)
CONSTRAINT chk_places_longitude CHECK (longitude >= -180 AND longitude <= 180)

-- Positive values
CONSTRAINT chk_places_price CHECK (price_per_night >= 0)
CONSTRAINT chk_places_rooms CHECK (number_of_rooms >= 0)

-- Review ratings
CONSTRAINT chk_reviews_rating CHECK (rating >= 1 AND rating <= 5)
```

### Unique Constraints
```sql
-- Prevent duplicate user emails
email VARCHAR(120) NOT NULL UNIQUE

-- Prevent duplicate amenity names
name VARCHAR(50) NOT NULL UNIQUE

-- Prevent duplicate reviews
CONSTRAINT uk_reviews_user_place UNIQUE (user_id, place_id)
```

### Foreign Key Relationships
```sql
-- Place belongs to user (host)
CONSTRAINT fk_places_host FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE

-- Review belongs to place and user
CONSTRAINT fk_reviews_place FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
CONSTRAINT fk_reviews_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

## Performance Optimization

### Indexes Created
```sql
-- User lookups
CREATE INDEX idx_users_email ON users(email);

-- Place queries
CREATE INDEX idx_places_host_id ON places(host_id);
CREATE INDEX idx_places_city_id ON places(city_id);
CREATE INDEX idx_places_price ON places(price_per_night);

-- Review queries
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- Amenity lookups
CREATE INDEX idx_amenities_name ON amenities(name);
```

## Troubleshooting

### Common Issues

1. **MySQL Connection Errors**:
   - Verify MySQL is running: `sudo systemctl status mysql`
   - Check credentials and permissions
   - Ensure database exists

2. **Permission Denied**:
   ```bash
   chmod +x run_sql_scripts.sh
   chmod +x test_sqlite_schema.py
   ```

3. **Foreign Key Constraint Failures**:
   - Ensure parent records exist before creating child records
   - Check cascade delete settings

4. **Data Type Mismatches**:
   - Verify UUIDs are 36-character strings
   - Check datetime formats
   - Validate numeric ranges

### Testing Individual Components

```bash
# Test only schema creation
mysql -u root -p hbnb_dev < schema.sql

# Test only data insertion
mysql -u root -p hbnb_dev < data.sql

# Test only CRUD operations
mysql -u root -p hbnb_dev < test_crud_operations.sql
```

## Integration with Application

These SQL scripts complement the SQLAlchemy models in the application:

- **Schema matches SQLAlchemy definitions**
- **Foreign keys align with relationship() definitions**
- **Constraints mirror model validation rules**
- **Initial data provides working test environment**

The database created by these scripts is fully compatible with the Flask-SQLAlchemy application and can be used as a starting point for development and testing.

---

**Created by Gabriel Garcia Muniz** | [GitHub](https://github.com/GG-Muniz) | Holberton School 2024
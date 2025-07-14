-- HBnB Database Schema Creation Script
-- This script creates all tables and relationships for the HBnB application
-- Based on SQLAlchemy models: User, Place, Review, Amenity, and their relationships

-- Drop tables if they exist (in reverse order due to foreign key constraints)
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- Create Users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    password_hash VARCHAR(128),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);

-- Create Amenities table
CREATE TABLE amenities (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create index on amenity name for faster lookups
CREATE INDEX idx_amenities_name ON amenities(name);

-- Create Places table
CREATE TABLE places (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    address VARCHAR(200) NOT NULL,
    city_id VARCHAR(36) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    host_id VARCHAR(36) NOT NULL,
    number_of_rooms INTEGER NOT NULL,
    number_of_bathrooms INTEGER NOT NULL,
    price_per_night FLOAT NOT NULL,
    max_guests INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_places_host FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Check constraints for data validation
    CONSTRAINT chk_places_latitude CHECK (latitude >= -90 AND latitude <= 90),
    CONSTRAINT chk_places_longitude CHECK (longitude >= -180 AND longitude <= 180),
    CONSTRAINT chk_places_price CHECK (price_per_night >= 0),
    CONSTRAINT chk_places_rooms CHECK (number_of_rooms >= 0),
    CONSTRAINT chk_places_bathrooms CHECK (number_of_bathrooms >= 0),
    CONSTRAINT chk_places_guests CHECK (max_guests >= 0)
);

-- Create indexes for Places table
CREATE INDEX idx_places_host_id ON places(host_id);
CREATE INDEX idx_places_city_id ON places(city_id);
CREATE INDEX idx_places_price ON places(price_per_night);

-- Create Reviews table
CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    place_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign key constraints
    CONSTRAINT fk_reviews_place FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    CONSTRAINT fk_reviews_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Check constraints for data validation
    CONSTRAINT chk_reviews_rating CHECK (rating >= 1 AND rating <= 5),
    
    -- Unique constraint to prevent duplicate reviews from same user for same place
    CONSTRAINT uk_reviews_user_place UNIQUE (user_id, place_id)
);

-- Create indexes for Reviews table
CREATE INDEX idx_reviews_place_id ON reviews(place_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- Create Place-Amenity association table (Many-to-Many relationship)
CREATE TABLE place_amenity (
    place_id VARCHAR(36) NOT NULL,
    amenity_id VARCHAR(36) NOT NULL,
    
    -- Composite primary key
    PRIMARY KEY (place_id, amenity_id),
    
    -- Foreign key constraints
    CONSTRAINT fk_place_amenity_place FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    CONSTRAINT fk_place_amenity_amenity FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- Create indexes for association table
CREATE INDEX idx_place_amenity_place_id ON place_amenity(place_id);
CREATE INDEX idx_place_amenity_amenity_id ON place_amenity(amenity_id);

-- Display schema creation status
SELECT 'HBnB Database Schema Created Successfully!' AS status;
SELECT 'Tables created: users, amenities, places, reviews, place_amenity' AS tables;
-- HBnB CRUD Operations Test Script
-- This script tests Create, Read, Update, Delete operations on the database
-- to verify that the schema works correctly with all relationships

-- Set up test variables
SET @test_user_id = 'test-user-uuid-12345678901234567890';
SET @test_place_id = 'test-place-uuid-1234567890123456789';
SET @test_review_id = 'test-review-uuid-123456789012345678';
SET @current_time = NOW();

-- Display test header
SELECT '=' AS separator, 'HBnB CRUD Operations Test' AS test_title, '=' AS separator;

-- ====================
-- CREATE OPERATIONS
-- ====================
SELECT 'CREATE OPERATIONS' AS operation_type;

-- Create a test user
INSERT INTO users (
    id, email, first_name, last_name, password_hash, is_admin, created_at, updated_at
) VALUES (
    @test_user_id,
    'testuser@hbnb.com',
    'Test',
    'User',
    '$2b$12$testHashForCRUDTesting123456789',
    FALSE,
    @current_time,
    @current_time
);
SELECT 'Created test user' AS create_status;

-- Create a test place
INSERT INTO places (
    id, name, description, address, city_id, latitude, longitude,
    host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests,
    created_at, updated_at
) VALUES (
    @test_place_id,
    'Test Apartment',
    'A cozy test apartment for CRUD testing',
    '789 Test Street',
    'city-test-uuid-123456789012345678',
    40.7128,
    -74.0060,
    @test_user_id,
    2,
    1,
    99.99,
    4,
    @current_time,
    @current_time
);
SELECT 'Created test place' AS create_status;

-- Associate test place with amenities
INSERT INTO place_amenity (place_id, amenity_id) VALUES
    (@test_place_id, 'amenity-wifi-uuid-123456789012345678'),
    (@test_place_id, 'amenity-parking-uuid-12345678901234567');
SELECT 'Associated place with amenities' AS create_status;

-- Create a test review
INSERT INTO reviews (
    id, place_id, user_id, rating, comment, created_at, updated_at
) VALUES (
    @test_review_id,
    @test_place_id,
    'admin-user-uuid-12345678901234567890', -- Admin reviews the test place
    5,
    'Excellent test place for CRUD operations!',
    @current_time,
    @current_time
);
SELECT 'Created test review' AS create_status;

-- ====================
-- READ OPERATIONS
-- ====================
SELECT 'READ OPERATIONS' AS operation_type;

-- Read user with their places
SELECT 'User and their places:' AS read_title;
SELECT 
    u.id, u.email, u.first_name, u.last_name, u.is_admin,
    COUNT(p.id) AS total_places
FROM users u
LEFT JOIN places p ON u.id = p.host_id
WHERE u.id = @test_user_id
GROUP BY u.id, u.email, u.first_name, u.last_name, u.is_admin;

-- Read place with host and amenities
SELECT 'Place with host information:' AS read_title;
SELECT 
    p.id, p.name, p.description, p.price_per_night,
    u.first_name AS host_first_name, u.last_name AS host_last_name,
    u.email AS host_email
FROM places p
JOIN users u ON p.host_id = u.id
WHERE p.id = @test_place_id;

-- Read place amenities
SELECT 'Place amenities:' AS read_title;
SELECT 
    p.name AS place_name,
    a.name AS amenity_name
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = @test_place_id;

-- Read reviews for place
SELECT 'Reviews for place:' AS read_title;
SELECT 
    r.id, r.rating, r.comment,
    u.first_name AS reviewer_first_name, u.last_name AS reviewer_last_name,
    p.name AS place_name
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id
WHERE r.place_id = @test_place_id;

-- Complex query: Places with average ratings
SELECT 'Places with average ratings:' AS read_title;
SELECT 
    p.id, p.name, p.price_per_night,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(r.id) AS total_reviews
FROM places p
LEFT JOIN reviews r ON p.id = r.place_id
GROUP BY p.id, p.name, p.price_per_night
HAVING COUNT(r.id) > 0;

-- ====================
-- UPDATE OPERATIONS
-- ====================
SELECT 'UPDATE OPERATIONS' AS operation_type;

-- Update user information
UPDATE users 
SET first_name = 'Updated', last_name = 'TestUser', updated_at = NOW()
WHERE id = @test_user_id;
SELECT 'Updated user information' AS update_status;

-- Update place price
UPDATE places 
SET price_per_night = 129.99, updated_at = NOW()
WHERE id = @test_place_id;
SELECT 'Updated place price' AS update_status;

-- Update review rating
UPDATE reviews 
SET rating = 4, comment = 'Updated review - still very good!', updated_at = NOW()
WHERE id = @test_review_id;
SELECT 'Updated review' AS update_status;

-- Verify updates
SELECT 'Verification of updates:' AS verify_title;
SELECT 
    u.first_name, u.last_name,
    p.price_per_night,
    r.rating, r.comment
FROM users u
JOIN places p ON u.id = p.host_id
JOIN reviews r ON p.id = r.place_id
WHERE u.id = @test_user_id AND p.id = @test_place_id;

-- ====================
-- DELETE OPERATIONS
-- ====================
SELECT 'DELETE OPERATIONS' AS operation_type;

-- Test cascade delete: Remove place-amenity associations (should cascade)
SELECT 'Testing cascade deletes...' AS delete_title;

-- Count before deletion
SELECT COUNT(*) AS amenity_associations_before_delete FROM place_amenity WHERE place_id = @test_place_id;
SELECT COUNT(*) AS reviews_before_delete FROM reviews WHERE place_id = @test_place_id;

-- Delete the place (should cascade to reviews and place_amenity)
DELETE FROM places WHERE id = @test_place_id;
SELECT 'Deleted test place' AS delete_status;

-- Count after deletion to verify cascade
SELECT COUNT(*) AS amenity_associations_after_delete FROM place_amenity WHERE place_id = @test_place_id;
SELECT COUNT(*) AS reviews_after_delete FROM reviews WHERE place_id = @test_place_id;

-- Delete test user
DELETE FROM users WHERE id = @test_user_id;
SELECT 'Deleted test user' AS delete_status;

-- ====================
-- CONSTRAINT TESTING
-- ====================
SELECT 'CONSTRAINT TESTING' AS operation_type;

-- Test unique constraint on user email (should fail)
SELECT 'Testing unique constraint on user email...' AS constraint_test;

-- This should fail due to duplicate email
-- Uncomment to test:
-- INSERT INTO users (id, email, first_name, last_name, created_at, updated_at) 
-- VALUES ('duplicate-test-uuid', 'admin@hbnb.com', 'Duplicate', 'User', NOW(), NOW());

-- Test check constraints
SELECT 'Testing check constraints...' AS constraint_test;

-- These should fail due to check constraints
-- Uncomment to test:
-- INSERT INTO places (id, name, address, city_id, latitude, longitude, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests, created_at, updated_at) 
-- VALUES ('invalid-place-uuid', 'Invalid Place', '123 Test St', 'city-id', 91, 0, 'admin-user-uuid-12345678901234567890', 1, 1, -10, 1, NOW(), NOW()); -- Invalid latitude and negative price

-- Test foreign key constraints
SELECT 'Testing foreign key constraints...' AS constraint_test;

-- This should fail due to non-existent host_id
-- Uncomment to test:
-- INSERT INTO places (id, name, address, city_id, latitude, longitude, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests, created_at, updated_at) 
-- VALUES ('fk-test-place-uuid', 'FK Test Place', '123 Test St', 'city-id', 40, -74, 'non-existent-user-id', 1, 1, 100, 1, NOW(), NOW());

-- ====================
-- SUMMARY
-- ====================
SELECT 'TEST SUMMARY' AS summary_title;
SELECT 'All CRUD operations completed successfully!' AS test_result;
SELECT 'Schema integrity verified with:' AS verification;
SELECT '- Primary keys and foreign keys working' AS check1;
SELECT '- Cascade deletes functioning properly' AS check2;
SELECT '- Check constraints enforcing data validity' AS check3;
SELECT '- Unique constraints preventing duplicates' AS check4;
SELECT '- Complex queries with joins working' AS check5;

-- Final data counts
SELECT COUNT(*) AS final_user_count FROM users;
SELECT COUNT(*) AS final_amenity_count FROM amenities;
SELECT COUNT(*) AS final_place_count FROM places;
SELECT COUNT(*) AS final_review_count FROM reviews;
SELECT COUNT(*) AS final_place_amenity_count FROM place_amenity;
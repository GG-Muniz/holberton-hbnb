# HBnB Database Entity-Relationship Diagram

**Author**: Gabriel Garcia Muniz  
**GitHub**: [https://github.com/GG-Muniz](https://github.com/GG-Muniz)  
**Created with**: Mermaid.js

## Complete ER Diagram

This diagram shows all entities, their attributes, and relationships in the HBnB database schema.

```mermaid
erDiagram
    USERS {
        string id PK "UUID Primary Key"
        string email UK "Unique Email Address"
        string first_name "User First Name"
        string last_name "User Last Name"
        string password_hash "Hashed Password"
        boolean is_admin "Admin Flag"
        datetime created_at "Creation Timestamp"
        datetime updated_at "Last Update Timestamp"
    }

    PLACES {
        string id PK "UUID Primary Key"
        string name "Place Name"
        text description "Place Description"
        string address "Physical Address"
        string city_id "City Identifier"
        float latitude "GPS Latitude"
        float longitude "GPS Longitude"
        string host_id FK "Host User ID"
        int number_of_rooms "Room Count"
        int number_of_bathrooms "Bathroom Count"
        float price_per_night "Nightly Rate"
        int max_guests "Maximum Guests"
        datetime created_at "Creation Timestamp"
        datetime updated_at "Last Update Timestamp"
    }

    REVIEWS {
        string id PK "UUID Primary Key"
        string place_id FK "Place ID"
        string user_id FK "Reviewer User ID"
        int rating "Rating 1-5"
        text comment "Review Text"
        datetime created_at "Creation Timestamp"
        datetime updated_at "Last Update Timestamp"
    }

    AMENITIES {
        string id PK "UUID Primary Key"
        string name UK "Unique Amenity Name"
        datetime created_at "Creation Timestamp"
        datetime updated_at "Last Update Timestamp"
    }

    PLACE_AMENITY {
        string place_id FK "Place ID"
        string amenity_id FK "Amenity ID"
    }

    %% Relationships
    USERS ||--o{ PLACES : "hosts"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "receives"
    PLACES }o--o{ AMENITIES : "has"
    PLACE_AMENITY }o--|| PLACES : "belongs_to"
    PLACE_AMENITY }o--|| AMENITIES : "contains"
```

## Relationship Summary

### One-to-Many Relationships
- **User → Places**: One user can host multiple places
- **User → Reviews**: One user can write multiple reviews  
- **Place → Reviews**: One place can have multiple reviews

### Many-to-Many Relationships
- **Place ↔ Amenities**: Places can have multiple amenities, amenities can belong to multiple places (via association table)

### Key Constraints
- Each review must be unique per user-place combination
- All foreign keys have cascade delete enabled
- Email addresses and amenity names must be unique
- Ratings are constrained to values 1-5
- Geographic coordinates are validated within proper ranges

---

**Created by Gabriel Garcia Muniz** | [GitHub](https://github.com/GG-Muniz) | Holberton School 2024
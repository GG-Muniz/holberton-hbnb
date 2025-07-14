# HBnB Database Relationship Diagrams

**Author**: Gabriel Garcia Muniz  
**GitHub**: [https://github.com/GG-Muniz](https://github.com/GG-Muniz)  
**Created with**: Mermaid.js

## Relationship Types and Patterns

### One-to-Many Relationships

#### User-Places Relationship (Host → Properties)

```mermaid
erDiagram
    USERS {
        string id PK
        string email UK
        string first_name
        string last_name
        boolean is_admin
    }

    PLACES {
        string id PK
        string name
        string address
        string host_id FK
        float price_per_night
        int max_guests
    }

    USERS ||--o{ PLACES : "hosts"
```

**Relationship Details:**
- **Type**: One-to-Many
- **Description**: One user can host multiple places
- **Foreign Key**: `places.host_id` → `users.id`
- **Cascade**: ON DELETE CASCADE (deleting user removes their places)
- **Business Rule**: Every place must have exactly one host

---

#### User-Reviews Relationship (Reviewer → Reviews)

```mermaid
erDiagram
    USERS {
        string id PK
        string email UK
        string first_name
        string last_name
    }

    REVIEWS {
        string id PK
        string user_id FK
        string place_id FK
        int rating
        text comment
    }

    USERS ||--o{ REVIEWS : "writes"
```

**Relationship Details:**
- **Type**: One-to-Many
- **Description**: One user can write multiple reviews
- **Foreign Key**: `reviews.user_id` → `users.id`
- **Cascade**: ON DELETE CASCADE (deleting user removes their reviews)
- **Business Rule**: Each user can only review a place once

---

#### Place-Reviews Relationship (Property → Reviews)

```mermaid
erDiagram
    PLACES {
        string id PK
        string name
        string address
        string host_id FK
        float price_per_night
    }

    REVIEWS {
        string id PK
        string place_id FK
        string user_id FK
        int rating
        text comment
    }

    PLACES ||--o{ REVIEWS : "receives"
```

**Relationship Details:**
- **Type**: One-to-Many
- **Description**: One place can receive multiple reviews
- **Foreign Key**: `reviews.place_id` → `places.id`
- **Cascade**: ON DELETE CASCADE (deleting place removes its reviews)
- **Business Rule**: Reviews are tied to specific places

---

### Many-to-Many Relationship

#### Place-Amenities Relationship (Properties ↔ Features)

```mermaid
erDiagram
    PLACES {
        string id PK
        string name
        string address
        float price_per_night
        int max_guests
    }

    AMENITIES {
        string id PK
        string name UK
    }

    PLACE_AMENITY {
        string place_id FK
        string amenity_id FK
    }

    PLACES }o--o{ AMENITIES : "has"
    PLACE_AMENITY }o--|| PLACES : "belongs_to"
    PLACE_AMENITY }o--|| AMENITIES : "includes"
```

**Relationship Details:**
- **Type**: Many-to-Many
- **Description**: Places can have multiple amenities, amenities can belong to multiple places
- **Association Table**: `place_amenity`
- **Composite Key**: `(place_id, amenity_id)`
- **Cascade**: ON DELETE CASCADE for both foreign keys
- **Business Rule**: Flexible amenity assignments per property

---

## Complete Relationship Flow

### Data Flow and Dependencies

```mermaid
graph TD
    A[USERS] --> B[PLACES]
    A --> C[REVIEWS]
    B --> C
    B --> D[PLACE_AMENITY]
    E[AMENITIES] --> D
    
    subgraph "Primary Entities"
        A
        E
    end
    
    subgraph "Dependent Entities"
        B
        C
    end
    
    subgraph "Association"
        D
    end
    
    style A fill:#e1f5fe
    style E fill:#e1f5fe
    style B fill:#fff3e0
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

**Dependency Order:**
1. **Independent**: Users, Amenities (can exist without others)
2. **Dependent**: Places (require Users as hosts)
3. **Highly Dependent**: Reviews (require both Users and Places)
4. **Association**: Place_Amenity (requires both Places and Amenities)

---

## Cascade Delete Behavior

### Delete Impact Analysis

```mermaid
graph TD
    A[Delete User] --> B[Cascade to Places]
    A --> C[Cascade to Reviews by User]
    B --> D[Cascade to Reviews of Places]
    B --> E[Remove Place-Amenity Links]
    
    F[Delete Place] --> G[Cascade to Reviews]
    F --> H[Remove Place-Amenity Links]
    
    I[Delete Amenity] --> J[Remove Place-Amenity Links]
    
    K[Delete Review] --> L[No Cascades]
    
    style A fill:#ffcdd2
    style F fill:#ffcdd2
    style I fill:#fff9c4
    style K fill:#c8e6c9
```

**Cascade Rules:**
- **User Deletion**: Removes all hosted places, all user reviews, and related associations
- **Place Deletion**: Removes all place reviews and amenity associations
- **Amenity Deletion**: Only removes associations with places
- **Review Deletion**: No cascade effects (safest operation)

---

## Constraint Relationships

### Business Logic Constraints

```mermaid
graph LR
    A[Unique Email] --> B[One Account per Email]
    C[Unique Amenity Names] --> D[No Duplicate Features]
    E[Unique User-Place Review] --> F[One Review per User per Place]
    G[Rating Range 1-5] --> H[Valid Review Scores]
    I[Geographic Bounds] --> J[Valid Coordinates]
    K[Positive Values] --> L[Valid Prices and Counts]
    
    subgraph "Data Integrity"
        A
        C
        E
    end
    
    subgraph "Business Rules"
        G
        I
        K
    end
```

**Constraint Types:**
- **Uniqueness**: Prevent data duplication
- **Range Validation**: Ensure realistic values
- **Referential Integrity**: Maintain relationship consistency
- **Business Logic**: Enforce application rules

---

## Query Pattern Optimization

### Common Query Patterns

```mermaid
graph TD
    A[User Queries] --> B[Find User Places]
    A --> C[Find User Reviews]
    
    D[Place Queries] --> E[Find Place Host]
    D --> F[Find Place Reviews]
    D --> G[Find Place Amenities]
    
    H[Search Queries] --> I[Places by City]
    H --> J[Places by Price Range]
    H --> K[Places by Amenities]
    H --> L[Places by Rating]
    
    M[Analytics] --> N[Average Ratings]
    M --> O[Popular Amenities]
    M --> P[Host Statistics]
```

**Optimized Access Patterns:**
- **User-centric**: Quick access to user's places and reviews
- **Place-centric**: Efficient retrieval of place details and relationships
- **Search-optimized**: Fast filtering by location, price, features
- **Analytics-ready**: Aggregation queries for business insights

---

**Created by Gabriel Garcia Muniz** | [GitHub](https://github.com/GG-Muniz) | Holberton School 2024
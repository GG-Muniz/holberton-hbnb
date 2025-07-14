# HBnB Mermaid Diagrams Quick Reference

**Author**: Gabriel Garcia Muniz  
**GitHub**: [https://github.com/GG-Muniz](https://github.com/GG-Muniz)

## 🎯 Quick Access to Diagrams

### Main ER Diagram
```bash
# View the complete database schema
cat database_er_diagram.md
```
**Contains**: All 5 entities with complete relationships

### Table Structures  
```bash
# View detailed table definitions
cat table_structure_diagrams.md
```
**Contains**: Individual table schemas, constraints, indexes

### Relationships
```bash
# View relationship patterns
cat relationship_diagrams.md  
```
**Contains**: One-to-Many, Many-to-Many relationship examples

## 🔗 Viewing Online

### Mermaid Live Editor
1. Go to: https://mermaid-live.github.io/
2. Copy any diagram code from the markdown files
3. Paste into the editor
4. View interactive diagram

### GitHub Integration
- All diagrams render automatically in GitHub markdown
- View directly in the repository

## 📊 Diagram Summary

| File | Diagrams | Purpose |
|------|----------|---------|
| `database_er_diagram.md` | 1 | Complete schema overview |
| `table_structure_diagrams.md` | 6 | Individual table details |
| `relationship_diagrams.md` | 8 | Relationship patterns |
| **Total** | **15** | **Complete visualization** |

## 🗂️ Entity Quick Reference

```
USERS (Host/Guest accounts)
├── id (PK)
├── email (UK) 
├── first_name, last_name
├── password_hash
└── is_admin

PLACES (Property listings)  
├── id (PK)
├── name, description, address
├── city_id, latitude, longitude
├── host_id (FK → users.id)
├── number_of_rooms, number_of_bathrooms
├── price_per_night, max_guests
└── timestamps

REVIEWS (User feedback)
├── id (PK)  
├── place_id (FK → places.id)
├── user_id (FK → users.id)
├── rating (1-5), comment
└── timestamps

AMENITIES (Property features)
├── id (PK)
├── name (UK)
└── timestamps

PLACE_AMENITY (Many-to-Many association)
├── place_id (FK → places.id)
└── amenity_id (FK → amenities.id)
```

## 🔗 Relationships at a Glance

```
User → Places (1:Many)    User hosts multiple places
User → Reviews (1:Many)   User writes multiple reviews  
Place → Reviews (1:Many)  Place receives multiple reviews
Place ↔ Amenities (M:M)   Places have multiple amenities
```

## ✅ Validation Status

All 15 diagrams have been validated:
- ✅ Valid Mermaid.js syntax
- ✅ Proper ER diagram structure  
- ✅ Accurate schema representation
- ✅ Complete documentation

## 🚀 Next Steps

1. **View diagrams**: Use Mermaid Live Editor for interactive viewing
2. **Reference during development**: Use diagrams for API design
3. **Update as needed**: Keep diagrams synchronized with schema changes
4. **Export for presentations**: Generate PNG/SVG from Mermaid Live Editor

---

**Created by Gabriel Garcia Muniz** | [GitHub](https://github.com/GG-Muniz) | Holberton School 2024
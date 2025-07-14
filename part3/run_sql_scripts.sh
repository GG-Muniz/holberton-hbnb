#!/bin/bash

# HBnB SQL Scripts Execution Script
# This script runs the schema creation, data insertion, and CRUD testing scripts

echo "=========================================="
echo "HBnB Database Setup and Testing Script"
echo "=========================================="

# Database configuration
DB_NAME="hbnb_test"
DB_USER="root"
DB_HOST="localhost"

# Check if MySQL is available
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL is not installed or not in PATH"
    echo "Please install MySQL and try again"
    exit 1
fi

# Function to execute SQL file
execute_sql_file() {
    local file=$1
    local description=$2
    
    echo ""
    echo "🔄 $description..."
    echo "   Executing: $file"
    
    if [ ! -f "$file" ]; then
        echo "❌ File not found: $file"
        return 1
    fi
    
    # Execute the SQL file
    mysql -u"$DB_USER" -p"$DB_NAME" < "$file"
    
    if [ $? -eq 0 ]; then
        echo "✅ $description completed successfully"
    else
        echo "❌ $description failed"
        return 1
    fi
}

# Create database if it doesn't exist
echo "🔄 Creating database if it doesn't exist..."
mysql -u"$DB_USER" -p -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Database ready"
else
    echo "❌ Failed to create database"
    echo "Please check MySQL credentials and try again"
    exit 1
fi

# Execute schema creation
execute_sql_file "schema.sql" "Schema creation"
if [ $? -ne 0 ]; then
    echo "❌ Schema creation failed. Stopping execution."
    exit 1
fi

# Execute data insertion
execute_sql_file "data.sql" "Initial data insertion"
if [ $? -ne 0 ]; then
    echo "❌ Data insertion failed. Stopping execution."
    exit 1
fi

# Execute CRUD testing
execute_sql_file "test_crud_operations.sql" "CRUD operations testing"
if [ $? -ne 0 ]; then
    echo "❌ CRUD testing failed. Stopping execution."
    exit 1
fi

echo ""
echo "=========================================="
echo "🎉 All SQL scripts executed successfully!"
echo "=========================================="
echo ""
echo "Summary:"
echo "✅ Database schema created with all tables and relationships"
echo "✅ Initial data inserted (admin user and amenities)"
echo "✅ CRUD operations tested and verified"
echo ""
echo "Tables created:"
echo "  - users (with admin user)"
echo "  - amenities (15 initial amenities)"
echo "  - places (2 sample places)"
echo "  - reviews"
echo "  - place_amenity (association table)"
echo ""
echo "The database is ready for use!"
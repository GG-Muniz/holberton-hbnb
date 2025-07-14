#!/usr/bin/env python3
"""
Database initialization script for the HBnB application
Creates all tables and sets up the database schema
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def init_database():
    """Initialize the database with all tables"""
    
    # Set environment to use SQLAlchemy
    os.environ['REPOSITORY_TYPE'] = 'sqlalchemy'
    
    # Create the Flask app
    app = create_app('development')
    
    with app.app_context():
        try:
            print("Creating database tables...")
            
            # Drop all tables (for fresh start)
            db.drop_all()
            
            # Create all tables
            db.create_all()
            
            print("✅ Database tables created successfully!")
            print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Created tables: {tables}")
            
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("HBnB Database Initialization")
    print("=" * 50)
    
    success = init_database()
    
    if success:
        print("\n🎉 Database initialization completed successfully!")
        print("\nTo use the application with database persistence:")
        print("1. export REPOSITORY_TYPE=sqlalchemy")
        print("2. python run.py")
    else:
        print("\n❌ Database initialization failed!")
        sys.exit(1)
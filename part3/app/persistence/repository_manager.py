"""Repository manager for handling different repository implementations"""

import os
from app.persistence.repository import InMemoryRepository
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class RepositoryManager:
    """Manager class to handle repository instantiation based on configuration"""
    
    @staticmethod
    def get_repository():
        """Get the appropriate repository based on configuration"""
        
        # Check environment variable to determine repository type
        repo_type = os.environ.get('REPOSITORY_TYPE', 'in_memory')
        
        if repo_type == 'sqlalchemy':
            return SQLAlchemyRepository()
        else:
            # Default to in-memory repository for backwards compatibility
            return InMemoryRepository()
    
    @staticmethod
    def get_sqlalchemy_repository():
        """Force SQLAlchemy repository (for future use when models are mapped)"""
        return SQLAlchemyRepository()
    
    @staticmethod
    def get_in_memory_repository():
        """Force in-memory repository (for testing or fallback)"""
        return InMemoryRepository()
#!/usr/bin/env python3
"""
Test script to verify SQLAlchemy repository integration
Note: This test validates the integration without database initialization
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_repository_manager():
    """Test repository manager functionality"""
    print("Testing Repository Manager...")
    
    from app.persistence.repository_manager import RepositoryManager
    from app.persistence.repository import InMemoryRepository
    from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
    
    # Test default repository (in-memory)
    os.environ.pop('REPOSITORY_TYPE', None)
    repo1 = RepositoryManager.get_repository()
    print(f"Default repository: {type(repo1).__name__}")
    assert isinstance(repo1, InMemoryRepository), "Default should be InMemoryRepository"
    
    # Test in-memory repository explicitly
    repo2 = RepositoryManager.get_in_memory_repository()
    print(f"In-memory repository: {type(repo2).__name__}")
    assert isinstance(repo2, InMemoryRepository), "Should be InMemoryRepository"
    
    # Test SQLAlchemy repository explicitly
    repo3 = RepositoryManager.get_sqlalchemy_repository()
    print(f"SQLAlchemy repository: {type(repo3).__name__}")
    assert isinstance(repo3, SQLAlchemyRepository), "Should be SQLAlchemyRepository"
    
    # Test environment variable switching
    os.environ['REPOSITORY_TYPE'] = 'sqlalchemy'
    repo4 = RepositoryManager.get_repository()
    print(f"Repository with REPOSITORY_TYPE=sqlalchemy: {type(repo4).__name__}")
    assert isinstance(repo4, SQLAlchemyRepository), "Should switch to SQLAlchemyRepository"
    
    print("✓ Repository Manager tests passed!")

def test_facade_integration():
    """Test facade integration with repository manager"""
    print("\nTesting Facade Integration...")
    
    from app.services.facade import HBnBFacade
    from app.persistence.repository import InMemoryRepository
    from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
    
    # Test with in-memory repository
    os.environ.pop('REPOSITORY_TYPE', None)
    facade1 = HBnBFacade()
    print(f"Facade with default repository: {type(facade1.repo).__name__}")
    assert isinstance(facade1.repo, InMemoryRepository), "Should use InMemoryRepository"
    
    # Test with SQLAlchemy repository
    os.environ['REPOSITORY_TYPE'] = 'sqlalchemy'
    facade2 = HBnBFacade()
    print(f"Facade with SQLAlchemy repository: {type(facade2.repo).__name__}")
    assert isinstance(facade2.repo, SQLAlchemyRepository), "Should use SQLAlchemyRepository"
    
    print("✓ Facade integration tests passed!")

def test_repository_interface():
    """Test that both repositories implement the same interface"""
    print("\nTesting Repository Interface...")
    
    from app.persistence.repository import Repository, InMemoryRepository
    from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
    
    # Check that both repositories inherit from Repository
    assert issubclass(InMemoryRepository, Repository), "InMemoryRepository should inherit from Repository"
    assert issubclass(SQLAlchemyRepository, Repository), "SQLAlchemyRepository should inherit from Repository"
    
    # Check that both have required methods
    required_methods = ['add', 'get', 'get_all', 'update', 'delete', 'get_by_attribute']
    
    in_memory_repo = InMemoryRepository()
    sqlalchemy_repo = SQLAlchemyRepository()
    
    for method in required_methods:
        assert hasattr(in_memory_repo, method), f"InMemoryRepository missing {method}"
        assert hasattr(sqlalchemy_repo, method), f"SQLAlchemyRepository missing {method}"
        assert callable(getattr(in_memory_repo, method)), f"InMemoryRepository {method} not callable"
        assert callable(getattr(sqlalchemy_repo, method)), f"SQLAlchemyRepository {method} not callable"
    
    print("✓ Repository interface tests passed!")

if __name__ == "__main__":
    print("=" * 50)
    print("SQLAlchemy Repository Integration Test")
    print("=" * 50)
    
    try:
        test_repository_manager()
        test_facade_integration()
        test_repository_interface()
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! SQLAlchemy repository integration is working correctly.")
        print("=" * 50)
        print("\nTo use SQLAlchemy repository in your application:")
        print("1. Set environment variable: export REPOSITORY_TYPE=sqlalchemy")
        print("2. Initialize the database models (in the next task)")
        print("3. The facade will automatically use SQLAlchemy for persistence")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
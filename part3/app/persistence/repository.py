from typing import Dict, List, Optional, Type
from abc import ABC, abstractmethod
from app.models.base_model import BaseModel

class Repository(ABC):
    """Abstract base class for repository implementations"""
    
    @abstractmethod
    def add(self, obj: BaseModel) -> None:
        """Add an object to the repository"""
        pass
    
    @abstractmethod
    def get(self, model_class: Type[BaseModel], obj_id: str) -> Optional[BaseModel]:
        """Retrieve an object by its ID"""
        pass
    
    @abstractmethod
    def get_all(self, model_class: Type[BaseModel]) -> List[BaseModel]:
        """Retrieve all objects of a given class"""
        pass
    
    @abstractmethod
    def update(self, obj: BaseModel) -> None:
        """Update an existing object"""
        pass
    
    @abstractmethod
    def delete(self, model_class: Type[BaseModel], obj_id: str) -> bool:
        """Delete an object by its ID"""
        pass
    
    @abstractmethod
    def get_by_attribute(self, model_class: Type[BaseModel], **kwargs) -> List[BaseModel]:
        """Get objects by attribute values"""
        pass

class InMemoryRepository(Repository):
    """In-memory repository for storing objects"""

    def __init__(self):
        self._storage: Dict[str, Dict[str, BaseModel]] = {}

    def add(self, obj: BaseModel) -> None:
        """Add an object to the repository"""
        class_name = obj.__class__.__name__
        if class_name not in self._storage:
            self._storage[class_name] = {}
        self._storage[class_name][obj.id] = obj

    def get(self, model_class: Type[BaseModel], obj_id: str) -> Optional[BaseModel]:
        """Retrieve an object by its ID"""
        class_name = model_class.__name__
        if class_name in self._storage and obj_id in self._storage[class_name]:
            return self._storage[class_name][obj_id]
        return None

    def get_all(self, model_class: Type[BaseModel]) -> List[BaseModel]:
        """Retrieve all objects of a given class"""
        class_name = model_class.__name__
        if class_name in self._storage:
            return list(self._storage[class_name].values())
        return []

    def update(self, obj: BaseModel) -> None:
        """Update an existing object"""
        class_name = obj.__class__.__name__
        if class_name in self._storage and obj.id in self._storage[class_name]:
            obj.save()  # Update the updated_at timestamp
            self._storage[class_name][obj.id] = obj

    def delete(self, model_class: Type[BaseModel], obj_id: str) -> bool:
        """Delete an object by its ID"""
        class_name = model_class.__name__
        if class_name in self._storage and obj_id in self._storage[class_name]:
            del self._storage[class_name][obj_id]
            return True
        return False

    def get_by_attribute(self, model_class: Type[BaseModel], **kwargs) -> List[BaseModel]:
        """Get objects by attribute values"""
        class_name = model_class.__name__
        if class_name not in self._storage:
            return []

        results = []
        for obj in self._storage[class_name].values():
            match = True
            for key, value in kwargs.items():
                if not hasattr(obj, key) or getattr(obj, key) != value:
                    match = False
                    break
            if match:
                results.append(obj)
        return results

from abc import ABC, abstractmethod

class Repository(ABC):
    """Abstract base class for repositories"""
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass


class InMemoryRepository(Repository):
    """In-memory implementation of Repository"""
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Adds an object to storage"""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Gets an object by id"""
        return self._storage.get(obj_id)

    def get_all(self):
        """Gets all objects"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Updates an object"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)

    def delete(self, obj_id):
        """Deletes an object"""
        if obj_id in self._storage:
            del self._storage[obj_id]

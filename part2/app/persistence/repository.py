# part2/app/persistence/repository.py

from abc import ABC, abstractmethod

class Repository(ABC):
    """
    Abstract Base Class for a generic repository.
    Defines the interface for data operations.
    """

    @abstractmethod
    def add(self, entity):
        """Adds a new entity to the repository."""
        pass

    @abstractmethod
    def get(self, entity_id):
        """Retrieves an entity by its ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieves all entities."""
        pass

    @abstractmethod
    def update(self, entity_id, new_data):
        """Updates an existing entity by its ID with new data."""
        pass

    @abstractmethod
    def delete(self, entity_id):
        """Deletes an entity by its ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attribute_name, attribute_value):
        """Retrieves entities by a specific attribute and its value."""
        pass

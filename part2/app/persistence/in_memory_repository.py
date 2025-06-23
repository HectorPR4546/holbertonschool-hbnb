# part2/app/persistence/in_memory_repository.py

from app.persistence.repository import Repository # Correctly imports the abstract base class

class InMemoryRepository(Repository):
    """
    An in-memory implementation of the Repository interface.
    Stores data in a dictionary.
    """
    def __init__(self):
        # A dictionary to simulate a database/storage
        # Keys are entity IDs, values are entity objects
        self.data = {}

    def add(self, entity):
        """Adds/Saves a new entity to the in-memory store.
           This method fulfills the 'add' abstract method.
        """
        if entity.id in self.data:
            raise ValueError(f"Entity with ID {entity.id} already exists.")
        self.data[entity.id] = entity
        return entity

    def get(self, entity_id):
        """Retrieves an entity by its ID.
           This method fulfills the 'get' abstract method.
        """
        return self.data.get(entity_id)

    def get_all(self):
        """Retrieves all entities."""
        return list(self.data.values())

    def update(self, entity_id, new_data):
        """Updates an existing entity by its ID with new data."""
        entity = self.data.get(entity_id)
        if entity:
            # Assuming entity objects have an 'update' method to apply new_data
            entity.update(new_data)
            return entity
        return None # Indicate entity not found

    def delete(self, entity_id):
        """Deletes an entity by its ID."""
        if entity_id in self.data:
            del self.data[entity_id]
            return True # Indicate successful deletion
        return False # Indicate entity not found

    def get_by_attribute(self, attribute_name, attribute_value):
        """
        Retrieves entities by a specific attribute and its value.
        Returns a list of matching entities.
        """
        matches = []
        for entity in self.data.values():
            if hasattr(entity, attribute_name) and getattr(entity, attribute_name) == attribute_value:
                matches.append(entity)
        return matches

    def clear(self):
        """
        Clears all data from the repository.
        Crucial for isolating tests to prevent side effects between runs.
        This method is specific to InMemoryRepository and not part of the abstract interface.
        """
        self.data = {}

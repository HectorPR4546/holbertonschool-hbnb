# part2/app/persistence/in_memory_repository.py

# It's important that this import correctly points to your base Repository class
# For example, if Repository is in repository.py in the same folder:
from .repository import Repository

class InMemoryRepository(Repository):
    """
    An in-memory implementation of the Repository interface.
    Stores data in a dictionary.
    """
    def __init__(self):
        # We use a dictionary to simulate a database/storage
        # Keys are entity IDs, values are entity objects
        self.data = {}

    def save(self, entity):
        """Saves an entity to the in-memory store."""
        # This assumes entities have a unique 'id' attribute
        self.data[entity.id] = entity
        return entity

    def get_by_id(self, entity_id):
        """Retrieves an entity by its ID."""
        return self.data.get(entity_id)

    def get_all(self):
        """Retrieves all entities."""
        return list(self.data.values())

    def update(self, entity_id, new_data):
        """Updates an existing entity by its ID with new data."""
        entity = self.data.get(entity_id)
        if entity:
            # Assuming your model entities have an `update` method
            # that takes a dictionary of new_data and applies it.
            entity.update(new_data)
            # Re-save to ensure any internal updates (like timestamps) are handled
            self.save(entity)
            return entity
        return None

    def delete(self, entity_id):
        """Deletes an entity by its ID."""
        if entity_id in self.data:
            del self.data[entity_id]
            return True
        return False
    
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
        """
        self.data = {}

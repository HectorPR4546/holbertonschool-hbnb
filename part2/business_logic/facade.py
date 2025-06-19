"""Facade pattern implementation for HBnB business logic."""

from persistence.repository import Repository
from persistence.in_memory_repo import InMemoryRepository

class HBNBFacade:
    """Facade class to abstract business logic operations."""
    
    def __init__(self):
        """Initialize the facade with an in-memory repository."""
        self._repository = InMemoryRepository()
    
    @property
    def repository(self) -> Repository:
        """Get the repository instance."""
        return self._repository

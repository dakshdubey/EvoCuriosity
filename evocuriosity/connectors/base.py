from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseConnector(ABC):
    """Abstract base class establishing the contract for external database connectors."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish the connection to the database."""
        pass

    @abstractmethod
    def query(self, query_text: str) -> List[Dict[str, Any]]:
        """Perform a natural language or structured search query."""
        pass

    @abstractmethod
    def check_existence(self, concept: str) -> bool:
        """Check if a specific concept exists in the database."""
        pass

    @abstractmethod
    def fetch_related(self, concept: str) -> List[Dict[str, Any]]:
        """Fetch records related to the given concept if it exists."""
        pass

from typing import List, Dict, Any, Optional
from evocuriosity.connectors.base import BaseConnector

class DBAdapter:
    """High-level adapter wrapping various database connectors with semantic intelligence."""
    
    def __init__(self, connector: BaseConnector):
        self.connector = connector
        
    def semantic_query(self, query_text: str) -> List[Dict[str, Any]]:
        """Perform a semantic search across the connected database."""
        # In a real implementation, this might involve encoding the query_text first
        return self.connector.query(query_text)
        
    def check_existence(self, concept: str) -> bool:
        return self.connector.check_existence(concept)
        
    def fetch_related_data(self, concept: str) -> List[Dict[str, Any]]:
        return self.connector.fetch_related(concept)

__all__ = ["DBAdapter"]

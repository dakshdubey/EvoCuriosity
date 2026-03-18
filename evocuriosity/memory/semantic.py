from typing import Dict, Any, List
import numpy as np

class SemanticMemory:
    """Stores factual knowledge as concept-vector pairs or concept-definition pairs."""
    
    def __init__(self):
        # We store knowledge as simple dicts and vector embeddings if available
        self.facts: Dict[str, Any] = {}
        self.embeddings: Dict[str, np.ndarray] = {}
        
    def add_fact(self, concept: str, data: Any, embedding: np.ndarray = None):
        """Add a fact and its optional embedding to semantic memory."""
        self.facts[concept] = data
        if embedding is not None:
            self.embeddings[concept] = embedding
            
    def get_fact(self, concept: str) -> Any:
        return self.facts.get(concept)
        
    def get_all_embeddings(self) -> Dict[str, np.ndarray]:
        return self.embeddings
        
    def count(self) -> int:
        return len(self.facts)

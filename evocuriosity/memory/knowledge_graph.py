import networkx as nx
from typing import List, Tuple, Dict, Any

class KnowledgeGraph:
    """Maintains a conceptual graph representing relationships between concepts."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_concept(self, concept: str, attributes: Dict[str, Any] = None):
        """Add a node (concept) to the graph."""
        if attributes is None:
            attributes = {}
        self.graph.add_node(concept, **attributes)
        
    def add_relationship(self, concept_a: str, concept_b: str, relationship_type: str):
        """Add a directed edge (relationship) between concepts."""
        self.graph.add_edge(concept_a, concept_b, type=relationship_type)
        
    def get_related_concepts(self, concept: str) -> List[Tuple[str, str]]:
        """Given a concept, return concepts it connects to and the relationship type."""
        if not self.graph.has_node(concept):
            return []
            
        relations = []
        for neighbor in self.graph.successors(concept):
            edge_data = self.graph.get_edge_data(concept, neighbor)
            rel_type = edge_data.get('type', 'related')
            relations.append((neighbor, rel_type))
            
        return relations
        
    def has_concept(self, concept: str) -> bool:
        return self.graph.has_node(concept)

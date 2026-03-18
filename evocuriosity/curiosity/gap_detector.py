from typing import List, Dict, Any

class GapDetector:
    """Identifies knowledge gaps given extracted concepts and existing memory."""
    
    def detect_gaps(self, concepts: List[str], semantic_memory) -> Dict[str, Any]:
        """
        Compare concepts against semantic_memory.
        Returns known facts ratio, and missing concepts.
        """
        known_concepts = []
        missing_concepts = []
        
        for concept in concepts:
            if semantic_memory.get_fact(concept) is not None:
                known_concepts.append(concept)
            else:
                missing_concepts.append(concept)
                
        total = len(concepts)
        known_ratio = len(known_concepts) / total if total > 0 else 1.0
        
        return {
            "known_ratio": known_ratio,
            "missing_concepts": missing_concepts,
            "known_concepts": known_concepts
        }

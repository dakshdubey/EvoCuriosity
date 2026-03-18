import numpy as np
from typing import Dict, Tuple

class NoveltyDetector:
    """Detects novelty by comparing new inputs to memory."""
    
    def __init__(self, threshold: float = 0.7):
        """
        Threshold sets the boundary for novelty. 
        If max similarity < threshold, it is considered novel.
        """
        self.threshold = threshold
        
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def compute_novelty(self, input_embedding: np.ndarray, memory_embeddings: Dict[str, np.ndarray]) -> Tuple[bool, float, str]:
        """
        Compare input with memory embeddings.
        Returns:
            is_new (bool): whether the concept is novel.
            max_sim (float): the highest similarity found.
            closest_concept (str): the concept it matched most closely.
        """
        if not memory_embeddings:
            # If memory is empty, everything is novel
            return True, 0.0, None
            
        max_sim = -1.0
        closest_concept = None
        
        for concept, mem_emb in memory_embeddings.items():
            sim = self.cosine_similarity(input_embedding, mem_emb)
            if sim > max_sim:
                max_sim = sim
                closest_concept = concept
                
        is_new = max_sim < self.threshold
        
        return is_new, max_sim, closest_concept

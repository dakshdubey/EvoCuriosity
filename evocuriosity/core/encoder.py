import numpy as np
import hashlib
import logging

logger = logging.getLogger(__name__)

class Encoder:
    """Converts text/concepts into vector embeddings."""
    
    def __init__(self, use_mock: bool = True, dim: int = 256):
        self.use_mock = use_mock
        self.dim = dim
        self.model = None
        
        if not use_mock:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except ImportError:
                logger.warning("sentence-transformers not installed. Falling back to mock encoder.")
                self.use_mock = True

    def encode(self, text: str) -> np.ndarray:
        """Encode a string into a numeric vector."""
        if self.use_mock:
            # Deterministic mock embedding based on string hash
            hash_obj = hashlib.md5(text.encode())
            seed = int(hash_obj.hexdigest(), 16) % (2**32)
            rng = np.random.default_rng(seed)
            vector = rng.standard_normal(self.dim)
            return vector / np.linalg.norm(vector)  # Normalize
        else:
            vector = self.model.encode(text)
            return vector / np.linalg.norm(vector)

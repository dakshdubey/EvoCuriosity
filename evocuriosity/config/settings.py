import json
from pathlib import Path

class Config:
    """Core configuration for the Evocuriosity SDK."""
    
    # Curiosity threshold configuration
    NOVELTY_THRESHOLD = 0.7  # Cosine similarity below this triggers novelty
    CONFIDENCE_THRESHOLD = 0.8  # Confidence below this means high uncertainty
    
    # DB configuration
    ENABLE_DB = True
    DB_TYPE = "mongo"
    USE_VECTOR = True
    
    # Memory and Data Paths
    DATA_DIR = Path.home() / ".evocuriosity_data"
    
    @classmethod
    def setup(cls):
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)

config = Config()

from typing import List, Dict, Any
import re

class Perception:
    """Processes raw input data and extracts basic features/concepts."""
    
    def __init__(self):
        # Basic stop words for simple local concept extraction
        self.stop_words = {"a", "an", "the", "and", "or", "but", "is", "are", "was", "were", "to", "in", "on", "with"}
        
    def process_input(self, text: str) -> Dict[str, Any]:
        """Process raw text into clean concepts and basic metadata."""
        clean_text = text.lower().strip()
        words = re.findall(r'\b\w+\b', clean_text)
        
        # Human-like behavior: If it's a short phrase, treat the whole phrase as one concept
        if len(words) <= 4 and clean_text:
            concepts = [clean_text]
        else:
            concepts = [w for w in words if w not in self.stop_words and len(w) > 2]
        
        return {
            "raw": text,
            "clean_text": clean_text,
            "concepts": concepts,
            "word_count": len(words)
        }

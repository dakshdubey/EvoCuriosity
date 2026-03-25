from typing import Any, Dict, List
from .base import BaseAgent
from evocuriosity.curiosity.gap_detector import GapDetector

class ResearchAgent(BaseAgent):
    """Fetches knowledge from memory and external database connectors."""
    
    def __init__(self, memory_module, db_connector=None):
        super().__init__("Researcher")
        self.memory = memory_module
        self.db = db_connector
        self.gap_detector = GapDetector()
        
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        concepts = context.get("concepts", [])
        gaps = self.gap_detector.detect_gaps(concepts, self.memory)
        
        db_results = []
        knowledge_found = False
        
        if self.db:
            still_missing = []
            for concept in gaps.get("missing_concepts", []):
                if self.db.check_existence(concept):
                    knowledge_found = True
                    related = self.db.fetch_related(concept)
                    db_results.extend(related)
                    gaps["known_concepts"].append(concept)
                else:
                    still_missing.append(concept)
            gaps["missing_concepts"] = still_missing
            
        total = len(concepts)
        gaps["known_ratio"] = len(gaps["known_concepts"]) / total if total > 0 else 1.0
        
        return {
            "gaps": gaps,
            "db_results": db_results,
            "knowledge_found": knowledge_found
        }

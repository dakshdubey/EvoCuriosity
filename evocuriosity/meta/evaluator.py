from typing import Dict, Any

class Evaluator:
    """Scores the overall reasoning quality and output."""
    
    def evaluate(self, reflection_result: Dict[str, Any], emotion_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Evaluate the system state and output readiness.
        """
        curiosity_fulfilled = emotion_state.get("curiosity_level", 0.0) < 0.5
        
        return {
            "curiosity_fulfilled": curiosity_fulfilled,
            "system_health": "stable",
            "readiness_score": 0.9 if curiosity_fulfilled else 0.6
        }

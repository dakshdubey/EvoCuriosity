from typing import Any, Dict
from .base import BaseAgent
from evocuriosity.meta.reflection import Reflection
from evocuriosity.meta.evaluator import Evaluator

class CriticAgent(BaseAgent):
    """Validates findings, reasoning steps, and detects potential flaws."""
    
    def __init__(self, reflection_module=None, evaluator_module=None):
        super().__init__("Critic")
        self.reflection = reflection_module or Reflection()
        self.evaluator = evaluator_module or Evaluator()
        
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        hypotheses = context.get("hypotheses", [])
        probabilities = context.get("probabilities", {})
        questions = context.get("questions", [])
        emotion_state = context.get("emotion_status", {})
        
        reflection_data = self.reflection.reflect(hypotheses, probabilities, questions)
        evaluation_data = self.evaluator.evaluate(reflection_data, emotion_state)
        
        return {
            "reflection": reflection_data,
            "evaluation": evaluation_data
        }

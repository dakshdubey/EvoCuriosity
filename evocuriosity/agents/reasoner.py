from typing import Any, Dict
from .base import BaseAgent
from evocuriosity.reasoning.hypothesis import HypothesisGenerator
from evocuriosity.reasoning.probabilistic import ProbabilisticReasoning

class ReasoningAgent(BaseAgent):
    """Generates and ranks hypotheses based on identified gaps."""
    
    def __init__(self, hypothesis_gen=None, reasoning_module=None):
        super().__init__("Reasoner")
        self.hypothesis_gen = hypothesis_gen or HypothesisGenerator()
        self.reasoning = reasoning_module or ProbabilisticReasoning()
        
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        gaps = context.get("gaps", {})
        missing = gaps.get("missing_concepts", [])
        known = gaps.get("known_concepts", [])
        confidence = context.get("emotion_state", {}).get("confidence_level", 0.5)
        
        hypotheses = self.hypothesis_gen.generate(missing, known)
        probabilities = self.reasoning.assign_probabilities(hypotheses, confidence)
        
        return {
            "hypotheses": hypotheses,
            "probabilities": probabilities
        }

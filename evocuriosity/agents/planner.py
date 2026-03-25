from typing import Any, Dict, List
from .base import BaseAgent

class PlannerAgent(BaseAgent):
    """Determines the next logical steps for the cognitive loop and decomposes tasks."""
    
    def __init__(self):
        super().__init__("Planner")
        
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        curiosity_level = context.get("emotion_status", {}).get("curiosity_level", 0.5)
        missing_concepts = context.get("gaps", {}).get("missing_concepts", [])
        
        # Simple task decomposition based on curiosity
        plan = []
        if missing_concepts:
            plan.append("Search for missing concepts: " + ", ".join(missing_concepts))
            if curiosity_level > 0.7:
                plan.append("Deep dive and formulate advanced hypotheses")
            plan.append("Generate curiosity-driven question tree")
        else:
            plan.append("Consolidate existing knowledge")
            
        return {
            "execution_plan": plan,
            "next_step": plan[0] if plan else "Wait"
        }

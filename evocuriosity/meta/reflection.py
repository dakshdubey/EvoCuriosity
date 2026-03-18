from typing import List, Dict, Any

class Reflection:
    """Evaluates the cognitive cycle for missing assumptions and weak hypotheses."""
    
    def reflect(self, hypotheses: List[Dict[str, Any]], probabilities: Dict[str, float], questions: List[str]) -> Dict[str, Any]:
        """
        Check for missing assumptions, weak hypotheses, and unanswered questions.
        """
        insights = []
        weak_hypotheses = [h_id for h_id, prob in probabilities.items() if prob < 0.2]
        
        if weak_hypotheses:
            insights.append(f"Identified {len(weak_hypotheses)} weak hypotheses that require further evidence.")
            
        if len(questions) > 5:
            insights.append("High number of questions indicates significant knowledge gaps or high curiosity.")
            
        if not hypotheses:
            insights.append("No hypotheses generated. May need to seek new input concepts.")
            
        return {
            "weak_hypotheses": weak_hypotheses,
            "insights": insights,
            "reflection_status": "completed"
        }

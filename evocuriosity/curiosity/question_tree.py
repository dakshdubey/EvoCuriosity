import random
from typing import List, Dict, Any

class QuestionTreeGenerator:
    """Generates multi-level structured questions driven by curiosity and uncertainty."""
    
    def generate(self, missing_concepts: List[str], curiosity_level: float, user_sentiment: float = 0.0) -> Dict[str, Any]:
        """
        Level 1: Basic / What
        Level 2: Analytical / Why & How
        Level 3: Abstract / What-if
        """
        tree = {
            "level_1": [],
            "level_2": [],
            "level_3": []
        }
        
        if not missing_concepts:
            return {"tree": tree, "flat_questions": []}
            
        # Select primary concept to focus on
        concept = missing_concepts[0]
        
        # Tone setting
        prefix = ""
        if user_sentiment > 0.3:
            prefix = "This sounds really fascinating! "
        elif user_sentiment < -0.3:
            prefix = "I sense some frustration... let's break it down. "
            
        # Level 1: Basic
        tree["level_1"].append(f"{prefix}What exactly is {concept}?")
        tree["level_1"].append(f"How is {concept} defined in this context?")
        
        # Level 2: Analytical (Requires moderate curiosity)
        if curiosity_level > 0.4:
            tree["level_2"].append(f"Why is {concept} important to understand?")
            tree["level_2"].append(f"How does {concept} actually work under the hood?")
            
        # Level 3: Abstract (Requires high curiosity)
        if curiosity_level > 0.7:
            tree["level_3"].append(f"What would happen if {concept} didn't exist?")
            tree["level_3"].append(f"What are the current limitations in our understanding of {concept}?")

        # Flatten and Score questions
        flat_questions = []
        for level, questions in tree.items():
            level_weight = {"level_1": 1.0, "level_2": 1.5, "level_3": 2.0}[level]
            for q in questions:
                # question_score = curiosity × uncertainty (simulated as 1.0 - known_ratio) × level_weight
                # For simplicity here we just use curiosity and level_weight
                score = round(curiosity_level * level_weight, 2)
                flat_questions.append({"text": q, "score": score, "level": level})
                
        # Pick top 2 questions for human-like interaction
        selected_questions = [q["text"] for q in sorted(flat_questions, key=lambda x: x["score"], reverse=True)[:2]]
                
        return {
            "tree": tree,
            "flat_questions": selected_questions,
            "scored_questions": flat_questions
        }


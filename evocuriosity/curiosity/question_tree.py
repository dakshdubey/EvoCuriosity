from typing import List, Dict, Any

import random

class QuestionTreeGenerator:
    """Generates multi-level structured questions driven by curiosity."""
    
    def generate(self, missing_concepts: List[str], curiosity_level: float, user_sentiment: float = 0.0) -> Dict[str, Any]:
        """
        Level 1: What / Why
        Level 2: How / Factors (Triggered if curiosity is moderate/high)
        Level 3: What-if / Limitations (Triggered if curiosity is very high)
        Tone adjusts based on user_sentiment
        """
        tree = {
            "level_1": [],
            "level_2": [],
            "level_3": []
        }
        
        all_questions = []
        
        if not missing_concepts:
            return {"tree": tree, "flat_questions": []}
            
        # Human-like: Focus on the most important missing concept (the first one)
        concept = missing_concepts[0]
        
        # Tone setting
        prefix = ""
        if user_sentiment > 0.3:
            prefix = "This sounds really fascinating! "
        elif user_sentiment < -0.3:
            prefix = "I sense some frustration... let's break it down. "
            
        # Level 1
        q1 = f"{prefix}What exactly is {concept}?"
        q2 = f"Why is {concept} important to understand?"
        tree["level_1"].extend([q1, q2])
        
        # Level 2
        if curiosity_level > 0.3:
            q3 = f"How does {concept} actually work?"
            q4 = f"What are the main factors involved in {concept}?"
            tree["level_2"].extend([q3, q4])
            
        # Level 3
        if curiosity_level > 0.7:
            q5 = f"What would happen if {concept} didn't exist?"
            q6 = f"What are the current limitations in our understanding of {concept}?"
            tree["level_3"].extend([q5, q6])
            
        # Ask 1 or 2 natural questions so it doesn't sound robotic
        candidates = list(tree["level_1"])
        if curiosity_level > 0.4:
            candidates.extend(tree["level_2"])
        if curiosity_level > 0.8:
            candidates.extend(tree["level_3"])
            
        num_questions = 1 if curiosity_level < 0.6 else 2
        if candidates:
            # Pick a couple of questions randomly to act more human
            selected = random.sample(candidates, min(num_questions, len(candidates)))
            all_questions.extend(selected)
                
        return {
            "tree": tree,
            "flat_questions": all_questions
        }

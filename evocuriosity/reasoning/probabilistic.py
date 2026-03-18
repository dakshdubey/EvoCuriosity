from typing import List, Dict, Any

class ProbabilisticReasoning:
    """Assigns probabilities to hypotheses using Bayesian-style scoring."""
    
    def assign_probabilities(self, hypotheses: List[Dict[str, Any]], data_evidence: float) -> Dict[str, float]:
        """
        P(H|D) proportional to P(D|H) * P(H)
        data_evidence is a proxy for how much current confidence we have (P(D)).
        """
        scored_hypotheses = {}
        total_score = 0.0
        
        for h in hypotheses:
            # Prior P(H) -> assumption: simpler hypotheses have higher prior
            # For this mock, assign a base prior
            prior = 0.5 
            
            # Likelihood P(D|H) -> How likely is the evidence if H is true?
            # We mock this by assuming hypotheses linked to knowns are more likely.
            likelihood = data_evidence if "related_to" in h else (data_evidence * 0.5)
            
            # Unnormalized posterior
            posterior = likelihood * prior
            scored_hypotheses[h["id"]] = posterior
            total_score += posterior
            
        # Normalize probabilities
        if total_score > 0:
            for k in scored_hypotheses:
                scored_hypotheses[k] = round(scored_hypotheses[k] / total_score, 4)
                
        return scored_hypotheses

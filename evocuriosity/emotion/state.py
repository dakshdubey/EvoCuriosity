class EmotionState:
    """Maintains emotional metrics influencing cognitive processing."""
    
    def __init__(self):
        self.curiosity_level: float = 0.5
        self.confidence_level: float = 0.5
        self.uncertainty_level: float = 0.5
        self.user_sentiment: float = 0.0
        
    def update(self, novelty_score: float, known_facts_ratio: float, user_sentiment: float = 0.0):
        """
        Update states based on input novelty, memory confidence, and user sentiment.
        """
        self.confidence_level = known_facts_ratio
        self.user_sentiment = user_sentiment
        
        # Uncertainty = 1 - confidence
        self.uncertainty_level = 1.0 - self.confidence_level
        
        # Curiosity = novelty_score * uncertainty
        self.curiosity_level = novelty_score * self.uncertainty_level
        
        # Bound values
        self.confidence_level = max(0.0, min(1.0, self.confidence_level))
        self.uncertainty_level = max(0.0, min(1.0, self.uncertainty_level))
        self.curiosity_level = max(0.0, min(1.0, self.curiosity_level))
        
    def get_state(self):
        return {
            "curiosity_level": self.curiosity_level,
            "confidence_level": self.confidence_level,
            "uncertainty_level": self.uncertainty_level,
            "user_sentiment": self.user_sentiment
        }

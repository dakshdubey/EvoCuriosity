import re

class SentimentAnalyzer:
    """Basic lexicon-based sentiment analysis for local execution without heavy dependencies."""
    
    def __init__(self):
        # Basic lexicons to determine the user's emotional state
        self.positive_words = {
            "good", "great", "awesome", "excellent", "happy", "excited", 
            "love", "amazing", "fascinating", "interesting", "best", "brilliant", "cool"
        }
        self.negative_words = {
            "bad", "terrible", "awful", "sad", "angry", "hate", "worst", 
            "boring", "stupid", "frustrating", "confusing", "hard", "difficult", "tough"
        }
        
    def analyze(self, text: str) -> float:
        """Returns a sentiment score between -1.0 (very negative) and 1.0 (very positive)."""
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return 0.0
            
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        
        total_sentiment_words = pos_count + neg_count
        if total_sentiment_words == 0:
            return 0.0
            
        score = (pos_count - neg_count) / total_sentiment_words
        return round(score, 2)

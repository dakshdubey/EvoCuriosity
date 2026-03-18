from typing import List, Dict, Any
import time

class EpisodicMemory:
    """Stores sequences of past interactions and observations."""
    
    def __init__(self):
        self.episodes: List[Dict[str, Any]] = []
        
    def add_episode(self, observation: str, result: Dict[str, Any] = None):
        """Record an episode in time."""
        episode = {
            "timestamp": time.time(),
            "observation": observation,
            "result": result or {}
        }
        self.episodes.append(episode)
        
    def get_recent_episodes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve the latest episodes."""
        return self.episodes[-limit:]
        
    def count(self) -> int:
        return len(self.episodes)

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """Abstract base class for all internal cognitive agents."""
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's specialized task within the given context."""
        pass

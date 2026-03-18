from typing import Any, Dict
import json

def format_output(data: Dict[str, Any]) -> str:
    """Format dictionary output to a pretty JSON string."""
    return json.dumps(data, indent=2)

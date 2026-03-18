import sys
import json
from pathlib import Path

# Add the root directory to sys.path so we can import without pip installing locally during dev
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from evocuriosity import CuriosityEngine

def main():
    print("--- Evocuriosity Initialization ---")
    ai = CuriosityEngine()
    
    print("\n--- Observing Input ---")
    ai.observe("Quantum computing basics")
    
    print("\n--- Thinking / Cognitive Loop ---")
    ai.think()
    
    print("\n--- Output ---")
    result = ai.get_output()
    print(json.dumps(result, indent=2))
    
    print("\n--- Testing Episodic Memory State ---")
    print(f"Total Episodes logged: {ai.episodic_memory.count()}")
    
if __name__ == "__main__":
    main()

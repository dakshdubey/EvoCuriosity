import sys
import json
from pathlib import Path

# Fix relative import for local uninstalled testing execution
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from evocuriosity.core import CuriosityEngine
from evocuriosity.connectors.mongo import MongoConnector

def main():
    print("=== EvoCuriosity SDK v0.2.0 Final Upgrade Test ===\n")
    
    # 1. Initialize Engine with a DB Connector (Mocked)
    db = MongoConnector(uri="mongodb://localhost:27017")
    ai = CuriosityEngine(db_connector=db)
    
    # 2. Input to trigger curiosity loop
    user_input = "Tell me about the hidden properties of dark energy"
    print(f"User Input: \"{user_input}\"\n")
    
    # 3. Cognitive execution
    ai.observe(user_input)
    ai.think()
    
    # 4. View Results
    output = ai.get_output()
    
    print("--- Cognitive Output ---")
    print(f"Knowledge Found: {output['knowledge_found']}")
    print(f"Sources Used: {output['sources']}")
    
    print("\nGenerated Questions (Scored):")
    for q in output['questions']:
        print(f"• {q}")
        
    print("\nNext Actions (Planner):")
    for action in output['next_actions']:
        print(f"-> {action}")
        
    print("\nEmotion State:")
    print(json.dumps(output['emotion_state'], indent=2))
    
    print("\n--- Full Enterprise Result ---")
    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    main()

import sys
import json
from pathlib import Path

# Fix relative import for local uninstalled testing execution
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from evocuriosity import CuriosityEngine
from evocuriosity.connectors import MongoConnector

def main():
    print("--- Evocuriosity Sentiment Integration Test ---\n")
    
    # Initialize mock DB connector
    db = MongoConnector(uri="mongodb://localhost:27017")
    db.connect()
    
    # Engine with DB attached
    ai = CuriosityEngine(db_connector=db)
    
    test_inputs = [
        "Dark matter", 
        "Learning about Quantum physics is so frustrating and hard", 
        "This awesome new space telescope is amazing"
    ]
    
    for user_input in test_inputs:
        print("="*50)
        print(f"User input:\n\"{user_input}\"\n")
        print("AI:\n")
        
        # Process
        ai.observe(user_input)
        ai.think()
        
        out = ai.get_output()
        
        # formatting output dynamically like the prompt requested
        if out["knowledge_found"]:
            print("Database Check: ✅ Found")
            print("\nKnowledge Merged.\n")
        else:
            print("Database Check: ❌ Not found")
            print(f"\nCuriosity Triggered {'🔥' if out['emotion_state']['curiosity_level'] > 0.5 else ''}\n")
            
            print("Questions:")
            for q in out["questions"]:
                print(f"• {q}")
                
        print(f"\nUser Sentiment Score: {out['emotion_state'].get('user_sentiment', 0.0)}")
        print(f"Curiosity Level     : {round(out['emotion_state']['curiosity_level'], 2)}\n")
    
if __name__ == "__main__":
    main()

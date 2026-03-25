from typing import Any, Dict, List
from evocuriosity.agents import ResearchAgent, ReasoningAgent, CriticAgent, PlannerAgent

class CognitiveLoop:
    """Manages the multi-agent cognitive execution flow."""
    
    def __init__(self, engine):
        self.engine = engine
        self.researcher = ResearchAgent(engine.semantic_memory, engine.db)
        self.reasoner = ReasoningAgent(engine.hypothesis_generator, engine.probabilistic_reasoning)
        self.critic = CriticAgent(engine.reflection, engine.evaluator)
        self.planner = PlannerAgent()
        
    def run(self) -> Dict[str, Any]:
        """Execute a full cognitive cycle."""
        context = {
            "concepts": self.engine.current_concepts,
            "embeddings": self.engine.current_embeddings,
            "emotion_status": self.engine.emotion_state.get_state()
        }
        
        # 1. Research phase
        research_output = self.researcher.execute(context)
        context.update(research_output)
        
        # 2. Reasoning phase
        if context["gaps"].get("missing_concepts"):
            reasoning_output = self.reasoner.execute(context)
            context.update(reasoning_output)
            
            # 3. Curiosity phase (Integrated into planner/engine logic)
            self.engine.latest_gaps = context["gaps"]
            self.engine.latest_db_results = context["db_results"]
            self.engine.latest_knowledge_found = context["knowledge_found"]
            
            self.engine.trigger_curiosity()
            self.engine.generate_question_tree()
            
            # 4. Criticism phase
            context["questions"] = self.engine.latest_questions.get("flat_questions", [])
            critic_output = self.critic.execute(context)
            context.update(critic_output)
            
        # 5. Planning phase
        planner_output = self.planner.execute(context)
        context.update(planner_output)
        
        return context

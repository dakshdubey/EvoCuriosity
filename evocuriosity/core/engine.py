from typing import Dict, Any, List, Optional

from evocuriosity.config.settings import config
from evocuriosity.core.perception import Perception
from evocuriosity.core.encoder import Encoder
from evocuriosity.curiosity.novelty import NoveltyDetector
from evocuriosity.emotion.sentiment import SentimentAnalyzer
from evocuriosity.memory.semantic import SemanticMemory
from evocuriosity.memory.episodic import EpisodicMemory
from evocuriosity.memory.knowledge_graph import KnowledgeGraph
from evocuriosity.emotion.state import EmotionState
from evocuriosity.curiosity.gap_detector import GapDetector
from evocuriosity.curiosity.question_tree import QuestionTreeGenerator
from evocuriosity.reasoning.hypothesis import HypothesisGenerator
from evocuriosity.reasoning.probabilistic import ProbabilisticReasoning
from evocuriosity.meta.reflection import Reflection
from evocuriosity.meta.evaluator import Evaluator
from evocuriosity.core.loop import CognitiveLoop
from evocuriosity.adapters.llm_adapter import LLMAdapter

class CuriosityEngine:
    """Main orchestrator for the evocuriosity cognitive pipeline."""
    
    def __init__(self, db_connector=None, memory_module=None, reasoning_module=None, curiosity_module=None):
        # Configuration
        self.config = config
        self.db = db_connector
        self.llm = LLMAdapter(model_type="rule-based") # Default
        
        # Instantiate Modules (Customizable)
        self.perception = Perception()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.encoder = Encoder(use_mock=True)
        self.novelty_detector = NoveltyDetector(threshold=self.config.NOVELTY_THRESHOLD)
        
        self.semantic_memory = memory_module or SemanticMemory()
        self.episodic_memory = EpisodicMemory()
        self.knowledge_graph = KnowledgeGraph()
        
        self.emotion_state = EmotionState()
        
        self.gap_detector = GapDetector()
        self.question_generator = curiosity_module or QuestionTreeGenerator()
        
        if reasoning_module:
            self.hypothesis_generator = reasoning_module.get('hypothesis_generator', HypothesisGenerator())
            self.probabilistic_reasoning = reasoning_module.get('probabilistic_reasoning', ProbabilisticReasoning())
        else:
            self.hypothesis_generator = HypothesisGenerator()
            self.probabilistic_reasoning = ProbabilisticReasoning()
            
        self.reflection = Reflection()
        self.evaluator = Evaluator()
        
        # Multi-Agent Loop
        self.loop = CognitiveLoop(self)
        
        # State Tracking
        self.current_input: str = ""
        self.current_concepts: List[str] = []
        self.current_embeddings: Dict[str, Any] = {}
        
        self.latest_novelty: Dict[str, Any] = {}
        self.latest_gaps: Dict[str, Any] = {}
        self.latest_db_results: List[Any] = []
        self.latest_knowledge_found: bool = False
        
        self.latest_questions: Dict[str, Any] = {}
        self.latest_hypotheses: List[Any] = []
        self.latest_probabilities: Dict[str, float] = {}
        self.latest_reflection: Dict[str, Any] = {}
        self.latest_evaluation: Dict[str, Any] = {}
        self.latest_plan: List[str] = []

    def attach_llm(self, model_type: str, model_name: Optional[str] = None):
        """Plugin custom LLM capability."""
        self.llm = LLMAdapter(model_type, model_name)
        
    def observe(self, input_data: str):
        """Process input through perception and encoding."""
        self.current_input = input_data
        parsed = self.perception.process_input(input_data)
        self.current_concepts = parsed["concepts"]
        self.current_sentiment = self.sentiment_analyzer.analyze(input_data)
        
        self.current_embeddings = {}
        for c in self.current_concepts:
            self.current_embeddings[c] = self.encoder.encode(c)
            
    def detect_novelty(self):
        """Compare input with memory using similarity scoring."""
        self.latest_novelty = {}
        for concept, emb in self.current_embeddings.items():
            is_new, max_sim, closest = self.novelty_detector.compute_novelty(
                emb, self.semantic_memory.get_all_embeddings()
            )
            self.latest_novelty[concept] = {
                "is_new": is_new, "max_similarity": max_sim, "closest_match": closest
            }

    def trigger_curiosity(self):
        """Calculate and update Curiosity State."""
        avg_novelty = 1.0
        if self.latest_novelty:
            avg_sim = sum(n["max_similarity"] for n in self.latest_novelty.values()) / len(self.latest_novelty)
            avg_novelty = 1.0 - max(0.0, avg_sim)
            
        self.emotion_state.update(avg_novelty, self.latest_gaps.get("known_ratio", 1.0), getattr(self, "current_sentiment", 0.0))
        
    def generate_question_tree(self):
        """Generate structured questions based on curiosity level."""
        curiosity_val = self.emotion_state.curiosity_level
        sentiment_val = self.emotion_state.user_sentiment
        missing = self.latest_gaps["missing_concepts"]
        self.latest_questions = self.question_generator.generate(missing, curiosity_val, sentiment_val)
        
    def learn(self, final_context: Dict[str, Any]):
        """Persist findings to memory."""
        # Add new concepts
        for concept in self.latest_gaps.get("missing_concepts", []):
            emb = self.current_embeddings.get(concept)
            self.semantic_memory.add_fact(concept, {"source": "observed", "status": "hypothesized"}, emb)
            self.knowledge_graph.add_concept(concept, {"status": "hypothesized"})
            
        # Add relationships based on top hypothesis
        best_h_id = max(self.latest_probabilities.items(), key=lambda x: x[1])[0] if self.latest_probabilities else None
        
        if best_h_id:
            for h in self.latest_hypotheses:
                if h["id"] == best_h_id and "related_to" in h:
                    if self.knowledge_graph.has_concept(h["related_to"]):
                        self.knowledge_graph.add_relationship(h["related_to"], h["concept"], "hypothesized_link")
                        
        self.episodic_memory.add_episode(self.current_input, self.get_output())
        
    def think(self):
        """Execute the Multi-Agent Cognitive Loop."""
        if not self.current_input:
            raise ValueError("Call observe() first.")
            
        self.detect_novelty()
        
        # Hand off to the Multi-Agent Cognitive Loop
        loop_output = self.loop.run()
        
        # Sync loop results back to engine state for output
        self.latest_hypotheses = loop_output.get("hypotheses", [])
        self.latest_probabilities = loop_output.get("probabilities", {})
        self.latest_reflection = loop_output.get("reflection", {})
        self.latest_evaluation = loop_output.get("evaluation", {})
        self.latest_plan = loop_output.get("execution_plan", [])
        
        self.learn(loop_output)
        
    def get_output(self) -> Dict[str, Any]:
        """Return enterprise-ready structured result."""
        return {
            "knowledge_found": self.latest_knowledge_found,
            "sources": ["memory"] + (["database"] if self.latest_knowledge_found else []),
            "questions": self.latest_questions.get("flat_questions", []),
            "question_tree": self.latest_questions.get("tree", {}),
            "hypotheses": self.latest_hypotheses,
            "probabilities": self.latest_probabilities,
            "insights": self.latest_reflection.get("insights", []),
            "reflection": self.latest_reflection.get("logic_steps", []),
            "emotion_state": self.emotion_state.get_state(),
            "next_actions": self.latest_plan
        }

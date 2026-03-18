from typing import Dict, Any

from .config import config
from .cognition import Perception, Encoder, NoveltyDetector, SentimentAnalyzer
from .memory import SemanticMemory, EpisodicMemory, KnowledgeGraph
from .emotion import EmotionState
from .curiosity import GapDetector, QuestionTreeGenerator
from .reasoning import HypothesisGenerator, ProbabilisticReasoning
from .meta import Reflection, Evaluator

class CuriosityEngine:
    """Main orchestrator for the evocuriosity cognitive pipeline."""
    
    def __init__(self, db_connector=None, memory_module=None, reasoning_module=None, curiosity_module=None):
        # Configuration
        self.config = config
        self.db = db_connector
        
        # Instantiate Modules (Customizable)
        self.perception = Perception()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.encoder = Encoder(use_mock=True) # Defaults to mock for purely generic SDK compatibility
        self.novelty_detector = NoveltyDetector(threshold=self.config.NOVELTY_THRESHOLD)
        
        self.semantic_memory = memory_module or SemanticMemory()
        self.episodic_memory = EpisodicMemory()
        self.knowledge_graph = KnowledgeGraph()
        
        self.emotion_state = EmotionState()
        
        # Allowing curiosity override
        self.gap_detector = GapDetector()
        self.question_generator = curiosity_module or QuestionTreeGenerator()
        
        # Allowing reasoning override
        if reasoning_module:
            self.hypothesis_generator = reasoning_module.get('hypothesis_generator', HypothesisGenerator())
            self.probabilistic_reasoning = reasoning_module.get('probabilistic_reasoning', ProbabilisticReasoning())
        else:
            self.hypothesis_generator = HypothesisGenerator()
            self.probabilistic_reasoning = ProbabilisticReasoning()
            
        self.reflection = Reflection()
        self.evaluator = Evaluator()
        
        # State Tracking
        self.current_input: str = ""
        self.current_concepts: list = []
        self.current_embeddings: dict = {}
        
        self.latest_novelty: Dict[str, Any] = {}
        self.latest_gaps: Dict[str, Any] = {}
        self.latest_db_results: list = []
        self.latest_knowledge_found: bool = False
        
        self.latest_questions: Dict[str, Any] = {}
        self.latest_hypotheses: list = []
        self.latest_probabilities: Dict[str, float] = {}
        self.latest_reflection: Dict[str, Any] = {}
        self.latest_evaluation: Dict[str, Any] = {}
        
    def observe(self, input_data: str):
        """Process input through perception and encoding."""
        self.current_input = input_data
        
        # 1. Perception & Sentiment
        parsed = self.perception.process_input(input_data)
        self.current_concepts = parsed["concepts"]
        self.current_sentiment = self.sentiment_analyzer.analyze(input_data)
        
        # 2. Encoding
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
                "is_new": is_new,
                "max_similarity": max_sim,
                "closest_match": closest
            }
            
    def estimate_uncertainty(self):
        """Calculate confidence score passing gap data to emotion state."""
        self.latest_gaps = self.gap_detector.detect_gaps(self.current_concepts, self.semantic_memory)
        # We hold off updating EmotionState fully until we check the external DB.
        
    def check_external_knowledge(self):
        """Check external database for missing concepts and merge knowledge."""
        self.latest_db_results = []
        self.latest_knowledge_found = False
        
        if not self.db:
            return
            
        still_missing = []
        for concept in self.latest_gaps.get("missing_concepts", []):
            exists = self.db.check_existence(concept)
            if exists:
                self.latest_knowledge_found = True
                related = self.db.fetch_related(concept)
                self.latest_db_results.extend(related)
                
                # Merge knowledge: it is no longer missing
                self.latest_gaps["known_concepts"].append(concept)
            else:
                still_missing.append(concept)
                
        # Update missing list with only what DB couldn't find
        self.latest_gaps["missing_concepts"] = still_missing
        
        # Re-evaluate knowledge ratio 
        total = len(self.current_concepts)
        self.latest_gaps["known_ratio"] = len(self.latest_gaps["known_concepts"]) / total if total > 0 else 1.0

    def trigger_curiosity(self):
        """Curiosity is triggered based on final missing gaps after DB check."""
        avg_novelty = 1.0
        if self.latest_novelty:
            avg_sim = sum(n["max_similarity"] for n in self.latest_novelty.values()) / len(self.latest_novelty)
            avg_novelty = 1.0 - max(0.0, avg_sim)  # High when similarity is low
            
        self.emotion_state.update(avg_novelty, self.latest_gaps.get("known_ratio", 1.0), getattr(self, "current_sentiment", 0.0))
        
    def generate_question_tree(self):
        """Generate multi-level structured questions."""
        curiosity_val = self.emotion_state.curiosity_level
        sentiment_val = self.emotion_state.user_sentiment
        missing = self.latest_gaps["missing_concepts"]
        self.latest_questions = self.question_generator.generate(missing, curiosity_val, sentiment_val)
        
    def generate_hypotheses(self):
        """Create multiple possible explanations."""
        missing = self.latest_gaps["missing_concepts"]
        known = self.latest_gaps["known_concepts"]
        self.latest_hypotheses = self.hypothesis_generator.generate(missing, known)
        
    def assign_probabilities(self):
        """Rank hypotheses using probabilistic reasoning."""
        confidence = self.emotion_state.confidence_level
        self.latest_probabilities = self.probabilistic_reasoning.assign_probabilities(
            self.latest_hypotheses, confidence
        )
        
    def reflect(self):
        """Evaluate reasoning and detect missing gaps."""
        self.latest_reflection = self.reflection.reflect(
            self.latest_hypotheses, 
            self.latest_probabilities, 
            self.latest_questions.get("flat_questions", [])
        )
        self.latest_evaluation = self.evaluator.evaluate(self.latest_reflection, self.emotion_state.get_state())
        
    def learn(self):
        """Update semantic, episodic and graph memory."""
        # Add new concepts
        for concept in self.latest_gaps["missing_concepts"]:
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
        """Full cognitive loop execution."""
        if not self.current_input:
            raise ValueError("Call observe() with input_data before think()")
            
        self.detect_novelty()           # Local Novelty
        self.estimate_uncertainty()     # Identify Gaps
        self.check_external_knowledge() # Query External DB
        self.trigger_curiosity()        # Finalize Emotion State
        
        # Only generate questions and hypotheses if there are missing concepts
        if self.latest_gaps.get("missing_concepts"):
            self.generate_question_tree()
            self.generate_hypotheses()
            self.assign_probabilities()
        else:
            self.latest_questions = {}
            self.latest_hypotheses = []
            self.latest_probabilities = {}
            
        self.reflect()
        self.learn()
        
    def get_output(self) -> Dict[str, Any]:
        """Return structured result matching V2 schema."""
        return {
            "knowledge_found": self.latest_knowledge_found,
            "database_results": self.latest_db_results,
            "questions": self.latest_questions.get("flat_questions", []),
            "missing_areas": self.latest_gaps.get("missing_concepts", []),
            "insights": self.latest_reflection.get("insights", []),
            "emotion_state": self.emotion_state.get_state()
        }

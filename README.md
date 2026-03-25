# EvoCuriosity SDK

A production-grade, local-first cognitive AI framework implementing a modular curiosity-driven architecture.

## Overview
EvoCuriosity is designed to provide a robust foundation for building self-evolving AI systems that prioritize local-first execution and curiosity-driven discovery. The architecture facilitates complex reasoning through a multi-agent orchestration layer, ensuring high adaptability and efficient knowledge management.

## Key Features
- **Multi-Agent Reasoning:** Specialized Researcher, Reasoner, Critic, and Planner agents collaborating within a unified cognitive loop.
- **Database Integration:** Comprehensive support for SQL, MongoDB, and Vector databases through a standardized adapter interface.
- **Curiosity-Driven Logic:** Advanced gap detection and hierarchical question generation based on uncertainty and novelty thresholds.
- **Local-First Architecture:** Optimized for offline execution with pluggable LLM adapters for varied computational environments.

## Installation
The SDK can be installed via pip:
```bash
pip install evocuriosity
```

## Quick Start
```python
from evocuriosity.core import CuriosityEngine
from evocuriosity.connectors.mongo import MongoConnector

# 1. Initialize Engine and Database
db = MongoConnector(uri="mongodb://localhost:27017")
ai = CuriosityEngine(db_connector=db)

# 2. Configure Intelligence Adapter
ai.attach_llm("rule-based")

# 3. Cognitive Observation and Execution
ai.observe("Theoretical implications of quantum entanglement")
ai.think()

# 4. Retrieve Structured Output
results = ai.get_output()
print(results)
```

## Architecture
- `core/`: High-level orchestration and execution loops.
- `agents/`: Collaborative cognitive agents for research, reasoning, and planning.
- `adapters/`: Abstraction layers for Large Language Models and Databases.
- `connectors/`: Specialized database interface implementations.
- `memory/`: Multi-tiered storage for semantic, episodic, and relational data.

## Author
Daksha Dubey

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

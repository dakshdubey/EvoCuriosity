# evocuriosity

A highly advanced, local-first Python SDK that implements a cognitive architecture for curiosity-driven artificial intelligence.

## Features
- **Novelty Detection**: Compares input with semantic/episodic memory.
- **Uncertainty Estimation**: Identifies gaps in knowledge.
- **Curiosity Generation**: Builds structured, multi-level question trees.
- **Hypothesis Generation & Reasoning**: Employs probabilistic evaluation to form and test hypotheses.
- **Local First**: Pure Python SDK requiring zero external APIs.

## Installation
```bash
pip install -e .
```

## Basic Usage
```python
from evocuriosity import CuriosityEngine

ai = CuriosityEngine()
ai.observe("Quantum computing basics")
ai.think()

result = ai.get_output()
print(result)
```

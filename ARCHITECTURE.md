# EvoCuriosity Architecture

## Overview
EvoCuriosity implements a modular cognitive architecture inspired by human-like curiosity and gap-driven learning. The system is designed for local-first execution, ensuring privacy and offline capability.

## Core Components

### 1. Curiosity Engine (`core/engine.py`)
The main orchestrator that manages the perception-action loop. It coordinates between agents and memory to drive the system's focus.

### 2. Multi-Agent System (`agents/`)
Specialized agents collaborate to process information:
- **Research Agent:** Interfaces with `memory` and external `connectors` (SQL, MongoDB, Vector) to fetch relevant context.
- **Reasoning Agent:** Performs hypothesis generation and probabilistic scoring to fill information gaps.
- **Critic Agent:** Validates the reasoning process and identifies logical inconsistencies or missing evidence.
- **Planner Agent:** Decomposes complex goals into actionable tasks for the engine to execute.

### 3. Memory Subsystem (`memory/`)
- **Semantic Memory:** Long-term factual and conceptual knowledge.
- **Episodic Memory:** Temporal record of past interactions and internal states.
- **Knowledge Graph:** Relational mapping of concepts and hypotheses.

### 4. Curiosity & Emotion (`curiosity/`, `emotion/`)
- **Gap Detector:** Identifies missing information relative to current goals.
- **Question Tree Generator:** Creates hierarchical inquiry structures to resolve uncertainty.
- **Emotion State:** Tracks curiosity, confidence, and sentiment to modulate the system's behavior.

## Execution Flow
1. **Perception:** Input is parsed into concepts and sentiment.
2. **Novelty Detection:** Concepts are compared against semantic memory.
3. **Research:** Agents fetch existing knowledge from local and external sources.
4. **Reasoning:** Hypotheses are generated for missing information.
5. **Reflection:** The Critic validates the reasoning and generates curiosity-driven questions.
6. **Persistence:** New findings and episodes are stored in memory.

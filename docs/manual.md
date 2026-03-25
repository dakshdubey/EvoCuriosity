# User Manual - EvoCuriosity SDK

## Introduction
EvoCuriosity is a framework for building AI systems that actively seek information to resolve uncertainty. This manual covers installation, configuration, and advanced usage.

## Basic Usage

### Initializing the Engine
```python
from evocuriosity.core import CuriosityEngine
ai = CuriosityEngine()
```

### Working with Databases
EvoCuriosity supports pluggable connectors. To use a MongoDB connector:
```python
from evocuriosity.connectors.mongo import MongoConnector
db = MongoConnector(uri="mongodb://localhost:27017")
ai = CuriosityEngine(db_connector=db)
```

## Advanced Configuration

### Customizing Reasoning
You can inject custom reasoning modules:
```python
ai = CuriosityEngine(reasoning_module={
    'hypothesis_generator': MyCustomGenerator(),
    'probabilistic_reasoning': MyCustomScorer()
})
```

### LLM Adapters
To use a local Ollama model:
```python
ai.attach_llm(model_type="ollama", model_name="llama3")
```

## Curiosity-Driven Interface
The `get_output()` method provides structured insights into what the system is "thinking" and what it needs to learn next.

```python
ai.observe("How does photosynthesis work in deep-sea organisms?")
ai.think()
output = ai.get_output()

# Access generated questions
print(output['questions'])
```

## Support
For more information, refer to the [README](../README.md) or contact Daksha Dubey.

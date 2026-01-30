# 🤖 Moltbot Agents Collection
Colección de agentes especializados para diferentes tareas.

## 📁 Estructura

```
agents/
├── __init__.py           # Package exports
├── minimax_agent.py      # OpenCode MiniMax (gratis)
├── ollama_agent.py       # Modelos locales Ollama
├── lmstudio_agent.py     # LM Studio local
└── coordinator_agent.py  # Multi-agent coordinator
```

## 🚀 Uso Rápido

### Agente Individual
```python
from minimax_agent import create_minimax_agent

agent = create_minimax_agent()
result = agent.execute_task("Responde brevemente")
```

### Multi-Agent Crew
```python
from coordinator_agent import crew_coordinator

result = crew_coordinator.execute_task(
    task="Write a Python script to parse JSON",
    preferred="ollama"  # or "minimax", "lmstudio"
)
```

## 📊 Comparativa de Agentes

| Agente | Provider | Costo | Mejor Para |
|--------|----------|-------|------------|
| MiniMax | OpenCode | Gratis | Consultas rápidas |
| Ollama 8B | Local | Gratis | General purpose |
| Ollama Coder | Local | Gratis | Coding |
| Ollama 14B | Local | Gratis | Razonamiento |
| LM Studio | Local | Gratis | Modelos personalizados |

## ⚙️ Requisitos

- **Ollama Agent**: Ollama corriendo en localhost:11434
- **LM Studio Agent**: LM Studio corriendo en localhost:1234
- **MiniMax Agent**: Sin requisitos adicionales

## 📝 Ejemplo: Crew de Investigación

```python
from coordinator_agent import MultiAgentCoordinator

coordinator = MultiAgentCoordinator()

# Tarea compleja con múltiples agentes
crew = coordinator.get_crew_for_task("complex")
result = crew.kickoff(
    inputs={
        "task": "Research AI trends and write a summary",
        "context": "Focus on 2024 developments"
    }
)
```

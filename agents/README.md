# 🤖 Moltbot Agents Collection

Sistema de agentes con **solo los modelos que ya tienes configurados**.

## ✅ Agentes Configurados

| # | Agente | Provider | Estado | Mejor Para |
|---|--------|----------|--------|------------|
| 1 | **MiniMax** | OpenCode (cloud) | ✅ Siempre disponible | Consultas rápidas |
| 2 | Llama 3.1 8B | Ollama Local | ⚠️ Requiere Ollama | General purpose |
| 3 | Qwen 2.5 14B | Ollama Local | ⚠️ Requiere Ollama | Razonamiento |
| 4 | Qwen 2.5 Coder | Ollama Local | ⚠️ Requiere Ollama | Código |
| 5 | Ministral 3 8B | Ollama Local | ⚠️ Requiere Ollama | Efficient inference |
| 6 | LM Studio | LM Studio Local | ⚠️ Requiere LM Studio | Modelos personalizados |

## 📁 Estructura

```
agents/
├── __init__.py          # Package exports
├── README.md            # Esta documentación
├── registry.py          # Registro de agentes
├── agents.py            # Factory de agentes
└── agent_cli.py         # CLI tool
```

## 🚀 Uso CLI

```bash
# Ver estado de servicios
python3 agents/agent_cli.py --status

# Usar agente específico
python3 agents/agent_cli.py -u minimax -t "Hola"

# Auto-seleccionar
python3 agents/agent_cli.py -A -t "Escribe código Python"
```

## 🔧 Uso Programático

```python
from agents import (
    create_agent,
    get_best_agent_for_task,
    show_status
)

# Ver estado
show_status()

# Crear agente específico
agent = create_agent("minimax")       # Cloud gratuito
agent = create_agent("ollama-coder")  # Local código

# Auto-seleccionar
agent = get_best_agent_for_task("code")  # Usa el mejor para código
```

## ⚙️ Requisitos

- **MiniMax**: Sin requisitos (cloud gratuito)
- **Ollama**: `ollama serve` en localhost:11434
- **LM Studio**: LM Studio corriendo en localhost:1234

## 📊 Estado de Servicios

```bash
python3 agents/agent_cli.py --status
```

Muestra:
- ✅ OpenCode (MiniMax) - siempre disponible
- ⚠️ Ollama Local - verifica si está corriendo
- ⚠️ LM Studio - verifica si está corriendo

## 🎯 Prioridad de Uso

1. **MiniMax** (cloud) → Consultas simples
2. **Ollama** (local) → Fallback offline
3. **LM Studio** (local) → Modelos personalizados

## 📚 Repo

https://github.com/molder-opina/moltbot-projects

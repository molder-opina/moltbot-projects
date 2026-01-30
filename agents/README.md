# 🤖 Moltbot Agents Collection

Sistema completo de agentes AI con prioridad: **Cloud Free → Local Fallback**

## 📊 Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    SOLICITUD                            │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              CLOUD FREE AGENTS (PRIORIDAD)              │
├─────────────────────────────────────────────────────────┤
│ 1. OpenCode MiniMax     │ Consultas rápidas             │
│ 2. Google Gemini        │ Razonamiento                  │
│ 3. Groq (LLaMA, Mistral)│ Modelos ultra-rápidos         │
│ 4. HuggingFace          │ Modelos open source           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼ (Fallback)
┌─────────────────────────────────────────────────────────┐
│              LOCAL AGENTS (OFFLINE)                      │
├─────────────────────────────────────────────────────────┤
│ 5. Ollama               │ Modelos locales                │
│ 6. LM Studio            │ Modelos personalizados         │
└─────────────────────────────────────────────────────────┘
```

## 📁 Estructura

```
agents/
├── __init__.py                    # Package exports
├── README.md                      # Esta documentación
├── cloud_free_registry.py         # Registro de agentes
├── cloud_free_agents.py          # Factory de agentes
├── multi_provider_agent.py       # CLI tool
├── minimax_agent.py              # OpenCode MiniMax
├── ollama_agent.py               # Ollama local
└── lmstudio_agent.py             # LM Studio local
```

## 🚀 Uso Rápido

### 1. Listar agentes disponibles

```bash
python3 agents/multi_provider_agent.py --list
```

### 2. Ejecutar con agente específico

```bash
python3 agents/multi_provider_agent.py -a opencode-minimax -t "Hola, ¿cómo estás?"
```

### 3. Auto-seleccionar mejor agente

```bash
python3 agents/multi_provider_agent.py -A -t "Escribe código Python" --type code
```

### 4. Ver prioridad de agentes

```bash
python3 agents/multi_provider_agent.py --priority
```

## 📋 Agentes Cloud Free

| # | Agente | Provider | Mejor Para |
|---|--------|----------|------------|
| 1 | MiniMax | OpenCode | Consultas rápidas |
| 2 | Gemini 1.5 Flash | Google | Razonamiento, multimedia |
| 3 | Gemini 1.0 Pro | Google | Código, matemáticas |
| 4 | Groq LLaMA 3.1 70B | Groq | Inference rápida |
| 5 | Groq LLaMA 3 8B | Groq | Tareas ligeras |
| 6 | Groq Mistral 7B | Groq | Instrucciones |
| 7 | Groq Gemma 2 9B | Groq | Análisis |
| 8 | HuggingFace Zephyr | HF | Chat general |
| 9 | HuggingFace Mistral | HF | Código |

## 🏠 Agentes Locales (Fallback)

| # | Agente | Modelo | Mejor Para |
|---|--------|--------|------------|
| 1 | Ollama Llama 3.1 8B | llama3.1:8b | General |
| 2 | Ollama Qwen Coder 7B | qwen2.5-coder | Código |
| 3 | Ollama Qwen 14B | qwen2.5:14b | Razonamiento |

## 🔧 Uso Programático

```python
from agents import (
    create_agent,
    get_best_agent_for_task,
    get_fallback_agent
)

# Crear agente específico
agent = create_agent("opencode-minimax")

# Auto-seleccionar para tarea
agent = get_best_agent_for_task("code")

# Usar con CrewAI
from crewai import Crew, Task

crew = Crew(
    agents=[agent],
    tasks=[Task(description="Tu tarea", agent=agent)]
)

result = crew.kickoff()
```

## ⚙️ Configuración de API Keys

Para agentes cloud, configura las variables de entorno:

```bash
# Google Gemini
export GOOGLE_API_KEY="tu-key"

# Groq
export GROQ_API_KEY="tu-key"

# HuggingFace
export HF_API_KEY="tu-key"
```

Los agentes locales (Ollama, LM Studio) no requieren API keys.

## 🎯 Sistema de Prioridad

El sistema intenta usar agentes cloud primero:

1. **OpenCode MiniMax** → Consultas simples
2. **Google Gemini** → Razonamiento complejo
3. **Groq** → Inferencia rápida
4. **HuggingFace** → Modelos open source
5. **Ollama Local** → Fallback offline
6. **LM Studio** → Fallback personalizado

## 📚 Recursos

- Repo: https://github.com/molder-opina/moltbot-projects
- Docs: Ver `cloud_free_registry.py` para información detallada

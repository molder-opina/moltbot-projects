#!/usr/bin/env python3
"""
🤖 Configured Agents Registry
Solo agentes que ya tienes configurados y funcionando.

Modelos disponibles:
1. OpenCode MiniMax - Gratis (ya configurado)
2. Ollama Local - Offline (ya configurado)
   - llama3.1:8b
   - qwen2.5:14b
   - qwen2.5-coder:7b
   - ministral-3:8b
3. LM Studio Local - Offline (ya configurado)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

class Priority(Enum):
    """Prioridad de uso"""
    OPENCODE = 1      # Cloud gratuito
    OLLAMA = 10       # Local (fallback)
    LM_STUDIO = 11    # Local (fallback)

@dataclass
class AgentInfo:
    name: str
    provider: str
    model: str
    priority: Priority
    base_url: Optional[str]
    context_limit: int
    best_for: List[str]
    enabled: bool = True

# ═══════════════════════════════════════════════════════════════
#  AGENTES CONFIGURADOS Y FUNCIONANDO
# ═══════════════════════════════════════════════════════════════

CONFIGURED_AGENTS = [
    # === CLOUD: OpenCode (gratis, sin API key) ===
    AgentInfo(
        name="OpenCode MiniMax",
        provider="OpenCode",
        model="minimax/minimax-m2.1-free",
        priority=Priority.OPENCODE,
        base_url="https://opencode.ai/zen/v1",
        context_limit=131072,
        best_for=["Consultas rápidas", "Respuestas breves", "Tareas simples"]
    ),
    
    # === LOCAL: Ollama ===
    AgentInfo(
        name="Ollama Llama 3.1 8B",
        provider="Ollama Local",
        model="llama3.1:8b-instruct-q4_K_M",
        priority=Priority.OLLAMA,
        base_url="http://localhost:11434/v1",
        context_limit=131072,
        best_for=["General purpose", "Writing", "Analysis"]
    ),
    
    AgentInfo(
        name="Ollama Qwen 2.5 14B",
        provider="Ollama Local",
        model="qwen2.5:14b-instruct-q4_K_M",
        priority=Priority.OLLAMA,
        base_url="http://localhost:11434/v1",
        context_limit=131072,
        best_for=["Reasoning avanzado", "Matemáticas", "Investigación"]
    ),
    
    AgentInfo(
        name="Ollama Qwen 2.5 Coder 7B",
        provider="Ollama Local",
        model="qwen2.5-coder:7b-instruct-q4_K_M",
        priority=Priority.OLLAMA,
        base_url="http://localhost:11434/v1",
        context_limit=131072,
        best_for=["Code generation", "Debugging", "Documentation"]
    ),
    
    AgentInfo(
        name="Ollama Ministral 3 8B",
        provider="Ollama Local",
        model="ministral-3:8b",
        priority=Priority.OLLAMA,
        base_url="http://localhost:11434/v1",
        context_limit=131072,
        best_for=["Efficient inference", "Chat", "General"]
    ),
]

# ═══════════════════════════════════════════════════════════════
#  CONFIGURACIÓN DE LOCALES (DETECCIÓN AUTOMÁTICA)
# ════════════════════════════════════════════════

LOCAL_CONFIGS = {
    "ollama": {
        "url": "http://localhost:11434/v1",
        "embeddings_model": "nomic-embed-text:latest",
        "default_model": "llama3.1:8b-instruct-q4_K_M"
    },
    "lm_studio": {
        "url": "http://localhost:1234/v1",
        "default_model": None  # Se detecta automáticamente
    }
}

# ═══════════════════════════════════════════════════════════════
#  FUNCIONES DE CONSULTA
# ═══════════════════════════════════════════════════════════════

def get_cloud_agent() -> AgentInfo:
    """Obtener agente cloud (OpenCode MiniMax)"""
    return CONFIGURED_AGENTS[0]

def get_ollama_agents() -> List[AgentInfo]:
    """Lista de agentes Ollama"""
    return [a for a in CONFIGURED_AGENTS if a.provider == "Ollama Local"]

def get_agent_by_task(task_type: str) -> AgentInfo:
    """Obtener mejor agente según tipo de tarea"""
    
    task_map = {
        "quick": CONFIGURED_AGENTS[0],  # MiniMax
        "code": [a for a in CONFIGURED_AGENTS if "Coder" in a.name][0],
        "reasoning": [a for a in CONFIGURED_AGENTS if "14B" in a.name][0],
        "general": [a for a in CONFIGURED_AGENTS if "Llama 3.1 8B" in a.name][0],
    }
    
    return task_map.get(task_type, CONFIGURED_AGENTS[0])

def get_first_available() -> AgentInfo:
    """Obtener primer agente disponible (para fallback)"""
    return CONFIGURED_AGENTS[0]

def check_services():
    """Verificar servicios disponibles"""
    import requests
    
    status = {
        "opencode": False,
        "ollama": False,
        "lm_studio": False
    }
    
    # Check OpenCode
    try:
        resp = requests.get("https://opencode.ai/zen/v1/models", timeout=5)
        if resp.status_code == 200:
            status["opencode"] = True
    except:
        pass
    
    # Check Ollama
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=2)
        if resp.status_code == 200:
            status["ollama"] = True
    except:
        pass
    
    # Check LM Studio
    try:
        resp = requests.get("http://localhost:1234/v1/models", timeout=2)
        if resp.status_code == 200:
            status["lm_studio"] = True
    except:
        pass
    
    return status

def print_status():
    """Imprimir estado de servicios"""
    status = check_services()
    
    print("🤖 ESTADO DE SERVICIOS")
    print("=" * 50)
    
    for service, is_up in status.items():
        icon = "✅" if is_up else "❌"
        name = {
            "opencode": "OpenCode (MiniMax)",
            "ollama": "Ollama Local",
            "lm_studio": "LM Studio"
        }[service]
        print(f"  {icon} {name}")
    
    print("\n📋 AGENTES CONFIGURADOS")
    print("=" * 50)
    for agent in CONFIGURED_AGENTS:
        status_icon = "✅" if agent.enabled else "❌"
        print(f"  {status_icon} [{agent.priority.value}] {agent.name}")
        print(f"      Modelo: {agent.model}")
        print(f"      Mejor para: {', '.join(agent.best_for[:2])}")

if __name__ == "__main__":
    print_status()

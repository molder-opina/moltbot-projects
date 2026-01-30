#!/usr/bin/env python3
"""
☁️ Cloud Free Agents Registry
Registry de todos los agentes cloud gratuitos disponibles.

Agentes Cloud Gratuitos:
1. OpenCode MiniMax - Consultas rápidas
2. Google Gemini - Razonamiento
3. Groq - Modelos rápidos
4. HuggingFace - Modelos open source

Fallbac locales:
5. Ollama (cualquier modelo)
6. LM Studio (cualquier modelo)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Dict
from abc import ABC, abstractmethod

class AgentType(Enum):
    """Tipos de agentes"""
    CLOUD_FREE = "cloud_free"
    LOCAL = "local"

class Priority(Enum):
    """Prioridad de uso (menor = primero)"""
    OPENCODE = 1
    GEMINI = 2
    GROQ = 3
    HUGGINGFACE = 4
    OLLAMA = 10
    LM_STUDIO = 11

@dataclass
class AgentInfo:
    """Información de un agente"""
    name: str
    provider: str
    model: str
    priority: Priority
    agent_type: AgentType
    api_key_env: str
    base_url: Optional[str] = None
    context_limit: int = 131072
    best_for: List[str] = None
    enabled: bool = True
    
    def __post_init__(self):
        if self.best_for is None:
            self.best_for = []

# ═══════════════════════════════════════════════════════════════
#  REGISTRY DE AGENTES CLOUD FREE
# ═══════════════════════════════════════════════════════════════

CLOUD_FREE_AGENTS = [
    # === TIER 1: OpenCode (mayor prioridad) ===
    AgentInfo(
        name="OpenCode MiniMax",
        provider="OpenCode",
        model="minimax/minimax-m2.1-free",
        priority=Priority.OPENCODE,
        agent_type=AgentType.CLOUD_FREE,
        api_key_env="OPENCODE_API_KEY",  # Dummy
        base_url="https://opencode.ai/zen/v1",
        context_limit=131072,
        best_for=["Consultas rápidas", "Tareas simples", "Resumenes"]
    ),
    
    # === TIER 2: Google Gemini ===
    AgentInfo(
        name="Google Gemini 1.5 Flash",
        provider="Google",
        model="gemini-1.5-flash",
        priority=Priority.GEMINI,
        agent_type=AgentType.CLOUD_FREE,
        api_key_env="GOOGLE_API_KEY",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        context_limit=1048576,  # 1M tokens
        best_for=["Razonamiento", "Análisis", "Multimedia"]
    ),
    
    AgentInfo(
        name="Google Gemini 1.0 Pro",
        provider="Google",
        model="gemini-1.0-pro",
        priority=Priority.GEMINI,
        agent_type=AgentType.CLOUD_FREE,
        api_key_env="GOOGLE_API_KEY",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        context_limit=1048576,
        best_for=["Código", "Matemáticas", "Científico"]
    ),
    
    # === TIER 3: Groq (LLaMA rápido) ===
    AgentInfo(
        name="Groq LLaMA 3.1 70B",
        provider="Groq",
        model="llama-3.1-70b-versatile",
        priority=Priority.GROQ,
        agent_type=AgentType.CLOUD_FREE,
        api_key_env="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        context_limit=131072,
        best_for=["Inferencia rápida", "Chat", "Código"]
    ),
    
    AgentInfo(
        name="Groq LLaMA 3 8B",
        provider="Groq",
        model="llama-3-8b-8192",
        priority=Priority.GROQ,
        agent_type=AgentType.CLOUD_FREE,
        api_key_env="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        context_limit=8192,
        best_for=["Respuestas rápidas", "Tareas ligeras"]
    ),
    
    AgentInfo(
        name="Groq Mistral 7B",
        provider="Groq",
        model="mistral-7b-instruct-v0.1",
        priority=Priority.GROQ,
        agent_type=AgentType.CLOUD_FREE,
        api_key_env="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        context_limit=32768,
        best_for=["Instrucciones", "Chat", "Código"]
    ),
    
    AgentInfo(
        name="Groq Gemma 2 9B",
        provider="Groq",
        model="gemma2-9b-it",
        priority=Priority.GROQ,
        agent_type=AgentType.CLOUD_FREE,
        api_key_env="GROQ_API_KEY",
        base_url="https://api.groq.com/openai/v1",
        context_limit=8192,
        best_for=["Análisis", "Escritura", "Código"]
    ),
    
    # === TIER 4: HuggingFace Inference ===
    AgentInfo(
        name="HuggingFace Zephyr 7B",
        provider="HuggingFace",
        model="HuggingFaceH4/zephyr-7b-beta",
        priority=Priority.HUGGINGFACE,
        agent_type=AgentType.CLOUD_FREE,
        api_key_env="HF_API_KEY",
        base_url="https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
        context_limit=32768,
        best_for=["Chat", "Instrucciones", "General"]
    ),
    
    AgentInfo(
        name="HuggingFace Mistral 7B",
        provider="HuggingFace",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        priority=Priority.HUGGINGFACE,
        agent_type=AgentType.CLOUD_FREE,
        api_key_env="HF_API_KEY",
        base_url="https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
        context_limit=32768,
        best_for=["Código", "Instrucciones", "Chat"]
    ),
]

# ═══════════════════════════════════════════════════════════════
#  REGISTRY DE AGENTES LOCALES (FALLBACK)
# ═══════════════════════════════════════════════════════════════

LOCAL_AGENTS = [
    AgentInfo(
        name="Ollama Llama 3.1 8B",
        provider="Ollama Local",
        model="llama3.1:8b-instruct-q4_K_M",
        priority=Priority.OLLAMA,
        agent_type=AgentType.LOCAL,
        api_key_env="",
        base_url="http://localhost:11434/v1",
        context_limit=131072,
        best_for=["General", "Offline", "Privado"]
    ),
    
    AgentInfo(
        name="Ollama Qwen 2.5 Coder 7B",
        provider="Ollama Local",
        model="qwen2.5-coder:7b-instruct-q4_K_M",
        priority=Priority.OLLAMA,
        agent_type=AgentType.LOCAL,
        api_key_env="",
        base_url="http://localhost:11434/v1",
        context_limit=131072,
        best_for=["Código", "Debug", "Desarrollo"]
    ),
    
    AgentInfo(
        name="Ollama Qwen 2.5 14B",
        provider="Ollama Local",
        model="qwen2.5:14b-instruct-q4_K_M",
        priority=Priority.OLLAMA,
        agent_type=AgentType.LOCAL,
        api_key_env="",
        base_url="http://localhost:11434/v1",
        context_limit=131072,
        best_for=["Razonamiento avanzado", "Matemáticas"]
    ),
]

# ═══════════════════════════════════════════════════════════════
#  AGENT SELECTOR FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_cloud_agent(task_type: str) -> AgentInfo:
    """Obtener mejor agente cloud según tipo de tarea"""
    
    task_keywords = {
        "quick": ["minimax"],
        "code": ["llama", "mistral", "qwen", "zephyr"],
        "reasoning": ["gemini", "llama-3.1-70b", "qwen-14b"],
        "writing": ["gemma", "zephyr", "llama"],
        "chat": ["llama", "mistral", "gemma"],
        "analysis": ["gemini", "llama-3.1-70b", "gemma"],
        "multimodal": ["gemini-1.5"],
    }
    
    keywords = task_keywords.get(task_type, task_keywords["chat"])
    
    for agent in CLOUD_FREE_AGENTS:
        if agent.enabled and any(kw in agent.model.lower() for kw in keywords):
            return agent
    
    # Fallback al primer agente disponible
    for agent in CLOUD_FREE_AGENTS:
        if agent.enabled:
            return agent
    
    return None

def get_all_cloud_agents() -> List[AgentInfo]:
    """Lista de todos los agentes cloud disponibles"""
    return [a for a in CLOUD_FREE_AGENTS if a.enabled]

def get_fallback_agent() -> AgentInfo:
    """Obtener primer agente local como fallback"""
    for agent in LOCAL_AGENTS:
        if agent.enabled:
            return agent
    return None

def print_agent_registry():
    """Imprimir registro de agentes"""
    print("☁️ AGENTES CLOUD FREE (PRIORIDAD ALTA)")
    print("=" * 60)
    
    # Agrupar por provider
    providers = {}
    for agent in CLOUD_FREE_AGENTS:
        if agent.provider not in providers:
            providers[agent.provider] = []
        providers[agent.provider].append(agent)
    
    for provider, agents in providers.items():
        print(f"\n🏢 {provider}")
        for agent in agents:
            status = "✅" if agent.enabled else "❌"
            print(f"   {status} [{agent.priority.value}] {agent.name}")
            print(f"       Modelo: {agent.model}")
            print(f"       Mejor para: {', '.join(agent.best_for[:2])}")
    
    print("\n\n🏠 AGENTES LOCALES (FALLBACK)")
    print("=" * 60)
    for agent in LOCAL_AGENTS:
        status = "✅" if agent.enabled else "❌"
        print(f"   {status} {agent.name}")
        print(f"       URL: {agent.base_url}")

if __name__ == "__main__":
    print_agent_registry()

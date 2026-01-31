#!/usr/bin/env python3
"""
🤖 Configured Agents Factory
Solo agentes que ya tienes configurados.

Agentes disponibles:
- OpenCode MiniMax (cloud, gratis)
- Ollama Local (offline)
  - Llama 3.1 8B
  - Qwen 2.5 14B
  - Qwen 2.5 Coder 7B
  - Ministral 3 8B
- LM Studio Local (offline)
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Optional

from registry import (
    CONFIGURED_AGENTS,
    get_cloud_agent,
    get_ollama_agents,
    get_agent_by_task,
    check_services
)

# ═══════════════════════════════════════════════════════════════
#  OPENCODE MINIMAX (CLOUD - GRÁTIS)
# ═══════════════════════════════════════════════════════════════

def create_minimax_agent() -> Agent:
    """Crear agente OpenCode MiniMax (gratis)"""
    
    llm = ChatOpenAI(
        model="minimax/minimax-m2.1-free",
        base_url="https://opencode.ai/zen/v1",
        api_key="dummy",  # No requiere API key
        temperature=0.7,
        max_tokens=2048
    )
    
    return Agent(
        role="Quick Assistant",
        goal="Provide fast, concise responses",
        backstory="""You are a fast AI assistant powered by MiniMax via OpenCode.
You're optimized for quick answers and efficient communication.
Keep responses brief and helpful.""",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )

# ═══════════════════════════════════════════════════════════════
#  OLLAMA LOCAL AGENTS
# ═══════════════════════════════════════════════════════════════

def create_ollama_agent(model: str = None) -> Agent:
    """Crear agente Ollama local"""
    
    if not model:
        model = "llama3.1:8b-instruct-q4_K_M"
    
    llm = ChatOpenAI(
        model=model,
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        temperature=0.7,
        max_tokens=4096
    )
    
    # Rol según modelo
    role_map = {
        "llama3.1:8b-instruct-q4_K_M": ("General Assistant", "General purpose AI running locally"),
        "qwen2.5:14b-instruct-q4_K_M": ("Deep Reasoner", "Advanced reasoning AI running locally"),
        "qwen2.5-coder:7b-instruct-q4_K_M": ("Code Expert", "Specialized coding AI running locally"),
        "ministral-3:8b": ("Efficient Assistant", "Fast and efficient AI running locally"),
    }
    
    role, backstory = role_map.get(model, ("Local AI", "AI running locally on Ollama"))
    
    return Agent(
        role=role,
        goal="Provide helpful assistance",
        backstory=backstory,
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

def create_ollama_coder() -> Agent:
    """Crear agente especializado en código"""
    return create_ollama_agent("qwen2.5-coder:7b-instruct-q4_K_M")

def create_ollama_llama() -> Agent:
    """Crear agente con Llama 3.1"""
    return create_ollama_agent("llama3.1:8b-instruct-q4_K_M")

def create_ollama_qwen14b() -> Agent:
    """Crear agente con Qwen 2.5 14B"""
    return create_ollama_agent("qwen2.5:14b-instruct-q4_K_M")

# ═══════════════════════════════════════════════════════════════
#  LM STUDIO LOCAL AGENT
# ═══════════════════════════════════════════════════════════════

def create_lmstudio_agent(model: str = None) -> Optional[Agent]:
    """Crear agente LM Studio local"""
    
    import requests
    
    # Detectar modelo disponible
    if not model:
        try:
            resp = requests.get("http://localhost:1234/v1/models", timeout=2)
            if resp.status_code == 200:
                models = resp.json().get("data", [])
                if models:
                    model = models[0].get("id")
        except:
            pass
    
    if not model:
        return None
    
    llm = ChatOpenAI(
        model=model,
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        temperature=0.7,
        max_tokens=4096
    )
    
    return Agent(
        role="Local AI Assistant",
        goal="Provide helpful assistance using local resources",
        backstory="You are a private AI assistant running entirely locally via LM Studio.",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

# ═══════════════════════════════════════════════════════════════
#  AGENT FACTORY
# ═══════════════════════════════════════════════════════════════

def create_agent(agent_id: str) -> Optional[Agent]:
    """Crear agente por ID"""
    
    agent_map = {
        # Cloud
        "minimax": create_minimax_agent,
        "opencode": create_minimax_agent,
        # Ollama
        "ollama": create_ollama_agent,
        "ollama-llama": create_ollama_llama,
        "ollama-coder": create_ollama_coder,
        "ollama-qwen14b": create_ollama_qwen14b,
        # LM Studio
        "lmstudio": create_lmstudio_agent,
    }
    
    factory = agent_map.get(agent_id)
    if factory:
        return factory()
    return None

def get_best_agent_for_task(task: str, prefer_cloud: bool = True) -> Agent:
    """Obtener mejor agente para una tarea"""
    
    # Intentar cloud primero (MiniMax es gratis)
    if prefer_cloud:
        status = check_services()
        if status["opencode"]:
            return create_minimax_agent()
    
    # Fallback a Ollama local
    status = check_services()
    if status["ollama"]:
        task_lower = task.lower()
        if any(w in task_lower for w in ["code", "python", "debug", "script"]):
            return create_ollama_coder()
        elif any(w in task_lower for w in ["reason", "analyze", "math"]):
            return create_ollama_qwen14b()
        else:
            return create_ollama_llama()
    
    # Último recurso: LM Studio
    if status["lmstudio"]:
        agent = create_lmstudio_agent()
        if agent:
            return agent
    
    # Fallback absoluto: MiniMax (siempre debería funcionar)
    return create_minimax_agent()

# ═══════════════════════════════════════════════════════════════
#  STATUS & UTILS
# ═══════════════════════════════════════════════════════════════

def show_status():
    """Mostrar estado de servicios"""
    status = check_services()
    
    print("\n🤖 ESTADO DE SERVICIOS")
    print("=" * 40)
    
    services = [
        ("opencode", "☁️ OpenCode (MiniMax)", True),  # Siempre disponible
        ("ollama", "🏠 Ollama Local", status["ollama"]),
        ("lmstudio", "🏠 LM Studio Local", status["lmstudio"]),
    ]
    
    for key, name, is_up in services:
        icon = "✅" if is_up else "❌"
        print(f"  {icon} {name}")
    
    print("\n📋 AGENTES DISPONIBLES")
    print("=" * 40)
    print("  ✅ minimax / opencode  - Cloud gratuito")
    print("  ✅ ollama-llama        - Local general")
    print("  ✅ ollama-coder        - Local código")
    print("  ✅ ollama-qwen14b      - Local razonamiento")
    if status["lmstudio"]:
        print("  ✅ lmstudio           - Local personalizado")

def list_agents():
    """Listar agentes disponibles"""
    show_status()
    
    print("\n📝 USO")
    print("=" * 40)
    print("  create_agent('minimax')       → Cloud gratuito")
    print("  create_agent('ollama-coder')  → Local código")
    print("  get_best_agent_for_task(task) → Auto-seleccionar")

if __name__ == "__main__":
    list_agents()

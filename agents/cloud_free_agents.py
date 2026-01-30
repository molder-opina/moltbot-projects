#!/usr/bin/env python3
"""
🤖 Cloud Free Agent Factory
Factory para crear agentes de todos los modelos cloud gratuitos.

Uso:
    from cloud_free_agents import create_agent, get_best_agent_for_task
    
    # Crear agente específico
    agent = create_agent("opencode-minimax")
    
    # Obtener mejor agente para tarea
    agent = get_best_agent_for_task("code")
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Optional, Dict, Any

from cloud_free_registry import (
    CLOUD_FREE_AGENTS,
    LOCAL_AGENTS,
    AgentInfo,
    get_cloud_agent,
    get_fallback_agent
)

# ═══════════════════════════════════════════════════════════════
#  FACTORY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def create_opencode_minimax_agent() -> Agent:
    """Crear agente OpenCode MiniMax (gratis)"""
    llm = ChatOpenAI(
        model="minimax/minimax-m2.1-free",
        base_url="https://opencode.ai/zen/v1",
        api_key="dummy",
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

def create_gemini_agent(model: str = "gemini-1.5-flash") -> Agent:
    """Crear agente Google Gemini (gratis)"""
    import os
    api_key = os.getenv("GOOGLE_API_KEY", "")
    
    llm = ChatOpenAI(
        model=model,
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_key=api_key,
        temperature=0.7,
        max_tokens=8192
    )
    
    role_map = {
        "gemini-1.5-flash": "Fast Reasoner",
        "gemini-1.0-pro": "Deep Analyst"
    }
    
    return Agent(
        role=role_map.get(model, "Gemini Assistant"),
        goal="Provide thoughtful and comprehensive responses",
        backstory="You are powered by Google Gemini, capable of advanced reasoning and analysis.",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

def create_groq_agent(model: str = "llama-3.1-70b-versatile") -> Agent:
    """Crear agente Groq (gratis - extremadamente rápido)"""
    import os
    api_key = os.getenv("GROQ_API_KEY", "")
    
    llm = ChatOpenAI(
        model=model,
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
        temperature=0.7,
        max_tokens=4096
    )
    
    role_map = {
        "llama-3.1-70b-versatile": "Fast Reasoner",
        "llama-3-8b-8192": "Quick Assistant",
        "mistral-7b-instruct-v0.1": "Instruction Follower",
        "gemma2-9b-it": "Analyst"
    }
    
    return Agent(
        role=role_map.get(model, "Groq Assistant"),
        goal="Provide fast and accurate responses",
        backstory="You are powered by Groq's ultra-fast inference engine.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )

def create_huggingface_agent(model: str = "HuggingFaceH4/zephyr-7b-beta") -> Agent:
    """Crear agente HuggingFace (gratis)"""
    import os
    api_key = os.getenv("HF_API_KEY", "")
    
    llm = ChatOpenAI(
        model=model,
        base_url="https://api-inference.huggingface.co/models/" + model,
        api_key=api_key,
        temperature=0.7,
        max_tokens=2048
    )
    
    return Agent(
        role="Open Source Assistant",
        goal="Help with various tasks using open source models",
        backstory="You are powered by open source models from HuggingFace.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )

def create_local_agent(model: str = "llama3.1:8b-instruct-q4_K_M") -> Agent:
    """Crear agente local (fallback)"""
    llm = ChatOpenAI(
        model=model,
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        temperature=0.7,
        max_tokens=4096
    )
    
    return Agent(
        role="Local Assistant",
        goal="Provide helpful assistance offline",
        backstory="You are running locally with full privacy.",
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
        # Cloud Free
        "opencode-minimax": create_opencode_minimax_agent,
        "gemini-flash": lambda: create_groq_agent("gemini-1.5-flash"),
        "gemini-pro": lambda: create_groq_agent("gemini-1.0-pro"),
        "groq-llama70b": lambda: create_groq_agent("llama-3.1-70b-versatile"),
        "groq-llama8b": lambda: create_groq_agent("llama-3-8b-8192"),
        "groq-mistral": lambda: create_groq_agent("mistral-7b-instruct-v0.1"),
        "groq-gemma": lambda: create_groq_agent("gemma2-9b-it"),
        "hf-zephyr": lambda: create_huggingface_agent("HuggingFaceH4/zephyr-7b-beta"),
        "hf-mistral": lambda: create_huggingface_agent("mistralai/Mistral-7B-Instruct-v0.2"),
        # Locales
        "ollama-llama": lambda: create_local_agent("llama3.1:8b-instruct-q4_K_M"),
        "ollama-coder": lambda: create_local_agent("qwen2.5-coder:7b-instruct-q4_K_M"),
        "ollama-qwen14b": lambda: create_local_agent("qwen2.5:14b-instruct-q4_K_M"),
    }
    
    factory = agent_map.get(agent_id)
    if factory:
        return factory()
    return None

def get_best_agent_for_task(task: str, prefer_cloud: bool = True) -> Agent:
    """Obtener mejor agente para una tarea"""
    
    # Intentar cloud primero
    if prefer_cloud:
        cloud_agent = get_cloud_agent(task)
        if cloud_agent:
            agent = create_agent_by_model(cloud_agent.model)
            if agent:
                return agent
    
    # Fallback a local
    local_agent = get_fallback_agent()
    if local_agent:
        return create_agent_by_model(local_agent.model)
    
    # Último recurso: MiniMax
    return create_opencode_minimax_agent()

def create_agent_by_model(model: str) -> Optional[Agent]:
    """Crear agente según modelo"""
    
    model_map = {
        # OpenCode
        "minimax/minimax-m2.1-free": create_opencode_minimax_agent,
        # Gemini
        "gemini-1.5-flash": lambda: create_gemini_agent("gemini-1.5-flash"),
        "gemini-1.0-pro": lambda: create_gemini_agent("gemini-1.0-pro"),
        # Groq
        "llama-3.1-70b-versatile": lambda: create_groq_agent("llama-3.1-70b-versatile"),
        "llama-3-8b-8192": lambda: create_groq_agent("llama-3-8b-8192"),
        "mistral-7b-instruct-v0.1": lambda: create_groq_agent("mistral-7b-instruct-v0.1"),
        "gemma2-9b-it": lambda: create_groq_agent("gemma2-9b-it"),
        # HuggingFace
        "HuggingFaceH4/zephyr-7b-beta": lambda: create_huggingface_agent("HuggingFaceH4/zephyr-7b-beta"),
        "mistralai/Mistral-7B-Instruct-v0.2": lambda: create_huggingface_agent("mistralai/Mistral-7B-Instruct-v0.2"),
        # Locales
        "llama3.1:8b-instruct-q4_K_M": lambda: create_local_agent("llama3.1:8b-instruct-q4_K_M"),
        "qwen2.5-coder:7b-instruct-q4_K_M": lambda: create_local_agent("qwen2.5-coder:7b-instruct-q4_K_M"),
        "qwen2.5:14b-instruct-q4_K_M": lambda: create_local_agent("qwen2.5:14b-instruct-q4_K_M"),
    }
    
    factory = model_map.get(model)
    if factory:
        return factory()
    return None

# ═══════════════════════════════════════════════════════════════
#  USAGE EXAMPLES
# ═══════════════════════════════════════════════════════════════

def example_usage():
    """Ejemplos de uso"""
    
    # 1. Crear agente específico
    agent = create_agent("opencode-minimax")
    print(f"✅ Agente creado: {agent.role}")
    
    # 2. Obtener mejor agente para tarea
    code_agent = get_best_agent_for_task("code")
    print(f"✅ Agente para código: {code_agent.role}")
    
    # 3. Usar con CrewAI
    from crewai import Crew, Task
    
    crew = Crew(
        agents=[
            create_agent("opencode-minimax"),
            create_agent("groq-llama70b"),
        ],
        tasks=[
            Task(
                description="Answer quickly",
                agent=create_agent("opencode-minimax"),
                expected_output="Brief answer"
            ),
            Task(
                description="Provide detailed analysis",
                agent=create_agent("groq-llama70b"),
                expected_output="Detailed analysis"
            )
        ],
        process=0  # Sequential
    )
    
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    from cloud_free_registry import print_agent_registry
    
    print_agent_registry()
    
    print("\n" + "=" * 60)
    print("🚀 EJEMPLO: Crear agente")
    agent = create_agent("opencode-minimax")
    print(f"✅ {agent.role} creado")

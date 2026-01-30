#!/usr/bin/env python3
"""
🤖 MiniMax Agent - OpenCode (Gratis)
Especializado en respuestas breves y concisas

Configuración:
- Provider: OpenCode
- Model: minimax/MiniMax-M2.1-free
- Características: Rápido, gratuito, ideal para consultas simples
"""

from crewai import Agent
from langchain_openai import ChatOpenAI

def create_minimax_agent():
    """Crear agente con MiniMax (OpenCode)"""
    
    llm = ChatOpenAI(
        model="minimax/minimax-m2.1-free",
        base_url="https://opencode.ai/zen/v1",
        api_key="dummy",  # OpenCode no requiere API key
        temperature=0.7,
        max_tokens=2048
    )
    
    agent = Agent(
        role="Quick Assistant",
        goal="Provide fast, concise, and helpful responses",
        backstory="""You are a helpful AI assistant powered by MiniMax (via OpenCode).
You specialize in quick answers, summaries, and straightforward assistance.
Your responses are always brief and to the point.""",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    
    return agent

# Configuración del agente
AGENT_CONFIG = {
    "name": "MiniMax Agent",
    "provider": "OpenCode (MiniMax M2.1)",
    "model": "minimax/minimax-m2.1-free",
    "cost": "Gratis",
    "best_for": [
        "Consultas rápidas",
        "Respuestas breves",
        "Tareas simples",
        "Conversación casual"
    ],
    "limitations": [
        "Contexto limitado (131K tokens)",
        "Sin herramientas avanzadas"
    ]
}

if __name__ == "__main__":
    agent = create_minimax_agent()
    print(f"✅ {AGENT_CONFIG['name']} creado")
    print(f"   Provider: {AGENT_CONFIG['provider']}")
    print(f"   Best for: {', '.join(AGENT_CONFIG['best_for'][:2])}")

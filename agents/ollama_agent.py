#!/usr/bin/env python3
"""
🧠 Ollama Local Agent - Modelos Locales (Gratis)
Especializado en código, investigación y tareas complejas

Modelos disponibles:
- llama3.1:8b - General purpose
- qwen2.5:14b - Reasoning avanzado
- qwen2.5-coder:7b - Coding especializado
- nomic-embed-text - Embeddings locales
"""

from crewai import Agent
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

def create_ollama_agent(model: str = "llama3.1:8b-instruct-q4_K_M"):
    """Crear agente con Ollama local"""
    
    llm = ChatOpenAI(
        model=model,
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # Dummy key para local
        temperature=0.7,
        max_tokens=8192
    )
    
    # Selección de rol según modelo
    model_roles = {
        "llama3.1:8b-instruct-q4_K_M": {
            "role": "General Assistant",
            "goal": "Assist with a wide variety of tasks efficiently",
            "backstory": "You are a versatile AI assistant running locally on Ollama with Llama 3.1."
        },
        "qwen2.5:14b-instruct-q4_K_M": {
            "role": "Deep Reasoner",
            "goal": "Solve complex problems with advanced reasoning",
            "backstory": "You are an advanced reasoning AI powered by Qwen 2.5 14B, running locally on Ollama."
        },
        "qwen2.5-coder:7b-instruct-q4_K_M": {
            "role": "Code Expert",
            "goal": "Write, debug, and explain code",
            "backstory": "You are a specialized coding AI powered by Qwen 2.5 Coder, running locally on Ollama."
        }
    }
    
    config = model_roles.get(model, model_roles["llama3.1:8b-instruct-q4_K_M"])
    
    agent = Agent(
        role=config["role"],
        goal=config["goal"],
        backstory=config["backstory"],
        llm=llm,
        verbose=True,
        allow_delegation=True
    )
    
    return agent, model

# Configuraciones disponibles
OLLAMA_CONFIGS = {
    "llama3.1:8b": {
        "name": "Llama 3.1 8B",
        "provider": "Ollama Local",
        "context": "131K tokens",
        "best_for": ["General assistance", "Writing", "Analysis"]
    },
    "qwen2.5:14b": {
        "name": "Qwen 2.5 14B",
        "provider": "Ollama Local",
        "context": "131K tokens",
        "best_for": ["Complex reasoning", "Research", "Math"]
    },
    "qwen2.5-coder:7b": {
        "name": "Qwen 2.5 Coder 7B",
        "provider": "Ollama Local",
        "context": "131K tokens",
        "best_for": ["Code generation", "Debugging", "Documentation"]
    }
}

if __name__ == "__main__":
    # Demo: crear agente con diferentes modelos
    for model in ["llama3.1:8b-instruct-q4_K_M", "qwen2.5-coder:7b-instruct-q4_K_M"]:
        agent, m = create_ollama_agent(model)
        print(f"✅ Agente creado: {agent.role}")

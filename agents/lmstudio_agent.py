#!/usr/bin/env python3
"""
🏠 LM Studio Local Agent - Modelos Locales (Gratis)
Especializado en tareas que requieren modelos específicos

Características:
- Totalmente offline
- Modelos personalizados
- Privacidad total
- Sin límites de uso
"""

from crewai import Agent
from langchain_openai import ChatOpenAI

def create_lmstudio_agent(model_name: str = None):
    """Crear agente con LM Studio local"""
    
    # Detectar modelo disponible
    import requests
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=2)
        if response.status_code == 200:
            models = response.json().get("data", [])
            if models and not model_name:
                model_name = models[0].get("id", "unknown")
    except:
        model_name = model_name or "your-model"
    
    llm = ChatOpenAI(
        model=model_name,
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",  # Dummy key para local
        temperature=0.7,
        max_tokens=4096
    )
    
    agent = Agent(
        role="Local AI Assistant",
        goal="Provide helpful assistance using local resources",
        backstory="""You are a private AI assistant running entirely locally via LM Studio.
You have no external dependencies and respect user privacy completely.
You can handle a wide range of tasks efficiently.""",
        llm=llm,
        verbose=True,
        allow_delegation=True
    )
    
    return agent, model_name

def get_available_models():
    """Obtener modelos disponibles en LM Studio"""
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=2)
        if response.status_code == 200:
            return [m.get("id") for m in response.json().get("data", [])]
    except Exception as e:
        return []
    return []

# Configuración
LMSTUDIO_CONFIG = {
    "name": "LM Studio Agent",
    "provider": "LM Studio Local",
    "url": "http://localhost:1234/v1",
    "features": [
        "100% Offline",
        "Modelos personalizados",
        "Sin límites de uso",
        "Privacidad total"
    ]
}

if __name__ == "__main__":
    models = get_available_models()
    if models:
        print(f"📋 Modelos disponibles: {models}")
        agent, model = create_lmstudio_agent(models[0])
        print(f"✅ Agente creado con: {model}")
    else:
        print("⚠️ LM Studio no está corriendo en localhost:1234")
        print("💡 Inicia LM Studio y carga un modelo para usar este agente")

#!/usr/bin/env python3
"""
🎯 Multi-Agent Coordinator - CrewAI Integration
Coordina agentes especializados según la tarea

Agentes disponibles:
1. MiniMax (OpenCode) - Consultas rápidas
2. Ollama Local - Código y razonamiento
3. LM Studio - Modelos personalizados

Usage:
    from coordinator_agent import crew_coordinator
    
    result = crew_coordinator.kickoff(
        inputs={
            "task": "Write a Python script",
            "complexity": "high",
            "preferred_agent": "ollama"  # optional
        }
    )
"""

from crewai import Crew, Agent, Task, Process
from typing import Optional, Dict, List

# Importar agentes
from minimax_agent import create_minimax_agent, AGENT_CONFIG as MINIMAX_CONFIG
from ollama_agent import create_ollama_agent, OLLAMA_CONFIGS
from lmstudio_agent import create_lmstudio_agent, LMSTUDIO_CONFIG

class MultiAgentCoordinator:
    """Coordinador de agentes múltiples"""
    
    def __init__(self):
        self.minimax_agent = create_minimax_agent()
        self.ollama_general = create_ollama_agent("llama3.1:8b-instruct-q4_K_M")
        self.ollama_coder = create_ollama_agent("qwen2.5-coder:7b-instruct-q4_K_M")
        self.lmstudio_agent = None
        try:
            self.lmstudio_agent, _ = create_lmstudio_agent()
        except:
            pass
    
    def get_crew_for_task(self, task_type: str, complexity: str = "medium") -> Crew:
        """Obtener crew según tipo de tarea"""
        
        agents_map = {
            "quick": [self.minimax_agent],
            "general": [self.minimax_agent, self.ollama_general],
            "code": [self.ollama_coder],
            "research": [self.ollama_general, self.minimax_agent],
            "complex": [self.ollama_general, self.ollama_coder],
            "full": [self.minimax_agent, self.ollama_general, self.ollama_coder]
        }
        
        agents = agents_map.get(task_type, agents_map["general"])
        
        # Crear tareas según agentes
        tasks = []
        for i, agent in enumerate(agents):
            task = Task(
                description=f"Handle task part {i+1}: {task_type}",
                agent=agent,
                expected_output=f"Output for {agent.role}"
            )
            tasks.append(task)
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        return crew
    
    def execute_task(self, task: str, context: str = "", preferred: str = None) -> str:
        """Ejecutar tarea con agente preferido o automático"""
        
        if preferred == "minimax":
            crew = self.get_crew_for_task("quick")
        elif preferred == "ollama":
            crew = self.get_crew_for_task("general")
        elif preferred == "lmstudio" and self.lmstudio_agent:
            crew = Crew(
                agents=[self.lmstudio_agent],
                tasks=[Task(description=task, agent=self.lmstudio_agent)],
                process=Process.sequential
            )
        else:
            # Auto-seleccionar según tarea
            task_lower = task.lower()
            if any(w in task_lower for w in ["code", "python", "javascript", "debug", "script"]):
                crew = self.get_crew_for_task("code")
            elif any(w in task_lower for w in ["research", "analyze", "investigate"]):
                crew = self.get_crew_for_task("research")
            elif len(task) < 200:
                crew = self.get_crew_for_task("quick")
            else:
                crew = self.get_crew_for_task("complex")
        
        result = crew.kickoff(inputs={"task": task, "context": context})
        return result

# Instancia global
crew_coordinator = MultiAgentCoordinator()

# Mapeo de tareas
AGENT_SELECTOR = {
    "quick_question": ("minimax", "Consultas rápidas y simples"),
    "coding": ("ollama_coder", "Desarrollo de software"),
    "research": ("ollama_general", "Investigación y análisis"),
    "writing": ("ollama_general", "Escritura creativa"),
    "local_model": ("lmstudio", "Modelos personalizados locales"),
    "complex_task": ("ollama_14b", "Razonamiento avanzado")
}

if __name__ == "__main__":
    coordinator = MultiAgentCoordinator()
    
    print("🤖 Multi-Agent Coordinator Initialized")
    print(f"   ✅ MiniMax: {MINIMAX_CONFIG['provider']}")
    print(f"   ✅ Ollama: {len(OLLAMA_CONFIGS)} modelos")
    print(f"   ✅ LM Studio: {'Disponible' if coordinator.lmstudio_agent else 'No disponible'}")
    
    print("\n📋 Agentes disponibles:")
    for key, (agent, desc) in AGENT_SELECTOR.items():
        print(f"   • {key}: {desc}")

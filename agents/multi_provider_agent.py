#!/usr/bin/env python3
"""
🎯 Multi-Provider Agent System
Sistema que prioriza cloud free y usa locales como fallback.

Usage:
    python3 multi_provider_agent.py --agent opencode-minimax --task "Hola"
    python3 multi_provider_agent.py --task "Escribe código" --auto
    python3 multi_provider_agent.py --list
"""

import argparse
import sys
from crewai import Crew, Task

# Importar sistema de agentes
sys.path.insert(0, '/Users/molder/moltbot/projects/agents')
from cloud_free_agents import (
    create_agent,
    get_best_agent_for_task,
    example_usage
)
from cloud_free_registry import (
    print_agent_registry,
    get_all_cloud_agents,
    get_fallback_agent
)

def list_agents():
    """Listar todos los agentes disponibles"""
    print("\n🤖 AGENTES DISPONIBLES")
    print("=" * 60)
    
    cloud = get_all_cloud_agents()
    local = get_fallback_agent()
    
    print(f"\n☁️ CLOUD FREE ({len(cloud)} agentes)")
    print("-" * 40)
    for i, agent in enumerate(cloud, 1):
        print(f"  {i}. {agent.name}")
        print(f"     Modelo: {agent.model}")
        print(f"     Mejor para: {', '.join(agent.best_for[:2])}")
    
    print(f"\n🏠 LOCAL FALLBACK")
    print("-" * 40)
    if local:
        print(f"  • {local.name}")
        print(f"    Modelo: {local.model}")
    else:
        print("  ❌ No hay agentes locales configurados")

def run_task(agent_id: str, task: str):
    """Ejecutar tarea con agente específico"""
    
    agent = create_agent(agent_id)
    if not agent:
        print(f"❌ Agente '{agent_id}' no encontrado")
        print("💡 Usa --list para ver agentes disponibles")
        return
    
    print(f"🚀 Ejecutando con {agent.role}...")
    
    # Ejecutar tarea simple
    from crewai import Agent
    task_obj = Task(
        description=task,
        agent=agent,
        expected_output="Response to the task"
    )
    
    crew = Crew(agents=[agent], tasks=[task_obj])
    result = crew.kickoff()
    
    print(f"\n✅ Resultado:")
    print(result)

def run_auto(task: str, task_type: str = "general"):
    """Auto-seleccionar mejor agente"""
    
    agent = get_best_agent_for_task(task_type)
    print(f"🎯 Agente seleccionado: {agent.role}")
    
    task_obj = Task(
        description=task,
        agent=agent,
        expected_output="Response"
    )
    
    crew = Crew(agents=[agent], tasks=[task_obj])
    result = crew.kickoff()
    
    print(f"\n✅ Resultado:")
    print(result)

def show_priority_order():
    """Mostrar orden de prioridad"""
    print("\n📊 ORDEN DE PRIORIDAD")
    print("=" * 60)
    print("\n☁️ CLOUD FREE (primero):")
    print("   1. OpenCode MiniMax - Consultas rápidas")
    print("   2. Google Gemini - Razonamiento")
    print("   3. Groq - Modelos ultra-rápidos")
    print("   4. HuggingFace - Modelos open source")
    
    print("\n🏠 LOCAL (fallback):")
    print("   10. Ollama - Modelos locales")
    print("   11. LM Studio - Modelos personalizados")

def main():
    parser = argparse.ArgumentParser(
        description="Multi-Provider Agent System"
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="Listar agentes disponibles"
    )
    
    parser.add_argument(
        "--priority", "-p",
        action="store_true", 
        help="Mostrar orden de prioridad"
    )
    
    parser.add_argument(
        "--agent", "-a",
        type=str,
        help="ID del agente a usar"
    )
    
    parser.add_argument(
        "--task", "-t",
        type=str,
        help="Tarea a ejecutar"
    )
    
    parser.add_argument(
        "--auto", "-A",
        action="store_true",
        help="Auto-seleccionar mejor agente"
    )
    
    parser.add_argument(
        "--type",
        type=str,
        default="general",
        choices=["quick", "code", "reasoning", "writing", "chat", "analysis"],
        help="Tipo de tarea para auto-selección"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_agents()
    elif args.priority:
        show_priority_order()
    elif args.agent and args.task:
        run_task(args.agent, args.task)
    elif args.auto and args.task:
        run_auto(args.task, args.type)
    else:
        print("🎯 Multi-Provider Agent System")
        print("\nOpciones:")
        print("  -l, --list      Listar agentes")
        print("  -p, --priority  Ver prioridad")
        print("  -a AGENTE -t TAREA  Ejecutar con agente específico")
        print("  -A -t TAREA --type tipo  Auto-seleccionar agente")
        print("\nEjemplos:")
        print("  python3 multi_provider_agent.py -l")
        print("  python3 multi_provider_agent.py -a opencode-minimax -t 'Hola'")
        print("  python3 multi_provider_agent.py -A -t 'Escribe código' --type code")

if __name__ == "__main__":
    main()

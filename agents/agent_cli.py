#!/usr/bin/env python3
"""
🤖 Configured Agents CLI
Usa solo los agentes que ya tienes configurados.

Uso:
    python3 agent_cli.py --status
    python3 agent_cli.py --use minimax --task "Hola"
    python3 agent_cli.py --auto --task "Escribe código"
"""

import argparse
import sys
from crewai import Crew, Task

sys.path.insert(0, '/Users/molder/moltbot/projects/agents')

from agents import (
    create_agent,
    create_minimax_agent,
    create_ollama_coder,
    create_ollama_llama,
    create_ollama_qwen14b,
    create_lmstudio_agent,
    get_best_agent_for_task,
    show_status
)

def run_with_agent(agent_id: str, task: str):
    """Ejecutar tarea con agente específico"""
    
    agent = create_agent(agent_id)
    if not agent:
        print(f"❌ Agente '{agent_id}' no disponible")
        show_status()
        return
    
    print(f"🚀 Ejecutando con {agent.role}...")
    
    task_obj = Task(
        description=task,
        agent=agent,
        expected_output="Response"
    )
    
    crew = Crew(agents=[agent], tasks=[task_obj])
    result = crew.kickoff()
    
    print(f"\n✅ Resultado:")
    print(result)

def run_auto(task: str, task_type: str = "general"):
    """Auto-seleccionar mejor agente"""
    
    agent = get_best_agent_for_task(task)
    print(f"🎯 Usando: {agent.role}")
    
    task_obj = Task(
        description=task,
        agent=agent,
        expected_output="Response"
    )
    
    crew = Crew(agents=[agent], tasks=[task_obj])
    result = crew.kickoff()
    
    print(f"\n✅ Resultado:")
    print(result)

def main():
    parser = argparse.ArgumentParser(
        description="Configured Agents CLI"
    )
    
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Ver estado de servicios"
    )
    
    parser.add_argument(
        "--use", "-u",
        type=str,
        help="Agente a usar (minimax, ollama-coder, ollama-llama, etc.)"
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
        choices=["quick", "code", "reasoning", "general"],
        help="Tipo de tarea para auto-selección"
    )
    
    args = parser.parse_args()
    
    if args.status:
        show_status()
    elif args.use and args.task:
        run_with_agent(args.use, args.task)
    elif args.auto and args.task:
        run_auto(args.task, args.type)
    else:
        print("🤖 Configured Agents CLI")
        print("\nOpciones:")
        print("  -s, --status          Ver estado")
        print("  -u AGENTE -t TAREA    Ejecutar con agente")
        print("  -A -t TAREA           Auto-seleccionar")
        print("\nAgentes disponibles:")
        print("  minimax       - Cloud gratuito (siempre disponible)")
        print("  ollama-llama  - Local general")
        print("  ollama-coder  - Local código")
        print("  ollama-qwen14b- Local razonamiento")
        print("  lmstudio      - Local personalizado")
        show_status()

if __name__ == "__main__":
    main()

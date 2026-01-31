# Moltbot Agents Package
# Solo agentes que ya tienes configurados y funcionando

from registry import (
    # Registry
    CONFIGURED_AGENTS,
    get_cloud_agent,
    get_ollama_agents,
    get_agent_by_task,
    check_services,
    print_status,
    LOCAL_CONFIGS
)

from agents import (
    # Factory
    create_agent,
    create_minimax_agent,
    create_ollama_agent,
    create_ollama_coder,
    create_ollama_llama,
    create_ollama_qwen14b,
    create_lmstudio_agent,
    get_best_agent_for_task,
    show_status,
    list_agents
)

from agent_cli import (
    run_with_agent,
    run_auto
)

__all__ = [
    # Registry
    "CONFIGURED_AGENTS",
    "get_cloud_agent",
    "get_ollama_agents",
    "get_agent_by_task",
    "check_services",
    "print_status",
    "LOCAL_CONFIGS",
    
    # Factory
    "create_agent",
    "create_minimax_agent",
    "create_ollama_agent",
    "create_ollama_coder",
    "create_ollama_llama",
    "create_ollama_qwen14b",
    "create_lmstudio_agent",
    "get_best_agent_for_task",
    "show_status",
    "list_agents",
    
    # CLI
    "run_with_agent",
    "run_auto"
]

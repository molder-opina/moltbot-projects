# Moltbot Agents Package
# Sistema de agentes con prioridad: Cloud Free → Local Fallback

from cloud_free_registry import (
    # Registry
    CLOUD_FREE_AGENTS,
    LOCAL_AGENTS,
    AgentInfo,
    Priority,
    AgentType,
    get_cloud_agent,
    get_fallback_agent,
    get_all_cloud_agents,
    print_agent_registry
)

from cloud_free_agents import (
    # Factory
    create_agent,
    create_agent_by_model,
    create_opencode_minimax_agent,
    create_gemini_agent,
    create_groq_agent,
    create_huggingface_agent,
    create_local_agent,
    get_best_agent_for_task,
    example_usage
)

__all__ = [
    # Registry
    "CLOUD_FREE_AGENTS",
    "LOCAL_AGENTS", 
    "AgentInfo",
    "Priority",
    "AgentType",
    "get_cloud_agent",
    "get_fallback_agent",
    "get_all_cloud_agents",
    "print_agent_registry",
    
    # Factory
    "create_agent",
    "create_agent_by_model",
    "create_opencode_minimax_agent",
    "create_gemini_agent",
    "create_groq_agent",
    "create_huggingface_agent",
    "create_local_agent",
    "get_best_agent_for_task",
    "example_usage"
]

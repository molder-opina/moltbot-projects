# Moltbot Agents Package

from minimax_agent import create_minimax_agent, AGENT_CONFIG as MINIMAX_CONFIG
from ollama_agent import create_ollama_agent, OLLAMA_CONFIGS
from lmstudio_agent import create_lmstudio_agent, LMSTUDIO_CONFIG
from coordinator_agent import MultiAgentCoordinator, crew_coordinator, AGENT_SELECTOR

__all__ = [
    "create_minimax_agent",
    "MINIMAX_CONFIG",
    "create_ollama_agent",
    "OLLAMA_CONFIGS", 
    "create_lmstudio_agent",
    "LMSTUDIO_CONFIG",
    "MultiAgentCoordinator",
    "crew_coordinator",
    "AGENT_SELECTOR"
]

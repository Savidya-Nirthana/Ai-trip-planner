"""
Application configuration - loads from yaml param file

CONFIGURATION POLICY:
========================

Configuration is loaded from a params.yaml file and models.yaml file in stored in config directory.
Secrets (API keys) are stored only in .env file.

Supported multiple LLM providers via openrouter unified API or directly providers.
- Openrouter 
- OpenAI
- Anthropic
- Google
- Groq
- DeepSeek

"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import os
import yaml


# ================================
# Project paths 
# ================================

_PROJECT_DIR = Path(__file__).parent.parent.parent
_CONFIG_DIR = _PROJECT_DIR / "config"


# ================================
# Yaml Config Loading
# ===============================

def _load_yaml(filename: str) -> Dict[str, Any]:
    """Load a yaml file into a dictionary."""
    filepath = _CONFIG_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Config file {filename} not found.")
    with open(filepath, "r") as f:
        return yaml.safe_load(f) or {}
    

def _get_nested(d: Dict, *keys, default: None):
    """ Get nested dictionary value by key path """
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d if d is not None else default


# Load configs
_PARAMS = _load_yaml("params.yaml")
_MODELS = _load_yaml("models.yaml")


# ================================
# Provider Configuration
# ================================

PROVIDER = _get_nested(_PARAMS, "provider", "default" ,default="openrouter")
MODEL_TIER = _get_nested(_PARAMS, "provider", "tier", default="general")
OPENROUTER_BASE_URL = _get_nested(_PARAMS, "provider", "openrouter_base_url", 
                                    default="https://api.openrouter.ai/v1")

# ===================================
# Model names (from models.yaml)
# ===================================

def get_chat_model(provider: Optional[str] =None, tier: Optional[str] = None) -> str:
    """ Get chat model name for specified provider and tier. """
    provider = provider or PROVIDER
    tier = tier or MODEL_TIER

    if provider == 'google':
        provider = "google"
    elif provider == 'gemini':
        provider = "google"
    
    return _get_nested(_MODELS, provider, "chat", tier, default="google/gemini-2.5-flash")

EMBEDDING_TIER = _get_nested(_PARAMS, "embedding", "tier", default="small")

def get_embedding_model(provider: Optional[str] =None, tier: Optional[str] = None) -> str:
    """ Get embedding model name for specified provider and tier. """
    provider = provider or PROVIDER
    tier = tier or EMBEDDING_TIER

    if provider == 'google':
        provider = "google"
    elif provider == 'gemini':
        provider = "google"
    
    return _get_nested(_MODELS, provider, "embedding", tier, default="openai/text-embedding-3-small")


def get_api_key(provider: Optional[str] = None) -> Optional[str]:
    """ Get api keys given provider """
    provider = provider or PROVIDER
    key_map = {
        "openrouter": "OPENROUTER_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
        "groq": "GROQ_API_KEY",
        "deepseek" : "DEEPSEEK_API_KEY",
        "travily" : "TRAVILY_API_KEY"
    }

    env_var = key_map.get(provider, f"{provider.upper()}_API_KEY")
    return os.getenv(env_var)

ROUTER_MODEL = "openai/gpt-4o-mini"
ROUTER_PROVIDER = "openrouter"

CHAT_MODEL = "google/gemini-2.5-flash"
CHAT_PROVIDER = "openrouter"

EMBEDDING_MODEL = get_embedding_model()

OPENAI_CHAT_MODEL = CHAT_MODEL

EMBEDDING_DIM = 1536

if "large" in EMBEDDING_MODEL.lower():
    EMBEDDING_DIM = 3072
elif "small" in EMBEDDING_MODEL.lower():
    EMBEDDING_DIM = 1536
else:
    EMBEDDING_DIM = 1536


# ===================================
# LLM Parameters
# ===================================

LLM_TEMPERATURE = _get_nested(_PARAMS, "llm", "temperature", default=0.0)
LLM_MAX_TOKENS = _get_nested(_PARAMS, "llm", "max_tokens", default=2000)
LLM_STREAMING = _get_nested(_PARAMS, "llm", "streaming", default=False)

# ===================================
# Embedding Parameters
# ===================================

EMBEDDING_BATCH_SIZE = _get_nested(_PARAMS, "embedding", "batch_size", default=100)
EMBEDDING_SHOW_PROGRESS = _get_nested(_PARAMS, "embedding", "show_progress", default=False)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"







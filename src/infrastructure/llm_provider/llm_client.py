"""
Chat LLM Providers

Two specialized LLMs for different tasks:
- Router : routes user messages to the correct tool
- Agent: execute the tool and generate response

"""

from typing import Optional, Any, Dict
from langchain_openai import ChatOpenAI
from src.infrastructure.config import (
    OPENROUTER_BASE_URL,
    GROQ_BASE_URL
)

def _build_llm(
    model: str,
    provider: str,
    temperature: float = 0,
    streaming: bool = False,
    max_tokens: Optional[int] = None,
    **kwargs
) -> ChatOpenAI:
    """ Build ChatOpenAI instance with provider-specific configuration """
    llm_kwargs: Dict[str, Any] = dict(
        model= model,
        temperature = temperature,
        max_tokens = max_tokens,
        streaming = streaming,
        **kwargs
    )

    if provider == "openrouter":
        llm_kwargs['openai_api_base'] = OPENROUTER_BASE_URL
        llm_kwargs['openai_api_key'] = get_api_key(provider)

    elif provider == "groq":
        llm_kwargs['openai_api_key'] = get_api_key(provider)
        llm_kwargs["openai_api_base"] = GROQ_BASE_URL
    
    elif provider == "openai":
        llm_kwargs['openai_api_key'] = get_api_key(provider)
    

    return ChatOpenAI(**llm_kwargs)



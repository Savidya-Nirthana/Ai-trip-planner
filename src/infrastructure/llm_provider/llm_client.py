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
    GROQ_BASE_URL,
    CHAT_MODEL, 
    CHAT_PROVIDER,
    get_api_key,
    GROQ_MODEL
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
        llm_kwargs["openai_api_base"] = GROQ_BASE_URL
        llm_kwargs['openai_api_key'] = get_api_key(provider)
    
    elif provider == "openai":
        llm_kwargs['openai_api_key'] = get_api_key(provider)
    

    return ChatOpenAI(**llm_kwargs)


def get_chat_llm(provider: str = "openrouter", temperature: float = 0.0, **kwargs: Any) -> ChatOpenAI:
    """ Return the chat llm """
    return _build_llm(
        model = CHAT_MODEL if provider == "openrouter" else GROQ_MODEL,
        provider = provider,
        temperature = temperature,
        **kwargs
    )





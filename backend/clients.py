import os
import logging
from openai import OpenAI
from anthropic import Anthropic

logger = logging.getLogger(__name__)

def get_client_and_model(provider: str = None, model: str = None):
    """
    Returns (client, model_name).
    Supports 'anthropic', 'openrouter', and 'ollama'.
    """
    provider = provider or os.getenv("DEFAULT_PROVIDER", "openrouter")
    
    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        logger.info(f"Using Ollama at {base_url}")
        client = OpenAI(
            base_url=base_url,
            api_key="ollama", # Placeholder
        )
        return client, model or os.getenv("OLLAMA_MODEL", "llama3.2:latest")
        
    if provider == "openrouter":
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        logger.info("Using OpenRouter")
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
        )
        return client, model or os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    
    # Fallback to Anthropic
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    logger.info("Using native Anthropic client")
    client = Anthropic(api_key=anthropic_key)
    return client, model or "claude-3-5-sonnet-20240620"

def is_openai_client(client):
    return isinstance(client, OpenAI)

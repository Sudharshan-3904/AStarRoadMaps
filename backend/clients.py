import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

def get_client_and_model(provider: str = None, model: str = None):
    """
    Returns (client, model_name).
    Supports 'openrouter' and 'ollama'. Falls back to Ollama.
    """
    provider = provider or os.getenv("DEFAULT_PROVIDER", "ollama")
    
    if provider == "openrouter":
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            logger.info("Using OpenRouter client")
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_key,
            )
            return client, model or os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b:free")
    
    # Default to Ollama
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1")
    logger.info(f"Using Ollama client at {base_url}")
    client = OpenAI(
        base_url=base_url,
        api_key="ollama", # Placeholder for ollama
    )
    return client, model or os.getenv("OLLAMA_MODEL", "llama3.2:latest")

def is_openai_client(client):
    """Since we only use OpenAI-compatible clients now (OpenRouter/Ollama), this is always true."""
    return isinstance(client, OpenAI)

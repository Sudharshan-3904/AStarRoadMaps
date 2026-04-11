import os
from openai import OpenAI
from anthropic import Anthropic

def get_client_and_model(provider: str = None, model: str = None):
    """
    Returns (client, model_name).
    Supports 'anthropic', 'openrouter', and 'ollama'.
    """
    # Use provided values or fallback to env defaults
    provider = provider or os.getenv("DEFAULT_PROVIDER", "openrouter")
    
    if provider == "ollama":
        client = OpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key="ollama", # Placeholder for ollama
        )
        return client, model or os.getenv("OLLAMA_MODEL", "llama3")
        
    if provider == "openrouter":
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
        )
        return client, model or os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    
    # Fallback to Anthropic
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    client = Anthropic(api_key=anthropic_key)
    return client, model or "claude-3-5-sonnet-20240620"

def is_openai_client(client):
    return isinstance(client, OpenAI)

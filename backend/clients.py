import os
from openai import OpenAI
from anthropic import Anthropic

def get_client_and_model():
    """
    Returns (client, model_name).
    If OPENROUTER_API_KEY is present, it returns an OpenAI client configured for OpenRouter.
    Otherwise, it returns the native Anthropic client.
    """
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_key:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
        )
        model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
        return client, model
    
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    client = Anthropic(api_key=anthropic_key)
    model = "claude-3-5-sonnet-20240620"
    return client, model

def is_openai_client(client):
    return isinstance(client, OpenAI)

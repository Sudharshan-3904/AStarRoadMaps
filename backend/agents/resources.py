import json
from pathlib import Path
from tools.web_search import WEB_SEARCH_TOOL
from clients import is_openai_client

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

def run_resources(client, model_name: str, roadmap_dict: dict) -> dict:
    prompt_path = PROMPTS_DIR / "resources_system.txt"
    with open(prompt_path, "r") as f:
        system_prompt = f.read()

    user_message = json.dumps(roadmap_dict)
    
    if is_openai_client(client):
        # Tools on OpenAI require manual handling of the loop usually, 
        # but some OpenRouter endpoints might support tools.
        # For simplicity, if using OpenRouter, we'll try to use the model's 
        # internal knowledge with a hint that it cannot search if it fails,
        # or we just omit tools for now to avoid the complex loop implementation.
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=4096,
        )
        content = response.choices[0].message.content
    else:
        response = client.messages.create(
            model=model_name,
            max_tokens=4096,
            system=system_prompt,
            tools=[WEB_SEARCH_TOOL],
            messages=[{"role": "user", "content": user_message}]
        )
        # Handle multi-block responses as per instruction
        text_blocks = [b.text for b in response.content if b.type == "text"]
        if not text_blocks:
             # If tool use happened and no final text yet, 
             # the instruction says Anthropic handles loop internally.
             # This means the final response SHOULD have the text.
             raise ValueError("Resource Agent: No text blocks found in Anthropic response")
        content = text_blocks[-1]

    if "```" in content:
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.split("```")[0].strip()
        
    return json.loads(content)

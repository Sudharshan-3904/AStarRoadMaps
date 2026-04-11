import json
import logging
from pathlib import Path
from tools.web_search import WEB_SEARCH_TOOL
from clients import is_openai_client

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
logger = logging.getLogger(__name__)

def run_resources(client, model_name: str, roadmap_dict: dict) -> dict:
    logger.info(f"Enriching topics with resources using {model_name}...")
    prompt_path = PROMPTS_DIR / "resources_system.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    user_message = json.dumps(roadmap_dict)
    
    if is_openai_client(client):
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
        text_blocks = [b.text for b in response.content if b.type == "text"]
        if not text_blocks:
             raise ValueError("Resource Agent: Empty response from Anthropic")
        content = text_blocks[-1]

    if "<think>" in content:
        content = content.split("</think>")[-1].strip()

    if "```" in content:
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.split("```")[0].strip()
        
    try:
        data = json.loads(content)
        logger.info("Successfully enriched roadmap resources.")
        return data
    except json.JSONDecodeError:
        logger.error(f"JSON Parse Error. Content snapshot: {content[:100]}...")
        raise

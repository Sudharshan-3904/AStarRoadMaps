import json
import logging
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
logger = logging.getLogger(__name__)

def run_resources(client, model_name: str, roadmap_dict: dict) -> dict:
    logger.info(f"Enriching topics with resources using {model_name}...")
    prompt_path = PROMPTS_DIR / "resources_system.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Note: Tool use (web_search) is currently disabled as it was specific to the native Anthropic API.
    # We rely on the local model's extensive knowledge for resources.
    user_message = json.dumps(roadmap_dict)
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=4096,
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content

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

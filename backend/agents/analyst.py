import json
import logging
from pathlib import Path
from models.spec import UserSpec

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
logger = logging.getLogger(__name__)

def run_analyst(client, model_name: str, goal: str, skill_level: str, hours_per_week: int) -> UserSpec:
    logger.info(f"Starting analysis for goal: {goal}")
    prompt_path = PROMPTS_DIR / "analyst_system.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    user_message = f"Goal: {goal}\nSkill level: {skill_level}\nHours per week: {hours_per_week}"
    
    logger.info(f"Calling Ollama model: {model_name}...")
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
    
    if not content or not content.strip():
        logger.error("Received empty response from model.")
        raise ValueError("Analyst Agent: Empty response from model")

    if "<think>" in content:
        content = content.split("</think>")[-1].strip()

    if "```" in content:
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.split("```")[0].strip()
    
    try:
        data = json.loads(content)
        return UserSpec(**data)
    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode Error: {e}")
        logger.debug(f"Problematic content: {content}")
        raise

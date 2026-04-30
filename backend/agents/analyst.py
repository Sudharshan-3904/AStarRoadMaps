import json
import logging
from pathlib import Path
from models.spec import UserSpec

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
logger = logging.getLogger(__name__)

def run_analyst(client, model_name: str, goal: str, skill_level: str, hours_per_week: int) -> UserSpec:
    """
    Analyzes the user's learning goal and environment to determine a target scope.
    
    Acts as the initial step in the pipeline, transforming high-level requirements 
    into a structured UserSpec that guides subsequent agents.
    
    Args:
        client: The AI model client.
        model_name: Name of the model to use.
        goal: The user's primary learning objective.
        skill_level: The user's current experience level.
        hours_per_week: Commitment availability.
        
    Returns:
        A UserSpec object containing the goal, estimated duration, and metadata.
    """
    logger.info(f"Starting analysis for goal: {goal}")
    prompt_path = PROMPTS_DIR / "analyst_system.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    user_message = f"Goal: {goal}\nSkill level: {skill_level}\nHours per week: {hours_per_week}"
    
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
        logger.error("Empty response from AI model.")
        raise ValueError("Analyst Agent: Empty response from model")

    # Handle model-specific wrapping or thinking blocks
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
        logger.error(f"JSON Decode Error in Analyst: {e}")
        raise

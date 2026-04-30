import json
import logging
from pathlib import Path
from models.spec import UserSpec
from models.roadmap import Phase

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
logger = logging.getLogger(__name__)

def run_curriculum(client, model_name: str, spec: UserSpec, refinement_feedback: str = None) -> dict:
    logger.info(f"Building curriculum modules for: {spec.goal}")
    prompt_path = PROMPTS_DIR / "curriculum_system.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    user_message = spec.model_dump_json()
    if refinement_feedback:
        logger.info(f"Applying refinement feedback: {refinement_feedback}")
        user_message += f"\n\nRefinement request: {refinement_feedback}"
    
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
        # Structural validation
        if "phases" not in data or not isinstance(data["phases"], list):
            raise ValueError("Missing 'phases' list in curriculum output")
        
        # Validate each phase structure
        for i, phase_data in enumerate(data["phases"]):
            try:
                Phase(**phase_data)
            except Exception as e:
                logger.error(f"Phase {i} validation failed: {str(e)}")
                raise ValueError(f"Invalid structure in phase {i}") from e
                
        return data
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Curriculum validation failed: {str(e)}. Content snapshot: {content[:200]}...")
        raise

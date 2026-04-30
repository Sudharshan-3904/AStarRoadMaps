import json
import logging
from pathlib import Path
from pydantic import ValidationError
from models.roadmap import Phase

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
logger = logging.getLogger(__name__)

def run_resources(client, model_name: str, roadmap_dict: dict) -> dict:
    """
    Enriches a roadmap's topics with educational resources using an LLM.
    
    This agent processes each phase of the roadmap independently to maintain 
    high output quality and avoid token limit issues with smaller models.
    
    Args:
        client: The AI model client.
        model_name: Name of the model to use.
        roadmap_dict: The current roadmap structure as a dictionary.
        
    Returns:
        The roadmap dictionary updated with resource links for each topic.
    """
    logger.info(f"Enriching topics with resources using {model_name}...")
    prompt_path = PROMPTS_DIR / "resources_system.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    enriched_phases = []
    for phase in roadmap_dict.get("phases", []):
        logger.info(f"Processing phase {phase.get('phase_number')}: {phase.get('title')}")
        
        user_message = json.dumps(phase)
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=2000, 
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content

        # Extract content from model-specific wrapping (thinking blocks or markdown fences)
        if "<think>" in content:
            content = content.split("</think>")[-1].strip()

        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.split("```")[0].strip()
            
        try:
            enriched_phase_dict = json.loads(content)
            
            # Structural validation to ensure LLM respected the schema
            if not isinstance(enriched_phase_dict.get("topics"), list):
                raise ValueError("LLM returned non-list topics for phase")
            
            Phase(**enriched_phase_dict)
            enriched_phases.append(enriched_phase_dict)
        except (json.JSONDecodeError, ValidationError, ValueError) as e:
            logger.warning(
                f"Invalid structure for phase {phase.get('phase_number')}: {str(e)}. "
                "Falling back to original topics."
            )
            enriched_phases.append(phase)

    roadmap_dict["phases"] = enriched_phases
    logger.info("Successfully enriched all roadmap resources.")
    return roadmap_dict

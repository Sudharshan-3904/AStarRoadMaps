import json
import logging
from pathlib import Path
from pydantic import ValidationError
from models.roadmap import Phase

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
logger = logging.getLogger(__name__)

def run_resources(client, model_name: str, roadmap_dict: dict) -> dict:
    logger.info(f"Enriching topics with resources using {model_name}...")
    prompt_path = PROMPTS_DIR / "resources_system.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Process each phase independently to avoid model fatigue and token limits
    enriched_phases = []
    for phase in roadmap_dict.get("phases", []):
        logger.info(f"Processing phase {phase.get('phase_number')}: {phase.get('title')}")
        
        # Send only the current phase to the model
        user_message = json.dumps(phase)
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=2000, # Individual phase should fit easily
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
            enriched_phase_dict = json.loads(content)
            # Basic validation: ensure topics are still a list
            if not isinstance(enriched_phase_dict.get("topics"), list):
                raise ValueError("Topics is not a list")
            
            # Pydantic validation to ensure it matches the Phase schema
            Phase(**enriched_phase_dict)
            enriched_phases.append(enriched_phase_dict)
        except (json.JSONDecodeError, ValidationError, ValueError) as e:
            logger.warning(f"Model returned invalid structure for phase {phase.get('phase_number')}: {str(e)}. Falling back to original topics.")
            # Fallback: Use original topics but maybe they have empty resources?
            # Actually, the original topics from curriculum already have empty resources.
            enriched_phases.append(phase)

    roadmap_dict["phases"] = enriched_phases
    logger.info("Successfully enriched all roadmap resources.")
    return roadmap_dict


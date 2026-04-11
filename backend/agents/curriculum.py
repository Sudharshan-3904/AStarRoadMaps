import json
from pathlib import Path
from models.spec import UserSpec
from clients import is_openai_client

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

def run_curriculum(client, model_name: str, spec: UserSpec, refinement_feedback: str = None) -> dict:
    prompt_path = PROMPTS_DIR / "curriculum_system.txt"
    with open(prompt_path, "r") as f:
        system_prompt = f.read()

    user_message = spec.model_dump_json()
    if refinement_feedback:
        user_message += f"\n\nRefinement request: {refinement_feedback}"
    
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
            messages=[{"role": "user", "content": user_message}]
        )
        content = response.content[0].text
    
    if "```" in content:
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.split("```")[0].strip()
        
    return json.loads(content)

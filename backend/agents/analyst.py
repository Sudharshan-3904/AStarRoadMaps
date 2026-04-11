import json
from pathlib import Path
from models.spec import UserSpec
from clients import is_openai_client

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

def run_analyst(client, model_name: str, goal: str, skill_level: str, hours_per_week: int) -> UserSpec:
    prompt_path = PROMPTS_DIR / "analyst_system.txt"
    with open(prompt_path, "r") as f:
        system_prompt = f.read()

    user_message = f"Goal: {goal}\nSkill level: {skill_level}\nHours per week: {hours_per_week}"
    
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
    
    # Strip potential markdown fences if model ignored ONLY JSON rule
    if content.startswith("```json"):
        content = content.replace("```json", "", 1).rsplit("```", 1)[0].strip()
    elif content.startswith("```"):
        content = content.replace("```", "", 1).rsplit("```", 1)[0].strip()
        
    data = json.loads(content)
    return UserSpec(**data)

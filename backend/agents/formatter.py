import logging
from pathlib import Path
from models.roadmap import Roadmap
from models.progress import ProgressState
from clients import is_openai_client

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
logger = logging.getLogger(__name__)

def run_formatter(client, model_name: str, roadmap: Roadmap, progress: ProgressState) -> str:
    logger.info(f"Formatting roadmap: {roadmap.title}")
    prompt_path = PROMPTS_DIR / "formatter_system.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    user_message = f"Roadmap:\n{roadmap.model_dump_json()}\n\nProgress:\n{progress.model_dump_json()}"
    
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
    
    if "<think>" in content:
        content = content.split("</think>")[-1].strip()
        
    logger.info(f"Formatted Markdown length: {len(content)}")
    return content

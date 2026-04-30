import logging
from pathlib import Path
from models.roadmap import Roadmap
from models.progress import ProgressState

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
logger = logging.getLogger(__name__)

def run_formatter(client, model_name: str, roadmap: Roadmap, progress: ProgressState) -> str:
    """
    Transforms the structured roadmap data into a user-friendly Markdown document.
    
    Includes progress information to highlight completed or in-progress topics.
    
    Args:
        client: The AI model client.
        model_name: Name of the model to use.
        roadmap: The full Roadmap object.
        progress: The user's current progress state.
        
    Returns:
        A string containing the formatted Markdown content.
    """
    logger.info(f"Formatting roadmap: {roadmap.title}")
    prompt_path = PROMPTS_DIR / "formatter_system.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # Combine data models for a comprehensive formatting context
    user_message = f"Roadmap:\n{roadmap.model_dump_json()}\n\nProgress:\n{progress.model_dump_json()}"
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=4096,
    )
    content = response.choices[0].message.content
    
    if "<think>" in content:
        content = content.split("</think>")[-1].strip()
        
    logger.info(f"Formatted Markdown length: {len(content)}")
    return content

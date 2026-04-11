import json
import os
from pathlib import Path
from models.roadmap import Roadmap
from models.progress import ProgressState

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def save_roadmap(roadmap: Roadmap):
    path = DATA_DIR / f"{roadmap.id}.json"
    with open(path, "w") as f:
        f.write(roadmap.model_dump_json(indent=2))

def load_roadmap(roadmap_id: str) -> Roadmap:
    path = DATA_DIR / f"{roadmap_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Roadmap {roadmap_id} not found")
    with open(path, "r") as f:
        data = json.load(f)
        return Roadmap(**data)

def save_progress(progress: ProgressState):
    path = DATA_DIR / f"{progress.roadmap_id}_progress.json"
    with open(path, "w") as f:
        f.write(progress.model_dump_json(indent=2))

def load_progress(roadmap_id: str) -> ProgressState:
    path = DATA_DIR / f"{roadmap_id}_progress.json"
    if not path.exists():
        # Fallback to creating a new progress state if not found
        # This shouldn't usually happen if logic is correct
        return ProgressState(roadmap_id=roadmap_id)
    with open(path, "r") as f:
        data = json.load(f)
        return ProgressState(**data)

def save_markdown(roadmap_id: str, content: str):
    path = DATA_DIR / f"{roadmap_id}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def load_markdown(roadmap_id: str) -> str:
    path = DATA_DIR / f"{roadmap_id}.md"
    if not path.exists():
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def list_roadmaps() -> list[dict]:
    roadmaps = []
    for file in DATA_DIR.glob("*.json"):
        if file.name.endswith("_progress.json"):
            continue
        try:
            with open(file, "r") as f:
                data = json.load(f)
                # Count topics
                topic_count = sum(len(phase['topics']) for phase in data.get('phases', []))
                roadmaps.append({
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "created_at": data.get("created_at"),
                    "status": data.get("status"),
                    "topic_count": topic_count
                })
        except Exception:
            continue
    return sorted(roadmaps, key=lambda x: x["created_at"], reverse=True)

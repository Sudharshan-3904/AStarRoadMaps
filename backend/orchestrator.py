import asyncio
import json
import uuid
from datetime import datetime
from agents.analyst import run_analyst
from agents.curriculum import run_curriculum
from agents.resources import run_resources
from agents.formatter import run_formatter
from models.roadmap import Roadmap
from models.progress import ProgressState, TopicStatus
from storage.file_store import save_roadmap, load_roadmap, save_progress, load_progress, save_markdown
from clients import get_client_and_model, is_openai_client

def classify_feedback(client, model_name: str, feedback: str) -> str:
    # Short Claude call: return one of "structure", "resources", "format"
    system_prompt = "Classify the following user feedback for a learning roadmap into one of these three categories: 'structure' (if it asks to add/remove topics, change phases, adjust depth), 'resources' (if it asks for better links, different tutorials), or 'format' (if it asks for layout, wording, or Markdown style changes). Respond ONLY with the category name."
    
    if is_openai_client(client):
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": feedback}
            ],
            max_tokens=50,
        )
        result = response.choices[0].message.content.strip().lower()
    else:
        response = client.messages.create(
            model=model_name,
            max_tokens=50,
            messages=[{"role": "user", "content": feedback}],
            system=system_prompt
        )
        result = response.content[0].text.strip().lower()
    
    for cat in ["structure", "resources", "format"]:
        if cat in result:
            return cat
    return "structure" # Default

async def run_pipeline(request_data: dict, refinement: dict = None):
    """
    Yields SSE event strings.
    request_data = { "goal": str, "skill_level": str, "hours_per_week": int, "provider": str, "model": str }
    refinement = { "feedback": str, "feedback_type": "structure"|"resources"|"format", "roadmap_id": str }
    """
    client, model_name = get_client_and_model(
        provider=request_data.get("provider"),
        model=request_data.get("model")
    )

    def emit(event_type: str, **kwargs) -> str:
        return f"data: {json.dumps({'type': event_type, **kwargs})}\n\n"

    roadmap_id = refinement["roadmap_id"] if refinement else str(uuid.uuid4())

    try:
        # --- ANALYST ---
        if not refinement:
            yield emit("agent_start", agent="analyst")
            spec = run_analyst(
                client, 
                model_name,
                request_data["goal"], 
                request_data["skill_level"], 
                request_data["hours_per_week"]
            )
            yield emit("agent_done", agent="analyst")
        else:
            old_roadmap = load_roadmap(roadmap_id)
            spec = old_roadmap.spec

        # --- CURRICULUM ---
        if not refinement or refinement["feedback_type"] in ("structure",):
            yield emit("agent_start", agent="curriculum")
            roadmap_dict = run_curriculum(client, model_name, spec, refinement["feedback"] if refinement else None)
            yield emit("agent_done", agent="curriculum")
        else:
            roadmap_dict = load_roadmap(roadmap_id).model_dump()

        # --- RESOURCES ---
        if not refinement or refinement["feedback_type"] in ("structure", "resources"):
            yield emit("agent_start", agent="resources")
            roadmap_dict = run_resources(client, model_name, roadmap_dict)
            yield emit("agent_done", agent="resources")

        # --- FORMATTER ---
        yield emit("agent_start", agent="formatter")
        
        # Create Roadmap object
        roadmap = Roadmap(
            id=roadmap_id, 
            created_at=datetime.utcnow().isoformat(), 
            spec=spec,
            **{k: v for k, v in roadmap_dict.items() if k not in ["id", "created_at", "spec"]}
        )
        
        # Load or Init Progress
        if refinement:
            progress = load_progress(roadmap_id)
            # Synchronize progress with new roadmap structure if structure changed
            existing_topics = progress.topics.copy()
            new_topics = {}
            for phase in roadmap.phases:
                for topic in phase.topics:
                    new_topics[topic.name] = existing_topics.get(topic.name, TopicStatus.not_started)
            progress.topics = new_topics
        else:
            progress = ProgressState(
                roadmap_id=roadmap_id, 
                topics={t.name: TopicStatus.not_started for p in roadmap.phases for t in p.topics}
            )
            
        markdown = run_formatter(client, model_name, roadmap, progress)
        yield emit("agent_done", agent="formatter")

        # --- SAVE ---
        roadmap.status = "complete"
        save_roadmap(roadmap)
        save_progress(progress)
        save_markdown(roadmap_id, markdown)

        yield emit("complete", roadmap_id=roadmap_id)

    except Exception as e:
        import traceback
        traceback.print_exc()
        yield emit("error", message=str(e))

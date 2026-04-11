import asyncio
import json
import uuid
import logging
from datetime import datetime
from typing import Callable, Any
from agents.analyst import run_analyst
from agents.curriculum import run_curriculum
from agents.resources import run_resources
from agents.formatter import run_formatter
from models.roadmap import Roadmap
from models.progress import ProgressState, TopicStatus
from storage.file_store import save_roadmap, load_roadmap, save_progress, load_progress, save_markdown
from clients import get_client_and_model

logger = logging.getLogger(__name__)

async def retry_with_checkpoint(func: Callable, *args, max_retries: int = 2, **kwargs) -> Any:
    """Helper to retry agent calls if they fail (e.g. validation errors)."""
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            logger.warning(f"Agent execution attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries:
                await asyncio.sleep(1) # Small delay before retry
    
    logger.error(f"Agent execution failed after {max_retries + 1} attempts.")
    raise last_error

def classify_feedback(client, model_name: str, feedback: str) -> str:
    logger.info(f"Classifying feedback: {feedback[:50]}...")
    system_prompt = "Classify the following user feedback for a learning roadmap into one of these three categories: 'structure', 'resources', or 'format'. Respond ONLY with the category name."
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": feedback}
        ],
        max_tokens=50,
    )
    result = response.choices[0].message.content.strip().lower()
    
    logger.info(f"Feedback classified as: {result}")
    for cat in ["structure", "resources", "format"]:
        if cat in result:
            return cat
    return "structure"

async def run_pipeline(request_data: dict, refinement: dict = None):
    roadmap_id = refinement["roadmap_id"] if refinement else str(uuid.uuid4())
    logger.info(f"Starting pipeline for Roadmap ID: {roadmap_id}")
    
    client, model_name = get_client_and_model(
        provider=request_data.get("provider"),
        model=request_data.get("model")
    )
    logger.info(f"Using provider: {request_data.get('provider')} | Model: {model_name}")

    def emit(event_type: str, **kwargs) -> dict:
        return {"data": json.dumps({"type": event_type, **kwargs})}

    try:
        # --- INITIAL STATE / CHECKPOINT RECOVERY ---
        try:
            roadmap = load_roadmap(roadmap_id)
            spec = roadmap.spec
            roadmap_dict = roadmap.model_dump()
            logger.info(f"Resuming/Refining existing roadmap {roadmap_id}")
        except FileNotFoundError:
            roadmap = None
            spec = None
            roadmap_dict = {}

        # --- ANALYST ---
        if not spec:
            logger.info("Step: Analyst")
            yield emit("agent_start", agent="analyst")
            spec = await retry_with_checkpoint(
                run_analyst,
                client, 
                model_name,
                request_data["goal"], 
                request_data["skill_level"], 
                request_data["hours_per_week"]
            )
            yield emit("agent_done", agent="analyst")
            
            # Checkpoint 1
            temp_roadmap = Roadmap(
                id=roadmap_id,
                title=f"Learning {spec.goal}",
                spec=spec,
                phases=[],
                created_at=datetime.utcnow().isoformat(),
                status="generating"
            )
            save_roadmap(temp_roadmap)
            logger.info("Checkpoint saved: Analyst")

        # --- CURRICULUM ---
        # Run if new generation OR if refinement is structural OR if existing roadmap has no phases
        if not refinement or refinement["feedback_type"] == "structure" or not roadmap_dict.get("phases"):
            logger.info("Step: Curriculum")
            yield emit("agent_start", agent="curriculum")
            roadmap_dict = await retry_with_checkpoint(
                run_curriculum, 
                client, model_name, spec, 
                refinement["feedback"] if refinement else None
            )
            yield emit("agent_done", agent="curriculum")
            
            # Checkpoint 2
            temp_roadmap = Roadmap(
                id=roadmap_id,
                created_at=datetime.utcnow().isoformat(),
                spec=spec,
                **{k: v for k, v in roadmap_dict.items() if k not in ["id", "created_at", "spec"]},
                status="generating"
            )
            save_roadmap(temp_roadmap)
            logger.info("Checkpoint saved: Curriculum")
        else:
            logger.info("Skipping Curriculum, using checkpoint data.")

        # --- RESOURCES ---
        # Run if new generation OR if refinement is structural/resources OR if existing topics have no resources
        has_resources = any(t.get("resources") for p in roadmap_dict.get("phases", []) for t in p.get("topics", []))
        if not refinement or refinement["feedback_type"] in ("structure", "resources") or not has_resources:
            logger.info("Step: Resources")
            yield emit("agent_start", agent="resources")
            roadmap_dict = await retry_with_checkpoint(run_resources, client, model_name, roadmap_dict)
            yield emit("agent_done", agent="resources")
            
            # Checkpoint 3
            temp_roadmap = Roadmap(
                id=roadmap_id,
                created_at=datetime.utcnow().isoformat(),
                spec=spec,
                **{k: v for k, v in roadmap_dict.items() if k not in ["id", "created_at", "spec"]},
                status="generating"
            )
            save_roadmap(temp_roadmap)
            logger.info("Checkpoint saved: Resources")
        else:
             logger.info("Skipping Resources, using checkpoint data.")

        # --- FORMATTER ---
        logger.info("Step: Formatter")
        yield emit("agent_start", agent="formatter")
        
        roadmap = Roadmap(
            id=roadmap_id, 
            created_at=datetime.utcnow().isoformat(), 
            spec=spec,
            **{k: v for k, v in roadmap_dict.items() if k not in ["id", "created_at", "spec"]}
        )
        
        try:
            progress = load_progress(roadmap_id)
            existing_topics = progress.topics.copy()
            new_topics = {}
            for phase in roadmap.phases:
                for topic in phase.topics:
                    new_topics[topic.name] = existing_topics.get(topic.name, TopicStatus.not_started)
            progress.topics = new_topics
        except FileNotFoundError:
            progress = ProgressState(
                roadmap_id=roadmap_id, 
                topics={t.name: TopicStatus.not_started for p in roadmap.phases for t in p.topics}
            )
            
        markdown = await retry_with_checkpoint(run_formatter, client, model_name, roadmap, progress)
        yield emit("agent_done", agent="formatter")

        # --- FINAL SAVE ---
        roadmap.status = "complete"
        save_roadmap(roadmap)
        save_progress(progress)
        save_markdown(roadmap_id, markdown)
        logger.info(f"Roadmap {roadmap_id} completed and saved.")

        yield emit("complete", roadmap_id=roadmap_id)

    except Exception as e:
        logger.error(f"Pipeline failed at checkpoint: {str(e)}", exc_info=True)
        yield emit("error", message=str(e))

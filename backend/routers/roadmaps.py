import uuid
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse
from clients import get_client_and_model

from models.roadmap import Roadmap
from models.spec import UserSpec
from schemas.requests import GenerateRequest, RefineRequest
from schemas.responses import GenerateResponse, RoadmapListItem
from storage.file_store import save_roadmap, load_roadmap, list_roadmaps, DATA_DIR
from orchestrator import run_pipeline, classify_feedback

router = APIRouter()

@router.post("/generate")
async def generate(body: GenerateRequest) -> GenerateResponse:
    roadmap_id = str(uuid.uuid4())
    
    # Store initial pending roadmap with the spec
    # We don't have phases yet
    roadmap = Roadmap(
        id=roadmap_id,
        title=f"Learning {body.goal}",
        spec=UserSpec(
            goal=body.goal,
            skill_level=body.skill_level,
            hours_per_week=body.hours_per_week,
            estimated_weeks=0, # To be determined by analyst
            provider=body.provider,
            model=body.model
        ),
        phases=[],
        created_at=datetime.utcnow().isoformat(),
        status="pending"
    )
    save_roadmap(roadmap)
    
    return GenerateResponse(roadmap_id=roadmap_id)

@router.get("/{roadmap_id}/stream")
async def stream(roadmap_id: str, feedback: str = None, feedback_type: str = None):
    try:
        roadmap = load_roadmap(roadmap_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    # Pass the spec to run_pipeline
    request_data = {
        "goal": roadmap.spec.goal,
        "skill_level": roadmap.spec.skill_level,
        "hours_per_week": roadmap.spec.hours_per_week,
        "provider": roadmap.spec.provider,
        "model": roadmap.spec.model
    }
    
    refinement = None
    if feedback and feedback_type:
        refinement = {
            "roadmap_id": roadmap_id,
            "feedback": feedback,
            "feedback_type": feedback_type
        }
    
    return EventSourceResponse(run_pipeline(request_data, refinement))

@router.get("/{roadmap_id}")
async def get_roadmap(roadmap_id: str) -> Roadmap:
    try:
        return load_roadmap(roadmap_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Roadmap not found")

@router.get("/{roadmap_id}/markdown")
async def get_markdown(roadmap_id: str):
    path = DATA_DIR / f"{roadmap_id}.md"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Markdown not found")
    return FileResponse(path, media_type="text/markdown", filename="roadmap.md")

@router.patch("/{roadmap_id}/refine")
async def refine(roadmap_id: str, body: RefineRequest):
    client, model_name = get_client_and_model(
        provider=roadmap.spec.provider,
        model=roadmap.spec.model
    )
    try:
        roadmap = load_roadmap(roadmap_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Roadmap not found")
        
    feedback_type = classify_feedback(client, model_name, body.feedback)
    
    # Note: The stream endpoint for refinement will need to handle this.
    # We can use the same /stream endpoint but it needs to know it's a refinement.
    # Maybe we should store the refinement request in the roadmap or status.
    # For now, let's assume the frontend will call /stream/{id} with query param or just /stream/{id} 
    # and backend checks if status is already complete.
    # But instruction says: "Return roadmap_id (client re-opens SSE stream)" and 
    # "feedback_type = classify_feedback(client, body.feedback)".
    # The orchestrator run_pipeline takes a 'refinement' dict.
    
    # We need a way for the subsequent /stream call to know about the refinement.
    # I'll store the refinement feedback in a companion file or in-memory if it's immediate.
    # Better: client passes feedback type back to stream?
    # Instruction for stream says: return EventSourceResponse(run_pipeline({"roadmap_id": roadmap_id, ...}))
    # This implies stream might take some params.
    
    return {"roadmap_id": roadmap_id, "feedback_type": feedback_type, "feedback": body.feedback}

@router.get("", response_model=list[RoadmapListItem])
async def list_all_roadmaps():
    return list_roadmaps()

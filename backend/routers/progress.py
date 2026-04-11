from fastapi import APIRouter, HTTPException
from models.progress import ProgressState
from schemas.requests import UpdateProgressRequest
from storage.file_store import load_progress, save_progress

router = APIRouter()

@router.get("/{roadmap_id}/progress")
async def get_progress(roadmap_id: str) -> ProgressState:
    try:
        return load_progress(roadmap_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Progress not found")

@router.patch("/{roadmap_id}/progress")
async def update_progress(roadmap_id: str, body: UpdateProgressRequest) -> ProgressState:
    try:
        progress = load_progress(roadmap_id)
        progress.topics[body.topic_name] = body.status
        save_progress(progress)
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

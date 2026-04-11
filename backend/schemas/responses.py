from pydantic import BaseModel

class GenerateResponse(BaseModel):
    roadmap_id: str

class RoadmapListItem(BaseModel):
    id: str
    title: str
    created_at: str
    status: str
    topic_count: int

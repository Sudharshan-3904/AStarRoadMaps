from pydantic import BaseModel
from typing import List, Optional
from .spec import UserSpec

class Resource(BaseModel):
    label: str
    url: str
    type: str  # "docs" | "video" | "article" | "interactive"

class Topic(BaseModel):
    name: str
    content: Optional[str] = ""
    subtopics: List[str]
    resources: List[Resource] = []
    project: Optional[str] = None

class Phase(BaseModel):
    phase_number: int
    title: str
    week_range: str
    topics: List[Topic]

class Roadmap(BaseModel):
    id: str
    title: str
    spec: UserSpec
    phases: List[Phase]
    created_at: str
    status: str = "pending"  # "pending" | "generating" | "complete" | "error"

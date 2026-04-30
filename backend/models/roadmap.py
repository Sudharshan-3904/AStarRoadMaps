from pydantic import BaseModel
from typing import List, Optional
from .spec import UserSpec

class Resource(BaseModel):
    """
    Represents a specific educational resource (link) for a topic.
    Types: "docs", "video", "article", "interactive"
    """
    label: str
    url: str
    type: str

class Topic(BaseModel):
    """
    A specific unit of study within a phase.
    Contains content summary, sub-tasks, and curated resources.
    """
    name: str
    content: Optional[str] = ""
    subtopics: List[str]
    resources: List[Resource] = []
    project: Optional[str] = None

class Phase(BaseModel):
    """
    A logical group of topics, typically spanning a specific timeframe (e.g., Week 1-2).
    """
    phase_number: int
    title: str
    week_range: str
    topics: List[Topic]

class Roadmap(BaseModel):
    """
    The root data model for a complete learning roadmap.
    Statuses: "pending", "generating", "complete", "error"
    """
    id: str
    title: str
    spec: UserSpec
    phases: List[Phase]
    created_at: str
    status: str = "pending"

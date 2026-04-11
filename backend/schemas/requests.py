from pydantic import BaseModel
from models.spec import SkillLevel

class GenerateRequest(BaseModel):
    goal: str
    skill_level: SkillLevel
    hours_per_week: int
    provider: str = "openrouter" # "anthropic" | "openrouter" | "ollama"
    model: str = "anthropic/claude-3.5-sonnet"

class RefineRequest(BaseModel):
    feedback: str

class UpdateProgressRequest(BaseModel):
    topic_name: str
    status: str  # "not_started" | "in_progress" | "done"

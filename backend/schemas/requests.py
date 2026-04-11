from pydantic import BaseModel
from models.spec import SkillLevel

class GenerateRequest(BaseModel):
    goal: str
    skill_level: SkillLevel
    hours_per_week: int
    provider: str = "ollama" # "anthropic" | "openrouter" | "ollama"
    model: str = "llama3.2:latest"

class RefineRequest(BaseModel):
    feedback: str

class UpdateProgressRequest(BaseModel):
    topic_name: str
    status: str  # "not_started" | "in_progress" | "done"

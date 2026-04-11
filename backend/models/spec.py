from pydantic import BaseModel
from enum import Enum

class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class UserSpec(BaseModel):
    goal: str
    skill_level: SkillLevel
    hours_per_week: int
    estimated_weeks: int
    provider: str = "openrouter"
    model: str = "anthropic/claude-3.5-sonnet"

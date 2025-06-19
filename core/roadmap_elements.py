from dataclasses import dataclass, field
from typing import List, Literal
from datetime import datetime


LearningLevel = Literal['beginner', 'intermediate', 'advanced', 'refresher']

@dataclass
class Resource:
    title: str
    url: str
    description: str = ""


@dataclass
class Keyframe:
    title: str
    description: str
    due_date: datetime
    completed: bool = False
    resources: List[Resource] = field(default_factory=list)


@dataclass
class Stage:
    name: str
    level: LearningLevel
    keyframes: List[Keyframe]


@dataclass
class Roadmap:
    topic: str
    created_at: datetime
    stages: List[Stage]
    user_id: str = "default_user"


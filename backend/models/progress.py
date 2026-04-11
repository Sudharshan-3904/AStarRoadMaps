from pydantic import BaseModel
from enum import Enum
from typing import Dict

class TopicStatus(str, Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    done = "done"

class ProgressState(BaseModel):
    roadmap_id: str
    topics: Dict[str, TopicStatus] = {}

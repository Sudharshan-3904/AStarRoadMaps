from dataclasses import dataclass, field, asdict
from typing import List, Literal, Optional
from datetime import datetime
import json


LearningLevel = Literal["beginner", "intermediate", "advanced", "refresher", "full"]

@dataclass
class Resource:
    def __init__(self, title: str, url: str, description: str = ""):
        self.title = title
        self.url = url
        self.description = description

@dataclass
class Keyframe:
    def __init__(self, title: str = "", description: str = "", due_date: datetime = datetime.now(), completed: bool = False, resources: List[Resource] = []):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.resources = field(default_factory=list)

    def mark_complete(self):
        self.completed = True

    def add_resource(self, resource: Resource):
        self.resources.append(resource)

@dataclass
class Stage:
    def __init__(self, name: str = "", level: LearningLevel = "beginner", keyframes: List[Keyframe] = []):
        self.name = name
        self.level = level
        self.keyframes = keyframes

    def add_keyframe(self, keyframe: Keyframe):
        self.keyframes.append(keyframe)

    def progress_percent(self) -> float:
        total = len(self.keyframes)
        if total == 0:
            return 0.0
        completed = sum(1 for k in self.keyframes if k.completed)
        return (completed / total) * 100

@dataclass
class Roadmap:
    def __init__(self, topic: str = "", created_at: datetime = datetime.now(), stages: List[Stage] = [], user_id: str = "default_user", level: LearningLevel= "beginner"):
        self.topic = topic
        self.created_at = created_at
        self.stages = stages
        self.user_id = user_id
        self.level = level

    def add_stage(self, stage: Stage):
        self.stages.append(stage)

    def get_total_progress(self) -> float:
        if not self.stages:
            return 0.0
        return sum(stage.progress_percent() for stage in self.stages) / len(self.stages)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, default=str, indent=4)

    @staticmethod
    def from_json(filepath: str) -> "Roadmap":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        stages = []
        for stage_data in data["stages"]:
            keyframes = []
            for kf in stage_data["keyframes"]:
                resources = [Resource(**r) for r in kf.get("resources", [])]
                keyframes.append(Keyframe(
                    title=kf["title"],
                    description=kf["description"],
                    due_date=datetime.fromisoformat(kf["due_date"]),
                    completed=kf.get("completed", False),
                    resources=resources
                ))
            stages.append(Stage(
                name=stage_data["name"],
                level=stage_data["level"],
                keyframes=keyframes
            ))

        return Roadmap(
            topic=data["topic"],
            created_at=datetime.fromisoformat(data["created_at"]),
            stages=stages,
            user_id=data.get("user_id", "default_user"),
            level=data.get("level")
        )

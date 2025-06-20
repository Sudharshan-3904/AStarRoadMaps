from dataclasses import dataclass, field, asdict
from typing import List, Literal, Optional
import datetime
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
    def __init__(self, title: str = "", description: str = "", completed: bool = False, resources: List[Resource] = []):
        self.title = title
        self.description = description
        self.resources = resources
        self.completed = completed
        self.completed_date = None
    
    def mark_complete(self):
        self.completed = True
        self.completed_date = datetime.datetime.now()

    def add_resource(self, resource: Resource):
        self.resources.append(resource)

@dataclass
class Stage:
    def __init__(self, name: str = "", completed: bool = False, level: LearningLevel = "beginner", keyframes: List[Keyframe] = []):
        self.name = name
        self.level = level
        self.keyframes = keyframes
        self.completed = completed
        self.completed_date = None
        self.completed_progress = 0
        self.completed_precentage = 0.0

    def add_keyframe(self, keyframe: Keyframe):
        self.keyframes.append(keyframe)
    
    def mark_complete(self):
        self.completed = True
        self.completed_date = datetime.datetime.now()
        self.update_progress()

    def progress_percent(self) -> float:
        total = len(self.keyframes)
        if total == 0:
            return 0.0
        completed = sum(1 for k in self.keyframes if k.completed)
        return (completed / total) * 100

    def update_progress(self):
        self.completed_progress = len([x for x in self.keyframes if x.__getattribute__('completed')==True])
        self.completed_precentage = round((self.completed_progress / len(self.keyframes)) * 100, 2)

@dataclass
class Roadmap:
    def __init__(self, topic: str = "", completed: bool = False, created_at: datetime.datetime = datetime.datetime.now(), stages: List[Stage] = [], level: LearningLevel= "beginner"):
        self.topic = topic
        self.created_at = created_at
        self.stages = stages
        self.level = level
        self.completed = completed
        self.completed_date = None
        self.completed_progress = 0
        self.completed_precentage = 0.0
    
    def mark_complete(self):
        self.completed = True
        self.completed_date = datetime.datetime.now()
        self.update_progress()

    def add_stage(self, stage: Stage):
        self.stages.append(stage)

    def get_total_progress(self) -> float:
        if not self.stages:
            return 0.0
        return sum(stage.progress_percent() for stage in self.stages) / len(self.stages)

    def to_dict(self) -> dict:
        return asdict(self)

    def save_to_json(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, default=str, indent=4)

    def update_progress(self):
        self.completed_progress = len([x for x in self.stages if x.__getattribute__('completed')==True])
        self.completed_precentage = round((self.completed_progress / len(self.stages)) * 100, 2)

    @staticmethod
    def load_from_json(filepath: str) -> "Roadmap":
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
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
            stages=stages,
            level=data.get("level")
        )

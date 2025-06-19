from core.roadmap_elements import Roadmap, Stage, Keyframe
from datetime import datetime, timedelta

def generate_basic_roadmap(topic: str, level: str = 'beginner') -> Roadmap:
    stage = Stage(
        name="Introduction",
        level=level,
        keyframes=[
            Keyframe(
                title="What is " + topic,
                description=f"Understand the basics of {topic}",
                due_date=datetime.now() + timedelta(days=3)
            )
        ]
    )
    roadmap = Roadmap(
        topic=topic,
        created_at=datetime.now(),
        stages=[stage]
    )
    return roadmap

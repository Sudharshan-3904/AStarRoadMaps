import json
import os
from typing import List
import plotly.figure_factory as ff
import plotly.graph_objs as go
import core.roadmap_elements as map_elements


def load_user_progress(filepath: str) -> map_elements.Roadmap:
    """Load user progress from a JSON file and return a Roadmap object."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Progress file not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Use Roadmap.from_json logic
    return map_elements.Roadmap.load_from_json(filepath)

def plot_gantt_chart(roadmap: map_elements.Roadmap):
    """Create and display a Gantt chart for the roadmap using Plotly."""
    tasks = []
    for stage in roadmap.stages:
        for kf in stage.keyframes:
            tasks.append(dict(
                Task=stage.name,
                Resource='Completed' if kf.completed else 'Pending',
                Description=kf.title
            ))

    if not tasks:
        print("No tasks to display.")
        return
    
    fig = ff.create_gantt(tasks, index_col='Resource', show_colorbar=True, group_tasks=True, showgrid_x=True, showgrid_y=True)
    for i, task in enumerate(tasks):
        fig.add_annotation(dict(x=task['Start'], y=i, text=task['Description'], showarrow=False))
    fig.update_layout(title='Learning Roadmap Gantt Chart')
    fig.show()

    return fig


if __name__ == '__main__':
    rhrm = load_user_progress("data\\Roman Emire History.json")
    plot_gantt_chart(rhrm)

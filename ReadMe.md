# AStarRoadMaps

AStarRoadMaps is a Python project that implements the A* (A-star) algorithm to find optimal routes on a road network. It includes visualization, modeling, and a simple UI to interact with maps and paths.

## Table of Contents

- [Features](#features)  
- [Repository Structure](#repository-structure)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Running the Application](#running-the-application)  
- [Usage](#usage)  
- [How It Works](#how-it-works)

## Features

- Implementation of the A* pathfinding algorithm over road networks  
- Visualization of graphs, nodes, and computed paths  
- Support for custom map/graph models  
- Simple UI layer to interactively choose source/destination and see results  
- Modular structure (core logic, models, UI)  

## Repository Structure

```text
AStarRoadMaps/
├── core/               # Core algorithm logic (A*, heuristics, graph operations)
├── models/             # Data models (nodes, edges, map importers, etc.)
├── ui/                 # UI / visualization components
├── documentation/      # Supporting docs, diagrams, explanations
├── main.py             # Entry point to launch the application
├── requirements.txt    # Python dependencies
├── ReadMe.md           # This README file
└── things.txt          # (Auxiliary / scratch file)
````

- **core/**: contains the implementation of the A* pathfinding logic, heuristic functions, and graph search utilities.
- **models/**: houses data structures (Node, Edge, Graph), and functions to load or parse map/road data.
- **ui/**: for drawing or rendering the graph, displaying the path, and interacting with the user (e.g. via console or GUI).
- **documentation/**: diagrams, design notes, algorithms, and any auxiliary descriptions.
- **main.py**: ties together the UI, models, and core logic to run the program.
- **requirements.txt**: lists all third-party Python packages required.

## Getting Started

### Prerequisites

- Python 3.8+ (or whichever version you use)
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Sudharshan-3904/AStarRoadMaps.git
   cd AStarRoadMaps
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

After installation, run:

```bash
python main.py
```

You should see a UI (or console prompts) to input source and destination nodes on the map. The application will compute the shortest path (via A*) and display it visually on the map / graph.

## Usage

1. Select or input a road network (e.g., from a file or built-in example).
2. Choose a start (source) node and a goal (destination) node.
3. The algorithm runs and returns the optimal path.
4. The UI displays the map with nodes, edges, and highlights the found path.
5. You may experiment with different heuristics to see how they impact performance.

You can also extend the project by:

- Importing real-world map data (e.g., OpenStreetMap).
- Supporting weighted edges (e.g., distance, travel time, traffic).
- Adding alternative algorithms (Dijkstra, BFS, etc.).
- Improving the UI (interactive map, zoom, pan, etc.).

## How It Works

- The **A*** algorithm is implemented in `core/` using a priority queue (e.g., min-heap).
- Each node has associated costs:

  - **g(n)** = the cost from the start to node *n*.
  - **h(n)** = heuristic estimate of cost from *n* to the goal.
  - **f(n) = g(n) + h(n)** guides the node expansion order.
- The heuristic must be admissible (never overestimates) to guarantee optimality.
- The graph structure (nodes, edges, weights) comes from `models/`.
- The UI layer visualizes nodes, edges, and highlights the computed path.

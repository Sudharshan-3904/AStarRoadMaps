# AStarRoadMaps

AStarRoadMaps is an AI-agent-based project that generates **learning roadmaps** for any given topic.  
It leverages **locally hosted language models** (via [LM Studio](https://lmstudio.ai/) or [Ollama](https://ollama.ai/)) to dynamically produce structured pathways tailored to different skill levels.

## 🚀 Features

- 📚 **AI-powered roadmap generation** for any topic
- 🎯 Roadmaps structured into levels:
  - Beginner
  - Intermediate
  - Advanced
  - Refresher
  - Full (comprehensive roadmap)
- 🔗 **Local-first**: integrates with locally hosted LLMs (LM Studio / Ollama)
- ⚡ Lightweight, modular design
- 📝 Easy to extend with additional models or roadmap stages

---

## 📂 Repository Structure

```text
AStarRoadMaps/
├── core/              # Core logic for AI-agent orchestration and roadmap generation
├── models/            # Model connectors for LM Studio, Ollama, etc.
├── ui/                # CLI / (future: web UI) for user interaction
├── documentation/     # Diagrams, project notes, and design documents
├── main.py            # Entry point to run the roadmap generator
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.9+
- pip (Python package installer)
- Either:

  - [LM Studio](https://lmstudio.ai/) (running locally), or
  - [Ollama](https://ollama.ai/) with your chosen model installed

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

---

## ▶️ Running the Project

Run the application with:

```bash
python main.py
```

You will be prompted to enter a **topic** (e.g., *Data Engineering*, *ReactJS*, *Cybersecurity Basics*).
The AI agent will generate a **roadmap** broken down into Beginner, Intermediate, Advanced, Refresher, and Full stages.

---

## 📖 Example

**Input:**

```input
Topic: Machine Learning
```

**Output (roadmap preview):**

- **Beginner**: Python basics, Linear Algebra, Statistics fundamentals
- **Intermediate**: Scikit-learn, Supervised/Unsupervised learning, Feature engineering
- **Advanced**: Deep Learning (PyTorch/TensorFlow), Optimization, Transformers
- **Refresher**: Key ML concepts, evaluation metrics, practical projects
- **Full**: Comprehensive journey combining all stages with recommended projects

> *(Output may vary depending on the model used.)*

---

## 🔍 How It Works

1. **User provides a topic** (e.g., "Web Development").
2. **AI agent (A* Agent)** structures queries to the local LLM.
3. The **model generates roadmap stages** for Beginner → Advanced.
4. Results are formatted and displayed via CLI / UI.

The "A*" in the name symbolizes **optimal roadmap generation**, inspired by search algorithms but applied to **learning paths**.

---

## 🧩 Future Enhancements

- Web-based UI with progress tracking
- Export roadmaps to **Markdown / PDF**
- Integration with **Docker** for containerized deployment
- Support for multiple roadmap styles (project-based, theory-first, etc.)
- Visualization of roadmap as a **graph/network**

---

## 💡 Inspiration

AStarRoadMaps is built to help learners, educators, and self-starters quickly obtain **clear, structured learning paths** using the power of **local AI models** — keeping data private, fast, and flexible.

---

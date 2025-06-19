# A\*S Road Maps

---

## 📁 Project Structure (Modular Architecture)

```structure
auto_roadmap/
│
├── core/
│   ├── roadmap_generator.py        # Main roadmap logic
│   ├── web_search.py               # Fetch relevant web articles
│   ├── roadmap_builder.py          # Build custom trackable roadmap
│   └── question_answering.py       # Use LLM to answer questions
│
├── ui/
│   ├── dashboard.py                # CLI or web dashboard (Streamlit/Gradio)
│   └── visualizer.py               # Plots, graphs (matplotlib/plotly)
│
├── models/
│   └── local_model_interface.py    # LangChain+MCP for local LLM queries
│
├── data/
│   └── user_progress.json          # Save user data and keyframes
│
├── docker/
│   ├── Dockerfile                  # For full project container
│   └── requirements.txt
│
├── main.py                         # Entry point
└── README.md
```

---

## 🧠 Core Features Explained

### ✅ 1. Web Searching

- Use **SerpAPI**, **DuckDuckGo**, or LangChain’s web search tool.
- Extract clean article text using `newspaper3k` or `trafilatura`.

### ✅ 2. Customizable Roadmap

- Break topics into phases: beginner → intermediate → advanced.
- Use JSON to store and track keyframes (e.g., concepts, deadlines).
- Allow status: _Not Started_, _In Progress_, _Completed_.

### ✅ 3. Multiple Learning Tracks

- Flag for user intent:

  - `--mode beginner`
  - `--mode refresher`
  - `--mode full`

- Adjust roadmap granularity based on input.

### ✅ 4. Progress Tracking

- Use **matplotlib/plotly** to render:

  - Gantt charts for roadmap
  - Completion curves
  - Time vs. progress graphs

### ✅ 5. Local LLM Q\&A

- Use **LangChain** to:

  - Load local models (LM Studio / Ollama)
  - Query based on generated roadmap content

---

## 🔧 Technologies

| Purpose          | Tool/Library          |
| ---------------- | --------------------- |
| LLM Framework    | LangChain + MCP       |
| Local Models     | LM Studio / Ollama    |
| Web Scraping     | newspaper3k / SerpAPI |
| Visualization    | Plotly / Matplotlib   |
| UI (Optional)    | Gradio / Streamlit    |
| Containerization | Docker                |
| State Management | JSON / SQLite         |

---

## 🐳 Docker Setup (Minimal)

### `Dockerfile`

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### `requirements.txt`

```txt
langchain
mcp
newspaper3k
plotly
streamlit
matplotlib
duckduckgo-search
```

---

## 🔄 Development Milestones

### ✅ Phase 1: Basic Python Implementation

- [ ] Input topic and generate roadmap skeleton
- [ ] Integrate web search and fetch relevant articles
- [ ] Allow roadmap customization + save JSON
- [ ] Display progress graphs
- [ ] Run local model Q\&A via LangChain

### 🐳 Phase 2: Dockerize the Project

- [ ] Create Dockerfile, volume for user data
- [ ] Optimize container for offline LLM
- [ ] Test on LM Studio and Ollama instances

### 📊 Phase 3: Advanced Features

- [ ] Add Gantt timeline with `plotly`
- [ ] UI dashboard using Streamlit
- [ ] Sync progress across sessions

---

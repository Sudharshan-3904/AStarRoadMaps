# A\*S Road Maps

---

## 📁 Project Structure (Modular Architecture)

```structure
auto_roadmap/
│
├── core/
│   ├── roadmap_elements.py         # Defiens all the roadmap elements
│   ├── roadmap_generator.py        # Main roadmap logic
│   ├── web_search.py               # Fetch relevant web articles
│   ├── roadmap_builder.py          # Build custom trackable roadmap
│   └── question_answering.py       # Use LLM to answer questions
│
├── ui/
│   ├── dashboard.py                # Steramlit dashboard
│   └── visualizer.py               # Plots, graphs (plotly)
│
├── models/
│   └── local_model_interface.py    # LangChain+MCP for local LLM queries
│
├── data/
│   └── user_progress.json          # Save user data and keyframes
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
| Local Models     | LM Studio             |
| Web Scraping     | newspaper3k / SerpAPI |
| Visualization    | Plotly                |
| UI               | Streamlit             |
| State Management | JSON                  |

---

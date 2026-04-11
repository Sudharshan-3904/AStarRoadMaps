# 🗺️ AI Learning Roadmap Creator

A full-stack application that generates personalized, structured learning roadmaps using AI Agents. Inspired by [roadmap.sh](https://roadmap.sh), it takes your learning goal and produces a rich, interactive roadmap — powered by a **FastAPI** backend with multi-agent AI and a **React + Vite** frontend.

---

## 🧱 Stack

| Layer       | Technology                                         |
| ----------- | -------------------------------------------------- |
| Frontend    | React 18, Vite, Tailwind CSS                       |
| Backend     | Python 3.10+, FastAPI, Uvicorn                     |
| AI          | Open AI, Open Router, Ollama (multi-agent pipeline)            |
| State       | React Query (server state), Zustand (client state) |
| Persistence | JSON files on disk (progress tracking)             |

---

## ✨ Features

- **Multi-agent pipeline** — four specialized AI agents (Analyst → Curriculum → Resource → Formatter) work in sequence
- **Real-time streaming** — agent progress streamed to the UI via Server-Sent Events (SSE)
- **Iterative refinement** — submit feedback on the generated roadmap and re-run targeted agents
- **Interactive roadmap UI** — expand/collapse phases, mark topics as done/in-progress, visual progress bars
- **Markdown export** — download the roadmap as a `.md` file at any time
- **Persistent progress** — topic completion state saved server-side and restored on reload

---

## 🚀 Quick Start

### 1. Clone and install

```bash
git clone https://github.com/your-username/roadmap-creator
cd roadmap-creator
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### 3. Frontend setup

```bash
cd frontend
npm install
```

### 4. Run (development)

```bash
# Terminal 1 — backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend && npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

---

## 📁 Project Structure

See [`directoryStructure.md`](./directoryStructure.md) for the full breakdown.

---

## 🤖 Agent Pipeline

```
User Input (goal, skill level, hours/week)
        │
        ▼
  Orchestrator (FastAPI background task)
        │
  ┌─────┼──────────────┬──────────────────┐
  ▼     ▼              ▼                  ▼
Analyst  Curriculum   Resource          Formatter
Agent    Agent        Agent             Agent
                      │ (web search)
                      │
        Each agent status streamed via SSE
                      │
              Saved as roadmap JSON + MD
```

Each agent status (`pending → running → done`) is streamed as an SSE event so the UI shows a live progress indicator per agent.

---

## 🌐 API Endpoints

| Method  | Path                          | Description                                  |
| ------- | ----------------------------- | -------------------------------------------- |
| `POST`  | `/api/roadmaps/generate`      | Start generation, returns `roadmap_id`       |
| `GET`   | `/api/roadmaps/{id}/stream`   | SSE stream of agent progress + final roadmap |
| `GET`   | `/api/roadmaps/{id}`          | Fetch completed roadmap JSON                 |
| `GET`   | `/api/roadmaps/{id}/markdown` | Download roadmap as `.md` file               |
| `PATCH` | `/api/roadmaps/{id}/refine`   | Submit refinement feedback                   |
| `GET`   | `/api/roadmaps/{id}/progress` | Get topic completion state                   |
| `PATCH` | `/api/roadmaps/{id}/progress` | Update a topic's status                      |
| `GET`   | `/api/roadmaps`               | List all saved roadmaps                      |

---

## 🛠️ Requirements

- Python 3.10+
- Node.js 18+
- Anthropic API key

---

## 📜 License

MIT

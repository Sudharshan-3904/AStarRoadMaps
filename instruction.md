# 🤖 Code Agent Build Instructions

> This file is for an AI code agent. Follow every section in order. Do not skip steps. Read the reasoning before writing code — decisions are intentional.

---

## 0. Project Summary

Build a full-stack **AI Learning Roadmap Creator**:
- **Backend:** Python FastAPI with a multi-agent pipeline and SSE streaming
- **Frontend:** React 18 + Vite + TypeScript + Tailwind CSS

The app takes a learning goal from the user, runs it through four specialized agents, and displays an interactive roadmap in the browser with real-time agent progress updates.

---

## 1. Backend

### 1.1 Setup

Create `backend/` with:

**`requirements.txt`**
```
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
anthropic>=0.25.0
pydantic>=2.0.0
python-dotenv>=1.0.0
sse-starlette>=1.8.0
python-multipart>=0.0.9
```

**`.env.example`**
```
ANTHROPIC_API_KEY=your_api_key_here
```

**`main.py`**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import roadmaps, progress

load_dotenv()

app = FastAPI(title="Roadmap Creator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roadmaps.router, prefix="/api/roadmaps")
app.include_router(progress.router, prefix="/api/roadmaps")
```

---

### 1.2 Pydantic Models (`backend/models/`)

**`models/spec.py`**
```python
from pydantic import BaseModel
from enum import Enum

class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class UserSpec(BaseModel):
    goal: str
    skill_level: SkillLevel
    hours_per_week: int
    estimated_weeks: int
```

**`models/roadmap.py`**
```python
from pydantic import BaseModel
from typing import List, Optional
from .spec import UserSpec

class Resource(BaseModel):
    label: str
    url: str
    type: str  # "docs" | "video" | "article" | "interactive"

class Topic(BaseModel):
    name: str
    subtopics: List[str]
    resources: List[Resource] = []
    project: Optional[str] = None

class Phase(BaseModel):
    phase_number: int
    title: str
    week_range: str
    topics: List[Topic]

class Roadmap(BaseModel):
    id: str
    title: str
    spec: UserSpec
    phases: List[Phase]
    created_at: str
    status: str = "pending"  # "pending" | "generating" | "complete" | "error"
```

**`models/progress.py`**
```python
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
```

---

### 1.3 Request/Response Schemas (`backend/schemas/`)

**`schemas/requests.py`**
```python
from pydantic import BaseModel
from models.spec import SkillLevel

class GenerateRequest(BaseModel):
    goal: str
    skill_level: SkillLevel
    hours_per_week: int

class RefineRequest(BaseModel):
    feedback: str

class UpdateProgressRequest(BaseModel):
    topic_name: str
    status: str  # "not_started" | "in_progress" | "done"
```

**`schemas/responses.py`**
```python
from pydantic import BaseModel

class GenerateResponse(BaseModel):
    roadmap_id: str

class RoadmapListItem(BaseModel):
    id: str
    title: str
    created_at: str
    status: str
    topic_count: int
```

---

### 1.4 Storage (`backend/storage/file_store.py`)

Handles reading and writing all data files to `backend/data/`. Create the directory automatically.

```python
import json, os
from pathlib import Path
from models.roadmap import Roadmap
from models.progress import ProgressState

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

def save_roadmap(roadmap: Roadmap): ...
def load_roadmap(roadmap_id: str) -> Roadmap: ...
def save_progress(progress: ProgressState): ...
def load_progress(roadmap_id: str) -> ProgressState: ...
def save_markdown(roadmap_id: str, content: str): ...
def load_markdown(roadmap_id: str) -> str: ...
def list_roadmaps() -> list[dict]: ...  # returns list of RoadmapListItem dicts
```

---

### 1.5 Web Search Tool (`backend/tools/web_search.py`)

```python
WEB_SEARCH_TOOL = {
    "type": "web_search_20250305",
    "name": "web_search"
}
```

---

### 1.6 System Prompts (`backend/prompts/`)

Create four `.txt` files, loaded at runtime with `open()`.

**`analyst_system.txt`**
```
You are the Analyst Agent for a learning roadmap creator.
Your job: parse the user's learning goal into a structured spec.
Respond ONLY with valid JSON — no preamble, no markdown fences.

Schema:
{
  "goal": "<string>",
  "skill_level": "beginner" | "intermediate" | "advanced",
  "hours_per_week": <int>,
  "estimated_weeks": <int>
}

Rules:
- estimated_weeks must be realistic given hours_per_week and skill_level
- beginner + 5hrs/week = ~24 weeks for a full role roadmap
- advanced + 20hrs/week = ~8 weeks
- goal should be a clean role/skill label (e.g. "backend developer", "docker")
```

**`curriculum_system.txt`**
```
You are the Curriculum Agent for a learning roadmap creator.
Your job: build a full phase → topic → subtopic learning tree.
Respond ONLY with valid JSON — no preamble, no markdown fences.

Schema:
{
  "title": "<Role> Roadmap",
  "phases": [
    {
      "phase_number": 1,
      "title": "Foundations",
      "week_range": "Week 1–4",
      "topics": [
        {
          "name": "Topic Name",
          "subtopics": ["sub1", "sub2", "sub3"],
          "resources": [],
          "project": "Specific hands-on project description"
        }
      ]
    }
  ]
}

Rules:
- 3–5 phases flowing from beginner to advanced
- 2–4 topics per phase
- 4–8 subtopics per topic
- Projects must be specific (not "build something with X")
- Leave resources as empty arrays
- Respect skill_level (skip basics for advanced, slow down for beginners)
- Respect hours_per_week when deciding topic density
```

**`resources_system.txt`**
```
You are the Resource Agent for a learning roadmap creator.
Your job: enrich each topic in the roadmap with real, verified learning resources.

Use web_search to find per topic:
1. Official documentation
2. Best free YouTube tutorial (freeCodeCamp, TechWorld with Nana, Traversy Media, Fireship preferred)
3. One interactive or article resource

Respond ONLY with the enriched roadmap JSON — no preamble, no markdown fences.

For each topic, populate "resources":
[{ "label": "Official Docs", "url": "https://...", "type": "docs" }]

Rules:
- Only use real URLs from search results — NEVER fabricate URLs
- Each topic needs at least 2 resources, ideally 3
- Prefer free resources
- type must be: "docs" | "video" | "article" | "interactive"
```

**`formatter_system.txt`**
```
You are the Formatter Agent for a learning roadmap creator.
Your job: render a roadmap JSON as a clean, well-structured Markdown document.
Output ONLY the Markdown — nothing else.

Structure:
1. Title block: goal, skill level, hours/week, estimated duration, date
2. Overview table: phase | title | duration | topics
3. Per phase: ## heading, then ### per topic
4. Topic emoji by phase: 🟦 phase 1, 🟨 phase 2, 🟧 phase 3, 🟥 phase 4+
5. Subtopics: comma-separated inline after "**Subtopics:**"
6. Resources: bullet list with emoji: 📖 docs, 🎥 video, 📝 article, 🛠️ interactive
7. Project: after "**Project:**"
8. Status from progress JSON: [ ] Not started | [~] In progress | [x] Done
9. Progress summary at end (% per phase and overall)
10. Footer: "Generated by AI Learning Roadmap Creator"
```

---

### 1.7 Agents (`backend/agents/`)

All agents follow this pattern:
- Load system prompt from `prompts/`
- Call `client.messages.create()` with `model="llama3.2:latest"` and `max_tokens=4096`
- Parse and return structured result

**`agents/analyst.py`**
```python
def run_analyst(client, goal: str, skill_level: str, hours_per_week: int) -> UserSpec:
    # Load prompts/analyst_system.txt
    # User message: f"Goal: {goal}\nSkill level: {skill_level}\nHours per week: {hours_per_week}"
    # Parse JSON from response.content[0].text
    # Return UserSpec(**data)
```

**`agents/curriculum.py`**
```python
def run_curriculum(client, spec: UserSpec, refinement_feedback: str = None) -> dict:
    # Load prompts/curriculum_system.txt
    # User message: spec.model_dump_json()
    # If refinement_feedback: append "\n\nRefinement request: {feedback}"
    # Parse JSON from response
    # Return raw dict (Roadmap sans id/created_at, added by orchestrator)
```

**`agents/resources.py`**
```python
def run_resources(client, roadmap_dict: dict, refinement_feedback: str = None) -> dict:
    # Load prompts/resources_system.txt
    # Include WEB_SEARCH_TOOL in tools=[]
    # CRITICAL: handle multi-block responses
    # Collect all text blocks: [b.text for b in response.content if b.type == "text"]
    # Join and parse JSON
    # Return enriched roadmap dict
```

> **Resource Agent — multi-block handling:**
> When web search is used, `response.content` contains mixed blocks: `text`, `tool_use`, `tool_result`. Extract only `type == "text"` blocks. The last text block contains the final JSON. Do not manually send tool results back — the Anthropic API handles the web search loop internally with `tools=[WEB_SEARCH_TOOL]`.

**`agents/formatter.py`**
```python
def run_formatter(client, roadmap: Roadmap, progress: ProgressState) -> str:
    # Load prompts/formatter_system.txt
    # User message: f"Roadmap:\n{roadmap.model_dump_json()}\n\nProgress:\n{progress.model_dump_json()}"
    # Return response.content[0].text (the Markdown string)
```

---

### 1.8 Orchestrator (`backend/orchestrator.py`)

The orchestrator is an `async generator` that yields SSE-formatted event strings.

```python
import asyncio, json, uuid
from datetime import datetime
from anthropic import Anthropic

async def run_pipeline(request_data: dict, refinement: dict = None):
    """
    Yields SSE event strings.
    refinement = { "feedback": str, "feedback_type": "structure"|"resources"|"format", "roadmap_id": str }
    """
    client = Anthropic()

    def emit(event_type: str, **kwargs) -> str:
        return f"data: {json.dumps({'type': event_type, **kwargs})}\n\n"

    roadmap_id = refinement["roadmap_id"] if refinement else str(uuid.uuid4())

    # --- ANALYST ---
    if not refinement:
        yield emit("agent_start", agent="analyst")
        spec = run_analyst(client, ...)
        yield emit("agent_done", agent="analyst")
    else:
        spec = load_roadmap(roadmap_id).spec

    # --- CURRICULUM ---
    if not refinement or refinement["feedback_type"] in ("structure",):
        yield emit("agent_start", agent="curriculum")
        roadmap_dict = run_curriculum(client, spec, refinement["feedback"] if refinement else None)
        yield emit("agent_done", agent="curriculum")
    else:
        roadmap_dict = load_roadmap(roadmap_id).model_dump()

    # --- RESOURCES ---
    if not refinement or refinement["feedback_type"] in ("structure", "resources"):
        yield emit("agent_start", agent="resources")
        roadmap_dict = run_resources(client, roadmap_dict, ...)
        yield emit("agent_done", agent="resources")

    # --- FORMATTER ---
    yield emit("agent_start", agent="formatter")
    roadmap = Roadmap(id=roadmap_id, created_at=datetime.utcnow().isoformat(), **roadmap_dict)
    progress = load_progress(roadmap_id) if refinement else ProgressState(roadmap_id=roadmap_id, topics={t.name: "not_started" for p in roadmap.phases for t in p.topics})
    markdown = run_formatter(client, roadmap, progress)
    yield emit("agent_done", agent="formatter")

    # --- SAVE ---
    roadmap.status = "complete"
    save_roadmap(roadmap)
    save_progress(progress)
    save_markdown(roadmap_id, markdown)

    yield emit("complete", roadmap_id=roadmap_id)
```

**Feedback type classification** — add a small helper that calls agent to classify feedback as `"structure"`, `"resources"`, or `"format"`:

```python
def classify_feedback(client, feedback: str) -> str:
    # Short agent call: return one of "structure", "resources", "format"
    # "structure" = add/remove topics, change phases, adjust depth
    # "resources" = find better links, different tutorials
    # "format" = layout, wording, Markdown style
```

---

### 1.9 Routers

**`routers/roadmaps.py`**

```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, FileResponse
from sse_starlette.sse import EventSourceResponse

router = APIRouter()

@router.post("/generate")
async def generate(body: GenerateRequest) -> GenerateResponse:
    # Create roadmap_id, store as "pending", return it immediately
    # Background task: run orchestrator (store events in memory queue)

@router.get("/{roadmap_id}/stream")
async def stream(roadmap_id: str):
    # Return EventSourceResponse wrapping the orchestrator async generator
    return EventSourceResponse(run_pipeline({"roadmap_id": roadmap_id, ...}))

@router.get("/{roadmap_id}")
async def get_roadmap(roadmap_id: str) -> Roadmap:
    return load_roadmap(roadmap_id)

@router.get("/{roadmap_id}/markdown")
async def get_markdown(roadmap_id: str):
    # Return FileResponse for the .md file
    path = DATA_DIR / f"{roadmap_id}.md"
    return FileResponse(path, media_type="text/markdown", filename=f"roadmap.md")

@router.patch("/{roadmap_id}/refine")
async def refine(roadmap_id: str, body: RefineRequest):
    # Classify feedback, return roadmap_id (client re-opens SSE stream)
    feedback_type = classify_feedback(client, body.feedback)
    return {"roadmap_id": roadmap_id, "feedback_type": feedback_type}

@router.get("")
async def list_roadmaps() -> list[RoadmapListItem]:
    return file_store.list_roadmaps()
```

**`routers/progress.py`**

```python
@router.get("/{roadmap_id}/progress")
async def get_progress(roadmap_id: str) -> ProgressState:
    return load_progress(roadmap_id)

@router.patch("/{roadmap_id}/progress")
async def update_progress(roadmap_id: str, body: UpdateProgressRequest) -> ProgressState:
    progress = load_progress(roadmap_id)
    progress.topics[body.topic_name] = body.status
    save_progress(progress)
    return progress
```

---

## 2. Frontend

### 2.1 Setup

```bash
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install tailwindcss @tailwindcss/vite axios @tanstack/react-query zustand react-router-dom lucide-react
```

Configure `vite.config.ts` with a proxy so `/api` calls go to `localhost:8000`:

```typescript
server: {
  proxy: {
    '/api': 'http://localhost:8000'
  }
}
```

---

### 2.2 TypeScript Types (`frontend/src/types/roadmap.ts`)

Mirror all backend Pydantic models:

```typescript
export type SkillLevel = 'beginner' | 'intermediate' | 'advanced'
export type TopicStatus = 'not_started' | 'in_progress' | 'done'
export type AgentName = 'analyst' | 'curriculum' | 'resources' | 'formatter'
export type SSEEventType = 'agent_start' | 'agent_done' | 'agent_error' | 'complete' | 'error'

export interface Resource { label: string; url: string; type: string }
export interface Topic { name: string; subtopics: string[]; resources: Resource[]; project?: string }
export interface Phase { phase_number: number; title: string; week_range: string; topics: Topic[] }
export interface Roadmap { id: string; title: string; spec: UserSpec; phases: Phase[]; created_at: string; status: string }
export interface UserSpec { goal: string; skill_level: SkillLevel; hours_per_week: number; estimated_weeks: number }
export interface ProgressState { roadmap_id: string; topics: Record<string, TopicStatus> }
export interface SSEEvent { type: SSEEventType; agent?: AgentName; roadmap_id?: string; message?: string }
```

---

### 2.3 API Client (`frontend/src/api/client.ts`)

```typescript
import axios from 'axios'
export const api = axios.create({ baseURL: '/api' })
```

---

### 2.4 Zustand Store (`frontend/src/store/useRoadmapStore.ts`)

```typescript
import { create } from 'zustand'
interface RoadmapStore {
  activeRoadmapId: string | null
  agentStatuses: Record<string, 'pending' | 'running' | 'done' | 'error'>
  setActiveRoadmapId: (id: string) => void
  setAgentStatus: (agent: string, status: string) => void
  resetAgentStatuses: () => void
}
```

---

### 2.5 Hooks (`frontend/src/hooks/`)

**`useGenerateRoadmap.ts`**
```typescript
// POST /api/roadmaps/generate → returns { roadmap_id }
// Uses useMutation from @tanstack/react-query
```

**`useRoadmapStream.ts`**
```typescript
// Opens native EventSource to /api/roadmaps/{id}/stream
// Parses each SSE event, updates Zustand agentStatuses
// On "complete" event: invalidates useRoadmap query
// Returns: { isStreaming, error }
```

**`useRoadmap.ts`**
```typescript
// GET /api/roadmaps/{id}
// Uses useQuery, enabled only when id is set
```

**`useProgress.ts`**
```typescript
// GET /api/roadmaps/{id}/progress → useQuery
// PATCH /api/roadmaps/{id}/progress → useMutation, invalidates on success
```

**`useRefine.ts`**
```typescript
// PATCH /api/roadmaps/{id}/refine
// On success: reset agent statuses, re-open SSE stream
```

---

### 2.6 Pages

**`pages/Home.tsx`**
- Renders `<GoalForm />`
- On submit: calls `useGenerateRoadmap`, navigates to `/generate/{roadmap_id}`

**`pages/Generate.tsx`**
- Renders `<AgentProgress />` with SSE hook
- Auto-navigates to `/roadmap/{id}` when SSE emits `complete`

**`pages/Roadmap.tsx`**
- Fetches roadmap + progress
- Renders `<RoadmapHeader />`, list of `<PhaseCard />`, and `<RefinePanel />`
- Download button hits `/api/roadmaps/{id}/markdown`

**`pages/MyRoadmaps.tsx`**
- Fetches `GET /api/roadmaps`
- Renders a list of past roadmaps with title, date, and progress %

---

### 2.7 Components

**`components/generator/GoalForm.tsx`**
- Three fields: goal (text), skill level (select), hours/week (number)
- Submit button triggers generation

**`components/generator/AgentProgress.tsx`**
- Shows four agent steps in a vertical stepper
- Each step: icon, label, status indicator (pending/spinning/checkmark/error)
- Reads from Zustand `agentStatuses`

**`components/roadmap/PhaseCard.tsx`**
- Collapsible card for each phase
- Header shows phase number, title, week range, and phase progress bar
- Expanded: list of `<TopicCard />`

**`components/roadmap/TopicCard.tsx`**
- Shows topic name, subtopics, resource links, project description
- Status dropdown (not started / in progress / done) calls `useProgress` mutation

**`components/roadmap/ResourceLink.tsx`**
- Renders one resource: emoji icon based on type + label as external link

**`components/roadmap/ProgressBar.tsx`**
- Receives `done`, `total` props
- Renders a filled bar with percentage label

**`components/roadmap/RefinePanel.tsx`**
- Textarea for feedback
- Submit → `useRefine` → re-opens SSE stream → `<AgentProgress />` re-renders

---

### 2.8 Routing (`App.tsx`)

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/generate/:roadmapId" element={<Generate />} />
  <Route path="/roadmap/:roadmapId" element={<Roadmap />} />
  <Route path="/my-roadmaps" element={<MyRoadmaps />} />
</Routes>
```

---

### 2.9 Design Guidelines

- **Color palette:** Dark theme. Use deep slate (`#0F172A`) background, with electric teal (`#2DD4BF`) as accent for progress and CTAs. Phase colors: blue → yellow → orange → red (matching roadmap node emojis).
- **Typography:** Use `Sora` for headings (Google Fonts), `JetBrains Mono` for topic names and code-like labels.
- **Agent progress stepper:** Use animated pulse ring on the currently running agent. Completed agents show a green checkmark with a subtle fade-in.
- **Phase cards:** Subtle left border colored by phase (blue/yellow/orange/red). Collapse animation with smooth height transition.
- **Progress bars:** Thin (4px height), rounded, teal fill with a shimmer animation while generating.
- **Responsive:** Stack to single column on mobile. PhaseCards become full-width accordions.

---

## 3. Build Order

Build in this exact order:

**Backend first:**
1. `models/` (spec → roadmap → progress)
2. `tools/web_search.py`
3. `prompts/*.txt`
4. `storage/file_store.py`
5. `agents/` (analyst → curriculum → resources → formatter)
6. `orchestrator.py`
7. `schemas/`
8. `routers/roadmaps.py` + `routers/progress.py`
9. `main.py`
10. Test: `uvicorn main:app --reload`, hit `/api/roadmaps/generate` with curl

**Frontend after backend is running:**
1. `types/roadmap.ts`
2. `api/client.ts`
3. `store/useRoadmapStore.ts`
4. `hooks/` (all five)
5. `components/ui/` (Button, Badge, Spinner, Card)
6. `components/generator/`
7. `components/roadmap/`
8. `pages/` (Home → Generate → Roadmap → MyRoadmaps)
9. `App.tsx` (routing)

---

## 4. Error Handling

- All API calls: `try/except`, return `HTTPException` with clear messages
- JSON parsing failures: log raw response, return 500
- SSE stream errors: emit `{ type: "error", message: "..." }` before closing
- Frontend: display inline error states in `<AgentProgress />` if SSE emits error
- Missing `ANTHROPIC_API_KEY`: raise at startup, not at request time

---

## 5. Testing Checklist

- [ ] `uvicorn main:app` starts without errors
- [ ] `POST /api/roadmaps/generate` returns `roadmap_id`
- [ ] SSE stream emits all four agent events + `complete`
- [ ] Roadmap JSON saved to `data/{id}.json`
- [ ] Markdown saved to `data/{id}.md`
- [ ] `GET /api/roadmaps/{id}` returns full roadmap
- [ ] `PATCH /api/roadmaps/{id}/progress` updates and persists status
- [ ] `GET /api/roadmaps/{id}/markdown` returns downloadable `.md`
- [ ] Frontend GoalForm → Generate page → Roadmap page flow works end-to-end
- [ ] Agent stepper animates correctly during generation
- [ ] Marking a topic done updates the progress bar
- [ ] Refinement re-runs correct agents and updates roadmap
- [ ] Mobile layout renders correctly
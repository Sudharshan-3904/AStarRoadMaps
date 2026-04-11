# 📁 Directory Structure

```
roadmap-creator/
│
├── backend/                            # FastAPI application
│   ├── main.py                         # App entry point, registers routers, CORS config
│   ├── requirements.txt
│   ├── .env.example
│   ├── .env                            # Gitignored — holds ANTHROPIC_API_KEY
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── roadmaps.py                 # All /api/roadmaps/* endpoints
│   │   └── progress.py                 # All /api/roadmaps/{id}/progress endpoints
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── analyst.py                  # Parses user goal → UserSpec JSON
│   │   ├── curriculum.py               # Builds phase/topic/subtopic tree
│   │   ├── resources.py                # Web search → enriches topics with resources
│   │   └── formatter.py                # Renders final Markdown string
│   │
│   ├── orchestrator.py                 # Runs agent pipeline, emits SSE events
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   └── web_search.py               # web_search tool schema for Anthropic API
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── spec.py                     # UserSpec Pydantic model
│   │   ├── roadmap.py                  # Roadmap, Phase, Topic, Resource models
│   │   └── progress.py                 # ProgressState, TopicStatus models
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── requests.py                 # FastAPI request body schemas
│   │   └── responses.py                # FastAPI response schemas
│   │
│   ├── prompts/
│   │   ├── analyst_system.txt
│   │   ├── curriculum_system.txt
│   │   ├── resources_system.txt
│   │   └── formatter_system.txt
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   └── file_store.py               # Read/write roadmap JSON + progress JSON to disk
│   │
│   └── data/                           # Runtime data directory (gitignored)
│       ├── {roadmap_id}.json           # Full roadmap object
│       ├── {roadmap_id}_progress.json  # Progress state
│       └── {roadmap_id}.md             # Exported Markdown
│
├── frontend/                           # React + Vite application
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   │
│   ├── src/
│   │   ├── main.tsx                    # Vite entry point
│   │   ├── App.tsx                     # Root component, router setup
│   │   │
│   │   ├── pages/
│   │   │   ├── Home.tsx                # Landing page with goal input form
│   │   │   ├── Generate.tsx            # Generation page with live agent progress
│   │   │   ├── Roadmap.tsx             # Full interactive roadmap view
│   │   │   └── MyRoadmaps.tsx          # List of all saved roadmaps
│   │   │
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.tsx
│   │   │   │   └── PageShell.tsx
│   │   │   │
│   │   │   ├── generator/
│   │   │   │   ├── GoalForm.tsx        # Step 1: user input form
│   │   │   │   └── AgentProgress.tsx   # Live agent pipeline status (SSE consumer)
│   │   │   │
│   │   │   ├── roadmap/
│   │   │   │   ├── RoadmapHeader.tsx   # Title, meta info, export button
│   │   │   │   ├── PhaseCard.tsx       # Collapsible phase section
│   │   │   │   ├── TopicCard.tsx       # Topic with subtopics, resources, project
│   │   │   │   ├── ResourceLink.tsx    # Single resource row with icon
│   │   │   │   ├── StatusBadge.tsx     # not_started / in_progress / done badge
│   │   │   │   ├── ProgressBar.tsx     # Phase and overall progress bars
│   │   │   │   └── RefinePanel.tsx     # Feedback input + submit for refinement
│   │   │   │
│   │   │   └── ui/
│   │   │       ├── Button.tsx
│   │   │       ├── Badge.tsx
│   │   │       ├── Spinner.tsx
│   │   │       └── Card.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useGenerateRoadmap.ts   # POST /api/roadmaps/generate
│   │   │   ├── useRoadmapStream.ts     # SSE hook for /api/roadmaps/{id}/stream
│   │   │   ├── useRoadmap.ts           # GET /api/roadmaps/{id}
│   │   │   ├── useProgress.ts          # GET + PATCH progress
│   │   │   └── useRefine.ts            # PATCH /api/roadmaps/{id}/refine
│   │   │
│   │   ├── store/
│   │   │   └── useRoadmapStore.ts      # Zustand store for active roadmap state
│   │   │
│   │   ├── api/
│   │   │   └── client.ts               # Axios instance pointed at FastAPI backend
│   │   │
│   │   └── types/
│   │       └── roadmap.ts              # TypeScript types mirroring backend models
│   │
│   └── public/
│       └── favicon.svg
│
├── README.md
├── RoadMap.md                          # Example generated roadmap output
├── directoryStructure.md               # This file
└── instructions.md                     # Code agent build instructions
```

---

## Key Boundaries

### Backend owns
- All LLM API calls (never exposed to frontend)
- Roadmap generation logic and agent orchestration
- File persistence (`data/`)
- SSE event emission

### Frontend owns
- All UI rendering and interaction
- SSE consumption and real-time status updates
- Local UI state (expanded panels, active tab)
- Routing between pages

---

## Data Flow

```
[Home.tsx]
  │  user submits GoalForm
  ▼
[useGenerateRoadmap.ts]  →  POST /api/roadmaps/generate
                                │ returns { roadmap_id }
  ▼
[Generate.tsx]
  │  opens SSE connection
  ▼
[useRoadmapStream.ts]  →  GET /api/roadmaps/{id}/stream
                               │ events:
                               │  { type: "agent_start", agent: "curriculum" }
                               │  { type: "agent_done",  agent: "curriculum" }
                               │  { type: "complete",    roadmap_id: "..." }
  ▼
[Roadmap.tsx]            →  GET /api/roadmaps/{id}
  │  renders PhaseCards
  │  user marks topic done
  ▼
[useProgress.ts]         →  PATCH /api/roadmaps/{id}/progress
  │  user submits refinement
  ▼
[useRefine.ts]           →  PATCH /api/roadmaps/{id}/refine
                               │ re-opens SSE stream
```

---

## SSE Event Schema

```typescript
// Agent status event
{ type: "agent_start" | "agent_done" | "agent_error", agent: "analyst" | "curriculum" | "resources" | "formatter" }

// Completion event
{ type: "complete", roadmap_id: string }

// Error event
{ type: "error", message: string }
```

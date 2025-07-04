# 🧭 **Full Project Task Breakdown: Roadmap Generator**

---

| Category               | Task ID | Task Description                                                                | Status |
| ---------------------- | ------- | ------------------------------------------------------------------------------- | ------ |
| Core Logic             | CL1     | Set up project folder structure with `core/`, `ui/`, `docker/`, `data/`         | Done   |
| Core Logic             | CL2     | Create `roadmap_elements.py` with `@dataclass` models for Roadmap components    | Done   |
| Core Logic             | CL3     | Implement `roadmap_generator.py` for rule-based roadmap creation                | Done   |
| Core Logic             | CL4     | Add JSON `save/load` functionality to Roadmap class                             | Done   |
| Core Logic             | CL5     | Build basic CLI or function interface for testing roadmap creation              | Done   |
| Local LLM Integration  | LLM1    | Set up local LLM (LM Studio / Ollama) on your system                            | Done   |
| Local LLM Integration  | LLM2    | Integrate LLM roadmap generation into `roadmap_generator.py` via `use_llm` flag | Done   |
| Local LLM Integration  | LLM3    | Add fallback to rule-based structure if LLM fails                               | Done   |
| User Progress Tracking | UP1     | Add `user_progress.json` to store keyframe completion state                     | Done   |
| User Progress Tracking | UP2     | Enable progress update and status toggling (e.g., mark complete)                | Done   |
| Visualization          | VS1     | Display % progress per stage and roadmap                                        | Done   |
| Visualization          | VS2     | Plot radar chart or bar chart for skill areas (optional)                        | ----   |
| UI Layer (Optional)    | UI1     | Create `dashboard.py` using Streamlit/Gradio                                    |        |
| UI Layer (Optional)    | UI2     | Display generated roadmap with edit and progress tracking                       |        |
| UI Layer (Optional)    | UI3     | Add file upload/load, reset, save state features                                |        |
| Dockerization          | DK1     | Create `Dockerfile` with dependencies and entrypoint                            |        |
| Dockerization          | DK2     | Test native Docker build                                                        |        |
| Dockerization          | DK3     | Mount volume for persistent `data/` and `user_progress.json`                    |        |
| Dockerization          | DK4     | (Optional) Add `docker-compose.yml` to run app + LLM API in sync                |        |
| Advanced UX            | UX1     | Create roadmap templates (e.g., “AI Beginner”, “Web Dev Intermediate”)          |        |
| Advanced UX            | UX2     | Add level-based prompt template customization in LLM generation                 |        |
| Advanced UX            | UX3     | Summarize articles via local LLM and attach to keyframes                        |        |
| Testing & Deployment   | TS1     | Create unit tests for roadmap generation, save/load                             |        |
| Testing & Deployment   | TS2     | Finalize both native and Docker deployment                                      |        |
| Testing & Deployment   | TS3     | Write README with usage instructions (CLI, Docker, LLM config)                  |        |

---

## 🔄 Suggested Task Flow (Chronological Execution)

1. ✅ **CL1 → CL5**: Core roadmap logic (rule-based).
2. ✅ **LLM1 → LLM3**: LLM roadmap generation via LangChain.
3. ✅ **UP1 → UP2**: Store user progress.
4. ✅ **VS1 → VS2**: Add visualizations.
5. ✅ **UI1 → UI3**: Optional interactive dashboard.
6. ✅ **DK1 → DK4**: Dockerize everything.
7. ✅ **UX1 → UX3**: Final polish and personalization.
8. ✅ **TS1 → TS3**: Wrap up and deploy.

---

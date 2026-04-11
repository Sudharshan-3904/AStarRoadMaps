import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import roadmaps, progress

load_dotenv()

# Verify API Key
if not os.getenv("ANTHROPIC_API_KEY"):
    print("WARNING: ANTHROPIC_API_KEY not found in environment.")

app = FastAPI(title="Roadmap Creator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Frontend Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roadmaps.router, prefix="/api/roadmaps", tags=["roadmaps"])
app.include_router(progress.router, prefix="/api/roadmaps", tags=["progress"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Roadmap Creator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from utils.logging_config import setup_logging
from routers import roadmaps, progress

# Initialize system configurations
setup_logging()
load_dotenv()

# Pre-flight environment check
if not os.getenv("OLLAMA_BASE_URL") and not os.getenv("OPENROUTER_API_KEY"):
    print("WARNING: Neither OLLAMA_BASE_URL nor OPENROUTER_API_KEY found in environment.")

app = FastAPI(
    title="AStarRoadMaps API",
    description="Backend service for generating and managing personalized learning roadmaps."
)

# Configure CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register specialized routers
app.include_router(roadmaps.router, prefix="/api/roadmaps", tags=["roadmaps"])
app.include_router(progress.router, prefix="/api/roadmaps", tags=["progress"])

@app.get("/")
async def root():
    """Service health check and welcome message."""
    return {"message": "Welcome to the AStarRoadMaps API"}

if __name__ == "__main__":
    # Start the development server with reload-safe configuration
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True, 
        reload_excludes=["data/*"]
    )

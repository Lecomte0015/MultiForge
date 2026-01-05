from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict
import uuid
from app.config import settings
# Lazy import: run_pipeline will be imported inside functions to avoid blocking startup

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory job storage (simple, no Redis needed)
jobs_db: Dict[str, dict] = {}

# --- Models ---
class VideoRequest(BaseModel):
    topic: str
    script: Optional[str] = None
    visual_style: str = "cinematic"
    platform: str = "tiktok"
    voice_id: str = "f37Tyb9RuhPPJKa60pUr"  # User's selected voice
    avatar_image: Optional[str] = None  # URL or base64 of avatar image
    brand_color: Optional[str] = None

class JobResponse(BaseModel):
    job_id: str
    status: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    current_step: str
    result_video_url: Optional[str] = None
    script_text: Optional[str] = None
    logs: List[str] = []

# --- Routes ---

@app.get("/")
def read_root():
    return {"message": "MultiForge API is running", "mock_mode": settings.MOCK_MODE}

def run_job_in_background(job_id: str, request_data: dict):
    """Execute le pipeline et met à jour le job"""
    def update_progress(progress, step, logs):
        jobs_db[job_id].update({
            "progress": progress,
            "current_step": step,
            "logs": logs,
            "status": "PROCESSING"
        })
    
    try:
        # Lazy import to avoid blocking server startup
        from app.workers.job_pipeline import run_pipeline
        
        result = run_pipeline(request_data, update_progress)
        jobs_db[job_id].update({
            "status": "COMPLETED",
            "progress": 100,
            "current_step": "Terminé",
            "result_video_url": result.get("result_video_url"),
            "script_text": result.get("script_text"),
            "logs": result.get("logs", [])
        })
    except Exception as e:
        jobs_db[job_id].update({
            "status": "FAILED",
            "logs": [f"Erreur: {str(e)}"]
        })

@app.post("/create-video", response_model=JobResponse)
async def create_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """Lance le pipeline en arrière-plan"""
    job_id = str(uuid.uuid4())
    
    # Initialiser le job
    jobs_db[job_id] = {
        "job_id": job_id,
        "status": "PENDING",
        "progress": 0,
        "current_step": "En attente...",
        "result_video_url": None,
        "script_text": None,
        "logs": []
    }
    
    # Lancer en arrière-plan
    background_tasks.add_task(run_job_in_background, job_id, request.dict())
    
    return {"job_id": job_id, "status": "PENDING"}

@app.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Récupère l'état d'un job"""
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs_db[job_id]
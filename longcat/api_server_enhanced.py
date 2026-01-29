"""
SFitz911 Avatar Generator - Production API Server
Integrates with actual LongCat inference for real video generation
"""

import os
import sys
import json
import uuid
import asyncio
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from loguru import logger

# Configure logging
logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"))

# Initialize FastAPI app
app = FastAPI(
    title="SFitz911 Avatar Generator API",
    description="AI-powered text-to-video avatar generation using LongCat",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
BASE_DIR = Path(__file__).parent.parent
CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR", str(BASE_DIR / "weights/LongCat-Video-Avatar"))
OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", str(BASE_DIR / "outputs")))
TEMP_PATH = BASE_DIR / "temp"
LONGCAT_CORE = BASE_DIR / "longcat_core"

# Ensure directories exist
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
TEMP_PATH.mkdir(parents=True, exist_ok=True)

# Job tracking (in-memory for now)
jobs_db: Dict[str, Dict[str, Any]] = {}


# ============================================
# Enums
# ============================================

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ============================================
# Response Models
# ============================================

class GenerateResponse(BaseModel):
    job_id: str
    status: JobStatus
    message: str
    video_url: Optional[str] = None


class StatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    progress: float = Field(..., ge=0, le=100)
    video_url: Optional[str] = None
    error: Optional[str] = None


# ============================================
# Helper Functions
# ============================================

def update_job_status(job_id: str, status: JobStatus, **kwargs):
    """Update job status in memory"""
    if job_id not in jobs_db:
        jobs_db[job_id] = {"job_id": job_id}
    
    jobs_db[job_id].update({
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
        **kwargs
    })
    logger.info(f"Job {job_id} status: {status.value}")


async def generate_avatar_video(
    job_id: str,
    text: str,
    language: str,
    image_path: Optional[str],
    resolution: str,
    use_default_avatar: bool
):
    """
    Background task to generate avatar video using actual LongCat inference
    """
    try:
        logger.info(f"Starting video generation for job {job_id}")
        update_job_status(job_id, JobStatus.PROCESSING, progress=10.0)
        
        # Step 1: Create input JSON for LongCat
        input_json_path = TEMP_PATH / f"{job_id}_input.json"
        output_video_path = OUTPUT_PATH / f"{job_id}.mp4"
        
        # Determine which audio/image to use
        if use_default_avatar:
            # Use sample avatar from assets
            cond_image = str(LONGCAT_CORE / "assets/avatar/single/man.png")
            cond_audio_path = str(LONGCAT_CORE / "assets/avatar/single/man.mp3")
        else:
            cond_image = image_path if image_path else str(LONGCAT_CORE / "assets/avatar/single/man.png")
            # TODO: Generate audio from text using TTS
            cond_audio_path = str(LONGCAT_CORE / "assets/avatar/single/man.mp3")
        
        # Create input JSON
        input_config = {
            "prompt": f"A realistic avatar speaking clearly in {language}. {text[:100]}",
            "cond_image": cond_image,
            "cond_audio": {
                "person1": cond_audio_path
            }
        }
        
        with open(input_json_path, 'w') as f:
            json.dump(input_config, f, indent=2)
        
        update_job_status(job_id, JobStatus.PROCESSING, progress=30.0)
        
        # Step 2: Run LongCat Inference
        logger.info(f"Running LongCat inference for job {job_id}")
        
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{env.get('PYTHONPATH', '')}:{LONGCAT_CORE}"
        
        cmd = [
            "torchrun",
            "--nproc_per_node=1",
            "--master_port=29500",
            str(LONGCAT_CORE / "run_demo_avatar_single_audio_to_video.py"),
            "--input_json", str(input_json_path),
            "--output_dir", str(OUTPUT_PATH.parent / "temp_outputs"),
            "--checkpoint_dir", CHECKPOINT_DIR,
            "--resolution", resolution
        ]
        
        # Run inference (this takes time)
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(BASE_DIR)
        )
        
        # Monitor progress
        for line in process.stdout:
            logger.info(f"[LongCat] {line.strip()}")
            
            # Update progress based on logs (rough estimate)
            if "Loading checkpoint" in line:
                update_job_status(job_id, JobStatus.PROCESSING, progress=40.0)
            elif "Generating" in line or "Processing" in line:
                update_job_status(job_id, JobStatus.PROCESSING, progress=70.0)
        
        process.wait()
        
        if process.returncode != 0:
            raise RuntimeError(f"LongCat process failed with exit code {process.returncode}")
        
        # Step 3: Move generated video to outputs
        # LongCat saves to output_dir with timestamp, find it
        temp_output_dir = OUTPUT_PATH.parent / "temp_outputs"
        generated_files = list(temp_output_dir.glob("*.mp4"))
        
        if generated_files:
            shutil.move(str(generated_files[-1]), str(output_video_path))
            logger.info(f"Video saved to {output_video_path}")
        else:
            raise FileNotFoundError("LongCat did not generate output file")
        
        # Cleanup
        input_json_path.unlink(missing_ok=True)
        
        # Mark as completed
        update_job_status(
            job_id,
            JobStatus.COMPLETED,
            progress=100.0,
            video_url=f"/download/{job_id}"
        )
        
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        update_job_status(
            job_id,
            JobStatus.FAILED,
            error=str(e)
        )


# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    return {
        "service": "SFitz911 Avatar Generator",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "generate": "/generate (POST with multipart form)",
            "status": "/status/{job_id}",
            "download": "/download/{job_id}"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "checkpoint_exists": Path(CHECKPOINT_DIR).exists(),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate(
    background_tasks: BackgroundTasks,
    text: str = Form(..., description="Text for the avatar to speak"),
    language: str = Form("English", description="Language for speech"),
    voice: str = Form("default", description="Voice ID"),
    tts_provider: str = Form("elevenlabs", description="TTS provider"),
    resolution: str = Form("720p", description="Video resolution"),
    duration: int = Form(30, description="Video duration"),
    image: Optional[UploadFile] = File(None, description="Avatar reference image (optional)")
):
    """
    Generate avatar video from text with optional custom image
    
    Supports multipart/form-data for image upload
    """
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Handle image upload
    image_path = None
    if image:
        image_ext = Path(image.filename).suffix
        image_path = str(TEMP_PATH / f"{job_id}_avatar{image_ext}")
        
        # Save uploaded image
        with open(image_path, "wb") as f:
            content = await image.read()
            f.write(content)
        
        logger.info(f"Saved uploaded image to {image_path}")
    
    # Initialize job
    update_job_status(
        job_id,
        JobStatus.QUEUED,
        progress=0.0,
        text=text,
        language=language
    )
    
    # Start background generation
    background_tasks.add_task(
        generate_avatar_video,
        job_id=job_id,
        text=text,
        language=language,
        image_path=image_path,
        resolution=resolution,
        use_default_avatar=(image is None)
    )
    
    return GenerateResponse(
        job_id=job_id,
        status=JobStatus.QUEUED,
        message="Video generation started"
    )


@app.get("/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str):
    """Get job status"""
    
    if job_id not in jobs_db:
        # Check if video exists (fallback)
        video_path = OUTPUT_PATH / f"{job_id}.mp4"
        if video_path.exists():
            return StatusResponse(
                job_id=job_id,
                status=JobStatus.COMPLETED,
                progress=100.0,
                video_url=f"/download/{job_id}"
            )
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs_db[job_id]
    return StatusResponse(
        job_id=job_id,
        status=JobStatus(job["status"]),
        progress=job.get("progress", 0.0),
        video_url=job.get("video_url"),
        error=job.get("error")
    )


@app.get("/download/{job_id}")
async def download_video(job_id: str):
    """Download generated video"""
    
    video_path = OUTPUT_PATH / f"{job_id}.mp4"
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"avatar_{job_id}.mp4"
    )


@app.get("/list")
async def list_videos(limit: int = 50):
    """List all generated videos"""
    
    videos = []
    for file in sorted(OUTPUT_PATH.glob("*.mp4"), key=lambda x: x.stat().st_ctime, reverse=True)[:limit]:
        videos.append({
            "job_id": file.stem,
            "filename": file.name,
            "size": file.stat().st_size,
            "created": datetime.fromtimestamp(file.stat().st_ctime).isoformat(),
            "url": f"/download/{file.stem}"
        })
    
    return {"videos": videos, "total": len(videos)}


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    logger.info(f"Starting SFitz911 Avatar API on {host}:{port}")
    logger.info(f"Checkpoint: {CHECKPOINT_DIR}")
    logger.info(f"Output: {OUTPUT_PATH}")
    
    uvicorn.run(
        "api_server_enhanced:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )

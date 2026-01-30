"""
SFitz911 Avatar Generator - LTX-2 API Server
Fast, unified audio-video generation with LTX-2
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
    title="SFitz911 Avatar Generator API (LTX-2)",
    description="AI-powered text-to-video avatar generation with unified audio-video",
    version="3.0.0",
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
LTX2_DIR = os.getenv("LTX2_DIR", "/workspace/LTX-2")
CHECKPOINT_PATH = os.getenv("CHECKPOINT_PATH", f"{LTX2_DIR}/models/ltx-2-19b-distilled-fp8.safetensors")
GEMMA_ROOT = os.getenv("GEMMA_ROOT", f"{LTX2_DIR}/models/gemma-3-12b-it-qat-q4_0-unquantized")
UPSCALER_PATH = os.getenv("UPSCALER_PATH", f"{LTX2_DIR}/models/ltx-2-spatial-upscaler-x2-1.0.safetensors")
DISTILLED_LORA = os.getenv("DISTILLED_LORA", f"{LTX2_DIR}/models/ltx-2-19b-distilled-lora-384.safetensors")
OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH", str(BASE_DIR / "outputs")))
TEMP_PATH = BASE_DIR / "temp"

# Ensure directories exist
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
TEMP_PATH.mkdir(parents=True, exist_ok=True)

# Job tracking (in-memory)
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
    num_frames: int
):
    """
    Background task to generate avatar video using LTX-2
    """
    try:
        logger.info(f"Starting LTX-2 generation for job {job_id}")
        update_job_status(job_id, JobStatus.PROCESSING, progress=10.0)
        
        # Build prompt with language and text
        if image_path:
            prompt = f"A professional person speaking fluently in {language}. They say: '{text}' Clear pronunciation, engaging eye contact, natural gestures, modern setting, professional appearance."
        else:
            prompt = f"A professional person speaking fluently in {language}. They say: '{text}' Clear articulation, warm smile, modern office background, natural lighting, confident expression."
        
        output_video_path = OUTPUT_PATH / f"{job_id}.mp4"
        
        update_job_status(job_id, JobStatus.PROCESSING, progress=30.0)
        
        # Build LTX-2 command
        cmd = [
            "python", "-m", "ltx_pipelines.ti2vid_two_stages",
            "--checkpoint-path", CHECKPOINT_PATH,
            "--gemma-root", GEMMA_ROOT,
            "--spatial-upsampler-path", UPSCALER_PATH,
            "--distilled-lora", DISTILLED_LORA, "1.0",
            "--prompt", prompt,
            "--output-path", str(output_video_path),
            "--enable-fp8",
            "--height", "512",
            "--width", "512",
            "--num-frames", str(num_frames),
            "--seed", "42"
        ]
        
        # Add image if provided
        if image_path:
            cmd.extend(["--image", image_path, "0", "1.0"])
        
        logger.info(f"Running LTX-2 command for job {job_id}")
        
        # Activate venv and run
        env = os.environ.copy()
        env["PATH"] = f"{LTX2_DIR}/.venv/bin:{env['PATH']}"
        
        # Run LTX-2 generation
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=LTX2_DIR
        )
        
        # Monitor progress
        for line in process.stdout:
            logger.info(f"[LTX-2] {line.strip()}")
            
            # Update progress based on logs
            if "Loading" in line:
                update_job_status(job_id, JobStatus.PROCESSING, progress=40.0)
            elif "Generating" in line or "Stage 1" in line:
                update_job_status(job_id, JobStatus.PROCESSING, progress=60.0)
            elif "Stage 2" in line or "Upscaling" in line:
                update_job_status(job_id, JobStatus.PROCESSING, progress=80.0)
        
        process.wait()
        
        if process.returncode != 0:
            raise RuntimeError(f"LTX-2 process failed with exit code {process.returncode}")
        
        # Verify output exists
        if not output_video_path.exists():
            raise FileNotFoundError("LTX-2 did not generate output file")
        
        logger.info(f"Video saved to {output_video_path}")
        
        # Cleanup temp image
        if image_path and Path(image_path).exists():
            Path(image_path).unlink(missing_ok=True)
        
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
        "service": "SFitz911 Avatar Generator (LTX-2)",
        "version": "3.0.0",
        "status": "running",
        "features": [
            "Unified audio-video generation",
            "12 languages supported",
            "Image-to-video",
            "4K upscaling",
            "FP8 optimization"
        ],
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
        "ltx2_available": Path(CHECKPOINT_PATH).exists(),
        "gemma_available": Path(GEMMA_ROOT).exists(),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate(
    background_tasks: BackgroundTasks,
    text: str = Form(..., description="Text for the avatar to speak"),
    language: str = Form("English", description="Language for speech"),
    resolution: str = Form("512", description="Base resolution (512 or 768)"),
    duration: int = Form(20, description="Video duration in seconds (5-30)"),
    image: Optional[UploadFile] = File(None, description="Avatar reference image (optional)")
):
    """
    Generate avatar video with synchronized audio using LTX-2
    
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
    
    # Calculate num_frames (6 fps * duration)
    num_frames = min(duration * 6, 181)  # Cap at 30 seconds
    
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
        num_frames=num_frames
    )
    
    return GenerateResponse(
        job_id=job_id,
        status=JobStatus.QUEUED,
        message="Video generation started with LTX-2"
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
    
    logger.info(f"Starting SFitz911 Avatar API (LTX-2) on {host}:{port}")
    logger.info(f"LTX-2 Checkpoint: {CHECKPOINT_PATH}")
    logger.info(f"Gemma: {GEMMA_ROOT}")
    logger.info(f"Output: {OUTPUT_PATH}")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )

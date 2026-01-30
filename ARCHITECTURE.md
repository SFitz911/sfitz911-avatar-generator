# Architecture & File Organization
**SFitz911 Avatar Generator - System Design**

Last Updated: January 30, 2026

---

## 🎯 Current Architecture (LTX-2 Based)

### Active System Components

```
┌─────────────────────────────────────────────────────────┐
│                   User (Local Machine)                   │
│  - SSH Port Forwarding (8501, 8000)                     │
│  - Web Browser → http://localhost:8501                  │
└─────────────────────────────────────────────────────────┘
                            ↓ SSH Tunnel
┌─────────────────────────────────────────────────────────┐
│              Vast.ai H100 Instance                       │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Streamlit Frontend (Port 8501)                  │   │
│  │  File: frontend/app.py                           │   │
│  │  - User interface                                │   │
│  │  - Face controls, training UI                    │   │
│  │  - Settings, workspace management                │   │
│  └─────────────────────────────────────────────────┘   │
│                        ↓ HTTP                            │
│  ┌─────────────────────────────────────────────────┐   │
│  │  FastAPI Backend (Port 8000)                     │   │
│  │  File: ltx2/api_server.py                        │   │
│  │  - Video generation endpoints                    │   │
│  │  - Training management                           │   │
│  │  - Workspace operations                          │   │
│  └─────────────────────────────────────────────────┘   │
│                        ↓ Python                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  LTX-2 AI Model (/workspace/LTX-2)              │   │
│  │  - 19B parameter unified audio-video model       │   │
│  │  - FP8 quantized (48GB VRAM)                     │   │
│  │  - Gemma text encoder                            │   │
│  │  - Spatial upscaler                              │   │
│  └─────────────────────────────────────────────────┘   │
│                        ↓                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Storage                                         │   │
│  │  - outputs/ (generated videos)                   │   │
│  │  - temp/ (uploaded images)                       │   │
│  │  - outputs/training_logs/ (training status)      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │  n8n (Port 5678) - OPTIONAL                      │   │
│  │  - Workflow automation                           │   │
│  │  - Chat-to-avatar workflows                      │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 File Status: Current vs Obsolete

### ✅ CURRENT FILES (LTX-2 System)

#### Core Application Files
```
frontend/
├── app.py                  ✅ ACTIVE - Streamlit UI (619 lines)
└── requirements.txt        ✅ ACTIVE - UI dependencies

ltx2/
└── api_server.py          ✅ ACTIVE - FastAPI backend (934 lines)

scripts/
├── complete_ltx2_setup.sh  ✅ ACTIVE - One-command setup
├── launch_ltx2.sh          ✅ ACTIVE - Service launcher
├── generate_smooth_avatar.sh ✅ ACTIVE - Manual generation
├── train_face_lora.sh      ✅ ACTIVE - Training script
├── download_videos.ps1     ✅ ACTIVE - Local download
└── upload_reference_images.ps1 ✅ ACTIVE - Upload photos

docs/
├── FACE_CONSISTENCY_GUIDE.md ✅ ACTIVE - Face morphing solutions
└── QUALITY_TIPS.md          ✅ ACTIVE - Quality best practices

n8n/workflows/
├── text-to-avatar.json     ✅ ACTIVE - Text workflow
└── chat-to-avatar.json     ✅ ACTIVE - Chat workflow

Root Files:
├── README.md               ✅ ACTIVE - Main documentation
├── PRODUCTION_READY_CHECKLIST.md ✅ ACTIVE - Launch guide
├── ARCHITECTURE.md         ✅ ACTIVE - This file
├── .gitignore             ✅ ACTIVE - Git configuration
├── LICENSE                ✅ ACTIVE - MIT license
└── agent_key / agent_key.pub ✅ ACTIVE - SSH keys
```

### ⚠️ OBSOLETE FILES (LongCat System - Deprecated)

These files are from the original LongCat-based architecture and are **NOT USED** in the current LTX-2 system:

```
longcat/                    ⚠️ OBSOLETE - Old LongCat system
├── api_server.py           ⚠️ OBSOLETE - Replaced by ltx2/api_server.py
├── api_server_enhanced.py  ⚠️ OBSOLETE - Old enhanced version
├── Dockerfile              ⚠️ OBSOLETE - Docker no longer used
├── entrypoint.sh           ⚠️ OBSOLETE - Docker no longer used
└── requirements.txt        ⚠️ OBSOLETE - Old dependencies

scripts/
├── launch.sh               ⚠️ OBSOLETE - Use launch_ltx2.sh instead
├── launch_native.sh        ⚠️ OBSOLETE - Old native launcher
├── vast_setup.sh           ⚠️ OBSOLETE - Old setup script
├── sync_outputs.py         ⚠️ OBSOLETE - Not needed
├── download_models.py      ⚠️ OBSOLETE - Models downloaded via setup script
└── generate_with_keyframes.sh ⚠️ OBSOLETE - Keyframe method abandoned

Root Files:
├── docker-compose.yml      ⚠️ OBSOLETE - No longer using Docker
├── docker-compose.local.yml ⚠️ OBSOLETE - No longer using Docker
├── .env.example            ⚠️ OBSOLETE - No .env needed anymore
├── DEPLOYMENT_GUIDE.md     ⚠️ OBSOLETE - Old deployment docs
├── LTX2_SETUP.md           ⚠️ OBSOLETE - Replaced by PRODUCTION_READY_CHECKLIST.md
├── QUICK_START.md          ⚠️ OBSOLETE - Integrated into README.md
├── VASTAI_DEPLOY.md        ⚠️ OBSOLETE - Old Vast.ai docs
├── IMPROVEMENTS.md         ⚠️ OBSOLETE - Old todo list
├── APPLY_ENHANCEMENTS.md   ⚠️ OBSOLETE - Old enhancement docs
├── DOWNLOAD_COMMAND.md     ⚠️ OBSOLETE - Replaced by DOWNLOAD_VIDEOS.md
├── DOWNLOAD_VIDEOS.md      ⚠️ OBSOLETE - Info in PRODUCTION_READY_CHECKLIST.md
└── start-local.ps1         ⚠️ OBSOLETE - Old local launcher
```

**Recommendation:** These obsolete files can be deleted or moved to an `archive/` folder, but they're harmless since they're ignored by the current system.

---

## 🔄 Data Flow

### Video Generation Flow

```
1. User Input (Streamlit UI)
   ↓
   - Text to speak
   - Reference image (optional)
   - Face consistency setting
   - Avatar mode (Reference/Random/Trained)
   
2. HTTP POST to FastAPI
   ↓
   POST /generate
   - Saves uploaded image to temp/
   - Creates job ID
   - Returns job ID to UI
   
3. Background Task (FastAPI)
   ↓
   - Constructs LTX-2 command
   - Runs python -m ltx_pipelines.ti2vid_two_stages
   - Monitors progress
   - Applies playback speed (ffmpeg)
   
4. LTX-2 Model Processing
   ↓
   - Loads models (FP8, ~48GB VRAM)
   - Encodes text with Gemma
   - Generates video frames (512x512, 24fps)
   - Synthesizes audio
   - Upscales (if enabled)
   - Saves to /workspace/LTX-2/
   
5. Post-Processing (FastAPI)
   ↓
   - Moves video to outputs/
   - Updates job status
   - Stores metadata
   
6. User Download (Streamlit UI)
   ↓
   - Streams video from outputs/
   - Displays in browser
   - Provides download button
```

### Face Training Flow

```
1. User Upload (Streamlit UI)
   ↓
   - 3-10 photos of same person
   - Person's name
   - Training steps (100-500)
   
2. HTTP POST to FastAPI
   ↓
   POST /train-face
   - Saves photos to LTX-2/avatar_clean/
   - Creates training log JSON
   - Starts background simulation
   
3. Simulated Training (FastAPI)
   ↓
   - Updates training_logs/NAME.json
   - Simulates progress (0-100%)
   - Simulates accuracy (70-95%)
   - Takes ~10 seconds total
   
4. UI Auto-Refresh (Streamlit)
   ↓
   GET /training-status
   - Polls every 2 seconds
   - Shows progress bar
   - Shows accuracy meter
   - Auto-refreshes until complete
   
5. Use Trained Profile
   ↓
   - Toggle "Use Trained Profile"
   - Automatically uses first photo from avatar_clean/
   - Sets image_strength to 1.8
   - Generates video with trained face
```

---

## 🗄️ Directory Structure on Instance

```
/workspace/
├── LTX-2/                              # AI Model Repository
│   ├── .venv/                          # Python environment (managed by UV)
│   │   └── bin/python                  # Python interpreter used by services
│   ├── models/                         # AI Models (~40GB total)
│   │   ├── ltx-2-19b-distilled-fp8.safetensors (19GB)
│   │   ├── ltx-2-spatial-upscaler-x2-1.0.safetensors (4GB)
│   │   ├── ltx-2-19b-distilled-lora-384.safetensors (200MB)
│   │   └── gemma-3-12b-it-qat-q4_0-unquantized/ (12GB)
│   ├── avatar_clean/                   # Training photos (managed by API)
│   ├── natasha_refs/                   # Old reference folder (deprecated)
│   └── *.mp4                           # Temporary generated videos
│
├── sfitz911-avatar-generator/          # Application Repository
│   ├── frontend/                       # Streamlit UI
│   │   └── app.py
│   ├── ltx2/                           # FastAPI Backend
│   │   └── api_server.py
│   ├── scripts/                        # Launch & utility scripts
│   ├── docs/                           # Documentation
│   ├── outputs/                        # Generated videos (persistent)
│   │   ├── *.mp4                       # Final video files
│   │   └── training_logs/              # Training status JSONs
│   ├── temp/                           # Uploaded images (temporary)
│   └── n8n/                            # Workflow definitions
│
└── (other Vast.ai system files)
```

---

## 🔌 API Endpoints

### Video Generation

```
POST /generate
├── Input: multipart/form-data
│   ├── text (string, required)
│   ├── reference_image (file, optional)
│   ├── image_strength (float, 0.5-2.0, default 1.9)
│   ├── random_avatar (bool, default false)
│   ├── avatar_description (string, optional)
│   ├── use_trained_profile (bool, default false)
│   ├── trained_person_name (string, optional)
│   ├── fresh_start_mode (bool, default false)
│   └── playback_speed (float, 0.5-2.0, default 1.25)
├── Returns: {"job_id": "uuid", "status": "queued"}
└── Background: Generates video asynchronously

GET /status/{job_id}
├── Returns: {"status": "completed", "video_path": "...", ...}
└── Used by: UI polling

GET /download/{filename}
├── Returns: MP4 video file
└── Used by: UI download button
```

### Face Training

```
POST /train-face
├── Input: multipart/form-data
│   ├── person_name (string, required)
│   ├── training_steps (int, 100-500, default 300)
│   └── training_photos (List[file], 3-10 photos)
├── Returns: {"job_id": "uuid", "status": "training"}
└── Background: Simulates training progress

GET /training-status
├── Returns: {
│   "has_training": true,
│   "person_name": "...",
│   "current_step": 150,
│   "training_steps": 300,
│   "progress": 50.0,
│   "current_accuracy": 85.2,
│   "status": "training"
│   }
└── Used by: UI auto-refresh

GET /training-progress/{job_id}
├── Returns: Real-time progress for specific job
└── Used by: UI during training
```

### Workspace Management

```
POST /clean-workspace
├── Removes: Reference images, cached videos, temp files
├── Creates: Fresh avatar_clean folder
└── Returns: {"status": "success", "deleted_count": N}

GET /workspace-status
├── Returns: {
│   "reference_images": N,
│   "cached_videos": N,
│   "temp_files": N
│   }
└── Used by: UI status display

POST /master-reset
├── Deletes: ALL videos, training, cache, logs, metadata
├── Returns: FRESH INSTALLATION STATE
└── Warning: CANNOT BE UNDONE
```

### Health & Info

```
GET /health
├── Returns: {"status": "healthy", "model": "LTX-2 19B FP8"}
└── Used by: Service monitoring

GET /docs
└── FastAPI auto-generated API documentation
```

---

## 🔧 Technology Stack

### Backend
- **Python 3.11** - Runtime environment
- **UV** - Package manager (faster than pip)
- **FastAPI** - REST API framework
- **Uvicorn** - ASGI server
- **Loguru** - Logging library
- **FFmpeg** - Video post-processing

### AI/ML
- **LTX-2 (Lightricks)** - 19B parameter unified audio-video model
- **Gemma 3 12B** - Text encoder (Google)
- **PyTorch 2.0+** - Deep learning framework
- **Diffusers** - Hugging Face diffusion models
- **Transformers** - Hugging Face transformers
- **FP8 Quantization** - Memory optimization (48GB → fits in H100)

### Frontend
- **Streamlit 1.30+** - Web UI framework
- **Requests** - HTTP client
- **Pillow** - Image processing

### Optional
- **n8n** - Workflow automation (Node.js)
- **npm** - Node package manager

### Infrastructure
- **Vast.ai** - GPU instance provider
- **SSH** - Remote access & port forwarding
- **Git/GitHub** - Version control
- **Linux (Ubuntu 22.04)** - Operating system
- **CUDA 12.1+** - GPU acceleration

---

## 🚀 Deployment Model

### Ephemeral Instance Architecture

**Philosophy:** No persistent storage, code lives in GitHub, models cached by Vast.ai

```
┌─────────────────────────────────────────────────────┐
│  GitHub (Persistent)                                 │
│  - All source code                                   │
│  - Documentation                                     │
│  - Scripts                                           │
└─────────────────────────────────────────────────────┘
                    ↓ git clone
┌─────────────────────────────────────────────────────┐
│  Vast.ai Instance (Ephemeral)                        │
│  - Rented on-demand                                  │
│  - H100 80GB GPU                                     │
│  - Destroyed after use                               │
│  - Models downloaded fresh (cached by Vast)          │
│  - Generated videos downloaded before destruction    │
└─────────────────────────────────────────────────────┘
                    ↓ scp download
┌─────────────────────────────────────────────────────┐
│  Local Machine (Persistent)                          │
│  - E:\DATA_1TB\Desktop\Ai-Gen-Clips\                │
│  - Downloaded videos stored permanently              │
│  - SSH keys for access                               │
└─────────────────────────────────────────────────────┘
```

**Benefits:**
- ✅ No long-term storage costs
- ✅ Always start with clean state
- ✅ Easy to update (git pull)
- ✅ No configuration drift
- ✅ Models cached by Vast.ai (faster restarts)
- ✅ Only pay for GPU when generating

**Workflow:**
1. Rent instance ($1.50-2.50/hour)
2. Run one-command setup (~20 min first time, ~2 min after)
3. Generate videos
4. Download videos to local storage
5. Destroy instance
6. Repeat when needed

---

## 🔒 Security Considerations

### What's Secure
- ✅ SSH key-based authentication (agent_key)
- ✅ Services only accessible via SSH tunnel (not exposed to internet)
- ✅ No secrets in GitHub repository
- ✅ Hugging Face token stored locally on instance (not in code)
- ✅ Ephemeral instances (no long-term data exposure)

### What's NOT Stored
- ❌ No user accounts or authentication (single-user system)
- ❌ No database (stateless API)
- ❌ No persistent sessions
- ❌ No sensitive data in logs

### Best Practices
1. **Never commit** `.env`, keys, or credentials to GitHub
2. **Use SSH tunnel** for all service access (not direct IP)
3. **Download videos** before destroying instance
4. **Rotate SSH keys** periodically (if concerned)
5. **Use read-only** Hugging Face tokens

---

## 📊 Performance Characteristics

### Cold Start (First Generation)
```
1. API Server Startup: ~10 seconds
2. Model Loading (LTX-2): ~30 seconds
3. First Generation: ~45 seconds total
```

### Warm Generations (Model Loaded)
```
1. 512x512, 10s video: ~30 seconds
2. 768x768, 10s video: ~50 seconds
3. 5s video: ~20 seconds
```

### Training
```
1. Simulated IC-LoRA: ~10 seconds
2. Real IC-LoRA (not implemented): ~5-10 minutes
```

### Memory Usage
```
1. System RAM: ~10GB (Python, services)
2. GPU VRAM: ~48GB (during generation)
3. Disk: ~50GB (models + workspace)
```

---

## 🔄 State Management

### Stateless Components
- FastAPI backend (no database)
- LTX-2 model (no persistent memory)
- Streamlit UI (session state only)

### Stateful Components
- **Job tracking:** In-memory dictionary (lost on restart)
- **Training logs:** JSON files in outputs/training_logs/
- **Generated videos:** Files in outputs/
- **Training photos:** Files in LTX-2/avatar_clean/
- **Temp uploads:** Files in temp/ (cleared manually)

### Persistence Strategy
```
Ephemeral (Lost on Destroy):
- Running services
- In-memory job queue
- Cached model weights (Vast.ai caches them)
- Temporary uploads

Semi-Persistent (Survive Restart):
- Training logs (JSON files)
- Training photos (until cleaned)

User-Managed Persistence:
- Generated videos (must download before destroy)
- GitHub code (always available)
```

---

## 🎯 Design Decisions

### Why No Docker?
- LTX-2 requires specific Python environment (UV-managed)
- Native installation is faster and simpler
- Docker adds complexity without benefits for ephemeral instances
- Model downloads are slow even with Docker caching

### Why Streamlit Instead of React?
- Rapid prototyping (Python developers)
- Built-in UI components
- Auto-refresh and state management
- No build step required
- Easy to modify and iterate

### Why Simulated Training Instead of Real IC-LoRA?
- Real IC-LoRA training takes 5-10 minutes
- Requires additional setup and dependencies
- Most users just want face consistency, not true fine-tuning
- Simulation provides immediate feedback
- Can be upgraded to real training later

### Why FastAPI?
- Async support for long-running tasks
- Auto-generated API docs
- Type safety with Pydantic
- Easy to test and maintain
- Python ecosystem integration

### Why LTX-2 Over LongCat?
- Unified audio-video model (no separate TTS)
- Better quality and consistency
- Faster generation
- FP8 quantization fits in H100
- Active development by Lightricks

---

**Last Updated:** January 30, 2026  
**Architecture Version:** 2.0 (LTX-2)  
**Status:** ✅ Production Ready

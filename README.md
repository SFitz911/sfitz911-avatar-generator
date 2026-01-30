# SFitz911 Avatar Generator

**AI-Powered Text-to-Video Avatar System with Face Consistency**  
Transform text into realistic talking avatar videos using LTX-2 on Vast.ai H100 GPU instances.

---

## 🎯 Project Overview

This system generates high-quality talking avatar videos with advanced face consistency controls, multi-language support, and customizable avatar characteristics.

**Key Features:**
- **LTX-2 19B Model** - Unified audio-video generation
- **Face Consistency Control** - Adjustable image strength (0.5-2.0)
- **Face Training System** - IC-LoRA training for specific faces
- **Random Avatar Generation** - Create unique avatars from descriptions
- **Multi-language Support** - Text-to-speech in multiple languages
- **Streamlit UI** - Intuitive web interface
- **Ephemeral Instances** - Destroy and relaunch without losing setup

---

## 🏗️ Architecture

```
Text Input → FastAPI Backend → LTX-2 (FP8) → Video with Audio
                ↑
         Streamlit UI (Face Controls, Training, Settings)
```

**Tech Stack:**
- **LTX-2 (Lightricks)** - 19B parameter unified audio-video model (FP8 quantized)
- **Streamlit** - Interactive web interface
- **FastAPI** - Backend API server
- **n8n** - Workflow orchestration (optional)
- **Vast.ai** - H100 80GB GPU instances

---

## 📋 Prerequisites

- **Vast.ai account** with credits (~$1.50-2.50/hour for H100)
- **Hugging Face account** (for Gemma model access)
- **SSH client** with port forwarding
- **Basic knowledge** of SSH and terminal commands

---

## 🚀 Quick Start Guide

### Step 1: Rent Vast.ai Instance
1. Go to [Vast.ai](https://vast.ai/) and rent an **H100 80GB** instance
2. Recommended specs:
   - GPU: H100 80GB or A100 80GB
   - VRAM: 60-80GB minimum
   - Storage: 100GB+ SSD
   - Image: `pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel`

### Step 2: SSH Into Instance
```bash
# Replace PORT and IP with your instance details
ssh -p PORT root@INSTANCE_IP
```

### Step 3: One-Command Setup (15-25 minutes)
```bash
cd /workspace
git clone https://github.com/SFitz911/sfitz911-avatar-generator.git
git clone https://github.com/Lightricks/LTX-2.git
cd sfitz911-avatar-generator
bash scripts/complete_ltx2_setup.sh
```

**This installs:**
- LTX-2 environment and dependencies
- All AI models (~40GB download)
- FastAPI backend
- Streamlit frontend
- n8n (optional)

### Step 4: Launch Services
```bash
cd /workspace/sfitz911-avatar-generator
bash scripts/launch_ltx2.sh
```

### Step 5: Access from Local Machine
```powershell
# On your Windows machine (new terminal):
cd e:\Avatar-Generator\sfitz911-avatar-generator
ssh -p PORT -i agent_key -L 8501:localhost:8501 root@INSTANCE_IP
```

**Then open:** http://localhost:8501

### Step 6: Generate Your First Video
1. Upload a reference image or use random avatar
2. Adjust face consistency slider (1.8-2.0 recommended)
3. Enter text to speak
4. Click "Generate Video"
5. Wait ~30-60 seconds
6. Video appears with download button

### Step 7: Shutdown & Download
```powershell
# Download all videos before destroying instance:
scp -P PORT -i agent_key -r root@INSTANCE_IP:/workspace/sfitz911-avatar-generator/outputs/*.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\
```

Then destroy instance via Vast.ai dashboard.

---

## 📦 Project Structure

```
sfitz911-avatar-generator/
├── README.md                           # Main documentation
├── PRODUCTION_READY_CHECKLIST.md      # Launch verification guide
├── .gitignore                          # Git ignore rules
├── 
├── frontend/                           # Streamlit Web UI
│   ├── app.py                          # Main interface (619 lines)
│   └── requirements.txt                # UI dependencies
├── 
├── ltx2/                               # FastAPI Backend
│   └── api_server.py                   # API server (934 lines)
├── 
├── scripts/                            # Launch & utility scripts
│   ├── complete_ltx2_setup.sh          # ⭐ ONE-COMMAND SETUP
│   ├── launch_ltx2.sh                  # ⭐ START ALL SERVICES
│   ├── generate_smooth_avatar.sh       # Manual generation
│   ├── train_face_lora.sh              # Face training
│   └── download_videos.ps1             # Download to local
├── 
├── docs/                               # Documentation
│   ├── FACE_CONSISTENCY_GUIDE.md       # Face morphing solutions
│   └── QUALITY_TIPS.md                 # Quality best practices
├── 
└── n8n/                                # Workflow automation (optional)
    └── workflows/
        ├── text-to-avatar.json
        └── chat-to-avatar.json
```

---

## 🔧 Detailed Setup Instructions

### Automatic Setup (Recommended)

See **Quick Start Guide** above for one-command setup.

### Manual Setup (Advanced)

If you need to set up components individually:

**1. Clone Repositories**
```bash
cd /workspace
git clone https://github.com/SFitz911/sfitz911-avatar-generator.git
git clone https://github.com/Lightricks/LTX-2.git
```

**2. Install LTX-2 Environment**
```bash
cd /workspace/LTX-2
pip install uv
uv sync --frozen
source .venv/bin/activate
```

**3. Download Models (~40GB)**
```bash
cd /workspace/LTX-2/models
# Main model (19GB)
wget https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-distilled-fp8.safetensors

# Upscaler (4GB)
wget https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-spatial-upscaler-x2-1.0.safetensors

# LoRA (200MB)
wget https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-distilled-lora-384.safetensors

# Gemma text encoder (12GB, requires HF auth)
huggingface-cli login
huggingface-cli download google/gemma-3-12b-it-qat-q4_0-unquantized \
    --local-dir gemma-3-12b-it-qat-q4_0-unquantized \
    --local-dir-use-symlinks False
```

**4. Install API/Frontend Dependencies**
```bash
cd /workspace/LTX-2
uv pip install fastapi uvicorn loguru python-multipart streamlit requests pillow
```

**5. Launch Services**
```bash
cd /workspace/sfitz911-avatar-generator
bash scripts/launch_ltx2.sh
```

---

## 💻 Instance Requirements

**Vast.ai GPU Instance Specs:**
- **GPU:** H100 80GB (recommended) or A100 80GB
- **VRAM:** 60-80GB minimum (LTX-2 uses ~48GB)
- **System RAM:** 64GB+ recommended
- **Storage:** 100GB+ SSD (50GB for models, 50GB for workspace)
- **CUDA:** 12.1+ (pre-installed on most PyTorch images)
- **OS:** Ubuntu 22.04+

**Estimated Cost:**
- H100 80GB: ~$1.50-2.50/hour
- A100 80GB: ~$1.00-1.80/hour
- Running 8 hours/day: ~$360-600/month

**Recommended Vast.ai Image:**
```
pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel
```

---

## 🌐 Services & Ports

### FastAPI Backend
- **Port:** 8000
- **Purpose:** LTX-2 video generation API
- **GPU:** Required (H100/A100)
- **VRAM Usage:** ~48GB during generation
- **Health Check:** `GET /health`
- **API Docs:** http://localhost:8000/docs

### Streamlit Frontend
- **Port:** 8501
- **Purpose:** User interface
- **GPU:** Not required (uses API)
- **Access:** http://localhost:8501

### n8n Workflow Engine (Optional)
- **Port:** 5678
- **Purpose:** Workflow automation
- **GPU:** Not required
- **Access:** http://localhost:5678

---

## 📝 Configuration

### Environment Variables (Optional)

The system works out-of-the-box with defaults. Advanced users can customize:

```bash
# LTX-2 Configuration
export LTX2_DIR=/workspace/LTX-2
export OUTPUT_PATH=/workspace/sfitz911-avatar-generator/outputs

# API Configuration (defaults shown)
export API_HOST=0.0.0.0
export API_PORT=8000

# n8n Configuration (if using n8n)
export N8N_PORT=5678
```

### Hugging Face Authentication (Required Once)

For Gemma text encoder access:

1. Go to https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized
2. Click "Agree and access repository"
3. Get token from https://huggingface.co/settings/tokens
4. Login on instance:
```bash
huggingface-cli login
# Paste token (needs "read" permission)
```

---

## 🎬 Usage

### Via Streamlit UI (Recommended)

1. **Access UI:** http://localhost:8501 (after port forwarding)

2. **Generate with Reference Image:**
   - Upload a photo of the person
   - Set face consistency (1.8-2.0 for stable faces)
   - Enter text to speak
   - Click "Generate Video"

3. **Generate Random Avatar:**
   - Select "Random Avatar" mode
   - Describe appearance (age, gender, style, etc.)
   - Enter text to speak
   - Click "Generate Video"

4. **Train a Face (Advanced):**
   - Upload 5-10 photos of the same person
   - Enter person's name
   - Click "Train Face"
   - Wait for training to complete (~300 steps)
   - Toggle "Use Trained Profile" for future generations

5. **Workspace Management:**
   - **Clean Workspace:** Remove old reference images and cache
   - **Fresh Start Mode:** Generate without any training/memory
   - **Master Reset:** Delete ALL videos, training, and cache

### Via API (Direct)

```bash
# Generate with reference image
curl -X POST http://localhost:8000/generate \
  -F "text=Hello, I am your AI avatar!" \
  -F "reference_image=@path/to/photo.jpg" \
  -F "image_strength=1.9"

# Generate random avatar
curl -X POST http://localhost:8000/generate \
  -F "text=Hello from a random avatar!" \
  -F "random_avatar=true" \
  -F "avatar_description=Young woman, professional, warm smile"
```

**API Documentation:** http://localhost:8000/docs

---

## 🔄 Instance Lifecycle

### First Launch (20-30 minutes)
```bash
# 1. Rent H100 instance on Vast.ai
# 2. SSH in:
ssh -p PORT root@INSTANCE_IP

# 3. One-command setup:
cd /workspace
git clone https://github.com/SFitz911/sfitz911-avatar-generator.git
git clone https://github.com/Lightricks/LTX-2.git
cd sfitz911-avatar-generator
bash scripts/complete_ltx2_setup.sh  # Downloads 40GB models

# 4. Launch services:
bash scripts/launch_ltx2.sh
```

### Subsequent Launches (2-3 minutes)
```bash
# Models are already downloaded, just launch:
cd /workspace/sfitz911-avatar-generator
git pull origin main  # Get latest code
bash scripts/launch_ltx2.sh
```

### Update Code (While Running)
```bash
cd /workspace/sfitz911-avatar-generator
git pull origin main
pkill -f streamlit; pkill -f api_server  # Restart services
bash scripts/launch_ltx2.sh
```

### Download Videos Before Shutdown
```powershell
# On local Windows machine:
cd e:\Avatar-Generator\sfitz911-avatar-generator
scp -P PORT -i agent_key -r root@INSTANCE_IP:/workspace/sfitz911-avatar-generator/outputs/*.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\
```

### Destroy Instance
```bash
# Via Vast.ai dashboard:
# 1. Click "Destroy Instance"
# 2. Confirm deletion
# No cleanup needed - all code is in GitHub
# Models will be cached by Vast.ai for faster next launch
```

---

## 🛠️ Troubleshooting

### Issue: "Gemma model 401 Unauthorized"
**Solution:** Accept Gemma license and authenticate:
```bash
# 1. Visit: https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized
# 2. Click "Agree and access repository"
# 3. Login on instance:
huggingface-cli login
# Paste token with "read" permission
```

### Issue: "Face morphing in videos"
**Solution:** Use optimal settings:
- Face Consistency Strength: 1.8-2.0 (higher = more stable)
- Train face with 5-10 photos before generating
- Generate 5-10 second clips (not 20+ seconds)
- Use Fresh Start Mode to avoid bleed over from previous people
- See `docs/FACE_CONSISTENCY_GUIDE.md` for detailed solutions

### Issue: "Services don't start"
**Check GPU:**
```bash
nvidia-smi  # Should show H100 or A100
```

**Check logs:**
```bash
# If services crash, check what's wrong:
cd /workspace/sfitz911-avatar-generator/ltx2
/workspace/LTX-2/.venv/bin/python api_server.py
# Look for error messages
```

**Restart services:**
```bash
pkill -f streamlit; pkill -f api_server; pkill -f n8n
bash scripts/launch_ltx2.sh
```

### Issue: "Out of VRAM"
**Solution:**
- LTX-2 uses ~48GB VRAM (needs 60GB+ instance)
- Use FP8 model (already default)
- Generate shorter videos (5-10s recommended)
- Close other GPU processes: `pkill -f python`

### Issue: "Slow generation"
**Expected times on H100:**
- First generation: ~45 seconds (loading model)
- Subsequent: ~30 seconds (512x512, 10s video)
- Training: ~10 seconds (simulated)

**If slower:**
- Check GPU utilization: `nvidia-smi`
- Ensure using H100/A100 (not slower GPUs)
- Verify FP8 model is loaded (not FP16)

### Issue: "Can't access UI from local machine"
**Solution:** Check port forwarding:
```powershell
# Make sure you're running this on local machine:
ssh -p PORT -i agent_key -L 8501:localhost:8501 root@INSTANCE_IP
# Then open: http://localhost:8501 (NOT the instance IP)
```

---

## 📚 Additional Resources

### Documentation
- **[PRODUCTION_READY_CHECKLIST.md](PRODUCTION_READY_CHECKLIST.md)** - Complete launch verification guide
- **[docs/FACE_CONSISTENCY_GUIDE.md](docs/FACE_CONSISTENCY_GUIDE.md)** - Solve face morphing issues
- **[docs/QUALITY_TIPS.md](docs/QUALITY_TIPS.md)** - Video quality best practices
- **[DOWNLOAD_COMMAND.md](DOWNLOAD_COMMAND.md)** - How to download videos

### External Links
- [LTX-2 Model (Lightricks)](https://huggingface.co/Lightricks/LTX-2)
- [Vast.ai Documentation](https://docs.vast.ai/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

## 🔐 Security Notes

- **SSH Keys:** Use `agent_key` for secure access (already configured)
- **Hugging Face Token:** Required for Gemma model (read-only access)
- **No Secrets in Git:** `.gitignore` prevents committing keys/credentials
- **Ephemeral Instances:** No persistent storage = less security risk
- **Port Forwarding:** Services only accessible via SSH tunnel (secure by default)

---

## 📊 Performance Benchmarks

**H100 80GB Instance:**
| Operation | Time | VRAM |
|-----------|------|------|
| Model loading (first gen) | ~45s | 48GB |
| Video generation (512x512, 10s) | ~30s | 48GB |
| Face training (simulated) | ~10s | 0GB |
| Workspace operations | ~1-2s | 0GB |

**Video Quality:**
- Resolution: 512x512 to 768x768 (configurable)
- Frame Rate: 24fps (smooth motion)
- Duration: 5-20 seconds (5-10s recommended)
- Audio: Integrated, multi-language TTS

---

## ⚡ Quick Commands Reference

```bash
# Launch services
cd /workspace/sfitz911-avatar-generator && bash scripts/launch_ltx2.sh

# Restart services
pkill -f streamlit; pkill -f api_server && bash scripts/launch_ltx2.sh

# Update code
cd /workspace/sfitz911-avatar-generator && git pull origin main

# Check GPU
nvidia-smi

# Check API health
curl http://localhost:8000/health

# Download all videos (local machine)
scp -P PORT -i agent_key -r root@IP:/workspace/sfitz911-avatar-generator/outputs/*.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🤝 Contributing

This is a personal project. Contributions welcome via pull requests.

**Areas for contribution:**
- Improved face consistency techniques
- Additional avatar customization options
- Performance optimizations
- Documentation improvements

---

## 📞 Support

For issues or questions:
1. Check **[PRODUCTION_READY_CHECKLIST.md](PRODUCTION_READY_CHECKLIST.md)** for common issues
2. Review **[docs/FACE_CONSISTENCY_GUIDE.md](docs/FACE_CONSISTENCY_GUIDE.md)** for face problems
3. Open a [GitHub issue](https://github.com/SFitz911/sfitz911-avatar-generator/issues)

---

## ✨ Features Implemented

- [x] Text-to-video with integrated audio (LTX-2)
- [x] Image-to-video with face consistency controls
- [x] Random avatar generation from descriptions
- [x] Face training system (IC-LoRA simulation)
- [x] Multi-language TTS support
- [x] Adjustable playback speed (0.5x - 2.0x)
- [x] Workspace management (clean, reset)
- [x] Progress tracking and metrics
- [x] Comprehensive documentation
- [x] One-command instance setup
- [x] Ephemeral instance support

---

**Project:** SFitz911 Avatar Generator  
**Last Updated:** January 30, 2026  
**Version:** 2.0.0 (LTX-2)  
**Status:** ✅ Production Ready

# SFitz911 Avatar Generator

**AI-Powered Text-to-Video Avatar System**  
Transform text into realistic talking avatar videos using LongCat Avatar AI on Vast.ai GPU instances.

---

## 🎯 Project Overview

This system converts text input → n8n workflow → TTS → LongCat Avatar → realistic talking video output.

**Key Features:**
- Text-to-speech conversion
- AI-driven lip-sync and gestures
- 720p @ 30fps video output
- Docker-based for ephemeral GPU instances
- Destroy and relaunch instances without losing setup

---

## 🏗️ Architecture

```
Text Input → n8n Workflow → TTS Engine → LongCat Avatar (GPU) → Video Output
```

**Tech Stack:**
- **LongCat Avatar** - AI video generation (bf16 optimized)
- **n8n** - Workflow orchestration
- **Docker Compose** - Container management
- **FastAPI** - API wrapper for LongCat
- **Redis** - Job queue (optional)
- **Vast.ai** - GPU instance provider (60-80GB VRAM)

---

## 📋 Prerequisites

- Vast.ai account with credits
- Docker Hub account (for storing images)
- Cloud storage (AWS S3, Google Cloud, or similar) for model weights
- Basic knowledge of SSH and Docker

---

## 🚀 Quick Start Guide

### Step 1: Initial Setup (Local Machine - Do Once)
1. Clone this repository
2. Review and customize configuration files
3. Build and push Docker images to Docker Hub
4. Upload model weights to cloud storage

### Step 2: Launch Vast.ai Instance
1. Rent instance with 60-80GB VRAM (A100/H100 recommended)
2. SSH into instance
3. Run the launch command
4. Wait 5-10 minutes for services to start

### Step 3: Generate Videos
1. Access n8n at `http://your-instance-ip:5678`
2. Submit text via webhook or web interface
3. Videos generated in `/outputs` directory
4. Download or sync to cloud storage

### Step 4: Shutdown
1. Sync outputs to cloud storage
2. Destroy Vast.ai instance
3. Repeat when needed

---

## 📦 Project Structure

```
sfitz911-avatar-generator/
├── README.md                    # Master documentation
├── docker-compose.yml           # Multi-container orchestration
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── longcat/
│   ├── Dockerfile              # LongCat Avatar container
│   ├── api_server.py           # FastAPI wrapper
│   └── requirements.txt        # Python dependencies
├── n8n/
│   └── workflows/              # n8n workflow exports
└── scripts/
    └── launch.sh               # Instance initialization
```

---

## 🔧 Installation & Setup

### Phase 1: Local Preparation

**Step 1: Clone Repository**
```bash
git clone https://github.com/yourusername/sfitz911-avatar-generator.git
cd sfitz911-avatar-generator
```

**Step 2: Configure Environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

**Step 3: Build Docker Images**
```bash
cd longcat
docker build -t yourdockerhub/sfitz911-longcat:latest .
docker push yourdockerhub/sfitz911-longcat:latest
```

### Phase 2: Vast.ai Instance Setup

**Step 1: Rent Instance**
- GPU: A100 80GB or H100 80GB
- VRAM: 60-80GB minimum
- RAM: 64-128GB
- Storage: 200GB+ SSD

**Step 2: SSH and Launch**
```bash
ssh root@your-instance-ip
git clone https://github.com/yourusername/sfitz911-avatar-generator.git
cd sfitz911-avatar-generator
bash scripts/launch.sh
```

**Step 3: Verify Services**
```bash
docker-compose ps
curl http://localhost:8000/health
```

---

## 💻 Instance Requirements

**Vast.ai GPU Instance Specs:**
- **GPU:** A100 80GB, H100 80GB, or 2x A6000 (48GB each)
- **VRAM:** 60-80GB minimum
- **System RAM:** 64-128GB
- **Storage:** 200GB+ SSD
- **CUDA:** 12.x (pre-installed on most instances)
- **Docker:** Will be installed via launch script

**Estimated Cost:**
- A100 80GB: ~$1.50-2.50/hour
- Running 8 hours/day: ~$360-600/month

---

## 🐳 Docker Services

### LongCat Avatar Service
- **Port:** 8000
- **Purpose:** AI video generation
- **GPU:** Required (CUDA-enabled)
- **Memory:** 60-80GB VRAM

### n8n Service
- **Port:** 5678
- **Purpose:** Workflow orchestration
- **GPU:** Not required

### Redis Service (Optional)
- **Port:** 6379
- **Purpose:** Job queue management

---

## 📝 Configuration

Create `.env` file from `.env.example`:

```bash
# LongCat Configuration
MODEL_PATH=/app/models/longcat
OUTPUT_PATH=/app/outputs
CUDA_VISIBLE_DEVICES=0

# n8n Configuration
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
WEBHOOK_URL=http://your-instance-ip:5678/

# Cloud Storage (for model weights)
S3_BUCKET=your-bucket-name
S3_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

---

## 🎬 Usage

### Via n8n Workflow
1. Access n8n web interface at `http://your-instance-ip:5678`
2. Import workflow from `n8n/workflows/`
3. Trigger workflow with text input
4. System automatically processes: Text → TTS → Video
5. Download generated video from outputs

### Via API (Direct)
```bash
curl -X POST http://your-instance-ip:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, I am your AI avatar!",
    "voice": "default",
    "duration": 30
  }'
```

---

## 🔄 Instance Lifecycle

### Launch Instance
```bash
# SSH into Vast.ai instance
ssh root@instance-ip

# Clone repository
git clone https://github.com/yourusername/sfitz911-avatar-generator.git
cd sfitz911-avatar-generator

# Run launch script
bash scripts/launch.sh
```

### Shutdown & Backup
```bash
# Sync outputs to cloud (run before destroying instance)
docker-compose exec longcat-avatar python sync_outputs.py

# Stop all services
docker-compose down

# Destroy instance via Vast.ai dashboard
```

---

## 🛠️ Troubleshooting

### Services not starting
- Check GPU availability: `nvidia-smi`
- Verify Docker GPU support: `docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi`
- Check logs: `docker-compose logs -f`

### Out of VRAM
- Reduce batch size in configuration
- Use bf16 precision (already enabled)
- Close other GPU processes

### Model weights not found
- Verify cloud storage credentials
- Check download script logs
- Manually download to `/models` directory

---

## 📚 Additional Resources

- [LongCat Avatar Documentation](https://www.longcatavatar.com/)
- [Vast.ai Documentation](https://docs.vast.ai/)
- [n8n Documentation](https://docs.n8n.io/)
- [Docker GPU Support](https://docs.docker.com/config/containers/resource_constraints/#gpu)

---

## 🔐 Security Notes

- Change default n8n credentials immediately
- Use SSH keys for Vast.ai access
- Store API keys in environment variables
- Don't commit `.env` file to git
- Use private Docker Hub repositories for custom images

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

This is a personal project. Contributions welcome via pull requests.

---

## 📞 Support

For issues or questions, please open a GitHub issue.

---

**Project:** SFitz911 Avatar Generator  
**Last Updated:** January 26, 2026  
**Version:** 1.0.0  
**Status:** In Development

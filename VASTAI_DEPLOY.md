# Deploy to Vast.ai - Simple Guide

## 🚀 Quick Deploy (5-10 Minutes)

### Step 1: Rent Vast.ai Instance

1. Go to https://cloud.vast.ai/
2. Filter for:
   - **GPU**: A100 80GB or H100 (or 2x A6000)
   - **VRAM**: 60GB minimum
   - **RAM**: 64GB minimum
   - **Storage**: 200GB minimum
3. Click **RENT** on a cheap instance
4. Wait for instance to start (shows IP address)

---

### Step 2: SSH into Instance

Copy the SSH command from Vast.ai (looks like this):

```bash
ssh root@123.456.789.0 -p 12345
```

---

### Step 3: Clone Your Repository

```bash
# Clone from GitHub
git clone https://github.com/SFitz911/sfitz911-avatar-generator.git
cd sfitz911-avatar-generator
```

---

### Step 4: Create .env File

```bash
# Copy example
cp .env.example .env

# Edit with nano
nano .env
```

**Minimum required variables:**
```bash
# Docker
DOCKER_USERNAME=sfitz911  # Your Docker Hub username

# AWS S3 (for models)
AWS_ACCESS_KEY_ID=your-key-here
AWS_SECRET_ACCESS_KEY=your-secret-here
S3_BUCKET=your-bucket-name

# n8n
N8N_BASIC_AUTH_PASSWORD=your-secure-password

# TTS (optional)
ELEVENLABS_API_KEY=your-key-here
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

---

### Step 5: Run Launch Script

```bash
# Make script executable
chmod +x scripts/launch.sh

# Run it (installs Docker, NVIDIA toolkit, starts everything)
bash scripts/launch.sh
```

**This will:**
- ✅ Check GPU
- ✅ Install Docker & Docker Compose
- ✅ Install NVIDIA Container Toolkit
- ✅ Download models from S3 (if configured)
- ✅ Build Docker containers (8-10GB, takes 10-15 min)
- ✅ Start all services

**Go get coffee ☕ - this takes 10-15 minutes**

---

### Step 6: Verify Everything Works

After the script finishes:

```bash
# Check services
docker-compose ps

# Test API
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","model_loaded":true,...}
```

---

### Step 7: Get Your Public URL

```bash
# Get your instance IP
curl ifconfig.me
```

Your services are now available at:
- **API**: `http://YOUR-IP:8000`
- **API Docs**: `http://YOUR-IP:8000/docs`
- **n8n**: `http://YOUR-IP:5678`

---

## 🎬 Generate Your First Video

```bash
# Generate test video
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello! This is my first AI avatar video!",
    "duration": 15
  }'

# You'll get back a job_id
# {"job_id":"abc-123-xyz",...}

# Check status
curl http://localhost:8000/status/abc-123-xyz

# Download when complete
curl http://localhost:8000/download/abc-123-xyz -o test-video.mp4
```

---

## 📊 Monitoring

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f longcat-avatar

# Check GPU usage
nvidia-smi

# Watch GPU usage continuously
watch -n 1 nvidia-smi
```

---

## 🛑 Before Destroying Instance

**IMPORTANT**: Backup your videos before destroying the Vast.ai instance!

```bash
# Sync to S3
python3 scripts/sync_outputs.py \
  --provider s3 \
  --bucket your-bucket-name \
  --input ./outputs

# Or download locally via SCP
# From your local machine:
scp -r root@YOUR-IP:/root/sfitz911-avatar-generator/outputs ./backups/
```

---

## 🔧 Troubleshooting

### Services Won't Start

```bash
# Check Docker
docker ps

# Restart everything
docker-compose down
docker-compose up -d --build

# Check logs
docker-compose logs -f
```

### GPU Not Detected

```bash
# Check GPU
nvidia-smi

# Restart Docker
systemctl restart docker

# Verify GPU in Docker
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Out of Memory

```bash
# Edit .env
nano .env

# Set smaller batch size
BATCH_SIZE=1

# Restart
docker-compose restart longcat-avatar
```

---

## 💰 Cost Management

**Estimated Costs:**
- A100 80GB: ~$1.50-2.50/hour
- Running 8 hours: ~$12-20/day

**Tips:**
1. Destroy instance when not in use
2. Use spot instances (cheaper but can be interrupted)
3. Sync outputs before destroying
4. Use smaller models if available

---

## ✅ Success Checklist

- [ ] Vast.ai instance running
- [ ] SSH connected
- [ ] Repository cloned
- [ ] .env configured
- [ ] Launch script completed
- [ ] Services running (`docker-compose ps`)
- [ ] Health check passes
- [ ] Generated test video
- [ ] Can access n8n web UI

---

## 🎉 You're Ready!

Your SFitz Avatar Generator is now running on Vast.ai with:
- ✅ Enhanced API with Redis job tracking
- ✅ Optimized Docker containers
- ✅ Progress tracking
- ✅ TTS integration ready
- ✅ Automatic model downloading
- ✅ Full GPU acceleration

**Generate videos at**: `http://YOUR-IP:8000/docs`

**Have fun! 🚀**

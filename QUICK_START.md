# SFitz911 Avatar Generator - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Vast.ai account with GPU instance
- AWS S3 or Google Cloud Storage (for models)
- Docker & Docker Compose installed

---

## 📋 Setup Checklist

### 1. Configuration (2 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/sfitz911-avatar-generator.git
cd sfitz911-avatar-generator

# Create environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or vim, code, etc.
```

**Required Variables:**
```bash
# Minimum required
DOCKER_USERNAME=your-dockerhub-username
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET=your-bucket-name
ELEVENLABS_API_KEY=your-elevenlabs-key  # if using TTS
```

### 2. Local Build (Optional - 5 minutes)

```bash
# Build and push Docker image
cd longcat
docker build -t your-dockerhub/sfitz911-longcat:latest .
docker push your-dockerhub/sfitz911-longcat:latest
```

### 3. Deploy to Vast.ai (10 minutes)

```bash
# SSH into Vast.ai instance
ssh root@your-vast-instance-ip

# Clone repository
git clone https://github.com/yourusername/sfitz911-avatar-generator.git
cd sfitz911-avatar-generator

# Copy your .env file (or create it)
nano .env

# Run launch script
bash scripts/launch.sh
```

**The launch script will:**
- ✅ Check GPU availability
- ✅ Install Docker & NVIDIA Container Toolkit
- ✅ Download model weights (if configured)
- ✅ Build Docker images
- ✅ Start all services

### 4. Verify Installation (1 minute)

```bash
# Check service status
docker-compose ps

# Test API
curl http://localhost:8000/health

# Test n8n
curl http://localhost:5678
```

---

## 🎬 Generate Your First Video

### Method 1: Direct API Call

```bash
# Generate video from text
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello! I am your AI avatar assistant. This is a test video.",
    "duration": 10,
    "voice": "default",
    "avatar_id": "default"
  }'

# Response will include job_id
# {"job_id": "abc-123-def", "status": "queued", ...}

# Check status
curl http://localhost:8000/status/abc-123-def

# Download video when complete
curl http://localhost:8000/download/abc-123-def -o my-video.mp4
```

### Method 2: Via n8n Webhook

```bash
# Get your instance IP
INSTANCE_IP=$(curl -s ifconfig.me)

# Trigger workflow
curl -X POST http://$INSTANCE_IP:5678/webhook/generate-avatar \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello from n8n!",
    "duration": 15
  }'
```

### Method 3: n8n Web Interface

1. Open browser: `http://your-instance-ip:5678`
2. Login (default: admin / check your .env)
3. Import workflow: `n8n/workflows/text-to-avatar.json`
4. Activate workflow
5. Test with webhook URL

---

## 📊 Monitoring & Management

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f longcat-avatar
docker-compose logs -f n8n
docker-compose logs -f redis
```

### Check GPU Usage

```bash
# On host
nvidia-smi

# In container
docker exec sfitz911-longcat nvidia-smi
```

### List Generated Videos

```bash
# Via API
curl http://localhost:8000/list

# Via filesystem
ls -lh outputs/
```

---

## 🔄 Common Operations

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart longcat-avatar
```

### Update Code

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Backup Outputs

```bash
# Sync to S3 (before destroying instance)
python scripts/sync_outputs.py \
  --provider s3 \
  --bucket your-bucket \
  --input ./outputs
```

### Clean Up

```bash
# Stop services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v

# Remove old videos
rm outputs/*.mp4
```

---

## 🐛 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs longcat-avatar

# Check GPU access
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

# Restart Docker
sudo systemctl restart docker
docker-compose up -d
```

### Model Not Found

```bash
# Download models manually
python scripts/download_models.py \
  --provider s3 \
  --bucket your-bucket \
  --prefix models/longcat/ \
  --output ./models/longcat

# Or mount from host
# Edit docker-compose.yml volumes section
```

### Out of Memory

```bash
# Check GPU memory
nvidia-smi

# Reduce batch size in .env
BATCH_SIZE=1

# Restart service
docker-compose restart longcat-avatar
```

### Redis Connection Failed

```bash
# Check Redis status
docker-compose ps redis

# Restart Redis
docker-compose restart redis

# Check Redis logs
docker-compose logs redis
```

---

## 📈 Performance Tips

### Optimize for Speed

```env
# In .env file
BATCH_SIZE=1  # Reduce for lower memory usage
VIDEO_FPS=24  # Lower FPS = faster generation
VIDEO_RESOLUTION=720p  # Use 720p instead of 1080p
```

### Optimize for Quality

```env
BATCH_SIZE=2  # Increase if you have VRAM
VIDEO_FPS=30  # Standard quality
VIDEO_RESOLUTION=1080p  # Higher quality
```

### Cost Optimization

1. **Use spot instances** on Vast.ai (cheaper)
2. **Batch process** multiple videos at once
3. **Sync and destroy** instance when not in use
4. **Use smaller models** if available
5. **Compress videos** after generation

---

## 🔐 Security Best Practices

### Before Going Public

```bash
# Change default passwords
N8N_BASIC_AUTH_PASSWORD=your-secure-password

# Add API authentication
API_SECRET_KEY=$(openssl rand -hex 32)

# Restrict CORS
CORS_ORIGINS=https://yourdomain.com

# Use HTTPS (add nginx reverse proxy)
```

### Protect Your Credentials

```bash
# Never commit .env
git status  # Should not show .env

# Use environment-specific configs
cp .env .env.production
cp .env .env.development
```

---

## 📞 Getting Help

### Check Documentation

- Main README: `README.md`
- Improvements: `IMPROVEMENTS.md`
- n8n Workflows: `n8n/workflows/README.md`

### Debug Mode

```bash
# Enable debug logging
LOG_LEVEL=DEBUG docker-compose up

# Check API documentation
open http://localhost:8000/docs
```

### Common Issues

| Issue | Solution |
|-------|----------|
| GPU not detected | Install NVIDIA drivers, restart Docker |
| Model not loading | Check MODEL_PATH, download models |
| Out of VRAM | Reduce BATCH_SIZE, close other processes |
| Redis timeout | Increase REDIS_TIMEOUT, check network |
| n8n not accessible | Check firewall, use correct IP |

---

## 🎯 Next Steps

Once you have the basic setup working:

1. **Customize Avatars**: Add your own avatar models
2. **Enhance Workflows**: Create complex n8n workflows
3. **Add Features**: Implement custom TTS, post-processing
4. **Scale Up**: Deploy to multiple instances
5. **Monitor**: Add Prometheus/Grafana monitoring
6. **Automate**: Create CI/CD pipelines

---

## 📚 Useful Commands Reference

```bash
# Service Management
docker-compose up -d              # Start services
docker-compose down               # Stop services
docker-compose restart            # Restart all
docker-compose ps                 # Check status
docker-compose logs -f            # View logs

# API Testing
curl http://localhost:8000/health           # Health check
curl http://localhost:8000/list             # List videos
curl http://localhost:8000/docs             # API docs

# Maintenance
docker system prune -a            # Clean up Docker
df -h                             # Check disk space
nvidia-smi                        # Check GPU
htop                              # Check CPU/RAM

# Backup & Sync
python scripts/sync_outputs.py    # Sync to cloud
tar -czf backup.tar.gz outputs/   # Local backup
```

---

**Happy Generating! 🎬**

For more details, see `README.md` and `IMPROVEMENTS.md`

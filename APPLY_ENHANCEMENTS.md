# Apply Enhancements - Step by Step Guide

## 🎯 Goal
Replace your original API server and Dockerfile with the enhanced versions.

---

## ✅ Prerequisites
- PowerShell open in project directory: `C:\Projects\sfitz911-avatar-generator`
- Docker Desktop running (if testing locally)

---

## 📋 Step-by-Step Instructions

### Step 1: Backup Original Files (Safety First!)

```powershell
# Create backups directory
New-Item -ItemType Directory -Force -Path ".\backups"

# Backup original files
Copy-Item ".\longcat\api_server.py" ".\backups\api_server.py.backup"
Copy-Item ".\longcat\Dockerfile" ".\backups\Dockerfile.backup"
Copy-Item ".\docker-compose.yml" ".\backups\docker-compose.yml.backup"

Write-Host "✅ Backups created in .\backups\" -ForegroundColor Green
```

### Step 2: Apply Enhanced API Server

```powershell
# Replace old api_server.py with enhanced version
Move-Item -Force ".\longcat\api_server_enhanced.py" ".\longcat\api_server.py"

Write-Host "✅ Enhanced API server applied" -ForegroundColor Green
```

### Step 3: Apply Optimized Dockerfile

```powershell
# Replace old Dockerfile with optimized version
Move-Item -Force ".\longcat\Dockerfile.optimized" ".\longcat\Dockerfile"

Write-Host "✅ Optimized Dockerfile applied" -ForegroundColor Green
```

### Step 4: Make Entrypoint Script Executable (If on Linux/Vast.ai)

**On Windows (for now):** Skip this step

**Later on Vast.ai/Linux:**
```bash
chmod +x longcat/entrypoint.sh
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

### Step 5: Verify Changes

```powershell
# Check that new files are in place
Get-ChildItem ".\longcat" | Select-Object Name, Length, LastWriteTime

# You should see:
# - api_server.py (newer timestamp, larger size ~650+ lines)
# - Dockerfile (newer timestamp)
# - entrypoint.sh (new file)
```

---

## 🚀 Testing Locally (Optional)

If you want to test on your local machine before deploying to Vast.ai:

### Option A: Test Without GPU (Limited)

```powershell
# Remove GPU requirements temporarily
# Edit docker-compose.yml and comment out these lines:
#   runtime: nvidia
#   deploy:
#     resources:
#       reservations:
#         devices: ...

# Then start services
docker-compose up -d

# Check logs
docker-compose logs -f longcat-avatar
```

### Option B: Skip Local Testing

Just deploy directly to Vast.ai where you have a GPU!

---

## 🌩️ Deploy to Vast.ai

### Step 1: Commit Changes to Git

```powershell
# Add all changes
git add .

# Commit
git commit -m "Applied enhanced API server and optimized Dockerfile"

# Push to GitHub
git push origin main
```

### Step 2: SSH into Vast.ai Instance

```powershell
# Replace with your actual Vast.ai IP
ssh root@your-vast-instance-ip
```

### Step 3: Update Code on Vast.ai

```bash
# Navigate to project
cd sfitz911-avatar-generator

# Pull latest changes
git pull origin main

# Make scripts executable
chmod +x longcat/entrypoint.sh
chmod +x scripts/*.sh
chmod +x scripts/*.py

# Stop existing services
docker-compose down

# Rebuild with new code
docker-compose up -d --build

# Watch the logs
docker-compose logs -f
```

### Step 4: Test the Enhanced API

```bash
# Wait a minute for services to start, then test

# Health check
curl http://localhost:8000/health

# Generate a test video
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Testing the enhanced API server!",
    "duration": 10
  }'

# You should get a response with a job_id
# Copy the job_id from the response

# Check status (replace JOB_ID with actual ID)
curl http://localhost:8000/status/JOB_ID

# List all videos
curl http://localhost:8000/list
```

---

## 🎉 Success Checklist

- [ ] Backed up original files
- [ ] Applied enhanced API server
- [ ] Applied optimized Dockerfile
- [ ] Committed changes to Git
- [ ] Deployed to Vast.ai
- [ ] Services started successfully
- [ ] Health check returns `"status": "healthy"`
- [ ] Can generate test video
- [ ] Can check job status
- [ ] Can list videos

---

## 🐛 Troubleshooting

### Issue: "Cannot find api_server_enhanced.py"

**Solution:** The file should already exist. Check:
```powershell
Get-ChildItem ".\longcat\api_server_enhanced.py"
```

If missing, I can recreate it for you.

---

### Issue: Docker build fails

**Solution:** Check the logs:
```powershell
docker-compose logs longcat-avatar
```

Common fixes:
- Ensure you're connected to internet (for downloading packages)
- Ensure Docker has enough disk space
- Try: `docker system prune -a` to clean up

---

### Issue: "File is being used by another process"

**Solution:** Stop Docker first:
```powershell
docker-compose down
# Then try the file operations again
```

---

### Issue: Can't connect to Vast.ai

**Solution:**
- Check instance is running in Vast.ai dashboard
- Verify IP address is correct
- Ensure SSH port (22) is open

---

## 🔄 Rollback (If Needed)

If something goes wrong, restore from backups:

```powershell
# Stop services
docker-compose down

# Restore backups
Copy-Item -Force ".\backups\api_server.py.backup" ".\longcat\api_server.py"
Copy-Item -Force ".\backups\Dockerfile.backup" ".\longcat\Dockerfile"
Copy-Item -Force ".\backups\docker-compose.yml.backup" ".\docker-compose.yml"

# Restart
docker-compose up -d --build
```

---

## 📞 Need Help?

If you get stuck:
1. Check the logs: `docker-compose logs -f`
2. Verify files exist: `Get-ChildItem .\longcat`
3. Check Docker status: `docker-compose ps`

Let me know what error you see and I can help troubleshoot!

---

**Ready to apply the enhancements?**

Start with **Step 1** above and work through each step. Take your time!

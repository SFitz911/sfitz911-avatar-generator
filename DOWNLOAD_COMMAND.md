# 📥 Download All Videos Command

## Quick Download (Desktop PowerShell)

```powershell
# Navigate to project directory
e:
cd Avatar-Generator\sfitz911-avatar-generator

# Download all videos
.\scripts\download_videos.ps1
```

## What Gets Downloaded:

1. **LTX-2 Generated Videos**
   - Location: `/workspace/LTX-2/*.mp4`
   - Includes test videos, demos, training outputs

2. **API Output Videos**
   - Location: `/workspace/sfitz911-avatar-generator/outputs/*.mp4`
   - Includes all chat-generated avatar videos

3. **All Downloaded to:**
   - `E:\DATA_1TB\Desktop\Ai-Gen-Clips\`

## Manual Download Command

If you want to download specific folders:

```powershell
e:
cd Avatar-Generator\sfitz911-avatar-generator

# Download all videos from LTX-2 folder
scp -P 40106 -i agent_key root@173.207.82.240:/workspace/LTX-2/*.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\

# Download all videos from outputs folder
scp -P 40106 -i agent_key root@173.207.82.240:/workspace/sfitz911-avatar-generator/outputs/*.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\

# Download training photos
scp -P 40106 -i agent_key -r root@173.207.82.240:/workspace/LTX-2/avatar_clean E:\DATA_1TB\Desktop\Ai-Gen-Clips\training_photos\
```

## Download Everything (Including Training Data)

```powershell
e:
cd Avatar-Generator\sfitz911-avatar-generator

# Create backup folder
New-Item -ItemType Directory -Path "E:\DATA_1TB\Desktop\Ai-Gen-Clips\backup_$(Get-Date -Format 'yyyy-MM-dd_HHmm')" -Force

# Download all videos
scp -P 40106 -i agent_key root@173.207.82.240:/workspace/LTX-2/*.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\
scp -P 40106 -i agent_key root@173.207.82.240:/workspace/sfitz911-avatar-generator/outputs/*.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\

# Download training photos
scp -P 40106 -i agent_key -r root@173.207.82.240:/workspace/LTX-2/avatar_clean E:\DATA_1TB\Desktop\Ai-Gen-Clips\training_photos\

# Download training logs
scp -P 40106 -i agent_key -r root@173.207.82.240:/workspace/sfitz911-avatar-generator/outputs/training_logs E:\DATA_1TB\Desktop\Ai-Gen-Clips\training_logs\
```

## Auto-Sync (Continuous Download)

Use the auto-sync script to continuously monitor and download new videos:

```powershell
.\scripts\auto_sync_videos.ps1
```

This will check every 30 seconds and download any new videos automatically.

## Check What's on the Server

Before downloading, check what's available:

```powershell
ssh -p 40106 -i agent_key root@173.207.82.240 "ls -lh /workspace/LTX-2/*.mp4 /workspace/sfitz911-avatar-generator/outputs/*.mp4"
```

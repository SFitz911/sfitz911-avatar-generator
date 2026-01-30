# 🚀 Quick Reference Card
**SFitz911 Avatar Generator - Emergency Cheat Sheet**

Last Updated: January 30, 2026

---

## 🎯 Launch New Instance (20-30 min)

```bash
# 1. Rent H100 80GB on Vast.ai (~$1.50-2.50/hour)

# 2. SSH in:
ssh -p PORT root@INSTANCE_IP

# 3. Setup (one command):
cd /workspace && \
git clone https://github.com/SFitz911/sfitz911-avatar-generator.git && \
git clone https://github.com/Lightricks/LTX-2.git && \
cd sfitz911-avatar-generator && \
bash scripts/complete_ltx2_setup.sh

# 4. If Gemma fails (needs HF auth):
huggingface-cli login  # Paste token

# 5. Launch services:
bash scripts/launch_ltx2.sh
```

---

## 🔌 Access from Local Machine

```powershell
# PowerShell (Windows):
cd e:\Avatar-Generator\sfitz911-avatar-generator
ssh -p PORT -i agent_key -L 8501:localhost:8501 -L 8000:localhost:8000 root@INSTANCE_IP
```

**Then open:** http://localhost:8501

---

## ⚡ Common Commands

```bash
# Restart services
pkill -f streamlit; pkill -f api_server
bash scripts/launch_ltx2.sh

# Update code
cd /workspace/sfitz911-avatar-generator
git pull origin main

# Check GPU
nvidia-smi

# Check API health
curl http://localhost:8000/health

# View logs
tail -f /workspace/sfitz911-avatar-generator/ltx2/api.log
```

---

## 📥 Download Videos

```powershell
# All videos:
scp -P PORT -i agent_key -r root@INSTANCE_IP:/workspace/sfitz911-avatar-generator/outputs/*.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\

# Single video:
scp -P PORT -i agent_key root@INSTANCE_IP:/workspace/sfitz911-avatar-generator/outputs/VIDEO.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\
```

---

## 🎨 Best Settings for Face Consistency

```
✅ Image Strength: 1.8-2.0 (higher = more stable)
✅ Train face: 5-10 photos
✅ Video duration: 5-10 seconds
✅ Use Fresh Start Mode: Clear old training
✅ Frame rate: 24fps (default)
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Gemma 401 error | `huggingface-cli login` + paste token |
| Face morphing | Increase image strength to 1.9-2.0 |
| Services crashed | `pkill -f streamlit; bash scripts/launch_ltx2.sh` |
| Out of VRAM | Use shorter videos (5-10s), close other processes |
| Can't access UI | Check SSH tunnel is running with `-L 8501:localhost:8501` |

---

## 📂 Key Paths

```
/workspace/LTX-2/                           # AI Model
/workspace/LTX-2/models/                    # Model files (~40GB)
/workspace/LTX-2/.venv/bin/python           # Python interpreter
/workspace/sfitz911-avatar-generator/       # App code
/workspace/sfitz911-avatar-generator/outputs/   # Generated videos
/workspace/sfitz911-avatar-generator/temp/      # Uploaded images
```

---

## 📚 Full Documentation

- **[README.md](README.md)** - Complete guide
- **[PRODUCTION_READY_CHECKLIST.md](PRODUCTION_READY_CHECKLIST.md)** - Launch verification
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
- **[docs/FACE_CONSISTENCY_GUIDE.md](docs/FACE_CONSISTENCY_GUIDE.md)** - Face morphing fixes
- **[docs/QUALITY_TIPS.md](docs/QUALITY_TIPS.md)** - Quality improvements

---

## 🎯 Typical Workflow

```
1. Rent instance → Setup (20-30 min first time)
2. Launch services → Access UI
3. Generate videos → Download to local
4. Destroy instance → Only pay for usage
5. Repeat when needed (2-3 min restart)
```

---

## ⏱️ Performance (H100 80GB)

| Task | Time |
|------|------|
| Setup (first time) | 20-30 min |
| Setup (cached) | 2-3 min |
| Service start | 10 sec |
| First generation | 45 sec |
| Later generations | 30 sec |
| Face training | 10 sec |

---

## 💾 What to Backup

```
✅ Download: Generated videos (outputs/*.mp4)
✅ In GitHub: All code, scripts, documentation
✅ Cached by Vast.ai: Model files
❌ No backup needed: Training logs, temp files
```

---

## 🚨 Emergency Reset

```bash
# Via UI: Scroll to "Danger Zone" → Master Reset

# Via API:
curl -X POST http://localhost:8000/master-reset

# Manual:
rm -rf /workspace/LTX-2/avatar_clean
rm -rf /workspace/sfitz911-avatar-generator/outputs/*
rm -rf /workspace/sfitz911-avatar-generator/temp/*
```

---

## 📞 Need Help?

1. Check **[PRODUCTION_READY_CHECKLIST.md](PRODUCTION_READY_CHECKLIST.md)** troubleshooting section
2. Review **[docs/FACE_CONSISTENCY_GUIDE.md](docs/FACE_CONSISTENCY_GUIDE.md)** for face issues
3. Open GitHub issue: https://github.com/SFitz911/sfitz911-avatar-generator/issues

---

**Status:** ✅ Production Ready  
**Version:** 2.0.0 (LTX-2)  
**Last Updated:** January 30, 2026

**Sleep tight! Everything's documented and ready to go.** 😴

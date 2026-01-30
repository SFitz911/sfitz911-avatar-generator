# Download Videos to Your Computer

All generated videos are saved on your H100 instance. Here's how to get them to your local computer at `E:\DATA_1TB\Desktop\Ai-Gen-Clips`.

---

## 🎯 Quick Download (One-Time)

**In Desktop PowerShell:**

```powershell
cd e:\Avatar-Generator\sfitz911-avatar-generator
.\scripts\download_videos.ps1
```

This downloads all videos from your H100 to `E:\DATA_1TB\Desktop\Ai-Gen-Clips`.

---

## 🔄 Auto-Sync (Continuous)

Keep videos automatically synced while you work:

**In Desktop PowerShell:**

```powershell
cd e:\Avatar-Generator\sfitz911-avatar-generator
.\scripts\auto_sync_videos.ps1
```

This checks every 30 seconds for new videos and downloads them automatically.

Press `Ctrl+C` to stop.

---

## 📥 Manual Download (Single File)

To download a specific video:

**Desktop PowerShell:**
```powershell
# Download Maya's intro
scp -P 40106 -i agent_key root@173.207.82.240:/workspace/LTX-2/maya_intro.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\

# Download from outputs folder
scp -P 40106 -i agent_key root@173.207.82.240:/workspace/sfitz911-avatar-generator/outputs/VIDEO_NAME.mp4 E:\DATA_1TB\Desktop\Ai-Gen-Clips\
```

---

## 🌐 Browser Download (via HTTP)

### Step 1: Start file server in VAST Terminal
```bash
cd /workspace/LTX-2
python3 -m http.server 7777
```

### Step 2: Open in browser
```
http://localhost:7777/maya_intro.mp4
```

Right-click → Save As → `E:\DATA_1TB\Desktop\Ai-Gen-Clips\`

---

## 🤖 Automatic Download After Generation

Want videos to auto-download after each generation? Add this to the API server:

```python
# After video generation completes
subprocess.run([
    "scp", "-P", "40106", "-i", "agent_key",
    f"root@173.207.82.240:{video_path}",
    "E:\\DATA_1TB\\Desktop\\Ai-Gen-Clips\\"
])
```

---

## 📊 Check What's Downloaded

**Desktop PowerShell:**
```powershell
Get-ChildItem E:\DATA_1TB\Desktop\Ai-Gen-Clips -Filter *.mp4 | Sort-Object LastWriteTime -Descending | Select-Object Name, Length, LastWriteTime
```

---

**Once Maya's video finishes, run `.\scripts\download_videos.ps1` to grab it!** 📥

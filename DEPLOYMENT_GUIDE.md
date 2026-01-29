# SFitz911 Avatar Generator - Complete Deployment Guide

## 🎯 System Overview

A full-featured AI Avatar Chat System with:
- 💬 **Chat Interface** with LLM (ChatGPT/Claude)
- 🌍 **12 Languages** (including Hindi)
- 🖼️ **Custom Avatar Images** (drag-and-drop)
- 🎬 **HD Video Generation** (720p, 30fps)
- 🚀 **Optimized for H100/H200** (80-140GB VRAM)

---

## 📋 Prerequisites

### Vast.ai Instance Requirements
- **GPU:** H100 (80GB) or H200 (141GB) - REQUIRED
- **Storage:** 600GB+ SSD
- **Network:** Fast (for 129GB model download)

### API Keys Needed
1. **Vast.ai API Key** (for instance management)
2. **OpenAI API Key** (for LLM chat - optional if using direct mode)
3. **ElevenLabs API Key** (for high-quality TTS - optional)

---

## 🚀 Quick Start (10 Minutes to Live System)

### Step 1: Rent H100/H200 Instance
1. Go to [Vast.ai Console](https://console.vast.ai/)
2. Filter for:
   - VRAM: 80GB+ (H100 or H200)
   - Storage: 600GB+
   - Verified hosts only
3. Click "Rent"
4. Add your SSH key via the UI

### Step 2: Connect to Instance
From your local computer (in project folder):

**PowerShell Desktop:**
```powershell
e:
cd Avatar-Generator\sfitz911-avatar-generator
ssh -p [PORT] -i agent_key root@ssh[N].vast.ai -L 8000:localhost:8000 -L 5678:localhost:5678 -L 8501:localhost:8501
```

### Step 3: One-Click Setup
In the **VAST Terminal** (SSH session):

```bash
cd /workspace
git clone https://github.com/SFitz911/sfitz911-avatar-generator.git
cd sfitz911-avatar-generator
bash scripts/vast_setup.sh
```

**What it does:**
- ✅ Installs system dependencies (git, ffmpeg, nodejs)
- ✅ Installs Python AI libraries (torch, diffusers, transformers)
- ✅ Clones official LongCat code
- ✅ Downloads 129GB of AI models (takes 15-30 mins)
- ✅ Fixes dependency conflicts automatically
- ✅ Patches code for memory optimization

**Coffee break!** ☕ (The model download takes time, but it's fully automatic)

### Step 4: Launch Services
Once `vast_setup.sh` completes, start everything:

**VAST Terminal:**
```bash
bash scripts/launch_native.sh
```

This starts:
- 🔥 FastAPI (Port 8000) - Backend API
- 🤖 n8n (Port 5678) - Workflow Orchestrator
- 🎨 Streamlit (Port 8501) - Chat Interface

### Step 5: Access the Interface
Open your browser on your **local computer**:
```
http://localhost:8501
```

You should see the chat interface with:
- Language selector (including Hindi 🇮🇳)
- Image upload zone
- Chat box

---

## 💡 How to Use

### Basic Chat (Text-Only Mode)
1. Type a message in the chat box
2. Press Enter
3. The AI responds with text (via n8n → OpenAI)
4. The avatar speaks the response in a video

### Image-Driven Mode (Best Quality)
1. **Upload Your Photo** in the sidebar
2. Type your message
3. The AI generates a response
4. **Your face** speaks the AI's response

### Language Selection
1. Choose language from dropdown (e.g., "Hindi")
2. The AI will respond in Hindi
3. The TTS will speak in Hindi
4. The avatar lip-syncs to Hindi phonemes

---

## 🔧 Advanced Configuration

### Enable OpenAI Chat (LLM Brain)
1. Get OpenAI API key from [platform.openai.com](https://platform.openai.com)
2. Access n8n at `http://localhost:5678`
3. Import workflow: `n8n/workflows/chat-to-avatar.json`
4. Add OpenAI credentials in n8n settings
5. Activate the workflow

### Enable ElevenLabs (Premium TTS)
1. Get API key from [elevenlabs.io](https://elevenlabs.io)
2. Edit `.env` file:
   ```bash
   ELEVENLABS_API_KEY=your_key_here
   ```
3. Restart services

### Customize Avatar Prompt
In the Streamlit sidebar, you can edit the "System Prompt" to change the AI's personality:
```
You are a professional business coach. Respond in Hindi with formal language.
```

---

## 🎬 Video Generation Modes

### 1. ATI2V (Audio+Text+Image) - RECOMMENDED
- **Best Quality**: Uses your uploaded photo
- **No Degradation**: Locks face identity for long videos
- **Realistic**: Preserves facial features accurately

### 2. AT2V (Audio+Text Only)
- **Generic Avatar**: Uses default sample avatar
- **Faster**: No need to upload image each time
- **Lower Consistency**: Face may drift in long videos

---

## 📊 Performance Expectations

### H200 (141GB VRAM)
- **Video Generation:** ~30-60 seconds for 30-second video
- **Concurrent Jobs:** 2-3 simultaneous generations
- **Resolution:** Native 720p @ 30fps

### H100 (80GB VRAM)
- **Video Generation:** ~45-90 seconds for 30-second video
- **Concurrent Jobs:** 1-2 simultaneous generations
- **Resolution:** Native 720p @ 30fps

---

## 🛠️ Troubleshooting

### Frontend Not Loading
```bash
# Check if port is in use
lsof -i :8501

# Restart frontend
cd frontend
streamlit run app.py
```

### Video Generation Stuck
```bash
# Check GPU usage
nvidia-smi

# Check API logs
tail -f longcat/api.log
```

### Out of Memory (Even on H100)
This shouldn't happen with the patched code, but if it does:
```bash
# Verify patch was applied
grep "# self.text_encoder" longcat_core/longcat_video/pipeline_longcat_video_avatar.py
```

### N8n Workflow Not Working
1. Access n8n: `http://localhost:5678`
2. Default credentials: `admin` / `changeme`
3. Import `chat-to-avatar.json`
4. Add OpenAI credentials
5. Activate workflow

---

## 💰 Cost Optimization

### Running Costs (H200 @ $2.90/hr)
- **8 hours/day:** ~$23/day (~$700/month)
- **4 hours/day:** ~$12/day (~$360/month)

### Save Money Strategy
1. **Use Instance Pause**: Stop instance when not in use (keeps data, stops billing)
2. **Batch Processing**: Generate multiple videos in one session
3. **Optimize Duration**: Shorter videos = faster generation = less GPU time

---

## 🔐 Security Checklist

Before going live:
- [ ] Change n8n password (default: `changeme`)
- [ ] Add authentication to Streamlit (use `streamlit-authenticator`)
- [ ] Use HTTPS for production (add nginx reverse proxy)
- [ ] Restrict CORS origins in `api_server_enhanced.py`
- [ ] Store API keys in environment variables (never in code)

---

## 📝 Next Steps

### To Make it Production-Ready:
1. **Add Authentication**: Use `streamlit-authenticator` for user login
2. **Add Database**: Store chat history (SQLite or PostgreSQL)
3. **Add Video Storage**: Save videos to S3/R2 for persistence
4. **Add Rate Limiting**: Prevent abuse (use Redis + rate-limit middleware)
5. **Add Monitoring**: Set up logging and alerts

### To Improve Quality:
1. **Fine-tune Prompts**: Experiment with different system prompts
2. **Custom Voices**: Clone your voice with ElevenLabs
3. **Multi-Avatar**: Support multiple character images
4. **Emotion Control**: Add emotion/expression parameters

---

## 🆘 Support

If you encounter issues:
1. Check the logs in each service
2. Verify all ports are accessible via `curl`
3. Test components individually (API, n8n, frontend)

---

**Built for H100/H200 | Optimized for Speed | Ready for Production**

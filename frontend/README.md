# Avatar Chat Interface

Beautiful web interface for chatting with AI-powered video avatars.

## Features

- 💬 **Chat Interface**: Natural conversation with AI
- 🌍 **12 Languages**: English, Spanish, French, German, Italian, Portuguese, Hindi, Mandarin, Japanese, Korean, Russian, Arabic
- 🖼️ **Image Upload**: Drag-and-drop your avatar photo for personalized videos
- 🎙️ **Voice Selection**: Choose from multiple TTS providers
- 📺 **Video Output**: Watch your avatar respond in real-time
- 📥 **Download**: Save all generated videos

## Quick Start

### Option 1: Docker (Recommended)
The frontend is automatically included when you run:
```bash
docker-compose up -d
```

Access at: `http://localhost:8501`

### Option 2: Standalone (Development)
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## Usage Guide

1. **Upload Avatar Image** (Sidebar):
   - Click "Browse files" or drag-and-drop
   - Supported formats: PNG, JPG
   - For best quality, use a high-resolution front-facing photo

2. **Configure Language** (Sidebar):
   - Select your preferred language from the dropdown
   - The AI will respond in that language

3. **Chat**:
   - Type your message in the chat box at the bottom
   - Press Enter
   - Wait for the AI to think and generate the video response

4. **Download Videos**:
   - All generated videos appear in the "Download Videos" section at the bottom
   - Click the download button to save locally

## Architecture

```
User Input → Streamlit Frontend → n8n Workflow → OpenAI (LLM) → Response Text
                                                                        ↓
User Browser ← Video Display ← FastAPI Backend ← LongCat AI ← TTS Audio
```

## Configuration

Set these environment variables in `docker-compose.yml`:

- `API_URL`: URL of the LongCat API (default: `http://longcat-avatar:8000`)
- `N8N_URL`: URL of n8n (default: `http://n8n:5678`)

## Supported Languages

The system supports the following languages for both AI responses and avatar speech:

- 🇺🇸 English
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German
- 🇮🇹 Italian
- 🇵🇹 Portuguese
- 🇮🇳 Hindi
- 🇨🇳 Mandarin Chinese
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇷🇺 Russian
- 🇸🇦 Arabic

## Tips for Best Results

1. **Image Quality**: Use a clear, well-lit, front-facing photo (no sunglasses or obstructions)
2. **Resolution**: 720p provides the best balance of quality and speed
3. **Language**: The avatar automatically lip-syncs to any language
4. **Duration**: Keep responses under 60 seconds for optimal quality

## Troubleshooting

### Frontend won't load
- Check Docker logs: `docker-compose logs frontend`
- Verify port 8501 is not in use: `lsof -i :8501`

### Video generation fails
- Check API health: `curl http://localhost:8000/health`
- Verify H200 instance is running with enough VRAM
- Check logs: `docker-compose logs longcat-avatar`

### Language not working
- Verify n8n has OpenAI credentials configured
- Check the n8n workflow is active

## Development

To modify the interface:

1. Edit `frontend/app.py`
2. Rebuild container: `docker-compose build frontend`
3. Restart: `docker-compose restart frontend`

Or run in dev mode with auto-reload:
```bash
streamlit run app.py --server.runOnSave true
```

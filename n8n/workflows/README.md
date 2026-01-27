# n8n Workflows

This directory contains n8n workflow templates for the SFitz911 Avatar Generator.

## Available Workflows

### 1. Text to Avatar Video (`text-to-avatar.json`)

**Purpose:** Convert text input to avatar video via webhook

**Workflow:**
1. Webhook receives POST request with text
2. Process and validate input
3. Call LongCat API to generate video
4. Return job ID and status

**Usage:**
```bash
curl -X POST http://your-instance:5678/webhook/generate-avatar \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, I am your AI avatar!",
    "voice": "default",
    "duration": 30
  }'
```

## Importing Workflows

1. Access n8n at `http://your-instance-ip:5678`
2. Click "Workflows" → "Import from File"
3. Select the JSON file from this directory
4. Activate the workflow

## Creating Custom Workflows

You can extend these workflows with:
- **TTS Integration:** Add ElevenLabs, Azure Speech, or Google TTS nodes
- **Storage:** Add S3 or Google Cloud Storage nodes to save outputs
- **Notifications:** Add Slack, Discord, or email notifications
- **Queue Management:** Add Redis queue for batch processing
- **Post-Processing:** Add video editing or compression steps

## Workflow Variables

Configure these in your n8n environment:
- `LONGCAT_API_URL` - LongCat API endpoint (default: http://longcat-avatar:8000)
- `ELEVENLABS_API_KEY` - ElevenLabs API key for TTS
- `S3_BUCKET` - S3 bucket for output storage

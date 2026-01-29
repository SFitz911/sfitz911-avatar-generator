#!/bin/bash
set -e

# SFitz911 Avatar Generator - Vast.ai Native Setup Script
# Run this on a fresh Vast.ai instance to install everything automatically.

echo "=================================================="
echo "🚀 Starting SFitz911 Avatar Generator Setup"
echo "=================================================="

# 1. Install System Dependencies (ffmpeg, nodejs for n8n, git)
echo "📦 Step 1: Installing System Dependencies..."
apt-get update && apt-get install -y git ffmpeg nodejs npm python3-pip python3-venv

# 2. Configure Python Environment
echo "🐍 Step 2: Installing Python Libraries..."
python3 -m pip install --upgrade pip
# Force upgrade huggingface_hub to ensure we have the latest tools
pip install huggingface_hub[cli] -U
pip install -r requirements.txt

# 3. Download Models (Using Python script for reliability)
echo "⬇️  Step 3: Downloading AI Models (129GB)..."
cat <<EOF > download_models_temp.py
from huggingface_hub import snapshot_download
import os

print("   -> Downloading LongCat-Video-Avatar...")
snapshot_download(
    repo_id="meituan-longcat/LongCat-Video-Avatar", 
    local_dir="./weights/LongCat-Video-Avatar", 
    local_dir_use_symlinks=False, 
    ignore_patterns=["*.git*"]
)

print("   -> Downloading LongCat-Video...")
snapshot_download(
    repo_id="meituan-longcat/LongCat-Video", 
    local_dir="./weights/LongCat-Video", 
    local_dir_use_symlinks=False, 
    ignore_patterns=["*.git*"]
)
print("   -> Download Complete!")
EOF

python3 download_models_temp.py
rm download_models_temp.py

# 4. Install n8n
echo "🤖 Step 4: Installing n8n..."
npm install -g n8n

echo "=================================================="
echo "✅ Setup Complete!"
echo "You can now start the services:"
echo "1. Start API: python3 api_server.py"
echo "2. Start n8n: npx n8n start --tunnel"
echo "=================================================="

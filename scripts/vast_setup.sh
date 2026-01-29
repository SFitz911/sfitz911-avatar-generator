#!/bin/bash
set -e

echo "=================================================="
echo "🚀 Starting SFitz911 Avatar Generator Setup (H100 Optimized)"
echo "=================================================="

# 1. Install System Dependencies
echo "📦 Step 1: Installing System Dependencies..."
apt-get update && apt-get install -y git ffmpeg nodejs npm python3-pip python3-venv libsndfile1

# 2. Configure Python Environment
echo "🐍 Step 2: Configure Python..."
python3 -m pip install --upgrade pip
pip install huggingface_hub[cli] -U

# 3. Clone Official LongCat Repo (The "Brain")
echo "🧠 Step 3: Cloning LongCat Core..."
if [ ! -d "longcat_core" ]; then
    git clone https://github.com/meituan-longcat/LongCat-Video.git longcat_core
fi

# 4. Fix Dependency Conflicts (The "Dependency Hell" Fixes)
echo "🔧 Step 4: Patching Requirements..."
# Remove system libs that shouldn't be in pip
sed -i '/libsndfile1/d' longcat_core/requirements_avatar.txt
# Remove broken/missing packages
sed -i '/tritonserverclient/d' longcat_core/requirements_avatar.txt
# Remove flash-attn to install it manually
sed -i '/flash-attn/d' longcat_core/requirements.txt

# 5. Install PyTorch & AI Libraries
echo "🔥 Step 5: Installing AI Libraries..."
# Force install compatible Torch first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Try to build Flash Attention (Speed boost for H100)
echo "   -> Building Flash Attention (This takes a minute)..."
pip install flash-attn --no-build-isolation || echo "⚠️ Flash Attention build failed, continuing (it's optional)..."

# Install remaining dependencies
pip install -r longcat_core/requirements.txt
pip install -r longcat_core/requirements_avatar.txt
# Install API server dependencies
if [ -f "longcat/requirements.txt" ]; then
    pip install -r longcat/requirements.txt
fi

# 6. Patch Code for Memory Safety
echo "🩹 Step 6: Patching Pipeline Code..."
# Patch 1: Keep Text Encoder on CPU (Saves 10GB VRAM)
sed -i 's/self.text_encoder = self.text_encoder.to(device, non_blocking=True)/# self.text_encoder = self.text_encoder.to(device, non_blocking=True)/' longcat_core/longcat_video/pipeline_longcat_video_avatar.py || true

# 7. Download Models
echo "⬇️  Step 7: Downloading AI Models (129GB)..."
mkdir -p weights
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

# Run download only if weights don't exist yet
if [ ! -d "weights/LongCat-Video-Avatar" ]; then
    python3 download_models_temp.py
else
    echo "   -> Weights directory found, skipping download."
fi
rm download_models_temp.py

# 8. Install n8n
echo "🤖 Step 8: Installing n8n..."
npm install -g n8n

echo "=================================================="
echo "✅ Setup Complete! Ready for H100."
echo "To launch:"
echo "1. export PYTHONPATH=\$PYTHONPATH:\$(pwd)/longcat_core"
echo "2. python3 longcat_core/run_demo_avatar_single_audio_to_video.py ..."
echo "=================================================="

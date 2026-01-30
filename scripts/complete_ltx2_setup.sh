#!/bin/bash
# SFitz911 Avatar Generator - Complete LTX-2 Setup
# Run this on a fresh Vast.ai instance to set up everything automatically

set -e

echo "=================================================="
echo "🚀 SFitz911 Avatar Generator - Complete LTX-2 Setup"
echo "=================================================="
echo ""

# Step 1: Clone repositories
echo "📦 Step 1: Cloning repositories..."
cd /workspace

if [ ! -d "sfitz911-avatar-generator" ]; then
    git clone https://github.com/SFitz911/sfitz911-avatar-generator.git
fi

if [ ! -d "LTX-2" ]; then
    git clone https://github.com/Lightricks/LTX-2.git
fi

echo "✅ Repositories cloned"

# Step 2: Install LTX-2 dependencies
echo ""
echo "🔧 Step 2: Installing LTX-2 environment..."
cd /workspace/LTX-2
pip install uv
uv sync --frozen
source .venv/bin/activate

echo "✅ LTX-2 environment ready"

# Step 3: Download models
echo ""
echo "📥 Step 3: Downloading LTX-2 models (~40GB)..."
mkdir -p models
cd models

# Check if models already exist
if [ ! -f "ltx-2-19b-distilled-fp8.safetensors" ]; then
    echo "   Downloading main model..."
    wget -q --show-progress https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-distilled-fp8.safetensors
fi

if [ ! -f "ltx-2-spatial-upscaler-x2-1.0.safetensors" ]; then
    echo "   Downloading upscaler..."
    wget -q --show-progress https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-spatial-upscaler-x2-1.0.safetensors
fi

if [ ! -f "ltx-2-19b-distilled-lora-384.safetensors" ]; then
    echo "   Downloading LoRA..."
    wget -q --show-progress https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-distilled-lora-384.safetensors
fi

if [ ! -d "gemma-3-12b-it-qat-q4_0-unquantized" ]; then
    echo ""
    echo "⚠️  IMPORTANT: Gemma model requires Hugging Face authentication"
    echo "   1. Go to: https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized"
    echo "   2. Click 'Agree and access repository'"
    echo "   3. Get token from: https://huggingface.co/settings/tokens"
    echo "   4. Paste token when prompted:"
    echo ""
    huggingface-cli login
    echo ""
    echo "   Downloading Gemma text encoder..."
    huggingface-cli download google/gemma-3-12b-it-qat-q4_0-unquantized \
        --local-dir gemma-3-12b-it-qat-q4_0-unquantized \
        --local-dir-use-symlinks False
fi

echo "✅ All models downloaded"

# Step 4: Install API and Frontend dependencies
echo ""
echo "🔧 Step 4: Installing API and Frontend dependencies..."
cd /workspace/LTX-2

# Use UV to install in the LTX-2 venv (not pip!)
uv pip install fastapi uvicorn loguru python-multipart streamlit requests pillow

echo "✅ All Python dependencies installed"

# Step 6: Install n8n (optional)
echo ""
echo "🤖 Step 6: Installing n8n..."
if ! command -v n8n &> /dev/null; then
    npm install -g n8n
fi

echo "✅ n8n installed"

# Step 7: Create output directories
echo ""
echo "📁 Step 7: Creating directories..."
cd /workspace/sfitz911-avatar-generator
mkdir -p outputs temp

echo "✅ Setup complete!"
echo ""
echo "=================================================="
echo "🎉 Ready to Launch!"
echo "=================================================="
echo ""
echo "To start all services:"
echo "  cd /workspace/sfitz911-avatar-generator"
echo "  bash scripts/launch_ltx2.sh"
echo ""
echo "Then access:"
echo "  - Frontend: http://localhost:8501"
echo "  - API: http://localhost:8000"
echo "  - n8n: http://localhost:5678"
echo ""
echo "=================================================="

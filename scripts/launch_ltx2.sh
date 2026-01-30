#!/bin/bash
# SFitz911 Avatar Generator - LTX-2 Launch Script
# Run this to start all services with LTX-2 backend

set -e

echo "=================================================="
echo "🚀 Launching SFitz911 Avatar Generator (LTX-2)"
echo "=================================================="

# Move to project root
cd "$(dirname "$0")/.."

# Export paths
export LTX2_DIR=${LTX2_DIR:-"/workspace/LTX-2"}
export CHECKPOINT_PATH="$LTX2_DIR/models/ltx-2-19b-distilled-fp8.safetensors"
export GEMMA_ROOT="$LTX2_DIR/models/gemma-3-12b-it-qat-q4_0-unquantized"
export UPSCALER_PATH="$LTX2_DIR/models/ltx-2-spatial-upscaler-x2-1.0.safetensors"
export DISTILLED_LORA="$LTX2_DIR/models/ltx-2-19b-distilled-lora-384.safetensors"
export OUTPUT_PATH=$(pwd)/outputs
export PYTHONPATH=$PYTHONPATH:$LTX2_DIR

echo "📍 Paths:"
echo "   LTX-2: $LTX2_DIR"
echo "   Checkpoint: $CHECKPOINT_PATH"
echo "   Output: $OUTPUT_PATH"
echo ""

# Check if models exist
if [ ! -f "$CHECKPOINT_PATH" ]; then
    echo "❌ ERROR: LTX-2 checkpoint not found at $CHECKPOINT_PATH"
    exit 1
fi

echo "✅ LTX-2 models found"

# Step 1: Start FastAPI Server (Background)
echo ""
echo "🚀 Step 1: Starting FastAPI Server (LTX-2)..."
cd ltx2
python3 api_server.py &
API_PID=$!
cd ..
echo "   API running on PID $API_PID"

# Wait for API to be ready
echo "   Waiting for API to initialize..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health &> /dev/null; then
        echo "   ✅ API is healthy"
        break
    fi
    sleep 2
done

# Step 2: Start n8n (Background)
echo ""
echo "🤖 Step 2: Starting n8n..."
N8N_PORT=5678 npx n8n start &
N8N_PID=$!
echo "   n8n running on PID $N8N_PID"

# Wait for n8n to be ready
echo "   Waiting for n8n to initialize..."
for i in {1..30}; do
    if curl -f http://localhost:5678 &> /dev/null; then
        echo "   ✅ n8n is healthy"
        break
    fi
    sleep 2
done

# Step 3: Start Frontend (Foreground)
echo ""
echo "🎨 Step 3: Starting Frontend..."
cd frontend
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true

# Cleanup on exit
trap "kill $API_PID $N8N_PID" EXIT

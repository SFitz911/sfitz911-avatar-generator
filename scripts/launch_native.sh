#!/bin/bash
# SFitz911 Avatar Generator - Native Launch Script (H100/H200)
# Run this after vast_setup.sh completes to start all services

set -e

echo "=================================================="
echo "🚀 Launching SFitz911 Avatar Generator (Native)"
echo "=================================================="

# Move to project root
cd "$(dirname "$0")/.."

# Export paths
export PYTHONPATH=$PYTHONPATH:$(pwd)/longcat_core
export CHECKPOINT_DIR=$(pwd)/weights/LongCat-Video-Avatar
export OUTPUT_PATH=$(pwd)/outputs
export TORCH_DTYPE=float16

echo "📍 Paths:"
echo "   Checkpoint: $CHECKPOINT_DIR"
echo "   Output: $OUTPUT_PATH"
echo ""

# Check if models exist
if [ ! -d "$CHECKPOINT_DIR" ]; then
    echo "❌ ERROR: Model weights not found at $CHECKPOINT_DIR"
    echo "   Run: bash scripts/vast_setup.sh first"
    exit 1
fi

echo "✅ Model weights found"

# Step 1: Start FastAPI Server (Background)
echo ""
echo "🚀 Step 1: Starting FastAPI Server..."
cd longcat
python3 api_server_enhanced.py &
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

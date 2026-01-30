#!/bin/bash
# SFitz911 Avatar Generator - Smooth Avatar Generation
# Generates high-quality video with smooth motion and consistent face

# Usage: bash generate_smooth_avatar.sh "Your prompt here" /path/to/reference/image.png

set -e

PROMPT=${1:-"A professional woman speaking to camera"}
IMAGE_PATH=${2:-"/workspace/LTX-2/natasha_single/natasha.png"}
OUTPUT_NAME=${3:-"smooth_avatar.mp4"}
IMAGE_STRENGTH=${4:-"1.7"}
FRAME_RATE=${5:-"24"}

echo "=================================================="
echo "🎬 Generating Smooth Avatar Video"
echo "=================================================="
echo "Prompt: $PROMPT"
echo "Reference Image: $IMAGE_PATH"
echo "Image Strength: $IMAGE_STRENGTH (face consistency)"
echo "Frame Rate: $FRAME_RATE fps (smooth motion)"
echo "Output: $OUTPUT_NAME"
echo ""

# Check if reference image exists
if [ ! -f "$IMAGE_PATH" ]; then
    echo "❌ Error: Reference image not found: $IMAGE_PATH"
    exit 1
fi

cd /workspace/LTX-2

echo "🚀 Starting generation..."
echo ""

# Generate with optimized settings
# - Single reference image for clean, consistent face
# - 24fps for smooth, natural motion (not choppy 6fps)
# - Image strength 1.7 for strong face adherence
# - 121 frames = 5 seconds at 24fps
python -m ltx_pipelines.ti2vid_two_stages \
  --checkpoint-path models/ltx-2-19b-distilled-fp8.safetensors \
  --gemma-root models/gemma-3-12b-it-qat-q4_0-unquantized \
  --spatial-upsampler-path models/ltx-2-spatial-upscaler-x2-1.0.safetensors \
  --distilled-lora models/ltx-2-19b-distilled-lora-384.safetensors 1.0 \
  --image "$IMAGE_PATH" 0 "$IMAGE_STRENGTH" \
  --prompt "$PROMPT" \
  --output-path "$OUTPUT_NAME" \
  --enable-fp8 \
  --height 512 \
  --width 512 \
  --num-frames 121 \
  --frame-rate "$FRAME_RATE" \
  --video-cfg-guidance-scale 4.5

echo ""
echo "✅ Generation complete!"
echo "📁 Video saved to: $OUTPUT_NAME"
echo ""

# Show video info
if command -v ffprobe &> /dev/null; then
    echo "📊 Video info:"
    ffprobe "$OUTPUT_NAME" 2>&1 | grep -E "Duration|Video|Audio" || true
    echo ""
fi

echo "To download:"
echo "  scp -P 40106 -i agent_key root@173.207.82.240:/workspace/LTX-2/$OUTPUT_NAME E:\\DATA_1TB\\Desktop\\Ai-Gen-Clips\\"

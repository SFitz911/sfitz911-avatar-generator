#!/bin/bash
# SFitz911 Avatar Generator - Keyframe Generation Script
# Generates video with multiple reference images for face consistency

# Usage: bash generate_with_keyframes.sh "Your prompt text here"

set -e

PROMPT=${1:-"A professional woman speaking to camera"}
OUTPUT_NAME=${2:-"output_keyframe.mp4"}
REFS_DIR="/workspace/LTX-2/natasha_refs"

echo "=================================================="
echo "🎬 Generating Video with Keyframe Interpolation"
echo "=================================================="
echo "Prompt: $PROMPT"
echo "Output: $OUTPUT_NAME"
echo ""

# Check if reference images exist
if [ ! -d "$REFS_DIR" ] || [ -z "$(ls -A $REFS_DIR 2>/dev/null)" ]; then
    echo "❌ Error: No reference images found in $REFS_DIR"
    echo "   Upload photos first using: upload_reference_images.ps1"
    exit 1
fi

# List available images
echo "📸 Available reference images:"
ls -1 $REFS_DIR/
echo ""

# Get first 3 images
IMAGE_FILES=($(ls $REFS_DIR/*.{jpg,png,jpeg} 2>/dev/null | head -3))

if [ ${#IMAGE_FILES[@]} -lt 2 ]; then
    echo "❌ Error: Need at least 2 images for keyframe interpolation"
    exit 1
fi

echo "🎯 Using ${#IMAGE_FILES[@]} keyframe(s):"
for i in "${!IMAGE_FILES[@]}"; do
    echo "   Frame $((i*60)): ${IMAGE_FILES[$i]}"
done
echo ""

# Build image arguments
IMAGE_ARGS=""
for i in "${!IMAGE_FILES[@]}"; do
    FRAME_IDX=$((i * 60))
    IMAGE_ARGS="$IMAGE_ARGS --image ${IMAGE_FILES[$i]} $FRAME_IDX 1.0"
done

# Run generation
cd /workspace/LTX-2

echo "🚀 Starting generation..."
echo ""

python -m ltx_pipelines.keyframe_interpolation \
  --checkpoint-path models/ltx-2-19b-distilled-fp8.safetensors \
  --gemma-root models/gemma-3-12b-it-qat-q4_0-unquantized \
  --spatial-upsampler-path models/ltx-2-spatial-upscaler-x2-1.0.safetensors \
  --distilled-lora models/ltx-2-19b-distilled-lora-384.safetensors 1.0 \
  $IMAGE_ARGS \
  --prompt "$PROMPT" \
  --output-path "$OUTPUT_NAME" \
  --enable-fp8 \
  --height 512 \
  --width 512 \
  --num-frames 121 \
  --frame-rate 6

echo ""
echo "✅ Generation complete!"
echo "📁 Video saved to: $OUTPUT_NAME"
echo ""
echo "To download:"
echo "  scp -P 40106 -i agent_key root@173.207.82.240:/workspace/LTX-2/$OUTPUT_NAME E:\\DATA_1TB\\Desktop\\Ai-Gen-Clips\\"

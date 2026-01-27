#!/bin/bash
# ============================================
# SFitz911 Avatar Generator - Entrypoint Script
# Handles initialization and model downloading
# ============================================

set -e

echo "=========================================="
echo "SFitz911 Avatar Generator - Starting"
echo "=========================================="

# Check GPU availability
if command -v nvidia-smi &> /dev/null; then
    echo "✓ GPU detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo "⚠ WARNING: No GPU detected!"
fi

# Create directories
mkdir -p "$MODEL_PATH" "$OUTPUT_PATH" /app/temp
echo "✓ Directories created"

# Download models if not present
if [ ! -d "$MODEL_PATH/checkpoints" ]; then
    echo "⚠ Model not found at $MODEL_PATH"
    
    if [ -n "$S3_BUCKET" ] && [ -n "$AWS_ACCESS_KEY_ID" ]; then
        echo "→ Downloading model from S3..."
        python3 -c "
import boto3
import os
from pathlib import Path

s3 = boto3.client('s3')
bucket = os.getenv('S3_BUCKET')
prefix = os.getenv('S3_MODEL_PATH', 'models/longcat/')
local_path = os.getenv('MODEL_PATH')

print(f'Downloading from s3://{bucket}/{prefix} to {local_path}')

# List and download all files
paginator = s3.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
    if 'Contents' in page:
        for obj in page['Contents']:
            key = obj['Key']
            local_file = os.path.join(local_path, key.replace(prefix, ''))
            Path(local_file).parent.mkdir(parents=True, exist_ok=True)
            print(f'  → {key}')
            s3.download_file(bucket, key, local_file)

print('✓ Model download complete')
" || echo "⚠ Model download failed - will attempt to continue"
    else
        echo "⚠ No S3 credentials found - model must be mounted as volume"
    fi
else
    echo "✓ Model found at $MODEL_PATH"
fi

# Print configuration
echo "=========================================="
echo "Configuration:"
echo "  MODEL_PATH: $MODEL_PATH"
echo "  OUTPUT_PATH: $OUTPUT_PATH"
echo "  CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
echo "  API_PORT: ${API_PORT:-8000}"
echo "=========================================="

# Execute the main command
echo "→ Starting API server..."
exec "$@"

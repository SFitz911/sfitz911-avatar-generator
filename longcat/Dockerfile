# ============================================
# SFitz911 Avatar Generator - Optimized LongCat Container
# Multi-stage build for smaller image size
# ============================================

# ============================================
# Stage 1: Builder
# ============================================
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA 12.1 support
RUN pip3 install --no-cache-dir \
    torch==2.1.0 \
    torchvision==0.16.0 \
    torchaudio==2.1.0 \
    --index-url https://download.pytorch.org/whl/cu121

# Install additional ML libraries
RUN pip3 install --no-cache-dir \
    transformers>=4.35.0 \
    diffusers>=0.24.0 \
    accelerate>=0.25.0 \
    xformers>=0.0.23 \
    einops>=0.7.0 \
    omegaconf>=2.3.0 \
    safetensors>=0.4.0

# ============================================
# Stage 2: Runtime
# ============================================
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set Python 3.10 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set working directory
WORKDIR /app

# Copy application code
COPY api_server.py /app/api_server.py
COPY entrypoint.sh /app/entrypoint.sh

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Create necessary directories
RUN mkdir -p /app/models /app/outputs /app/temp && \
    chmod 777 /app/outputs /app/temp

# Set environment variables
ENV MODEL_PATH=/app/models/longcat
ENV OUTPUT_PATH=/app/outputs
ENV CUDA_VISIBLE_DEVICES=0
ENV TORCH_HOME=/app/models/torch
ENV HF_HOME=/app/models/huggingface

# Expose API port
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5m --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Use entrypoint script for initialization
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["python", "api_server.py"]

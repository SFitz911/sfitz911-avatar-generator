# SFitz911 Avatar Generator - LongCat Avatar Container
# CUDA-enabled container for AI video generation

FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Prevent interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    wget \
    curl \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Clone LongCat repository (bf16 optimized version)
# Note: Replace with actual repository URL when available
RUN git clone https://github.com/fjkane/LongCat-Video-Avatar-bf16.git /app/longcat || \
    git clone https://github.com/meituan-longcat/LongCat-Video.git /app/longcat || \
    echo "Repository will be cloned during runtime"

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA 12.1 support
RUN pip install --no-cache-dir \
    torch==2.1.0 \
    torchvision==0.16.0 \
    torchaudio==2.1.0 \
    --index-url https://download.pytorch.org/whl/cu121

# Install additional ML libraries
RUN pip install --no-cache-dir \
    transformers \
    diffusers \
    accelerate \
    xformers \
    einops \
    omegaconf \
    safetensors

# Copy API server code
COPY api_server.py /app/api_server.py

# Create necessary directories
RUN mkdir -p /app/models /app/outputs /app/temp

# Set environment variables
ENV MODEL_PATH=/app/models/longcat
ENV OUTPUT_PATH=/app/outputs
ENV CUDA_VISIBLE_DEVICES=0
ENV TORCH_HOME=/app/models/torch

# Expose API port
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5m --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI server
CMD ["python", "api_server.py"]

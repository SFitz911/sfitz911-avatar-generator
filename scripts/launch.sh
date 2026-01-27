#!/bin/bash
# SFitz911 Avatar Generator - Instance Launch Script
# Run this script on fresh Vast.ai instances to set up everything

set -e  # Exit on error

echo "=================================================="
echo "  SFitz911 Avatar Generator - Launch Script"
echo "=================================================="
echo ""

# ============================================
# Step 1: Check System Requirements
# ============================================
echo "📋 Step 1: Checking system requirements..."

# Check for NVIDIA GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ ERROR: nvidia-smi not found. GPU drivers not installed."
    exit 1
fi

echo "✅ GPU detected:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

# ============================================
# Step 2: Install Docker & Docker Compose
# ============================================
echo ""
echo "🐳 Step 2: Installing Docker..."

if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl start docker
    systemctl enable docker
    echo "✅ Docker installed"
else
    echo "✅ Docker already installed"
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    apt-get update
    apt-get install -y docker-compose-plugin
    echo "✅ Docker Compose installed"
else
    echo "✅ Docker Compose already installed"
fi

# ============================================
# Step 3: Install NVIDIA Container Toolkit
# ============================================
echo ""
echo "🎮 Step 3: Installing NVIDIA Container Toolkit..."

if ! command -v nvidia-ctk &> /dev/null; then
    echo "Installing NVIDIA Container Toolkit..."
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    apt-get update
    apt-get install -y nvidia-container-toolkit
    nvidia-ctk runtime configure --runtime=docker
    systemctl restart docker
    echo "✅ NVIDIA Container Toolkit installed"
else
    echo "✅ NVIDIA Container Toolkit already installed"
fi

# Test GPU access in Docker
echo "Testing GPU access in Docker..."
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi || {
    echo "❌ ERROR: GPU not accessible in Docker"
    exit 1
}
echo "✅ GPU accessible in Docker"

# ============================================
# Step 4: Download Model Weights
# ============================================
echo ""
echo "📦 Step 4: Checking model weights..."

if [ ! -d "./models/longcat" ]; then
    echo "⚠️  Model weights not found in ./models/longcat"
    echo "Please download model weights manually or configure cloud storage sync"
    echo ""
    echo "Options:"
    echo "  1. Download from Hugging Face: huggingface-cli download ..."
    echo "  2. Sync from S3: aws s3 sync s3://your-bucket/models ./models"
    echo "  3. Sync from GCS: gsutil -m rsync -r gs://your-bucket/models ./models"
    echo ""
    read -p "Do you want to continue without models? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Model weights found"
fi

# ============================================
# Step 5: Configure Environment
# ============================================
echo ""
echo "⚙️  Step 5: Configuring environment..."

if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your credentials before starting services"
    echo ""
    read -p "Press Enter to continue after editing .env..."
else
    echo "✅ .env file exists"
fi

# ============================================
# Step 6: Pull Docker Images
# ============================================
echo ""
echo "📥 Step 6: Pulling Docker images..."

docker-compose pull || echo "⚠️  Could not pull pre-built images, will build locally"

# ============================================
# Step 7: Build Custom Images
# ============================================
echo ""
echo "🔨 Step 7: Building custom Docker images..."

docker-compose build

# ============================================
# Step 8: Start Services
# ============================================
echo ""
echo "🚀 Step 8: Starting services..."

docker-compose up -d

# ============================================
# Step 9: Wait for Services
# ============================================
echo ""
echo "⏳ Step 9: Waiting for services to initialize..."

sleep 10

# Check service health
echo ""
echo "Checking service health..."

# Check LongCat API
for i in {1..30}; do
    if curl -f http://localhost:8000/health &> /dev/null; then
        echo "✅ LongCat API is healthy"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "⚠️  LongCat API not responding yet (this is normal if models are still loading)"
    fi
    sleep 2
done

# Check n8n
for i in {1..30}; do
    if curl -f http://localhost:5678 &> /dev/null; then
        echo "✅ n8n is healthy"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "⚠️  n8n not responding yet"
    fi
    sleep 2
done

# ============================================
# Step 10: Display Status
# ============================================
echo ""
echo "=================================================="
echo "  🎉 SFitz911 Avatar Generator is Running!"
echo "=================================================="
echo ""
echo "Services:"
echo "  • LongCat API: http://localhost:8000"
echo "  • n8n:         http://localhost:5678"
echo "  • Redis:       localhost:6379"
echo ""
echo "Useful Commands:"
echo "  • View logs:        docker-compose logs -f"
echo "  • Stop services:    docker-compose down"
echo "  • Restart services: docker-compose restart"
echo "  • Check status:     docker-compose ps"
echo ""
echo "Next Steps:"
echo "  1. Access n8n at http://$(curl -s ifconfig.me):5678"
echo "  2. Configure workflows in n8n/workflows/"
echo "  3. Test API: curl http://localhost:8000/health"
echo ""
echo "=================================================="

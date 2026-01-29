# SFitz911 Avatar Generator - Local Startup Script
# This script starts the services using the local compose file (no GPU required)

Write-Host "=================================================="
Write-Host "  SFitz911 Avatar Generator - Local Startup"
Write-Host "=================================================="
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker status..."
try {
    docker ps | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not responding"
    }
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Desktop is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}

# Navigate to project directory
Set-Location $PSScriptRoot

# Check if .env exists
if (!(Test-Path .env)) {
    Write-Host "Creating .env file from .env.example..."
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env file with your credentials if needed" -ForegroundColor Yellow
}

# Create outputs directory if it doesn't exist
if (!(Test-Path outputs)) {
    New-Item -ItemType Directory -Path outputs | Out-Null
    Write-Host "Created outputs directory"
}

Write-Host ""
Write-Host "Starting services (this may take a few minutes to pull images)..." -ForegroundColor Cyan
Write-Host ""

# Start services using local compose (no GPU)
docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=================================================="
    Write-Host "  🎉 Services Started Successfully!"
    Write-Host "=================================================="
    Write-Host ""
    Write-Host "Services:" -ForegroundColor Cyan
    Write-Host "  • LongCat API: http://localhost:8000"
    Write-Host "  • n8n:         http://localhost:5678"
    Write-Host "  • Redis:       localhost:6379"
    Write-Host ""
    Write-Host "Useful Commands:" -ForegroundColor Cyan
    Write-Host "  • View logs:        docker-compose -f docker-compose.yml -f docker-compose.local.yml logs -f"
    Write-Host "  • Stop services:    docker-compose -f docker-compose.yml -f docker-compose.local.yml down"
    Write-Host "  • Check status:     docker-compose -f docker-compose.yml -f docker-compose.local.yml ps"
    Write-Host ""
    Write-Host "Note: This is running in local mode (no GPU)." -ForegroundColor Yellow
    Write-Host "      The LongCat service may not work fully without GPU support." -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Failed to start services. Check the error messages above." -ForegroundColor Red
    Write-Host "View logs with: docker-compose -f docker-compose.yml -f docker-compose.local.yml logs" -ForegroundColor Yellow
}

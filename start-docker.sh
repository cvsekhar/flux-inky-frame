#!/bin/bash

# Quick start script for FLUX Image Generator Docker deployment

set -e

echo "🐳 FLUX Image Generator - Docker Quick Start"
echo "=============================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✓ Docker is installed"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
    echo "❌ docker-compose is not installed!"
    echo "Please install docker-compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ docker-compose is available"

# Detect GPU support
HAS_GPU=false
if command -v nvidia-smi &> /dev/null; then
    if nvidia-smi &> /dev/null; then
        echo "✓ NVIDIA GPU detected"
        HAS_GPU=true
    fi
fi

if [ "$HAS_GPU" = false ]; then
    echo "⚠️  No GPU detected - will use CPU mode (slower)"
fi

echo ""
echo "📦 Preparing volumes..."

# Create generated_images directory
mkdir -p generated_images
echo "✓ Created ./generated_images directory"

echo ""
echo "🏗️  Building Docker image..."
echo "This may take a few minutes..."

if [ "$HAS_GPU" = true ]; then
    docker-compose build
else
    docker-compose -f docker-compose-cpu.yml build
fi

echo ""
echo "✓ Docker image built successfully!"
echo ""
echo "🚀 Starting container..."

if [ "$HAS_GPU" = true ]; then
    docker-compose up -d
else
    docker-compose -f docker-compose-cpu.yml up -d
fi

echo ""
echo "⏳ Waiting for container to be ready..."
sleep 5

echo ""
echo "✅ Container is starting!"
echo ""
echo "📊 Important Information:"
echo "------------------------"
echo "• Access the app at: http://localhost:5000"
echo "• First run will download model (~8GB) - takes 5-15 minutes"
echo "• Generated images saved to: ./generated_images/"
echo "• Model cache is persisted in Docker volume"
echo ""
echo "📝 Useful commands:"
echo "  View logs:     docker-compose logs -f"
echo "  Stop:          docker-compose down"
echo "  Restart:       docker-compose restart"
echo "  Check status:  docker-compose ps"
echo ""
echo "🎉 Setup complete! Opening app in browser..."
echo ""

# Try to open browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000 2>/dev/null &
elif command -v open &> /dev/null; then
    open http://localhost:5000 2>/dev/null &
fi

# Show logs
echo "📋 Following logs (Ctrl+C to exit, container keeps running):"
echo "=============================================================="
echo ""

if [ "$HAS_GPU" = true ]; then
    docker-compose logs -f
else
    docker-compose -f docker-compose-cpu.yml logs -f
fi

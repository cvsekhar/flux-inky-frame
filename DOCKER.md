# Docker Deployment Guide

Complete guide for deploying the FLUX Image Generator using Docker.

## 📦 What's Included

- **Dockerfile** - Container image definition
- **docker-compose.yml** - GPU-enabled deployment
- **docker-compose-cpu.yml** - CPU-only deployment
- **Persistent volumes** for models and generated images

## 🗂️ Volumes

The setup uses two volumes to persist data:

1. **HuggingFace Cache** (`huggingface-cache`)
   - Stores downloaded models (~8GB)
   - Named volume (managed by Docker)
   - Persists between container restarts
   - Location in container: `/root/.cache/huggingface`

2. **Generated Images** (`./generated_images`)
   - Stores your generated images
   - Bind mount (folder on your host machine)
   - Location in container: `/app/generated_images`
   - Accessible from host at `./generated_images/`

## 🚀 Quick Start

### Option 1: With GPU (Recommended)

**Prerequisites:**
- Docker with GPU support
- NVIDIA Container Toolkit installed
- CUDA-capable GPU

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Access the app
open http://localhost:5000
```

### Option 2: CPU Only

```bash
# Build and start the container (CPU mode)
docker-compose -f docker-compose-cpu.yml up -d

# View logs
docker-compose -f docker-compose-cpu.yml logs -f

# Access the app
open http://localhost:5000
```

## 🛠️ Installation Steps

### 1. Install Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
```bash
brew install --cask docker
```

**Windows:**
Download from [docker.com](https://www.docker.com/products/docker-desktop)

### 2. Install NVIDIA Container Toolkit (for GPU)

**Ubuntu/Debian:**
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

Verify GPU access:
```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### 3. Build and Run

```bash
# Clone/download the project
cd flux-inky-frame

# Build the Docker image
docker-compose build

# Start the container
docker-compose up -d

# Check it's running
docker-compose ps
```

## 📊 First Run

On the first run, the container will:
1. Start the Flask app
2. Download FLUX.2-klein-4B model (~8GB) to the cache volume
3. Load the model into memory (~13GB VRAM)
4. Start serving on port 5000

**This takes 5-15 minutes on the first run!**

Subsequent runs will be much faster as the model is cached.

## 🔧 Common Commands

```bash
# Start the container
docker-compose up -d

# Stop the container
docker-compose down

# View logs
docker-compose logs -f

# Restart the container
docker-compose restart

# Rebuild the image
docker-compose build --no-cache

# Access container shell
docker-compose exec flux-inky-frame bash

# View container stats (CPU, memory, GPU)
docker stats flux-inky-frame
```

## 📁 Volume Management

### View Generated Images on Host

```bash
# Images are in ./generated_images/
ls -lh generated_images/
```

### Backup Generated Images

```bash
# Create a backup
tar -czf images-backup-$(date +%Y%m%d).tar.gz generated_images/

# Restore from backup
tar -xzf images-backup-20250124.tar.gz
```

### Clear Generated Images

```bash
# Stop container first
docker-compose down

# Clear images
rm -rf generated_images/*

# Or use the app's Settings -> Cleanup feature
```

### Manage Model Cache

```bash
# View cache volume
docker volume ls
docker volume inspect flux-inky-frame_huggingface-cache

# Remove cache volume (will re-download model on next run)
docker-compose down
docker volume rm flux-inky-frame_huggingface-cache
```

## 🌐 Port Configuration

Default port is 5000. To change:

```yaml
# In docker-compose.yml, change:
ports:
  - "8080:5000"  # Access on port 8080
```

## 💾 Disk Space

**Requirements:**
- Docker image: ~5GB
- HuggingFace model cache: ~8GB
- Generated images: Varies (~2-5MB per image pair)

**Total:** ~15GB + your generated images

## 🔍 Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs

# Common issues:
# 1. Port 5000 already in use
sudo lsof -i :5000

# 2. GPU not detected
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Out of memory

```bash
# Check GPU memory
nvidia-smi

# If using CPU, check system memory
free -h
```

### Model download fails

```bash
# Check internet connection
# Check HuggingFace is accessible
curl -I https://huggingface.co

# Clear cache and retry
docker-compose down
docker volume rm flux-inky-frame_huggingface-cache
docker-compose up -d
```

### Permission issues with generated_images

```bash
# Fix permissions
sudo chown -R $USER:$USER generated_images/
chmod -R 755 generated_images/
```

## 🚢 Production Deployment

### Using Docker Compose

```bash
# Run in production mode
docker-compose -f docker-compose.yml up -d

# Enable auto-restart
# (already configured with restart: unless-stopped)
```

### Using Docker Run

```bash
# Build the image
docker build -t flux-inky-frame .

# Run with volumes
docker run -d \
  --name flux-inky-frame \
  --gpus all \
  -p 5000:5000 \
  -v flux-hf-cache:/root/.cache/huggingface \
  -v $(pwd)/generated_images:/app/generated_images \
  --restart unless-stopped \
  flux-inky-frame
```

### Behind a Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name flux.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # For large image uploads/downloads
        client_max_body_size 50M;
        proxy_read_timeout 300;
    }
}
```

## 🔐 Security Notes

- The app runs on port 5000 by default
- No authentication is built-in
- For production, use a reverse proxy with HTTPS
- Consider adding rate limiting for the /generate endpoint
- Restrict access with firewall rules if needed

## 📈 Monitoring

### View Resource Usage

```bash
# CPU, Memory, GPU usage
docker stats flux-inky-frame

# GPU usage specifically
nvidia-smi -l 1
```

### Check Disk Usage

```bash
# Volume sizes
docker system df -v

# Generated images size
du -sh generated_images/
```

## 🧹 Cleanup

### Remove everything

```bash
# Stop and remove container
docker-compose down

# Remove volumes
docker volume rm flux-inky-frame_huggingface-cache

# Remove generated images
rm -rf generated_images/

# Remove Docker image
docker rmi flux-inky-frame
```

### Prune Docker system

```bash
# Remove unused containers, images, networks
docker system prune -a

# Remove unused volumes
docker volume prune
```

## 🎯 Next Steps

After deployment:
1. Access http://localhost:5000
2. Wait for model to load (first run: ~10 min)
3. Generate your first image
4. Check `./generated_images/` for outputs
5. Use the Gallery tab to browse images
6. Use Settings tab to cleanup when needed

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

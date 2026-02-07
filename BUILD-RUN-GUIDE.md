# 🚀 Docker Build & Run Guide

## Quick Start

```bash
# Build the image
docker-compose build

# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Access the app
open http://localhost:5000
```

## Build Process

The build will:
1. Pull Python 3.10 slim image
2. Install curl
3. Download and install uv
4. Install Python dependencies (~2-5 minutes)
5. Copy app code
6. Create directories

**Expected build time:** 3-7 minutes (first time)

## First Run

When you start the container:
1. App starts up (~10 seconds)
2. Downloads FLUX model (~8GB, 5-10 minutes) - **ONLY FIRST TIME**
3. Loads model into memory (2-3 minutes)
4. Ready to generate images!

**Watch the logs:**
```bash
docker-compose logs -f
```

You'll see:
```
🚀 Starting FLUX Image Generator for Inky Frame
============================================================
Loading FLUX.2-klein-4B model...
Device: cpu
Dtype: torch.float32
============================================================
```

Then model download progress, then:
```
✓ Model loaded successfully!
============================================================
🌐 Starting Flask server on http://0.0.0.0:5000
```

## Common Issues

### Build fails with "uv: not found"
Already fixed in the current Dockerfile! If you still see this:
```bash
# Clear Docker cache and rebuild
docker-compose build --no-cache
```

### Port 5000 already in use
```bash
# Check what's using port 5000
sudo lsof -i :5000

# Or change port in docker-compose.yml:
ports:
  - "8080:5000"  # Use 8080 instead
```

### Out of disk space
```bash
# Check Docker disk usage
docker system df

# Clean up unused Docker data
docker system prune -a
```

### Build is very slow
This is normal on first build. Docker is:
- Downloading base image
- Installing uv
- Downloading Python packages
- Compiling PyTorch, etc.

**Tip:** Subsequent builds are much faster due to layer caching.

### Container starts but crashes
```bash
# Check logs for errors
docker-compose logs

# Common issues:
# - Not enough RAM (need ~4GB for model on CPU)
# - Not enough disk space (need ~20GB total)
```

## Verify Everything Works

```bash
# Check container is running
docker-compose ps

# Should show:
# NAME                STATE     PORTS
# flux-inky-frame     running   0.0.0.0:5000->5000/tcp

# Check logs for "Model loaded successfully"
docker-compose logs | grep "Model loaded"

# Test the web interface
curl http://localhost:5000

# Should return the HTML page
```

## Storage Locations

```bash
# See volumes
docker volume ls | grep huggingface-cache

# See generated images
ls -lh generated_images/

# Check sizes
du -sh generated_images/
docker system df -v | grep huggingface-cache
```

## Complete Rebuild

If something goes wrong:
```bash
# Stop and remove everything
docker-compose down

# Remove the image
docker rmi flux-inky-frame

# Remove volumes (will re-download model!)
docker volume rm flux-inky-frame_huggingface-cache

# Rebuild from scratch
docker-compose build --no-cache

# Start fresh
docker-compose up -d
```

## Performance Tips

### CPU Mode Performance
- Model loading: 2-3 minutes
- First image: 60-120 seconds
- Subsequent images: 30-90 seconds
- Varies by CPU speed and cores

### Memory Usage
- Docker container: ~4-6GB RAM
- Model in memory: ~4GB
- Generation: +1-2GB during generation
- **Total:** ~8GB RAM recommended

### Disk Usage
- Docker image: ~5GB
- Model cache: ~8GB
- Generated images: ~2-5MB per pair
- **Total:** ~15GB + images

## Development Mode

Want to edit code without rebuilding?

```bash
# Stop container
docker-compose down

# Add bind mount for app.py in docker-compose.yml:
volumes:
  - ./app.py:/app/app.py
  - huggingface-cache:/root/.cache/huggingface
  - ./generated_images:/app/generated_images

# Restart
docker-compose up -d

# Now changes to app.py take effect on restart
docker-compose restart
```

## Production Deployment

```bash
# Build optimized
docker-compose build

# Run in background
docker-compose up -d

# Enable restart on boot
# (already configured with restart: unless-stopped)

# Check it's running
docker-compose ps

# Monitor
docker stats flux-inky-frame

# View logs
docker-compose logs -f --tail=100
```

## Useful Commands Reference

```bash
# Build
docker-compose build              # Normal build
docker-compose build --no-cache   # Clean build

# Run
docker-compose up -d              # Start in background
docker-compose up                 # Start with logs

# Control
docker-compose down               # Stop and remove
docker-compose restart            # Restart
docker-compose stop               # Stop (keep container)
docker-compose start              # Start (if stopped)

# Inspect
docker-compose ps                 # Status
docker-compose logs -f            # Follow logs
docker-compose logs --tail=50     # Last 50 lines
docker-compose exec flux-inky-frame bash  # Shell access

# Cleanup
docker-compose down -v            # Remove volumes too
docker system prune -a            # Clean everything
```

## Success Indicators

✅ **Build successful:**
```
Successfully built <image-id>
Successfully tagged flux-inky-frame:latest
```

✅ **Container running:**
```
$ docker-compose ps
NAME                STATE     PORTS
flux-inky-frame     running   0.0.0.0:5000->5000/tcp
```

✅ **Model loaded:**
```
$ docker-compose logs | grep "Model loaded"
✓ Model loaded successfully!
```

✅ **Web interface accessible:**
```
$ curl -I http://localhost:5000
HTTP/1.1 200 OK
```

## Next Steps

Once everything is running:
1. Open http://localhost:5000
2. Go to Generate tab
3. Enter a prompt
4. Wait for image generation
5. Check Gallery tab to see all images
6. Check `./generated_images/` folder on your computer

Enjoy! 🎨

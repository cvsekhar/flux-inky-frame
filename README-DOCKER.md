# 🚀 Quick Docker Start (CPU Mode)

Since you're running on CPU, here's the simplified setup:

## ⚡ Super Quick Start

```bash
# One command to rule them all!
./start-docker.sh
```

That's it! The script will:
- Build the Docker image
- Create volumes for model cache and images
- Start the container
- Open http://localhost:5000 in your browser

## 📝 Manual Start (if you prefer)

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

## ⏱️ What to Expect

**First Run:**
- Model download: 5-10 minutes (~8GB)
- Model loading: 2-3 minutes
- First image generation: 30-120 seconds

**Subsequent Runs:**
- Model loading: 2-3 minutes (already cached)
- Image generation: 30-120 seconds each

**CPU mode is slower but works perfectly!**

## 📂 Your Files

- **Model cache:** Stored in Docker volume (automatic)
- **Generated images:** `./generated_images/` folder
  - `*_original.jpg` - 800×480 original
  - `*_inky.jpg` - 480×800 for Inky Frame

## 🎮 Using the App

1. **Generate Tab** - Create new images
2. **Gallery Tab** - Browse all past generations
3. **Settings Tab** - Clean up old images

## 🛑 Stop/Start/Restart

```bash
# Stop
docker-compose down

# Start
docker-compose up -d

# Restart
docker-compose restart

# View what's running
docker-compose ps
```

## 💾 Backup Your Images

```bash
# Simple backup
cp -r generated_images generated_images_backup

# Or create archive
tar -czf images-$(date +%Y%m%d).tar.gz generated_images/
```

## 🗑️ Cleanup

```bash
# Delete all generated images (or use Settings tab in app)
rm -rf generated_images/*

# Remove everything (including model cache)
docker-compose down
docker volume rm flux-inky-frame_huggingface-cache
```

## ❓ Troubleshooting

**Port 5000 already in use?**
```bash
# Edit docker-compose.yml and change:
ports:
  - "8080:5000"  # Use port 8080 instead
```

**Container won't start?**
```bash
docker-compose logs
```

**Need more help?**
See full documentation in [DOCKER.md](DOCKER.md)

## 🎯 That's It!

Your images will be in `./generated_images/` and the model cache persists between restarts. Enjoy! 🎨

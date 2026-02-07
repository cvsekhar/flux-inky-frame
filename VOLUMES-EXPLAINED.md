# 📦 Docker Volumes Explained

## Understanding Volume Types

Docker has two types of volumes:

### 1. **Named Volumes** (Managed by Docker)
```yaml
volumes:
  - huggingface-cache:/root/.cache/huggingface
```
- ✅ Docker manages storage location
- ✅ Survives container deletion
- ✅ Easy to manage with `docker volume` commands
- ❌ Not directly visible in your project folder
- **Location:** Usually `/var/lib/docker/volumes/` on Linux, Docker VM on Mac/Windows

### 2. **Bind Mounts** (Your filesystem)
```yaml
volumes:
  - ./generated_images:/app/generated_images
```
- ✅ You see the actual folder in your project
- ✅ Easy to backup, browse, copy
- ✅ Can use relative (`./folder`) or absolute (`/home/user/folder`) paths
- ❌ Must manage the folder yourself

## Current Configuration

### Default (`docker-compose.yml`)

```yaml
volumes:
  # Named volume - Docker manages it
  - huggingface-cache:/root/.cache/huggingface
  
  # Bind mount - visible in your project
  - ./generated_images:/app/generated_images
```

**What this means:**
- **HuggingFace cache:** Hidden in Docker's storage, you don't see it
- **Generated images:** In `./generated_images/` folder, you can see/access them

**When you run `docker-compose up`:**
1. Creates `generated_images/` folder in same directory as docker-compose.yml
2. Creates Docker-managed volume for model cache

## Alternative Configurations

### Option A: Everything on Host (All Visible)

Use `docker-compose-host-volumes.yml`:
```yaml
volumes:
  # Both are folders you can see
  - ./huggingface-cache:/root/.cache/huggingface
  - ./generated_images:/app/generated_images
```

**Start with:**
```bash
docker-compose -f docker-compose-host-volumes.yml up -d
```

**Result:**
```
your-project/
├── docker-compose-host-volumes.yml
├── huggingface-cache/          ← You can see this! (~8GB)
│   └── hub/
│       └── models--black-forest-labs--FLUX.2-klein-4B/
└── generated_images/            ← Your images
    ├── 20250124_153045_a1b2c3d4_original.jpg
    └── 20250124_153045_a1b2c3d4_inky.jpg
```

### Option B: Absolute Paths

Edit docker-compose.yml:
```yaml
volumes:
  - /home/myuser/ai-models/huggingface:/root/.cache/huggingface
  - /home/myuser/inky-images:/app/generated_images
```

**Good for:**
- Storing models in a different drive
- Centralized storage location
- Multiple projects sharing models

## Relative vs Absolute Paths

### Relative Path (`./folder`)
- Relative to docker-compose.yml location
- `./generated_images` = same directory
- `../images` = parent directory

### Absolute Path (`/full/path/to/folder`)
- Full path from root
- `/home/user/images`
- `C:/Users/YourName/images` (Windows with WSL)

## Common Scenarios

### Scenario 1: "I want to see everything"
✅ Use `docker-compose-host-volumes.yml`
```bash
docker-compose -f docker-compose-host-volumes.yml up -d
```

### Scenario 2: "I want to share models between projects"
✅ Use absolute path for cache:
```yaml
volumes:
  - /home/user/shared-ai-models/huggingface:/root/.cache/huggingface
  - ./generated_images:/app/generated_images
```

### Scenario 3: "I want images on external drive"
✅ Use absolute path for images:
```yaml
volumes:
  - huggingface-cache:/root/.cache/huggingface
  - /mnt/external-drive/inky-images:/app/generated_images
```

### Scenario 4: "Keep it simple, don't care about cache"
✅ Use default `docker-compose.yml` (current setup)

## Managing Named Volumes

```bash
# List all volumes
docker volume ls

# Inspect a volume (see actual location)
docker volume inspect flux-inky-frame_huggingface-cache

# Remove a volume (will re-download model on next run)
docker volume rm flux-inky-frame_huggingface-cache

# See volume size
docker system df -v
```

## Backup Strategies

### Backing up Generated Images (Bind Mount)
```bash
# Easy - just copy the folder!
cp -r generated_images generated_images_backup
tar -czf images-backup.tar.gz generated_images/
```

### Backing up Model Cache (Named Volume)
```bash
# Option 1: Export the volume
docker run --rm \
  -v flux-inky-frame_huggingface-cache:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/model-cache-backup.tar.gz -C /data .

# Option 2: Switch to host volume (use docker-compose-host-volumes.yml)
```

### Backing up Model Cache (Bind Mount)
```bash
# If using host volumes - super easy!
tar -czf model-cache-backup.tar.gz huggingface-cache/
```

## Which Should You Use?

### Use Default (docker-compose.yml) if:
- ✅ You just want it to work
- ✅ Don't need to access model files
- ✅ Want Docker to handle everything

### Use Host Volumes (docker-compose-host-volumes.yml) if:
- ✅ You want to see/backup all files
- ✅ Want to share models between projects
- ✅ Have limited Docker VM space (Mac/Windows)
- ✅ Need to manually manage storage

## Quick Reference

| Volume Type | Syntax | Location | Visibility |
|------------|--------|----------|------------|
| Named | `huggingface-cache:/path` | Docker managed | Hidden |
| Bind (Relative) | `./folder:/path` | Next to docker-compose.yml | Visible |
| Bind (Absolute) | `/full/path:/path` | Anywhere on system | Visible |

## Changing Configuration

### Switch from named volume to host folder:

1. Stop container:
```bash
docker-compose down
```

2. Copy model from named volume to host:
```bash
mkdir -p huggingface-cache
docker run --rm \
  -v flux-inky-frame_huggingface-cache:/source \
  -v $(pwd)/huggingface-cache:/dest \
  alpine cp -r /source/. /dest/
```

3. Use host volumes config:
```bash
docker-compose -f docker-compose-host-volumes.yml up -d
```

4. (Optional) Remove old named volume:
```bash
docker volume rm flux-inky-frame_huggingface-cache
```

## Summary

**Current setup (default):**
- Model cache: Named volume (Docker manages, ~8GB, hidden)
- Images: `./generated_images/` (you can see them)

**To see everything:**
- Use `docker-compose-host-volumes.yml`
- Everything in visible folders

**Both work perfectly! Choose what fits your workflow.** 🎯

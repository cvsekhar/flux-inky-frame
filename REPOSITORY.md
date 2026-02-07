# Repository Structure

## 📁 Complete File Listing

### Core Application
- **app.py** - Main Flask application (single-file, ~1165 lines)
  - Web interface (embedded HTML/CSS/JS)
  - FLUX.2-klein-4B integration
  - DSPy prompt refinement
  - Image generation and rotation
  - Gallery management
  - API endpoints

### Configuration Files
- **pyproject.toml** - uv project dependencies and metadata
- **.python-version** - Python version specification (3.10)
- **.env.example** - Environment variables template
- **requirements.txt** - pip-compatible dependencies (legacy)

### Docker Files
- **Dockerfile** - Container build configuration (uv-based, Debian slim)
- **docker-compose.yml** - Default CPU configuration
- **docker-compose-gpu.yml** - GPU-enabled configuration
- **docker-compose-host-volumes.yml** - All volumes on host
- **.dockerignore** - Docker build exclusions

### Documentation
- **README.md** - Main project documentation
- **DOCKER.md** - Complete Docker guide
- **LLM-SETUP.md** - Local LLM configuration
- **README-DOCKER.md** - Quick Docker reference
- **BUILD-RUN-GUIDE.md** - Build troubleshooting
- **VOLUMES-EXPLAINED.md** - Docker volume management
- **CHANGELOG.md** - Version history
- **LICENSE** - MIT License

### Git Configuration
- **.gitignore** - Git exclusions (venv, cache, generated images, .env)

### Scripts
- **start-docker.sh** - Automated Docker setup script
- **test_setup.py** - Environment validation script
- **rotate_image.py** - Standalone image rotation utility

## 🎯 Key Features by File

### app.py
```python
# Routes
GET  /                  # Main web interface
POST /generate          # Generate image pair
GET  /gallery           # List all images
GET  /latest.jpg        # Latest inky image
DELETE /delete/<id>     # Delete image pair
POST /cleanup           # Delete all images
GET  /download/<file>   # Download image
GET  /view/<file>       # View image

# Functions
init_dspy()            # Configure DSPy + LLM
init_model()           # Load FLUX model
refine_prompt()        # AI prompt enhancement
generate_image()       # Image generation endpoint
rotate_and_convert()   # Image rotation utility
```

### docker-compose.yml
```yaml
# Services
flux-inky-frame:       # Main application
  - Port: 5000
  - Volumes: huggingface-cache, generated_images
  - CPU mode (default)
  - Environment: LLM_API_BASE, LLM_MODEL
```

### pyproject.toml
```toml
[project]
name = "flux-inky-frame"
requires-python = ">=3.10,<3.11"

[dependencies]
flask>=3.0.0
torch>=2.0.0
diffusers>=0.31.0
transformers>=4.38.0
dspy-ai>=2.4.0
pillow>=10.0.0
# ... (7 total dependencies)
```

## 📊 File Statistics

| Category | Count | Total Lines |
|----------|-------|-------------|
| Python Files | 3 | ~1200 |
| Documentation | 8 | ~1500 |
| Configuration | 7 | ~200 |
| Docker Files | 4 | ~150 |
| **Total** | **22** | **~3050** |

## 🔗 File Dependencies

```
app.py
  ├── pyproject.toml (dependencies)
  ├── .env.example (configuration)
  └── generated_images/ (output)

Dockerfile
  ├── pyproject.toml (build deps)
  ├── .python-version (Python version)
  └── .dockerignore (exclusions)

docker-compose.yml
  ├── Dockerfile (build)
  ├── .env (runtime config)
  └── volumes/ (data persistence)
```

## 🚀 Quick Start Map

### Local Development
```
.python-version → uv → pyproject.toml → app.py
         ↓
   .env.example → .env → LLM_API_BASE
```

### Docker Deployment
```
Dockerfile → docker-compose.yml → docker-compose up
     ↓              ↓
pyproject.toml    .env
```

## 📝 Documentation Hierarchy

1. **README.md** - Start here
   ↓
2. **DOCKER.md** - If using Docker
   ↓
3. **LLM-SETUP.md** - For prompt refinement
   ↓
4. **VOLUMES-EXPLAINED.md** - For data management
   ↓
5. **BUILD-RUN-GUIDE.md** - If issues arise

## 🔄 Typical Workflows

### First Time Setup
1. Clone repository
2. Read README.md
3. Copy .env.example → .env
4. Read LLM-SETUP.md
5. Run: `uv run python app.py` or `docker-compose up -d`

### Development
1. Edit app.py
2. Test locally: `uv run python app.py`
3. Rebuild Docker: `docker-compose build`
4. Deploy: `docker-compose up -d`

### Deployment
1. Read DOCKER.md
2. Configure .env
3. Choose docker-compose file
4. Run: `docker-compose up -d`
5. Monitor: `docker-compose logs -f`

## 🗂️ Generated/Runtime Files (Not in Git)

```
.venv/                  # Python virtual environment (local)
.uv/                    # uv cache (local)
generated_images/       # Output images
huggingface-cache/      # FLUX model cache
.env                    # Local configuration
uv.lock                 # uv lock file
__pycache__/            # Python bytecode
*.log                   # Application logs
```

## 📦 Models Downloaded at Runtime

```
~/.cache/huggingface/
  └── hub/
      └── models--black-forest-labs--FLUX.2-klein-4B/
          └── snapshots/
              └── [hash]/
                  ├── model.safetensors (~8GB)
                  ├── config.json
                  └── ... (other files)

Ollama models:
  ~/.ollama/models/
    └── llama3.2/ (~3GB)
```

## 🎯 Entry Points

### Application Entry
```python
# app.py
if __name__ == '__main__':
    init_dspy()    # Optional: LLM setup
    init_model()   # Required: FLUX setup
    app.run()      # Start Flask
```

### Docker Entry
```dockerfile
# Dockerfile
CMD [".venv/bin/python", "app.py"]
```

### Script Entry
```bash
# start-docker.sh
#!/bin/bash
docker-compose up -d
docker-compose logs -f
```

## 📈 Version Control

```
main
  ├── df0b861 - Initial commit
  └── 8159896 - Add CHANGELOG.md
```

Tags: v1.0.0 (ready to tag)

## 🔐 Sensitive Files (.gitignore)

- `.env` - Local configuration
- `generated_images/` - User content
- `.venv/` - Python environment
- `huggingface-cache/` - Model cache
- `*.log` - Application logs

## 🌐 External Dependencies

### PyPI Packages
- flask, torch, diffusers, transformers, accelerate, pillow, safetensors, dspy-ai

### HuggingFace Models
- black-forest-labs/FLUX.2-klein-4B (~8GB)

### Optional Local Services
- Ollama (llama3.2 ~3GB)
- LM Studio
- Any OpenAI-compatible LLM

---

Last Updated: 2026-02-07
Repository Version: 1.0.0

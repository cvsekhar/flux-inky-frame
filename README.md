# FLUX Inky Frame Image Generator

A Flask web application for generating AI images optimized for Inky Frame 7.3" e-ink displays using FLUX.2-klein-4B model. Features automatic prompt refinement with local LLMs via DSPy.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10-blue.svg)

## ✨ Features

- 🎨 **FLUX.2-klein-4B** image generation (4B parameters, Apache 2.0 license)
- 🤖 **AI Prompt Refinement** using DSPy with local LLMs (Ollama, LM Studio, etc.)
- 🖼️ **Dual Output**: Original (800×480) + rotated for Inky Frame (480×800)
- 📱 **Web Interface**: Clean, responsive UI with real-time progress tracking
- 🗂️ **Gallery Browser**: View, download, and manage generated images
- ⏱️ **Performance Tracking**: Real-time elapsed time and generation metrics
- 🐳 **Docker Support**: CPU and GPU configurations with volume management
- 🔒 **Privacy-First**: Completely local, no external API calls (except optional LLM)

## 🚀 Quick Start

### Local Development (uv)

\`\`\`bash
# 1. Clone the repository
git clone <repository-url>
cd flux-inky-frame

# 2. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Set up local LLM (optional but recommended)
# See LLM-SETUP.md for details
ollama pull llama3.2

# 4. Run the app
uv run python app.py
\`\`\`

Open http://localhost:5000 in your browser.

### Docker (Recommended for Production)

\`\`\`bash
# 1. Clone the repository
git clone <repository-url>
cd flux-inky-frame

# 2. Build and run
docker-compose up -d

# 3. View logs
docker-compose logs -f
\`\`\`

See [DOCKER.md](DOCKER.md) for complete Docker documentation.

## 📋 Requirements

### System Requirements
- **Disk Space**: ~20GB (5GB image + 8GB FLUX model + 3GB LLM + overhead)
- **RAM**: ~8GB recommended (4GB model + 2GB generation + 2GB overhead)
- **CPU**: Any modern CPU (GPU optional but faster)
- **Network**: Stable connection for initial ~11GB model downloads

### Software Requirements
- Python 3.10 (managed by uv)
- Docker & Docker Compose (for containerized deployment)
- Ollama or LM Studio (optional, for prompt refinement)

## 🎯 How It Works

1. **Enter Prompt**: Type your image description
2. **AI Refinement**: Local LLM enhances your prompt (optional, ~2-5s)
3. **Image Generation**: FLUX creates 800×480 image (~30-120s on CPU)
4. **Auto-Rotate**: Creates 480×800 version for Inky Frame
5. **Download**: Get both versions or use \`/latest.jpg\` endpoint

## 🔧 Configuration

Create a \`.env\` file (copy from \`.env.example\`):

\`\`\`bash
# OpenAI-compatible LLM for prompt refinement
LLM_API_BASE=http://localhost:11434/v1
LLM_MODEL=llama3.2
\`\`\`

## 📚 Documentation

- [DOCKER.md](DOCKER.md) - Complete Docker guide
- [LLM-SETUP.md](LLM-SETUP.md) - Local LLM setup guide
- [.env.example](.env.example) - Configuration template

## ⚡ Quick Commands

\`\`\`bash
# Start app (local)
uv run python app.py

# Start app (Docker)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop app
docker-compose down
\`\`\`

## 📝 License

MIT License - see LICENSE file for details

---

Made with ❤️ for Inky Frame displays

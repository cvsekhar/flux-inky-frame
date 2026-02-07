# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-07

### Added
- Initial release of FLUX Inky Frame Image Generator
- FLUX.2-klein-4B model integration for image generation
- DSPy-powered prompt refinement using local LLMs (OpenAI-compatible)
- Dual image output: original (800×480) and rotated (480×800) for Inky Frame
- Web interface with three tabs: Generate, Gallery, Settings
- Real-time progress tracking with elapsed timer
- Gallery browser with image preview and metadata
- Individual image pair deletion
- Bulk cleanup functionality
- `/latest.jpg` endpoint for automated downloads
- Docker support with CPU and GPU configurations
- Volume management (named volumes and bind mounts)
- Comprehensive documentation:
  - README.md - Main project documentation
  - DOCKER.md - Docker setup and troubleshooting
  - LLM-SETUP.md - Local LLM configuration guide
- Example environment configuration (.env.example)
- uv-based dependency management
- Automatic model caching
- Image rotation and format conversion
- Seed randomization for varied outputs
- Guidance scale optimization (4.0)

### Technical Details
- Python 3.10 requirement
- Flask web framework
- PyTorch for model inference
- Diffusers for FLUX integration
- DSPy for LLM orchestration
- PIL for image processing
- Single-file Flask application
- Embedded HTML/CSS/JS (no templates directory)

### Configuration
- Configurable LLM endpoint (Ollama, LM Studio, vLLM, etc.)
- OpenAI-compatible API format
- Environment variable support
- Docker Compose configurations for different use cases

### Performance
- CPU mode: 30-120s per image
- GPU mode: 5-15s per image (optional)
- Prompt refinement: 2-5s (CPU) / 0.5-2s (GPU)
- Model size: ~8GB FLUX + ~3GB LLM
- Image quality: JPG at 70% quality

[1.0.0]: https://github.com/yourusername/flux-inky-frame/releases/tag/v1.0.0

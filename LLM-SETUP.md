# Local LLM Setup for Prompt Refinement

The app uses DSPy with an OpenAI-compatible local LLM to refine prompts before generating images.

## Quick Setup with Ollama (Recommended)

### 1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or visit: https://ollama.com/download
```

### 2. Pull a Model

```bash
# Small and fast (recommended)
ollama pull llama3.2

# Or other options
ollama pull llama3.1
ollama pull mistral
ollama pull qwen2.5
```

### 3. Verify Ollama is Running

```bash
# Ollama automatically provides OpenAI-compatible API
curl http://localhost:11434/v1/models
```

### 4. Run the App

The app will automatically connect to Ollama at `http://localhost:11434/v1`

```bash
# Local
uv run python app.py

# Docker
docker-compose up -d
```

## Configuration

The app uses OpenAI-compatible format:

```python
dspy.LM(
    model='openai/llama3.2',
    api_base='http://localhost:11434/v1',
    api_key='not-needed'
)
```

### Environment Variables

```bash
# .env file
LLM_API_BASE=http://localhost:11434/v1  # Note: /v1 suffix!
LLM_MODEL=llama3.2
```

## Alternative: LM Studio

### 1. Install LM Studio
Download from: https://lmstudio.ai/

### 2. Load a Model
- Open LM Studio
- Download a model (e.g., Llama 3.2)
- Start local server (port 1234)

### 3. Configure

```bash
# .env file
LLM_API_BASE=http://localhost:1234/v1
LLM_MODEL=local-model
```

## Alternative: vLLM

```bash
# Start vLLM server
vllm serve meta-llama/Llama-3.2-3B-Instruct --port 8000

# Configure
LLM_API_BASE=http://localhost:8000/v1
LLM_MODEL=meta-llama/Llama-3.2-3B-Instruct
```

## Alternative: Any OpenAI-Compatible API

Works with any endpoint that implements OpenAI's API format:
- LocalAI
- Text Generation WebUI (with `--api` flag)
- Anything with `/v1/chat/completions` endpoint

```bash
# .env file
LLM_API_BASE=http://your-server:port/v1
LLM_MODEL=your-model-name
```

## Docker Setup

If running in Docker and LLM on host:

```yaml
# docker-compose.yml
environment:
  - LLM_API_BASE=http://host.docker.internal:11434/v1
  - LLM_MODEL=llama3.2
```

## Verification

When you start the app, you should see:

```
🚀 Starting FLUX Image Generator for Inky Frame
Configuring DSPy with OpenAI-compatible LLM: llama3.2 at http://localhost:11434/v1
✓ DSPy initialized with OpenAI-compatible local LLM for prompt refinement
```

If LLM is not available:

```
⚠️  Failed to initialize DSPy: ...
⚠️  Prompt refinement disabled - will use original prompts
```

The app will still work, just without prompt refinement!

## Recommended Models

**For Speed (CPU):**
- `llama3.2` (3B) - Fast, good quality
- `mistral` (7B) - Balanced
- `qwen2.5:3b` - Very fast

**For Quality (GPU):**
- `llama3.1:8b` - Better quality
- `qwen2.5:14b` - Excellent quality
- `mistral:7b` - Good balance

## Performance

**Refinement times:**
- 3B model on CPU: 2-5 seconds
- 7B model on CPU: 5-15 seconds
- 3B model on GPU: 0.5-2 seconds
- 7B model on GPU: 1-3 seconds

Total generation time = Refinement + FLUX generation (~30-120s on CPU)

## Troubleshooting

### "Connection refused"
- Make sure Ollama is running: `ollama serve`
- Check: `curl http://localhost:11434/v1/models`
- **Important:** Use `/v1` suffix in the URL!

### "Model not found"
- Pull the model: `ollama pull llama3.2`
- List available: `ollama list`

### Docker can't reach host
- Use `host.docker.internal` instead of `localhost`
- Example: `http://host.docker.internal:11434/v1`

### Wrong API format
- Make sure your endpoint has `/v1` suffix
- Check if it supports OpenAI-compatible format
- Test: `curl http://localhost:11434/v1/models`

### Too slow
- Use a smaller model: `llama3.2` (3B)
- Or disable refinement (it will skip automatically if LLM fails)

## Testing Your Setup

```bash
# Test Ollama endpoint
curl http://localhost:11434/v1/models

# Should return JSON with available models
```

## OpenAI API Compatibility

The endpoint must support:
- `/v1/chat/completions` - Chat completions endpoint
- OpenAI message format
- Streaming (optional)

Most modern LLM servers support this out of the box!

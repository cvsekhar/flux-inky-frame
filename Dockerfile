FROM debian:bookworm-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal - uv will handle Python)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Set environment variables for better build behavior
ENV UV_LINK_MODE=copy
ENV RUST_BACKTRACE=1

# Copy project files
COPY pyproject.toml .
COPY .python-version .

# Let uv install Python and create venv with dependencies
# Use --no-cache to avoid filling up build cache with large packages
RUN uv sync --no-dev --no-cache

# Copy application code
COPY app.py .

# Create directories for volumes
RUN mkdir -p /app/generated_images && \
    mkdir -p /root/.cache/huggingface

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/root/.cache/huggingface

# Run the application with uv (uv manages Python)
CMD ["uv", "run", "app.py"]

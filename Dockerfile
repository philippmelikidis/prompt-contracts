# Dockerfile for prompt-contracts v0.3.1
# Provides fully reproducible environment for PCSL evaluation
FROM python:3.11.7-slim

LABEL maintainer="prompt-contracts team"
LABEL version="0.3.1"
LABEL description="Reproducible environment for prompt contract testing with fixed dependencies"

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies with pinned versions
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir --upgrade pip==24.0 && \
    pip install --no-cache-dir -r requirements.txt

# Install optional dependencies for v0.3.1 (pinned for reproducibility)
RUN pip install --no-cache-dir \
    sentence-transformers==2.2.2 \
    numpy==1.24.3 \
    torch==2.0.1

# Copy project files
COPY . /workspace/

# Install prompt-contracts in editable mode
RUN pip install -e .

# Set environment variables for reproducibility
ENV PYTHONUNBUFFERED=1
ENV PCSL_VERSION=0.3.1
ENV PYTHONHASHSEED=42
ENV OMP_NUM_THREADS=1
ENV TOKENIZERS_PARALLELISM=false

# Environment variables for API rate limiting
ENV OPENAI_MAX_RETRIES=3
ENV OPENAI_TIMEOUT=30
ENV OPENAI_RETRY_DELAY=1.0

# Default seed for all evaluations
ENV PCSL_DEFAULT_SEED=42

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD prompt-contracts --version || exit 1

# Default command
CMD ["prompt-contracts", "--help"]

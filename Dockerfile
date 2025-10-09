# Dockerfile for prompt-contracts v0.3.0
FROM python:3.11-slim

LABEL maintainer="prompt-contracts team"
LABEL version="0.3.0"
LABEL description="Reproducible environment for prompt contract testing"

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# Install optional dependencies for v0.3.0
RUN pip install --no-cache-dir \
    sentence-transformers==2.2.2 \
    numpy==1.24.3

# Copy project files
COPY . /workspace/

# Install prompt-contracts in editable mode
RUN pip install -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PCSL_VERSION=0.3.0

# Default command
CMD ["prompt-contracts", "--help"]

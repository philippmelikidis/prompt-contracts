# Dockerfile for Prompt Contracts v0.3.2
# Reproducible evaluation environment with pinned dependencies

FROM python:3.11.7-slim

# Set reproducibility environment variables
ENV PYTHONHASHSEED=42
ENV OMP_NUM_THREADS=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    make \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt setup.py pyproject.toml ./
COPY promptcontracts/ ./promptcontracts/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Copy examples and scripts
COPY examples/ ./examples/
COPY scripts/ ./scripts/
COPY Makefile ./

# Verify installation
RUN prompt-contracts --version

# Default command
CMD ["bash"]

# To build:
#   docker build -t prompt-contracts:0.3.2 .
#
# To run evaluation:
#   docker run --rm prompt-contracts:0.3.2 python scripts/run_full_evaluation.py
#
# To run interactive shell:
#   docker run --rm -it prompt-contracts:0.3.2

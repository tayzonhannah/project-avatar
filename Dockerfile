# Project Avatar: Containerized Environment for PJDSC 2026
# Base image: Python 3.12 Slim (Linux Debian Bookworm)
FROM python:3.12-slim

# Enforce non-interactive debian frontend and deterministic python runtime
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=42 \
    PORT=8501

# Install system dependencies (build-essential, git, curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install via pip with strict pinned versions
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code and data assets
COPY . /app/

# Expose Streamlit application port
EXPOSE 8501

# Healthcheck to ensure container availability
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command to run the interactive Streamlit dashboard
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]

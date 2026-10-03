# ============================================================
# JAHIZ Backend - Docker Image
# Multi-purpose: development + production
# ============================================================

FROM python:3.11-slim

# ---------- System dependencies ----------
# Prophet يحتاج build tools (gcc, g++, make)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- Working directory ----------
WORKDIR /app

# ---------- Python dependencies ----------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---------- Application code ----------
COPY app/ ./app/

# ---------- Generate synthetic data at build time ----------
RUN python -m app.data_generator

# ---------- Metadata ----------
LABEL org.opencontainers.image.title="JAHIZ Backend"
LABEL org.opencontainers.image.description="Instant SME Financing Readiness Engine"
LABEL org.opencontainers.image.version="0.1.0"

# ---------- Runtime ----------
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

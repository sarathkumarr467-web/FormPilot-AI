# ====================================================================
# FORMPILOT AI — PRODUCTION MULTI-STAGE DOCKERFILE
# ====================================================================

FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies for OCR and PDF processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmupdf-dev \
    tesseract-ocr \
    tesseract-ocr-tam \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run ML model training if model file does not exist
RUN if [ ! -f "ml/models/document_classifier.joblib" ]; then python ml/train.py; fi

# Create directories
RUN mkdir -p uploads generated static/images

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

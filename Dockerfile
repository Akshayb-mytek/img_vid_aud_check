FROM python:3.10-slim

# Install system deps (FFmpeg for video/audio, libgl for OpenCV)
RUN apt-get update && apt-get install -y ffmpeg libavcodec-extra libgl1 libglib2.0-0 \
    && apt-get clean

WORKDIR /app

# 👇 FIX 1: force numpy version BEFORE requirements
RUN pip install --no-cache-dir "numpy<2"

# Copy requirements
COPY requirements.txt .

# 👇 FIX 2: install CPU-only torch (avoid GPU junk)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install remaining deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Pre-download all AI models to bake them directly into the Docker image.
# This ensures zero-dependency, sub-second startup times in production.
RUN python scripts/download_models.py

# Expose the API port
EXPOSE 8000

# Start the application using Uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

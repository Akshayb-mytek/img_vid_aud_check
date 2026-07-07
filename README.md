# Unified AI Verification API

This repository contains a monolithic FastAPI microservice that consolidates Video Moderation, Audio Verification, and Photo KYC Verification into a single, high-performance deployment. It utilizes multiprocessing to manage CPU-intensive AI inferences (Whisper, InsightFace, NudeNet, Pyannote, etc.) without blocking the core event loop.

## Prerequisites

- **Python**: 3.10 to 3.12 (Do **not** use 3.13 or 3.14 as PyTorch/Torchaudio do not fully support them yet).
- **OS**: Windows, macOS, or Linux.
- **FFmpeg**: Required for audio processing, but handled automatically via setup scripts.

---

## Local Development Setup

We have provided simple bootstrap scripts to automatically handle your local environment, install dependencies, and download necessary binaries (like FFmpeg).

### 1. Clone the repository
```bash
git clone https://github.com/ashishjaiswal222/img_vid_aud_check.git
cd img_vid_aud_check
```

### 2. Run the Bootstrap Script
**On Windows:**
```powershell
# Open PowerShell and run:
.\setup.bat
```

**On Linux / macOS:**
```bash
bash setup.sh
```

*(This script will create a virtual environment, install all `requirements.txt` dependencies safely, download FFmpeg into a local `bin/` directory, and generate a `.env` file).*

### 3. Configure `.env`
Open the newly created `.env` file in the root directory and fill in the required values (like your HuggingFace token and AWS credentials).

### 4. Start the Server
Do **not** run `python main.py` directly. You must start the server using the Uvicorn ASGI server.

```bash
# Ensure your virtual environment is active, then run:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*(Note: On the first boot, the server will automatically download necessary AI models like `blaze_face_short_range.tflite` to `app/models/`. This might take a few minutes).*

---

## Production Deployment (Docker)

For production, this API is designed to run in a Docker container on AWS (or any cloud provider). The `Dockerfile` natively handles system-level dependencies like `libgl1` (for OpenCV) and `ffmpeg`.

### 1. Build the Docker Image
```bash
docker build -t unified-ai-api .
```

### 2. Run the Container
You must pass your `.env` variables to the container.
```bash
docker run -d --name ai-api -p 8000:8000 --env-file .env unified-ai-api
```

## API Documentation
Once the server is running, visit the interactive Swagger UI to test the endpoints:
- **Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

### Available Routes:
- `/moderation/analyze`: Video/Image moderation
- `/moderation/audio-verify/check`: Audio verification (speaker count, overlap, clarity)
- `/moderation/photo-verify/check-single`: Photo KYC validation (blur, lighting, spoofing, identity matching)

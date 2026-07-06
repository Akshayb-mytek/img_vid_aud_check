import os
import structlog
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.middleware.rate_limit import RateLimitMiddleware
from app.routes.moderation import moderation_router
from app.routes.audio import router as audio_router
from app.routes.photo import router as photo_router

# Setup structlog for unified logging
logger = structlog.get_logger()

# Audio Worker Pool
from app.services.audio.workers.pool import start_worker_pool as start_audio_pool, stop_worker_pool as stop_audio_pool

# Photo Worker Pool
from app.services.photo.workers.pool import get_pool as start_photo_pool, shutdown_pool as stop_photo_pool
import numpy as np

IS_PHOTO_READY = False

async def warmup_photo_pool():
    global IS_PHOTO_READY
    logger.info("Warming up photo worker pool with dummy inference...")
    pool = start_photo_pool()
    loop = asyncio.get_running_loop()
    
    dummy_img = np.zeros((480, 480, 3), dtype=np.uint8)
    dummy_img[:, :] = (255, 0, 0)
    
    import cv2
    _, encoded = cv2.imencode('.jpg', dummy_img)
    dummy_bytes = encoded.tobytes()
    
    from app.services.photo.pipeline import verify_image
    from app.config import settings
    
    try:
        tasks = []
        for _ in range(settings.photo_worker_pool_size):
            tasks.append(loop.run_in_executor(pool, verify_image, dummy_bytes, "image/jpeg", "front"))
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        logger.debug(f"Warmup inference completed with error: {e}")
        
    IS_PHOTO_READY = True
    logger.info("Photo Models are loaded. Photo Verification API is ready.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Unified API...")
    
    # 1. Start Audio Pool
    start_audio_pool()
    
    # 2. Start Photo Pool & Warmup
    start_photo_pool()
    asyncio.create_task(warmup_photo_pool())
    
    yield
    
    logger.info("Shutting down Unified API...")
    stop_audio_pool()
    stop_photo_pool()

app = FastAPI(
    title="Unified Moderation & Verification API",
    description="Monolithic API handling Video Moderation, Audio Verification, and Photo Verification.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(RateLimitMiddleware)

# Existing Moderation Routes (/moderation/analyze, /moderation/health)
app.include_router(moderation_router)

# Ported Audio Routes
app.include_router(audio_router, prefix="/moderation/audio-verify", tags=["Audio Verification"])

# Ported Photo Routes
app.include_router(photo_router, prefix="/moderation/photo-verify", tags=["Photo Verification"])

@app.get("/health")
def health():
    return {"status": "ok", "photo_api_ready": IS_PHOTO_READY}
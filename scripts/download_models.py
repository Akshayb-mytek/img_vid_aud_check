import os

print("--- Pre-downloading Photo API Models ---")
try:
    from app.services.photo.models_loader import MediaPipeModels
    # We instantiate the class directly to trigger _load_models() which downloads everything
    MediaPipeModels()
    print("Photo models downloaded successfully.")
except Exception as e:
    print(f"Warning: Photo models warmup encountered an issue (can be ignored if non-critical): {e}")

print("--- Pre-downloading Audio API Models ---")
try:
    from app.services.audio.models_loader import init_worker_models
    init_worker_models()
    print("Audio models downloaded successfully.")
except Exception as e:
    print(f"Warning: Audio models warmup encountered an issue (HF_TOKEN missing is normal): {e}")

print("All pre-downloads complete!")

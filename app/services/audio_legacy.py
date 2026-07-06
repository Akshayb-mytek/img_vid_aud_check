import os
import whisper

# ✅ ADD THIS (must be before loading model)
# FFMPEG_DIR = r"C:\ffmpeg\ffmpeg-2026-04-22-git-162ad61486-essentials_build\bin"
# os.environ["PATH"] = FFMPEG_DIR + os.pathsep + os.environ["PATH"]

model = whisper.load_model("base")

def speech_to_text(audio_path):
    if not os.path.exists(audio_path):
        return ""

    result = model.transcribe(audio_path)
    return result["text"]

import cv2
import os
import subprocess

def extract_frames(video_path, output_dir, frames_per_second=10):
    frame_dir = os.path.join(output_dir, "frames")
    os.makedirs(frame_dir, exist_ok=True)

    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS) or 1

    interval = int(fps / frames_per_second)
    if interval <= 0:
        interval = 1

    count = 0
    frames = []

    success, image = vidcap.read()
    while success:
        if count % interval == 0:
            frame_path = os.path.join(frame_dir, f"frame_{count}.jpg")
            cv2.imwrite(frame_path, image)
            frames.append(frame_path)

        success, image = vidcap.read()
        count += 1

    return frames


def extract_audio(video_path):
    audio_path = video_path.rsplit(".", 1)[0] + ".wav"

    # FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-2026-04-22-git-162ad61486-essentials_build\bin\ffmpeg.exe"  # adjust if different

    command = [
    # FFMPEG_PATH,
    "-y",
    "-i", video_path,
    "-q:a", "0",
    "-map", "a",
    audio_path
]

    subprocess.run(command)

    return audio_path

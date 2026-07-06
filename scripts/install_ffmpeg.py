import os
import urllib.request
import zipfile
import shutil
import sys

def install_ffmpeg():
    print("Starting FFmpeg installation for Windows...")
    
    # Define paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bin_dir = os.path.join(project_root, 'bin')
    
    if os.path.exists(os.path.join(bin_dir, 'ffmpeg.exe')) and os.path.exists(os.path.join(bin_dir, 'ffprobe.exe')):
        print("✅ FFmpeg is already installed in the 'bin' folder!")
        return

    os.makedirs(bin_dir, exist_ok=True)
    zip_path = os.path.join(bin_dir, 'ffmpeg.zip')

    # Download from gyan.dev (standard Windows build)
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    print(f"Downloading FFmpeg from {url} ... (This may take a minute)")
    
    try:
        urllib.request.urlretrieve(url, zip_path)
    except Exception as e:
        print(f"❌ Failed to download FFmpeg: {e}")
        sys.exit(1)
        
    print("Download complete. Extracting...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(bin_dir)
            
        # Find the extracted folder (usually named ffmpeg-xxx-essentials_build)
        extracted_folder = None
        for item in os.listdir(bin_dir):
            if item.startswith('ffmpeg') and os.path.isdir(os.path.join(bin_dir, item)):
                extracted_folder = os.path.join(bin_dir, item)
                break
                
        if extracted_folder:
            # Move ffmpeg.exe and ffprobe.exe to the bin directory
            ffmpeg_exe = os.path.join(extracted_folder, 'bin', 'ffmpeg.exe')
            ffprobe_exe = os.path.join(extracted_folder, 'bin', 'ffprobe.exe')
            
            if os.path.exists(ffmpeg_exe):
                shutil.move(ffmpeg_exe, os.path.join(bin_dir, 'ffmpeg.exe'))
            if os.path.exists(ffprobe_exe):
                shutil.move(ffprobe_exe, os.path.join(bin_dir, 'ffprobe.exe'))
                
            # Cleanup
            shutil.rmtree(extracted_folder)
            os.remove(zip_path)
            print("✅ FFmpeg installed successfully in the 'bin' directory!")
        else:
            print("❌ Could not find extracted FFmpeg folder.")
            
    except Exception as e:
        print(f"❌ Failed to extract FFmpeg: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_ffmpeg()

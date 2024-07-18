import subprocess
import os

def extract_audio(video_path, audio_path):
    command = f'ffmpeg -i "{video_path}" -q:a 0 -map a "{audio_path}"'
    subprocess.run(command, shell=True, check=True)

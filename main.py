import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from translate import translate_srt_file
from video_downloader import download_video
from audio_extractor import extract_audio
from transcriber import transcribe_audio
from merge_subtitles import merge_video_and_subtitles, sanitize_filename, to_latin
import os
import tempfile
import shutil
import logging

logging.basicConfig(level=logging.INFO)

def process_video():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return

    target_language = language_combobox.get().split(' - ')[0]
    translation_service = service_combobox.get()
    if not target_language:
        messagebox.showwarning("Input Error", "Please select a target language.")
        return

    try:
        # Prepare paths
        output_folder = "output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        video_info = download_video(url, os.path.join(output_folder, "downloaded_video.mp4"))
        video_title = sanitize_filename(video_info.get('title', 'downloaded_video'))
        
        video_folder = os.path.join(output_folder, video_title)
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)

        video_path = os.path.join(video_folder, f"{video_title}.mp4")
        audio_path = os.path.join(video_folder, f"{video_title}.mp3")
        transcript_path = os.path.join(video_folder, "transcript")

        logging.info(f"Video path: {video_path}")
        logging.info(f"Audio path: {audio_path}")
        logging.info(f"Transcript path: {transcript_path}")

        # Download video
        download_video(url, video_path)
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found at {video_path}")

        # Extract audio and transcribe
        extract_audio(video_path, audio_path)
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio not found at {audio_path}")

        transcribe_audio(audio_path, transcript_path)
        if not os.path.exists(f"{transcript_path}.srt"):
            raise FileNotFoundError(f"Transcript not found at {transcript_path}.srt")

        # Translate the SRT file
        translated_srt_path, full_translated_content = translate_srt_file(f"{transcript_path}.srt", target_language, translation_service)
        if not os.path.exists(translated_srt_path):
            raise FileNotFoundError(f"Translated SRT not found at {translated_srt_path}")
        
        # Merge the translated subtitles with the video
        output_video_path = os.path.join(video_folder, f"{video_title}_with_subtitles.mp4")
        logging.info(f"Merging video {video_path} with subtitles {translated_srt_path} into {output_video_path}")
        merge_video_and_subtitles(video_path, translated_srt_path, output_video_path)

        messagebox.showinfo("Success", f"File translated and merged successfully and saved as {output_video_path}")

        # Display translated content in the console
        print("Translated Content:")
        print(full_translated_content)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print("Error:", e)

root = tk.Tk()
root.title("SRT Translator and Video Processor")

# Enhance UI
root.configure(bg="#f0f0f0")
root.geometry("400x450")

url_label = tk.Label(root, text="Enter video URL:", bg="#f0f0f0", font=("Helvetica", 10))
url_label.pack(pady=(20, 0))

url_entry = tk.Entry(root, font=("Helvetica", 10), width=50)
url_entry.pack(pady=10)

language_label = tk.Label(root, text="Select target language:", bg="#f0f0f0", font=("Helvetica", 10))
language_label.pack(pady=(20, 0))

language_combobox = Combobox(root, values=[
    "FR - French",
    "ES - Spanish",
    "DE - German",
    "IT - Italian",
    "ZH - Chinese",
    "JA - Japanese",
    "RU - Russian",
    "NL - Dutch",
    "PT - Portuguese",
    "AR - Arabic",
    "HI - Hindi",
    "KO - Korean",
    "TR - Turkish"
], font=("Helvetica", 10))
language_combobox.pack(pady=10)

service_label = tk.Label(root, text="Select translation service:", bg="#f0f0f0", font=("Helvetica", 10))
service_label.pack(pady=(20, 0))

service_combobox = Combobox(root, values=["ChatGPT", "DeepL"], font=("Helvetica", 10))
service_combobox.pack(pady=10)

process_button = tk.Button(root, text="Process Video", command=process_video, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=10)
process_button.pack(pady=20)

root.mainloop()

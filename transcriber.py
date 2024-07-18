import subprocess
import json
import os

def transcribe_audio(audio_path, transcript_path, model_name='openai/whisper-large-v3', use_flash=False):
    # Run the transcription
    command = f'insanely-fast-whisper --file-name "{audio_path}" --transcript-path "{transcript_path}.json" --model-name {model_name}'
    if use_flash:
        command += " --flash True"
    subprocess.run(command, shell=True, check=True)
    
    # Convert JSON transcript to SRT format
    with open(f"{transcript_path}.json", 'r', encoding='utf-8') as f:
        transcript = json.load(f)

    if 'chunks' not in transcript:
        print("Transcription JSON content:", transcript)  # Print the entire JSON content for debugging
        raise ValueError("The transcription output does not contain 'chunks'")

    with open(f"{transcript_path}.srt", 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(transcript['chunks']):
            start = format_time(chunk['timestamp'][0])
            end = format_time(chunk['timestamp'][1])
            text = chunk['text']
            f.write(f"{i + 1}\n{start} --> {end}\n{text}\n")

def format_time(seconds):
    """ Convert seconds to SRT time format """
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

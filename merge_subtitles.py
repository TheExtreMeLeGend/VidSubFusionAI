import subprocess
import os
import shutil
import logging
import tempfile
import unicodedata

logging.basicConfig(level=logging.INFO)

def to_latin(input_str):
    return unicodedata.normalize('NFKD', input_str).encode('ascii', 'ignore').decode('ascii')

def merge_video_and_subtitles(video_path, srt_path, output_path):
    logging.info(f"Merging video {video_path} with subtitles {srt_path} into {output_path}")

    # Vérifiez l'existence des fichiers avant de les copier
    if not os.path.exists(video_path):
        logging.error(f"Video file not found: {video_path}")
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if not os.path.exists(srt_path):
        logging.error(f"Subtitle file not found: {srt_path}")
        raise FileNotFoundError(f"Subtitle file not found: {srt_path}")

    # Temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Simplified temporary paths
        temp_video_path = os.path.join(temp_dir, "temp_video.mp4")
        temp_srt_path = os.path.join(temp_dir, "temp_subs.srt")
        temp_output_path = os.path.join(temp_dir, "temp_output.mp4")

        logging.info(f"Copying video to temporary path: {temp_video_path}")
        logging.info(f"Copying subtitles to temporary path: {temp_srt_path}")

        # Copy files to temporary paths
        try:
            shutil.copyfile(video_path, temp_video_path)
            shutil.copyfile(srt_path, temp_srt_path)
        except FileNotFoundError as e:
            logging.error(f"Error copying file: {e}")
            raise

        # Ensure files exist before proceeding
        if not os.path.exists(temp_video_path):
            logging.error(f"Temporary video file not found: {temp_video_path}")
            raise FileNotFoundError(f"Temporary video file not found: {temp_video_path}")

        if not os.path.exists(temp_srt_path):
            logging.error(f"Temporary subtitle file not found: {temp_srt_path}")
            raise FileNotFoundError(f"Temporary subtitle file not found: {temp_srt_path}")

        logging.info(f"Temporary video path: {temp_video_path}")
        logging.info(f"Temporary subtitles path: {temp_srt_path}")

        # Additional verification for readability
        try:
            with open(temp_video_path, 'rb') as f:
                pass
            with open(temp_srt_path, 'r', encoding='utf-8') as f:
                pass
        except Exception as e:
            logging.error(f"File read error: {e}")
            raise

        # HandBrakeCLI command
        command = [
            'HandBrakeCLI',
            '-i', temp_video_path,
            '-o', temp_output_path,
            '--srt-file', temp_srt_path,
            '--srt-codeset', 'UTF-8',
            '--srt-default'
        ]

        logging.info(f"Running command: {' '.join(command)}")

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logging.info("HandBrakeCLI output:")
            logging.info(result.stdout)
            logging.info("HandBrakeCLI errors:")
            logging.info(result.stderr)

            # Ensure the output file was created
            if not os.path.exists(temp_output_path):
                logging.error(f"Temporary output file not created: {temp_output_path}")
                raise FileNotFoundError(f"Temporary output file not created: {temp_output_path}")

            # Move the output file to the desired location
            shutil.move(temp_output_path, output_path)
            logging.info(f"Successfully merged video and subtitles. Output: {output_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error: {e}")
            logging.error("HandBrakeCLI output:")
            logging.error(e.stdout)
            logging.error("HandBrakeCLI errors:")
            logging.error(e.stderr)
            raise e

def sanitize_filename(filename):
    return "".join(c if c.isalnum() or c in " ._-()" else "_" for c in filename)

# Example usage
if __name__ == "__main__":
    video_path = os.path.abspath("output/359 - هداية التوفيق والإلهام - عثمان الخميس/359 - هداية التوفيق والإلهام - عثمان الخميس.mp4")
    srt_path = os.path.abspath("output/359 - هداية التوفيق والإلهام - عثمان الخميس/transcript_translated_to_FR.srt")
    output_path = os.path.abspath("output/359 - هداية التوفيق والإلهام - عثمان الخميس/359 - هداية التوفيق والإلهام - عثمان الخميس_with_subtitles.mp4")

    merge_video_and_subtitles(video_path, srt_path, output_path)

VidSubFusionAI aaaaaaaa
VidSubFusionAI is a comprehensive tool for downloading YouTube videos, transcribing audio, translating subtitles using AI services like DeepL and ChatGPT, and merging these subtitles back into the video.

Features
Download YouTube Videos: Easily download videos from YouTube in the best available quality.
Transcribe Audio: Convert audio from the downloaded video into text using Whisper.
Translate Subtitles: Translate the transcribed text into multiple languages using DeepL or ChatGPT.
Merge Subtitles: Integrate the translated subtitles back into the video, creating a seamless viewing experience.
Requirements
Python 3.6 or higher
yt-dlp for downloading YouTube videos
ffmpeg for video processing
openai and deepl for translation services
tkinter for the graphical user interface
Installation
Clone the repository:

bash
Copier le code
git clone https://github.com/yourusername/VidSubFusionAI.git
cd VidSubFusionAI
Install the required packages:

bash
Copier le code
pip install -r requirements.txt
Install ffmpeg:

Windows: Download from ffmpeg.org and add to PATH.
Mac: Use Homebrew
bash
Copier le code
brew install ffmpeg
Linux: Use your distribution's package manager
bash
Copier le code
sudo apt-get install ffmpeg
Usage
Run the application:

bash
Copier le code
python main.py
Enter the YouTube video URL in the provided field.

Select the target language for translation.

Choose the translation service (DeepL or ChatGPT).

Click "Process Video" to start the downloading, transcribing, translating, and merging process.

Current Issue
We are currently facing an issue with merging the translated subtitles back into the video. The FFmpeg command used for this process returns an error related to input file handling. We suspect this might be due to the handling of special characters in file paths or other encoding issues.

The error message is as follows:

swift
Copier le code
Error: Command '['ffmpeg', '-i', 'C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\tmpbg5wg8wi\\temp_video.mp4', '-vf', "subtitles='C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\tmpbg5wg8wi\\temp_subs.srt':force_style='Fontname=Arial,Fontsize=24'", '-c:a', 'copy', "'C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\tmpbg5wg8wi\\temp_output.mp4'"]' returned non-zero exit status 4294967274.
Seeking Help
This project has been largely developed with the assistance of ChatGPT. We are seeking contributions and expertise to resolve the subtitle merging issue and improve the overall functionality of the software. If you have experience with FFmpeg, Python, or handling subtitle files, your help would be greatly appreciated.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any questions or suggestions, feel free to open an issue or contact us at your.email@example.com.

Feel free to customize the above README as per your specific needs and details.

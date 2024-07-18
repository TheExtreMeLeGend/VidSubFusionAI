import openai
import deepl
import re
import os

# Configure your OpenAI API key
#openai.api_key = 'OPEIN-AI-APIKEY'
# Configure your DeepL API key
#deepl_auth_key = 'DEEPL-API-KEY'
deepl_translator = deepl.Translator(deepl_auth_key)

def split_srt_file(file_path, max_segments=12):
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    # Split the content by each subtitle entry
    segments = re.split(r'(\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n)', srt_content)
    temp_files = []
    chunk = ''
    count = 0
    file_index = 0

    for i in range(1, len(segments), 3):
        if count >= max_segments:
            temp_file_path = f"temp_srt_part_{file_index}.srt"
            with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                temp_file.write(chunk)
            temp_files.append(temp_file_path)
            chunk = ''
            count = 0
            file_index += 1
        if i + 1 < len(segments):
            chunk += segments[i-1] + segments[i] + segments[i+1]
            count += 1

    if chunk:
        temp_file_path = f"temp_srt_part_{file_index}.srt"
        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(chunk)
        temp_files.append(temp_file_path)

    return temp_files

def translate_content(content, target_language, translation_service):
    def extract_timecodes_and_text(content):
        pattern = r'(\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n)(.*?)(?=\n\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches

    def reconstruct_content(translations):
        return '\n\n'.join([''.join(pair) for pair in translations])

    segments = extract_timecodes_and_text(content)
    translated_segments = []

    for timecode, text in segments:
        if translation_service == "ChatGPT":
            prompt = f"Translate the following text to {target_language}. Please ensure the translation is accurate and maintains the original meaning. Do not include any additional comments, explanations, or formatting. Keep the timecodes intact and ensure the translation is seamless. Only provide the translation in the target language:\n\n{text.strip()}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a translator."},
                    {"role": "user", "content": prompt}
                ]
            )
            translated_text = response.choices[0].message["content"].strip()
        elif translation_service == "DeepL":
            result = deepl_translator.translate_text(text.strip(), target_lang=target_language)
            translated_text = result.text
        
        translated_segments.append((timecode, translated_text + '\n'))

    return reconstruct_content(translated_segments)

def translate_srt_file(file_path, target_language, translation_service):
    try:
        temp_files = split_srt_file(file_path)
        translated_chunks = []

        for temp_file in temp_files:
            with open(temp_file, 'r', encoding='utf-8') as file:
                content = file.read()
            translated_content = translate_content(content, target_language, translation_service)
            translated_chunks.append(translated_content)
            os.remove(temp_file)

        # Combine all translated chunks
        full_translated_content = '\n\n'.join(translated_chunks)

        output_file_path = os.path.splitext(file_path)[0] + f'_translated_to_{target_language}.srt'
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(full_translated_content)

        return output_file_path, full_translated_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

import os
from google.genai import types

try:
    os.environ["DEBIL_TOKEN"]
except KeyError:
    print("Config variable \"DEBIL_TOKEN\" is unreachable. Please, add this!")
    exit()

ffmpeg_path = {
    "windows": r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
    "linux": "ffmpeg"
}

settings = {
    "token": os.environ["DEBIL_TOKEN"],
    "prefix": 'd.',
    "bot_status": "Юзай /",
    "main_embed_color": 0xf0cd4f,
    "path_to_ffmpeg": ffmpeg_path.get('linux'),
    "deno_path": "deno",
    "emojis": {'wuuut': 518051242807787520,
               'youtube': 878537811601555466,
               'stonks': 879411306157985862,
               'squid_cleaning': 880326444356612116}, # Replace this dict values to your Emoji Id's.
}

YDL_OPTIONS = {'format': 'bestaudio',
               'noplaylist': 'True',
               'quiet': True,
               'extractor_args': {"youtube:player-client": "web_embedded,web,tv",
                                  "youtube:player_js_version": "actual"},
               'js-runtimes': f"deno:{settings.get('deno_path')}" # idk if u need to use this
               }
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                  'options': '-vn'}

google_ai_settings = {
    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    "google_api_key": os.environ.get("GOOGLE_API_KEY"), # https://aistudio.google.com/app/apikey
    "gemini_model": "gemini-3.6-flash", # Recommend to use flash models
    "config": types.GenerateContentConfig(
        temperature = 0.9,
        top_p = 1,
        top_k = 0,
        max_output_tokens = 1700,
        response_mime_type = "text/plain",
        safety_settings = [
            types.SafetySetting(
                category = 'HARM_CATEGORY_HATE_SPEECH',
                threshold = 'BLOCK_ONLY_HIGH'
            ),
        ]
    )
}
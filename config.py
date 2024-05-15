import os
import discord

try:
    os.environ['DEBIL_TOKEN']
except KeyError:
    print('Config variable "DEBIL_TOKEN" is unreachable. Please, add this!')
    exit()

path = {
    'windows': r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
    'linux': 'ffmpeg'
}

settings = {
    'token': os.environ['DEBIL_TOKEN'],
    'prefix': 'd.',
    'path_to_ffmpeg': path.get('linux'), # If u are use Windows, type path.get('windows') and type path to the ffmpeg, else if u are use Linux, or Heroku, type path.get('linux')
    'emojis': {'wuuut': 518051242807787520,
               'youtube': 878537811601555466,
               'stonks': 879411306157985862,
               'squid_cleaning': 880326444356612116}, # Replace this dict values to your Emoji Id's.
}
google_ai_settings = {
    'google_api_key': os.environ.get("GOOGLE_API_KEY"), # https://aistudio.google.com/app/apikey
    # Create the model
    # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
    "generation_config": {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 0,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    },
    "safety_settings": [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]
}
import os

try:
    os.environ['DEBIL_TOKEN']
except KeyError:
    print('Config variable "DEBIL_TOKEN" is unreachable. Please, add this!')
    exit()

settings = {
    'token': os.environ['DEBIL_TOKEN'],
    'prefix': 'd.',
    'path_to_ffmpeg': r'C:\Program Files\ffmpeg\bin\ffmpeg.exe', # Path to ffmpeg. For Linux users just type "ffmpeg"
}
import os

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
    'path_to_ffmpeg': path.get('linux') # If u are use Windows, type path.get('windows') and type path to the ffmpeg, else if u are use Linux, or Heroku, type path.get('linux')
}
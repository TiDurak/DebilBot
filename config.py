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
    'emojis': {'wuuut': 518051242807787520, 'youtube': 878537811601555466,
               'stonks': 879411306157985862, 'squid_cleaning': 880326444356612116}, # Replace this dict values to your Emoji Id's.
    'activities': [discord.Activity(type=discord.ActivityType.watching, name="зомбоящик"),
                   discord.Activity(type=discord.ActivityType.watching, name="на пизду"),
                   discord.Activity(type=discord.ActivityType.watching, name="и охуевает"),
                   discord.Activity(type=discord.ActivityType.watching, name="какой у тебя маленький хуй"),
                   discord.Activity(type=discord.ActivityType.watching, name="на глистов у тебя в жопе"),
                   discord.Activity(type=discord.ActivityType.listening, name="ровный базар"),
                   discord.Activity(type=discord.ActivityType.listening, name="моргенчлена, твоего батю блядь"),
                   discord.Activity(type=discord.ActivityType.watching, name="поруху с собакой"),
                   discord.Game(name="игру"),
                   discord.Game(name="ебанину нахуй")]
}

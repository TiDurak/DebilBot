from cogs import converters
from cogs import games
from cogs import help
from cogs import moderation
from cogs import music
from cogs import listeners
from cogs import text
from config import settings
import sys

from rich import print


from discord.ext import commands
from discord_components import DiscordComponents

print(f'[b yellow] Python {sys.version}')

bot = commands.Bot(command_prefix = settings['prefix'])
DiscordComponents(bot)

converters.setup(bot)
print('[blue] converters.py file has been loaded!')

games.setup(bot)
print('[blue] games.py file has been loaded!')

help.setup(bot)
print('[blue] help.py file has been loaded!')

moderation.setup(bot)
print('[blue] moderation.py file has been loaded!')

music.setup(bot)
print('[blue] music.py file has been loaded!')

listeners.setup(bot)
print('[blue] listeners.py file has been loaded!')

text.setup(bot)
print('[blue] text.py file has been loaded!')

print('[b i blue] All cogs has been loaded. Starting...')

bot.run(settings['token'])
from cogs import converters, fun, help, moderation, information, music, listeners, text
from config import settings
import sys
import asyncio

from rich import print

from discord import Intents
from discord.ext import commands

print(f'[b yellow]Python {sys.version}')

intents = Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

asyncio.run(converters.setup(bot))
print('[blue]converters.py file has been loaded!')

asyncio.run(fun.setup(bot))
print('[blue]fun.py file has been loaded!')

asyncio.run(help.setup(bot))
print('[blue]help.py file has been loaded!')

asyncio.run(moderation.setup(bot))
print('[blue]moderation.py file has been loaded!')

asyncio.run(information.setup(bot))
print('[blue]information.py file has been loaded!')

asyncio.run(music.setup(bot, intents))
print('[blue]music.py file has been loaded!')

asyncio.run(listeners.setup(bot))
print('[blue]listeners.py file has been loaded!')

asyncio.run(text.setup(bot))
print('[blue]text.py file has been loaded!')

print('[b i blue]All cogs has been loaded. Starting...')

bot.run(settings['token'])

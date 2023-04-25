from cogs import converters, fun, help, moderation, information, music, listeners, text, slash
from config import settings
import sys
import asyncio

from rich import print

from discord import Intents, app_commands
from discord.ext import commands

print(f'[b yellow]Python {sys.version}')

intents = Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

asyncio.run(converters.setup(bot))
asyncio.run(fun.setup(bot))
asyncio.run(help.setup(bot))
asyncio.run(moderation.setup(bot))
asyncio.run(information.setup(bot))
asyncio.run(music.setup(bot, intents))
asyncio.run(listeners.setup(bot))
asyncio.run(text.setup(bot))
asyncio.run(slash.setup(bot))

print("[b i blue]Starting a bot. It may take a few seconds")

bot.run(settings["token"])

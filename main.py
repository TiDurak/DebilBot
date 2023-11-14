from cogs import converters, fun, help, moderation, information, music, listeners, text
from cogs.context_menu import c_fun, c_information
from cogs.slash import s_fun, s_text, s_music, s_moderation, s_converters
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
asyncio.run(music.setup(bot))
asyncio.run(listeners.setup(bot))
asyncio.run(text.setup(bot))
asyncio.run(c_fun.setup(bot))
asyncio.run(c_information.setup(bot))
asyncio.run(s_fun.setup(bot))
asyncio.run(s_text.setup(bot))
asyncio.run(s_music.setup(bot))
asyncio.run(s_moderation.setup(bot))
asyncio.run(s_converters.setup(bot))

print("[b i blue]Starting a bot. It may take a few seconds")

bot.run(settings["token"])

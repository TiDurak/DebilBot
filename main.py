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

basic_cogs = [converters.setup(bot), fun.setup(bot), help.setup(bot), moderation.setup(bot),
              information.setup(bot), music.setup(bot), listeners.setup(bot), text.setup(bot)]
slash_cogs = [s_fun.setup(bot), s_text.setup(bot), s_music.setup(bot), s_moderation.setup(bot),
              s_converters.setup(bot)]
context_menu_cogs = [c_fun.setup(bot), c_information.setup(bot)]
cogs_array = [basic_cogs, slash_cogs, context_menu_cogs]
for array in cogs_array:
    for cog in array:
        asyncio.run(cog)

print("[b i blue]Starting a bot. It may take a few seconds")

bot.run(settings["token"])

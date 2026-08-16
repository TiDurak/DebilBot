from cogs import listeners
from cogs.context_menu import c_fun, c_information, c_reputation
from cogs.slash import s_fun, s_text, s_music, s_moderation, s_information, s_converters, s_reputation
from config import settings
from classes import reputation

import sys
import asyncio

from rich import print

from discord import Intents, app_commands
from discord.ext import commands

print(f'[b yellow]Python {sys.version}')

intents = Intents.default()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

rep = reputation.Reputation()
asyncio.run(rep.initialize())

basic_cogs = [listeners.setup(bot)]

slash_cogs = [s_fun.setup(bot),
              s_text.setup(bot),
              s_music.setup(bot),
              s_information.setup(bot),
              s_moderation.setup(bot),
              s_converters.setup(bot),
              s_reputation.setup(bot, rep),
              ]

context_menu_cogs = [c_fun.setup(bot),
                     c_information.setup(bot),
                     c_reputation.setup(bot, rep)]

cogs_array = [basic_cogs,
              slash_cogs,
              context_menu_cogs]

for array in cogs_array:
    for cog in array:
        asyncio.run(cog)

print("[b i blue]Starting a bot. It may take a few seconds")

bot.run(settings["token"])

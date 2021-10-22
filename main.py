import converters
import games
import help_command
import moderation
import music_bot
import listeners
import text_commands
from config import settings

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CommandNotFound, MissingPermissions, CommandInvokeError, MemberNotFound, BotMissingPermissions
from discord_components import DiscordComponents


bot = commands.Bot(command_prefix = settings['prefix'])
DiscordComponents(bot)

converter = converters.Convert(bot)
converters.setup(bot)

games_cog = games.Games(bot)
games.setup(bot)

help = help_command.Help(bot)
help_command.setup(bot)

moder = moderation.Moderation(bot)
moderation.setup(bot)

music = music_bot.Music(bot)
music_bot.setup(bot)

statchanger = listeners.StatChanger(bot)
listeners.setup(bot)

text = text_commands.Text(bot)
text_commands.setup(bot)

bot.run(settings['token'])
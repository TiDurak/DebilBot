import converters
import games
import help_command
import moderation
import music_bot
import listeners
import text_commands
from config import settings

from rich import print

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CommandNotFound, MissingPermissions, CommandInvokeError, MemberNotFound, BotMissingPermissions
from discord_components import DiscordComponents

print('[b blue] All modules has been loaded!')

bot = commands.Bot(command_prefix = settings['prefix'])
DiscordComponents(bot)

converter = converters.Convert(bot)
converters.setup(bot)
print('[blue] converters.py file has been loaded!')

games_cog = games.Games(bot)
games.setup(bot)
print('[blue] games.py file has been loaded!')

help = help_command.Help(bot)
help_command.setup(bot)
print('[blue] help_command.py file has been loaded!')

moder = moderation.Moderation(bot)
moderation.setup(bot)
print('[blue] moderation.py file has been loaded!')

music = music_bot.Music(bot)
music_bot.setup(bot)
print('[blue] music_bot.py file has been loaded!')

error_listener = listeners.ErrorListener(bot)
on_ready_listener = listeners.OnReady(bot)
listeners.setup(bot)
print('[blue] listeners.py file has been loaded!')

text = text_commands.Text(bot)
text_commands.setup(bot)
print('[blue] text_commands.py file has been loaded!')

print('[b i blue] All files has been loaded. Starting...')

bot.run(settings['token'])
from config import settings
import converters
import games
import help_command
import moderation
import music_bot
import listeners
import text_commands

### Discord Libs ###
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CommandNotFound, MissingPermissions, CommandInvokeError, MemberNotFound, BotMissingPermissions

from discord_components import DiscordComponents
### Discord Libs ###


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

### Errors catching ###
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('❌ Комманда не существует!')
    elif isinstance(error, MissingPermissions):
        await ctx.send('❌ У вас нету привилегий управления сообщениями!')
    elif isinstance(error, MemberNotFound):
        await ctx.send('❌ Участник не найден!')
### Errors catching ###


bot.run(settings['token'])
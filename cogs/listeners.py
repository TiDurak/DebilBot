import random
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MemberNotFound, MissingRequiredArgument
from rich import print
from config import settings

class ErrorListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send('❌ Комманда не существует! Ты вообще можешь хоть что-то правильно сделать, а?')
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f'❌ Не, ну ты внатуре дебил. Ты не ввёл нужные аргументы. введи `{settings.get("prefix")}help твоя_команда`! Например: d.help poll')
        elif isinstance(error, MissingPermissions):
            await ctx.send('❌ У тебя нету привилегий управления сообщениями, бомжара!')
        elif isinstance(error, MemberNotFound):
            await ctx.send('❌ Участник не найден, кретин!')
        else:
            raise error

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('[b green] Bot is ready! Just type d.help to see all bot commands.')
        while True:
            activity = random.choice(settings['activities'])
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            await asyncio.sleep(5)
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f"{settings.get('prefix')}help"))
            await asyncio.sleep(5)

async def setup(bot):
    await bot.add_cog(ErrorListener(bot))
    await bot.add_cog(OnReady(bot))
import random
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MemberNotFound
from rich import print
from config import settings

class ErrorListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send('❌ Комманда не существует!')
        elif isinstance(error, MissingPermissions):
            await ctx.send('❌ У вас нету привилегий управления сообщениями!')
        elif isinstance(error, MemberNotFound):
            await ctx.send('❌ Участник не найден!')
        else:
            raise error

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('[b green] Bot is ready! Just type d.help to see all bot commands.')
        activities = [discord.Activity(type=discord.ActivityType.watching, name="зомбоящик"),
                      discord.Activity(type=discord.ActivityType.watching, name="на писюны"),
                      discord.Activity(type=discord.ActivityType.listening, name="ровный базар"),
                      discord.Activity(type=discord.ActivityType.watching, name="порнушку"),
                      discord.Game(name="игру")]
        while True:
            activity = activities[random.randint(0, 4)]
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            await asyncio.sleep(5)
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(f"{settings.get('prefix')}help"))
            await asyncio.sleep(5)

def setup(bot):
    bot.add_cog(ErrorListener(bot))
    bot.add_cog(OnReady(bot))
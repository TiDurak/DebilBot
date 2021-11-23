import random
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MemberNotFound
from rich import print

class ErrorListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send('❌ Комманда не существует!')
        elif isinstance(error, MissingPermissions):
            await ctx.send('❌ У вас нету привилегий управления сообщениями!')
        elif isinstance(error, MemberNotFound):
            await ctx.send('❌ Участник не найден!')


class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('[b green] Bot is ready! Just type d.help to see all bot commands.')
        while True:
            RandomInteger = random.randint(0, 4)

            if RandomInteger == 0:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ровный базар"))
            elif RandomInteger == 1:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="порнушку"))
            elif RandomInteger == 2:
                await self.bot.change_presence(activity=discord.Game(name="игру"))
            elif RandomInteger == 3:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="зомбоящик"))
            elif RandomInteger == 4:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="на писюны"))


            await asyncio.sleep(5)
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Game("d.help"))
            await asyncio.sleep(5)

def setup(bot):
    bot.add_cog(ErrorListener(bot))
    bot.add_cog(OnReady(bot))
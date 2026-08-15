import discord
from discord.ext import commands
from rich import print
from config import settings

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

        print('[b green]Bot is ready to fuk ur mOm <3')
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(settings.get("bot_status")))


async def setup(bot):
    await bot.add_cog(OnReady(bot))
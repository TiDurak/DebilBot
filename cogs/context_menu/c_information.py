import discord
from discord import app_commands
from discord.ext import commands

class CInformation(commands.Cog):
    """Info"""

    def __init__(self, bot) -> None:
        self.bot = bot
        self.ctx_avatar = app_commands.ContextMenu(
            name="Получить Аватарку",
            callback=self.avatar,
        )
        self.bot.tree.add_command(self.ctx_avatar)

    async def avatar(self, interaction: discord.Interaction, member: discord.Member) -> None:
        await interaction.response.send_message(member.avatar.url)
        
async def setup(bot):
    await bot.add_cog(CInformation(bot))
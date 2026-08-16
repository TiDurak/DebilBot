import discord
from discord import app_commands
from discord.ext import commands

class CReputation(commands.Cog):
    """Reputation"""

    def __init__(self, bot, rep):
        self.__reputation = rep
        self.bot = bot
        self.ctx_add_reputation = app_commands.ContextMenu(
            name="+реп",
            callback=self.add_reputation,
        )
        self.ctx_remove_reputation = app_commands.ContextMenu(
            name="-реп",
            callback=self.remove_reputation,
        )
        self.bot.tree.add_command(self.ctx_add_reputation)
        self.bot.tree.add_command(self.ctx_remove_reputation)

    async def add_reputation(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.user == member:
            await interaction.response.send_message(
                "Слыш ты, гомик ебливый. Самолайк - залог охуения. Нельзя самому себе менять репутацию. Ану пездюки, "
                "захуярьте его")
            return
        result = await self.__reputation.give(member.id, interaction.guild.id, 1)
        reputation = await self.__reputation.get(member.id, interaction.guild.id)
        success = result.get("success")
        if success:
            await interaction.response.send_message(
                f"Пидору с ником **{member.mention}** была выдана репутация. Теперь она составляет {reputation}")
        else:
            time_remaining = result.get("remaining")
            await interaction.response.send_message(
                f"Этому челоёбу можно изменить репутацию только раз в 60 секунд. Жди `{time_remaining} сек`, пиздюк мелкий",
                ephemeral=True)

    async def remove_reputation(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.user == member:
            await interaction.response.send_message(
                "ты, я вижу, сам себя решил захуярить...", ephemeral=True)
            return
        result = await self.__reputation.give(member.id, interaction.guild.id, -1)
        reputation = await self.__reputation.get(member.id, interaction.guild.id)
        success = result.get("success")
        if success:
            await interaction.response.send_message(
                f"Пидору с ником **{member.mention}** была опущена репутация. Теперь она составляет {reputation}")
        else:
            time_remaining = result.get("remaining")
            await interaction.response.send_message(
                f"Этому челоёбу можно изменить репутацию только раз в 60 секунд. Жди `{time_remaining} сек`, пиздюк мелкий")

async def setup(bot, rep):
    await bot.add_cog(CReputation(bot, rep))
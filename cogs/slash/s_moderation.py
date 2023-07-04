from config import settings

import discord
from discord import app_commands
from discord.ext import commands


class SModeration(commands.Cog):
    """Moderation"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Очищает несколько сообщений")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(amount="Каличества саапщений, каторие я удолю",
                           member="Я буду чистеть сапщение только этава челавека")
    async def clear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 500], member: discord.Member = None):
        channel = interaction.channel

        def check_(m):
            return m.author == member

        if not member:
            await channel.purge(limit=amount)
        else:
            await channel.purge(limit=amount, check=check_)
        await interaction.response.send_message(f"{self.bot.get_emoji(settings['emojis']['squid_cleaning'])} Очищено {amount} сообщений")

    @app_commands.command(name="kick",
                          description="Кикает какого-то челика")
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction,
                   member: discord.Member, reason: str = "Не указано"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"Изгоняем участника {member} по причине: {reason}")

    @app_commands.command(name="ban",
                          description="Банит какого-то левого пидора")
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction,
                   member: discord.Member, reason: str = "Не указано"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"еБаним участника {member} по причине: {reason}")


async def setup(bot):
    await bot.add_cog(SModeration(bot))
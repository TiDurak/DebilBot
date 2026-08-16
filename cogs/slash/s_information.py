import discord
from discord import app_commands
from discord.ext import commands

from config import settings

class SInformation(commands.Cog):
    """Information commands"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Получить твою аву / аву указанного юзверя / твоей мамаши")
    @app_commands.describe(member="Покажу аватарку этого говноеда")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            user_avatar_url = interaction.user.avatar.url
        else:
            user_avatar_url = member.avatar.url
        await interaction.response.send_message(user_avatar_url)

    @app_commands.command(name="user", description="деанон хуесоса / тебя")
    @app_commands.describe(member="дам инфу любого уебана за 100 рублей")
    async def user_info(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        is_bot = "Да" if member.bot else "Нет"

        embed = discord.Embed(color=settings.get("main_embed_color"), title=f'Информация о пользователе {member}')
        embed.add_field(name='Имя Пользователя', value=member)
        embed.add_field(name='Пользователь На Сервере', value=member.mention)
        embed.add_field(name='ID Пользователя', value=member.id)
        embed.add_field(name='Бот', value=is_bot, inline=False)
        embed.add_field(name='Зашёл На Сервер', value=member.joined_at.strftime("%#d %B %Y, %H:%M"))
        embed.add_field(name='Дата Регистрации', value=member.created_at.strftime("%#d %B %Y, %H:%M"))
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"Запросил {interaction.user.name}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="server_info", description="невыдуманная инфа о сервере, о которой невозможно молчать")
    async def server_info(self, interaction: discord.Interaction):
        embed = discord.Embed(color=settings.get("main_embed_color"), title=f'Информация о сервере')
        embed.add_field(name='Имя Сервера', value=interaction.guild)
        embed.add_field(name='ID Сервера', value=interaction.guild.id)
        embed.add_field(name='Число Участников', value=interaction.guild.member_count, inline=False)
        embed.add_field(name='Дата Содания Сервера', value=interaction.guild.created_at.strftime("%#d %B %Y, %H:%M"))
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.set_footer(text=f"Запросил {interaction.user.name}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SInformation(bot))
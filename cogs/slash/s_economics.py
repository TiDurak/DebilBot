from config import settings

import discord
from discord import app_commands
from discord.ext import commands


class SEconomics(commands.Cog):
    """
    Economics cog
    Currency: ₲ - Gondon
    """
    def __init__(self, economics):
        self.__economics = economics

    @app_commands.command(name="daily", description="Забрать ежедневную подачку для лохов")
    async def daily(self, interaction: discord.Interaction):
        success, remaining = await self.__economics.get_daily(interaction.user.id)
        if success:
            balance = await self.__economics.get_balance(interaction.user.id)
            await interaction.response.send_message(
                f"**{interaction.user.mention}** забрал ежедневную подачку "
                f"в размере `1000 Gondons`. Теперь баланс составляет: `{balance} Gondons`")
        else:
            await interaction.response.send_message(
                "Бля, ты совсем еблан блядь сука блядь нахуй блядь? "
                "Тебе нахуй объяснить сука блядь, что означает \"ЕЖЕДНЕВНЫЙ\" приз? "
                "Если блядь по простому нахуй блядь сука блядь нахуй, то ты получаешь сука блядь "
                "государственную подачку для бомжей раз в 24 часа блядь нахуй. Это означает блядь, "
                f"что ты получишь свою карманку от меня через `{remaining}`. Всё. Пошёл нахуй, быдло блядь")

    @app_commands.command(name="balance", description="Посмотреть баланс Gondons'ов")
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        current_balance = await self.__economics.get_balance(member.id)
        embed = discord.Embed(color=settings.get("main_embed_color"),
                              title=f'💳 Баланс {member.name}')
        embed.add_field(name='Gondons', value=f"{current_balance} ₲")
        embed.set_footer(text=f"Запросил {interaction.user.name}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)



async def setup(bot, economics):
    await bot.add_cog(SEconomics(economics))
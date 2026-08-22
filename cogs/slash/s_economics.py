from config import settings

import discord
from discord import app_commands
from discord.ext import commands


class SEconomics(commands.Cog):
    HELP_NAME = "💰 Экономика"
    HELP_NAME_VALUE = "economics"
    HELP_DESCRIPTION = "Дегенератские и никому не нужные экономические финтиплюшки. Валюта: гондоны (Gondons ₲)"

    def __init__(self, economics, promo):
        self.__economics = economics
        self.__promo_keys = promo


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

    @app_commands.command(name="redeem_promo", description="Активировать код, полученный на сайте govnoed.de")
    async def redeem_promo(self, interaction: discord.Interaction, promo: str):
        reward = await self.__promo_keys.get_reward(promo)
        if reward > 0:
            balance = await self.__economics.edit_money(interaction.user.id, reward)
            await interaction.response.send_message(
                f"**{interaction.user.mention}** активировал ключ и забрал бомж пакет "
                f"в размере `{reward} Gondon'ов`")
        else:
            await interaction.response.send_message(
                "Твой промокод - фальшивка, или ты лох, и его уже заюзали")

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

    @app_commands.command(name="send", description="Отправить Gondon'ы другу-дегенерату")
    async def send(self, interaction: discord.Interaction,
                   member: discord.Member,
                   amount: app_commands.Range[int, 10, 100000]):
        if interaction.user.id == member.id:
            await interaction.response.send_message("Скажи честно, ты еблан? Нахуя сам себе деньги переводишь, пидорхуй "
                                                    "блядь")
            return
        success = await self.__economics.edit_money(interaction.user.id, -amount)
        if success:
            await self.__economics.edit_money(member.id, amount)
            current_self_balance = await self.__economics.get_balance(interaction.user.id)
            current_member_balance = await self.__economics.get_balance(member.id)
            embed = discord.Embed(color=settings.get("main_embed_color"),
                                  title=f'💳 Перевод')
            embed.add_field(name="Передано Gondons", value=f"{amount} ₲")
            embed.add_field(name=f"Осталось у {interaction.user.name}", value=f"{current_self_balance} ₲")
            embed.add_field(name=f"Текущий баланс у {member.name}", value=f"{current_member_balance} ₲", inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Пшёл нахуй гондон, у тебя не хватает денег")



async def setup(bot, economics, promo):
    await bot.add_cog(SEconomics(economics, promo))
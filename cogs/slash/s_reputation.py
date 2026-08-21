from config import settings

import discord
from discord import app_commands
from discord.ext import commands


class SReputation(commands.Cog):
    HELP_NAME = "📈 Репутация"
    HELP_NAME_VALUE = "reputation"
    HELP_DESCRIPTION = "Репутация - способ показать человеку его интеллектуальную ущербность"

    def __init__(self, reputation, economics):
        self.__reputation = reputation
        self.__economics = economics

    @app_commands.command(name="rep", description="+реп -реп / показать репутацию")
    @app_commands.choices(choice=[
        app_commands.Choice(name="➕ Дать 1 репутацию", value="+"),
        app_commands.Choice(name="➖ Забрать 1 репутацию", value="-"),
        app_commands.Choice(name="🔍 Показать репутацию, я этого пидора ненавижу", value="show")
    ])
    async def rep(self, interaction: discord.Interaction, choice: app_commands.Choice[str], member: discord.Member):
        if interaction.user == member and choice.value != "show":
            await interaction.response.send_message(
                "Слыш ты, гомик ебливый. Самолайк - залог охуения. Нельзя самому себе менять репутацию. Ану пездюки, "
                "захуярьте его")
            return
        if choice.value == "+":
            result = await self.__reputation.edit(member.id, interaction.guild.id, 1)
            string_addition = "выдана"
        elif choice.value == "-":
            result = await self.__reputation.edit(member.id, interaction.guild.id, -1)
            string_addition = "захуярена"
        else:
            reputation = await self.__reputation.get(member.id, interaction.guild.id)

            embed = discord.Embed(color=settings.get("main_embed_color"),
                                  title=f'📈 Репутация гомодрила {member.name}')
            embed.add_field(name='Репутация на сервере', value=reputation)
            embed.set_footer(text=f"Запросил {interaction.user.name}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

            return

        success = result.get("success")
        if success:
            reputation = await self.__reputation.get(member.id, interaction.guild.id)
            await interaction.response.send_message(
                f"Пидору с ником **{member.mention}** была {string_addition} репутация. Теперь на этом сервере "
                f"она составляет {reputation}")
        else:
            time_remaining = result.get("remaining")
            await interaction.response.send_message(
                f"Этому челоёбу можно изменить репутацию только раз в 60 секунд. Жди `{time_remaining} сек`, пиздюк мелкий",
                ephemeral=True)

    @app_commands.command(name="buy_reputation", description="Купить репутацию на этом сервере: 200₲ за 1 реп")
    @app_commands.describe(amount="Количество репутации (200₲ за штуку)")
    async def buy_reputation(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 1000]):
        price = -amount*200
        success = await self.__economics.edit_money(interaction.user.id, price)
        if success:
            await self.__reputation.edit(interaction.user.id, interaction.guild.id, amount)
            current_reputation = await self.__reputation.get(interaction.user.id, interaction.guild.id)
            embed = discord.Embed(color=settings.get("main_embed_color"),
                                  title=f'💵 Покупка удалась')
            embed.add_field(name="Получено репутации", value=amount)
            embed.add_field(name=f"Цена", value=f"{price}₲")
            embed.add_field(name=f"По курсу", value="200₲ за 1 реп.")
            embed.add_field(name=f"Репутация на сервере сейчас", value=current_reputation)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Пшёл нахуй гондон, у тебя не хватает денег")

    @app_commands.command(name="sell_reputation", description="Продать репутацию: 150₲ за 1 реп")
    @app_commands.describe(amount="Количество репутации к продаже (150₲ за штуку)")
    async def sell_reputation(self, interaction: discord.Interaction, amount: app_commands.Range[int, 5, 500]):
        price = amount * 150
        success = await self.__reputation.edit(interaction.user.id, interaction.guild.id, -amount)
        if success:
            await self.__economics.edit_money(interaction.user.id, price)
            current_reputation = await self.__reputation.get(interaction.user.id, interaction.guild.id)
            current_balance = await self.__economics.get_balance(interaction.user.id)
            embed = discord.Embed(color=settings.get("main_embed_color"),
                                  title=f'💵 Продажа удалась')
            embed.add_field(name="Продано репутации", value=amount)
            embed.add_field(name=f"Получено", value=f"{price}₲")
            embed.add_field(name=f"По курсу", value="150₲ за 1 реп.")
            embed.add_field(name=f"Репутация на сервере сейчас", value=current_reputation)
            embed.add_field(name=f"Баланс сейчас", value=current_balance)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Пшёл нахуй пиздюк говномпомазанный, у тебя нет столько репутации")

async def setup(bot, reputation, economics):
    await bot.add_cog(SReputation(reputation, economics))
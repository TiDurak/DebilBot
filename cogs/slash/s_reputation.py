from config import settings

import discord
from discord import app_commands
from discord.ext import commands


class SReputation(commands.Cog):
    """Reputation"""
    def __init__(self, rep):
        self.__reputation = rep

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
            result = await self.__reputation.give(member.id, interaction.guild.id, 1)
            string_addition = "выдана"
        elif choice.value == "-":
            result = await self.__reputation.give(member.id, interaction.guild.id, -1)
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

async def setup(bot, reputation):
    await bot.add_cog(SReputation(reputation))
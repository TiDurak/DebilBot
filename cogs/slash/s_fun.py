import random
import requests
import discord
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup as bs

from classes.quote_image_creator import QuoteImageCreator

class SFun(commands.Cog):
    """Fun"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="anekdot", description="Парсит анекдот из сайта, "
                                                      "и делится им с тобой, ибо ты даун, "
                                                      "не можешь сам его загуглить",
                          )
    @app_commands.describe(joke_number="Номер анекдота, число от 1 до 1142")
    async def joke(self, interaction: discord.Interaction, joke_number: app_commands.Range[int, 1, 1142] = None):
        if joke_number is None:
            joke_number = str(random.randint(1, 1142))

        joke_website = "https://baneks.ru/"

        joke_url = joke_website + str(joke_number)
        request = requests.get(joke_url)
        soup = bs(request.text, "html.parser")

        parsed = soup.find_all("article")
        for jokes in parsed:
            embed = discord.Embed(color=0x33bbff, title=f"📋 Анекдот #{str(joke_number)}",
                                  description=jokes.p.text)
            embed.set_footer(text="Этот даунский анек взят (*скомунизжен) из https://baneks.ru/")
            await interaction.response.send_message(embed=embed)
            message = await interaction.original_response()

            emojis = ['🤣', '😐', '💩', '🪗']

            for emoji in emojis:
                await message.add_reaction(emoji)

    @app_commands.command(name="quote", description="Создаёт картинку с цитатой жака фреско")
    @app_commands.describe(text="Ваша цитата (до 135 символов)",
                           user="Никнейм пользователя (по умолчанию ваш)")
    async def quote(self, interaction: discord.Interaction, text: app_commands.Range[str, 1, 135], user: discord.Member = None):
        if user == None:
            user = interaction.user
        quote_generator = QuoteImageCreator('assets/back.jpg')
        quote_image = quote_generator.create_quote_image(text, user.name)
        await interaction.response.send_message(file=discord.File(quote_image))

async def setup(bot):
    await bot.add_cog(SFun(bot))

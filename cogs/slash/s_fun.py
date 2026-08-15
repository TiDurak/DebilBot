import json
import random
import requests
import discord
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup as bs

from googletrans import Translator

from config import settings
from classes.quote_image_creator import QuoteImageCreator
from classes.exceptions import APIError
from classes import games


class SFun(commands.Cog):
    """Fun"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="anekdot", description="Парсит анекдот из сайта, "
                                                      "и делится им с тобой, ибо ты даун, "
                                                      "не можешь сам его загуглить")
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
            embed = discord.Embed(color=settings.get("main_embed_color"), title=f"📋 Анекдот #{str(joke_number)}",
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


    @app_commands.command(name="epicgames_giveaway", description="Список бесплатных раздач Epic Games Store")
    async def epicgames_giveaway(self, interaction: discord.Interaction):
        # TODO: https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=ru_RU&country=UA&allowCountries=UA
        url = "https://www.gamerpower.com/api/giveaways?platform=epic-games-store"
        response = requests.get(url)
        if response.status_code == 200:
            embed_list = []
            translator = Translator()
            for game in response.json():
                if game.get("worth") != "N/A":
                    continue
                translation = translator.translate(game.get('description'), dest="ru")
                date = game.get("end_date")
                if date != "N/A":
                    date = f"{date[8:10]}.{date[5:7]}.{date[0:4]} : {date[11:]}"
                embed = discord.Embed(title=game.get("title"), color=settings.get("main_embed_color"))
                embed.add_field(name="📃 Описание", value=translation.text, inline=False)
                embed.add_field(name="🛒 Тип товара", value=game.get("type"), inline=False)
                embed.add_field(name="📅 Дата окончания", value=date, inline=False)
                embed.set_thumbnail(url=game.get("thumbnail"))
                embed_list.append(embed)

                if embed_list == []:
                    await interaction.response.send_message("🚫 На данный момент бесплатных раздач нету (бля ☹️)")
                    return
            await interaction.response.send_message("# 🆓 Бесплатные раздачи Epic Games Store", embeds=embed_list)

        elif response.status_code == 201:
            await interaction.response.send_message("🚫 Ашалеть. Настал тот момент, когда у эпик гейсов не проходят раздачи")
        elif response.status_code == 500:
            await interaction.response.send_message("🚫 Ошибка API: Что-то случилось на серверах апишника. Попробуйте позже")
            raise APIError("Error 500. Somethin went wrong, try again later")
            return "error"

    @app_commands.command(name="steam_sales", description="Список скидок Steam")
    async def steam_sales(self, interaction: discord.Interaction):
        url = "https://www.gamerpower.com/api/giveaways?platform=steam"
        response = requests.get(url)
        if response.status_code == 200:
            embed_list = []
            translator = Translator()
            for game in response.json():
                translation = translator.translate(game.get('description'), dest="ru")
                date = game.get("end_date")
                if date != "N/A":
                    date = f"{date[8:10]}.{date[5:7]}.{date[0:4]} : {date[11:]}"
                embed = discord.Embed(title=game.get("title"), color=settings.get("main_embed_color"))
                embed.add_field(name="📃 Описание", value=translation.text, inline=False)
                embed.add_field(name="💵 Цена (в регионе США)", value=game.get("worth"), inline=False)
                embed.add_field(name="🛒 Тип товара", value=game.get("type"), inline=False)
                embed.add_field(name="📅 Дата окончания", value=date, inline=False)
                embed.set_thumbnail(url=game.get("thumbnail"))
                embed_list.append(embed)

                if embed_list == []:
                    await interaction.response.send_message("🚫 На данный момент бесплатных раздач нету (бля ☹️)")
                    return
                if len(embed_list) > 10:
                    await interaction.response.send_message(f"# 🏷️ Специальные предложения Steam", embeds=embed_list[:9])

        elif response.status_code == 201:
            await interaction.response.send_message("🚫 Ашалеть. Настал тот момент, когда у эпик гейсов не проходят раздачи")
        elif response.status_code == 500:
            await interaction.response.send_message("🚫 Ошибка API: Что-то случилось на серверах апишника. Попробуйте позже")
            raise APIError("Error 500. Somethin went wrong, try again later")
            return "error"

    @app_commands.command(name="rock_paper_scissors", description="Камень ножницы бумага! ЪУЪ Бляд!")
    @app_commands.choices(choices=[
        app_commands.Choice(name="🪨 Камень", value="Камень"),
        app_commands.Choice(name="✂️ Ножницы", value="Ножницы"),
        app_commands.Choice(name="🧻 Бумага", value="Бумага")
    ])
    async def rock_paper_scissors(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        rps = games.RockPaperScissors()
        description = await rps.get_embed_description(choices.value)
        embed = discord.Embed(color=settings.get("main_embed_color"), title="Камень Ножницы Бумага", description=description)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="slots", description="Азино три топора")
    async def slots(self, interaction: discord.Interaction):
        slots = games.Slots()
        result = await slots.get_result()
        slots_parsed = await slots.slots_parsed()
        embed = discord.Embed(color=settings.get("main_embed_color"), title='🎰 Slots Azino777',
                              description=slots_parsed)
        embed.set_footer(text=result, icon_url="https://i.imgur.com/uZIlRnK.png")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SFun(bot))

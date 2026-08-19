import requests
from textwrap import dedent
import discord
from discord import app_commands
from discord.ext import commands


from googletrans import Translator

from config import settings
from classes.quote_image_creator import QuoteImageCreator
from classes.exceptions import APIError
from classes import games, joke_parser

class SlotsButtons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(style=discord.ButtonStyle.blurple, label='Показать множители', emoji='🎰')
    async def button_multipliers(self, interaction: discord.Interaction, button: discord.ui.Button):
        multipliers = dedent("""
        👑👑👑 = x10
        👑👑 = x6.66
        7️⃣7️⃣7️⃣ = x50
        7️⃣7️⃣ = x7.5
        7️⃣ = x1.85
        🔔🔔🔔 = x4
        🔔🔔 = x1.75
        🍒🍒🍒 = x2
        🍒🍒 = x0.45
        ☠️☠️☠️ = x1.50
        ☠️☠️ = x0.65
        """)
        embed = discord.Embed(color=settings.get("main_embed_color"), title=f"🎰 Множители",
                              description=multipliers)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class SFun(commands.Cog):
    """Fun"""

    def __init__(self, bot, eco):
        self.bot = bot
        self.__economics = eco

    @app_commands.command(name="anekdot", description="Парсит анекдот из сайта, "
                                                      "и делится им с тобой, ибо ты даун, "
                                                      "не можешь сам его загуглить")
    @app_commands.describe(joke_number="Номер анекдота, число от 1 до 1142")
    async def joke(self, interaction: discord.Interaction, joke_number: app_commands.Range[int, 1, 1142] = None):
        joke = joke_parser.JokeParser()
        parsed_joke = await joke.get_joke(joke_number)
        embed = discord.Embed(color=settings.get("main_embed_color"), title=f"📋 Анекдот #{str(joke_number)}",
                              description=parsed_joke)
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
    @app_commands.describe(bet="Размер ставки в Gondon'ах")
    async def slots(self, interaction: discord.Interaction, bet: app_commands.Range[int, 50, 10000]):
        success = await self.__economics.edit_money(interaction.user.id, -bet)
        if success:
            slots = games.Slots()
            bet_multiplier = await slots.get_result()
            await self.__economics.edit_money(interaction.user.id, round(bet * bet_multiplier, 2))
            balance = await self.__economics.get_balance(interaction.user.id)
            slots_parsed = await slots.slots_parsed()
            embed = discord.Embed(color=settings.get("main_embed_color"), title='🎰 Казик Azino777 - ненаёб100%',
                                  description=slots_parsed)
            embed.add_field(name="✖️ Полученный множитель", value=f"x{bet_multiplier}")
            embed.add_field(name="📈 Прибыль", value = round(bet * bet_multiplier - bet, 2))
            embed.set_footer(text=f"Текущий баланс {balance}₲", icon_url="https://i.imgur.com/uZIlRnK.png")
            view = SlotsButtons()
            await interaction.response.send_message(embed=embed, view=view)
        else:
            balance = await self.__economics.get_balance(interaction.user.id)
            await interaction.response.send_message(f"Ты даун? у тебя на балансе `{balance} Gondon'ов`. "
                                                    f"Как ты хочешь сделать ставку {bet} Gondon'ов? Я тебе не банк, "
                                                    "кредит не выдам")

async def setup(bot, eco):
    await bot.add_cog(SFun(bot, eco))

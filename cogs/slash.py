import random
import requests
from config import settings

import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator
from bs4 import BeautifulSoup as bs

from discord.ext import commands


class Slash(commands.Cog):
    """Основные слэш-команды"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="echo", description="Выводит текст от лица бота")
    @app_commands.describe(message="Твоё сообщение, которое я напишу за тебя")
    async def echo(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    @app_commands.command(name="poll", description="ГАЛАСАВАНИЕ")
    @app_commands.describe(question="Задай тему голосования",
                           option1="Первый вариант ответа (обязательно)",
                           option2="Второй вариант ответа",
                           option3="Третий варик",
                           option4="Ну ты понял короче")
    async def poll(self, interaction: discord.Interaction,
                   question: str, option1: str, option2: str = "None",
                   option3: str = "None", option4: str = "None", option5: str = "None",
                   option6: str = "None", option7: str = "None", option8: str = "None"):

        options_template = [option1, option2, option3,
                            option4, option5, option6,
                            option7, option8]

        options = []
        for opt in options_template:
            if opt != "None":
                options.append(opt)

        if len(options) < 1:
            await interaction.response.send_message('❌ Для создания голосования нужно хотя-бы 1 ответ!')
            return

        reactions_template = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']
        reactions = []
        for emoji in range(len(options)):
            reactions.append(reactions_template[emoji])

        description = []
        for x, option in enumerate(options):
            description += '\n{} {}'.format(reactions[x], option)

        embed = discord.Embed(color=0xffcd4c,
                              title=f'{self.bot.get_emoji(settings["emojis"]["stonks"])} {interaction.user}: {question}',
                              description=''.join(description))

        await interaction.response.send_message(embed=embed)
        react_message = await interaction.original_response()
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)

    @app_commands.command(name="translate", description="Переводит текст, ибо ты даун, "
                                                        "не можешь перевести сам")
    @app_commands.describe(language="Язык, на который я переведу текст",
                           text="Текст, который я переведу на выбранный тобой язык",
                           is_embed="Как выводить перевод")
    @app_commands.choices(language=[
        app_commands.Choice(name="Английский", value="en"),
        app_commands.Choice(name="Арабский", value="ar"),
        app_commands.Choice(name="Африканский", value="af"),
        app_commands.Choice(name="Белорусский", value="be"),
        app_commands.Choice(name="Болгарский", value="bg"),
        app_commands.Choice(name="Венгерский", value="hu"),
        app_commands.Choice(name="Грецкий", value="el"),
        app_commands.Choice(name="Иврит", value="iw"),
        app_commands.Choice(name="Итальянский", value="it"),
        app_commands.Choice(name="Китайский (традиционный)", value="zh-tw"),
        app_commands.Choice(name="Латинский", value="la"),
        app_commands.Choice(name="Немецкий", value="de"),
        app_commands.Choice(name="Польский", value="pl"),
        app_commands.Choice(name="Русский", value="ru"),
        app_commands.Choice(name="Украинский", value="uk"),
        app_commands.Choice(name="Французский", value="fr"),
        app_commands.Choice(name="Чешский", value="cs"),
    ], is_embed=[
        app_commands.Choice(name="Вывести в виде вложения (По умолчанию)", value=1),
        app_commands.Choice(name="Вывести в виде обычного текста", value=0),
    ])
    async def translate(self, interaction: discord.Interaction,
                        language: app_commands.Choice[str], text: str,
                        is_embed: app_commands.Choice[int] = 1):  # Using "int" instead "bool", because second is not allowed
        translator = Translator()
        translation = translator.translate(text, dest=str(language.value))

        if is_embed == 1:
            embed = discord.Embed(color=0xffcd4c, title=f"{interaction.user} :: DebilBot Super Mega 228 Translator")
            embed.add_field(name="Исходный Текст", value=text, inline=False)
            embed.add_field(name=f"Перевод на {language.name}", value=translation.text, inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(translation.text)

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


async def setup(bot):
    await bot.add_cog(Slash(bot))

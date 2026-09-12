from config import settings, ai_settings

import discord
from discord import app_commands
from discord.ext import commands

from googletrans import Translator
from classes import openrouter_chat_sessions


class SText(commands.Cog):
    HELP_NAME = "💬 Текст"
    HELP_NAME_VALUE = "text"
    HELP_DESCRIPTION = "Текстовые говносрани"

    def __init__(self, bot, eco):
        self.bot = bot
        self.__economics = eco
        self.chat_sessions = {}
        

    @app_commands.command(name="echo", description="Выводит текст от лица бота")
    @app_commands.describe(message="Твоё сообщение, которое я напишу за тебя")
    async def echo(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

    @app_commands.command(name="translate", description="Переводит текст, ибо ты даун, "
                                                        "не можешь перевести сам")
    @app_commands.describe(language="Язык, на который я переведу текст",
                           text="Текст, который я переведу на выбранный тобой язык")
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
    ])
    async def translate(self, interaction: discord.Interaction,
                        language: app_commands.Choice[str], text: str):  # Using "int" instead "bool", because second is not allowed
        translator = Translator()
        translation = translator.translate(text, dest=str(language.value))

        embed = discord.Embed(color=settings.get("main_embed_color"), title=f"{interaction.user.name} :: DebilBot Super Mega 228 Translator")
        embed.add_field(name="Исходный Текст", value=text, inline=False)
        embed.add_field(name=f"Перевод на {language.name}", value=translation.text, inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ai", description="Общение с нейросетью. Стоимость запроса: 15₲")
    @app_commands.describe(message="Задай свой вопрос, скотина блядь")
    async def ai(self, interaction: discord.Interaction, message: str):
        success = await self.__economics.edit_money(interaction.user.id, -15)
        if success:
            balance = await self.__economics.get_balance(interaction.user.id)
            embed = discord.Embed(color=settings.get("main_embed_color"), title=f"{interaction.user.name} :: {message}")
            await interaction.response.send_message(embed=embed)
            embed.set_footer(text=f"Powered by Openrouter. Осталось {balance}₲")

            chat_session = self.chat_sessions.get(interaction.guild.id)
            if chat_session is None:
                chat_session = openrouter_chat_sessions.ChatSession(
                    api_key = ai_settings.get("openrouter_api_key"),
                    model = ai_settings.get("ai_model")
                )
            self.chat_sessions[interaction.guild.id] = chat_session

            answer = await chat_session.send_message(message)

            if len(answer) > 1000:
                j = 1
                embed.add_field(name="\u200b", value=answer[:999], inline=False)
                while True:
                    j += 1
                    answer = answer[999:]
                    if len(answer) > 1000:
                        embed.add_field(name="\u200b", value=answer[0:999], inline=False)
                    else:
                        embed.add_field(name="\u200b", value=answer, inline=False)
                        break
            else:
                embed.add_field(name="\u200b", value=answer, inline=False)

            await interaction.edit_original_response(embed=embed)
        else:
            await interaction.response.send_message("У тебя кончились бабки. Ты теперь бичара. Юзай `/daily`, "
                                                    "или выиграй бабки в казике")


async def setup(bot, eco):
    await bot.add_cog(SText(bot, eco))

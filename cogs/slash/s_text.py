from config import settings, google_ai_settings

import discord
from discord import app_commands
from discord.ext import commands

from googletrans import Translator
import google.generativeai as genai
from google.generativeai.types import StopCandidateException


class SText(commands.Cog):
    """Text"""

    def __init__(self, bot):
        self.bot = bot
        genai.configure(api_key=google_ai_settings.get("google_api_key"))

        

        self.model = genai.GenerativeModel(
          model_name="gemini-3.6-flash",
          safety_settings=google_ai_settings.get("safety_settings"),
          generation_config=google_ai_settings.get("generation_config"),
        )
        self.chat_sessions = {}
        

    @app_commands.command(name="echo", description="Выводит текст от лица бота")
    @app_commands.describe(message="Твоё сообщение, которое я напишу за тебя")
    async def echo(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

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
                        is_embed: app_commands.Choice[
                            int] = 1):  # Using "int" instead "bool", because second is not allowed
        translator = Translator()
        translation = translator.translate(text, dest=str(language.value))

        if is_embed == 1:
            embed = discord.Embed(color=0xffcd4c, title=f"{interaction.user.name} :: DebilBot Super Mega 228 Translator")
            embed.add_field(name="Исходный Текст", value=text, inline=False)
            embed.add_field(name=f"Перевод на {language.name}", value=translation.text, inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(translation.text) @ app_commands.command(name="translate",
                                                                                             description="Переводит текст, ибо ты даун, "
                                                                                                         "не можешь перевести сам")

    @app_commands.command(name="ai", description="Общение с нейросетью Google Gemini")
    @app_commands.describe(message="Задай свой вопрос, скотина блядь")
    async def ai(self, interaction: discord.Interaction, message: str):
        embed = discord.Embed(color=0xffcd4c, title=f"{interaction.user.name} :: {message}")
        await interaction.response.send_message(embed=embed)
        embed.set_footer(text="DebilAI - Powered by Google Gemini 1.5 Flash",
                         icon_url="https://tidurak.github.io/google-gemini-icon.png")
        chat_session = self.chat_sessions.get(interaction.guild.id)
        if chat_session == None:
            self.chat_sessions[interaction.guild.id] = self.model.start_chat(history=[])
            chat_session = self.chat_sessions.get(interaction.guild.id)
            response = None

        try:
            response = chat_session.send_message(message)
        except StopCandidateException:
            fuck_you_message = "ТЫ еблаН? Я нейронка от гугла, и у меня ёбнутые фильтры на т.н. \"опасный\" контент. ЫЫЫЫЫ"
            embed.add_field(name="🚫 Иди нахуй", value=fuck_you_message, inline=False)
            await interaction.edit_original_response(embed=embed)
            return

        if len(response.text) > 1000:
            res = response.text
            j = 1
            embed.add_field(name="\u200b", value=res[:999], inline=False)
            while True:
                j += 1
                res = res[999:]
                if len(res) > 1000:
                    embed.add_field(name="\u200b", value=res[0:999], inline=False)
                else:
                    embed.add_field(name="\u200b", value=res, inline=False)
                    break
        else:
            embed.add_field(name="\u200b", value=response.text, inline=False)
        
        await interaction.edit_original_response(embed=embed)


async def setup(bot):
    await bot.add_cog(SText(bot))

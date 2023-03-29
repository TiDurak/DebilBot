from config import settings

import discord
from discord import app_commands
from discord.ext import commands
from googletrans import Translator


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
                   question: str, option1: str, option2: str=None,
                   option3: str="None", option4: str="None", option5: str="None",
                   option6: str="None", option7: str="None", option8: str="None"):

        options_template = [option1, option2, option3,
                            option4, option5, option6,
                            option7, option8]

        options = []
        for opt in options_template:
            if opt is not "None":
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


async def setup(bot):
    await bot.add_cog(Slash(bot))

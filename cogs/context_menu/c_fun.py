import discord
from discord import app_commands
from discord.ext import commands

from classes.quote_image_creator import QuoteImageCreator

class CFun(commands.Cog):
    """Fun"""

    def __init__(self, bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Сделать Цитату",
            callback=self.quote,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def quote(self, interaction: discord.Interaction, message: discord.Message) -> None:
        if len(message.content) > 135:
            await interaction.response.send_message("⚠️ ЭЭЭээээ слиш ти педрило-хуило, низя больше 135 символов в цитати, "
                                                    "ти миня понеЛ?!!!?!??!11?!?!", 
                                                    delete_after=10)
        elif len(message.content) < 1:
            await interaction.response.send_message("⚠️ ээээиий вай вах дАрагои, што ти дэлат?! "
                                                    "нужна хатябы 1 букава для цытати, мой дарагои, ваххх", 
                                                    delete_after=10)
        else:
            quote_generator = QuoteImageCreator('assets/back.jpg')
            quote_image = quote_generator.create_quote_image(message.content, message.author.name)
            await interaction.response.send_message(file=discord.File(quote_image))

async def setup(bot):
    await bot.add_cog(CFun(bot))
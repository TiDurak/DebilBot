import discord
from discord import app_commands
from discord.ext import commands

from classes.quote_image_creator import QuoteImageCreator
from classes.eblan_photo import EblanPhoto

class CFun(commands.Cog):
    """Fun"""

    def __init__(self, bot, eco) -> None:
        self.bot = bot
        self.__economics = eco
        self.ctx_quote = app_commands.ContextMenu(
            name="Сделать Цитату",
            callback=self.quote,
        )
        self.ctx_eblan = app_commands.ContextMenu(
            name="Ты Еблан! - 250₲",
            callback=self.get_eblan,
        )
        self.bot.tree.add_command(self.ctx_quote)
        self.bot.tree.add_command(self.ctx_eblan)

    async def quote(self, interaction: discord.Interaction, message: discord.Message) -> None:
        if len(message.content) > 135:
            await interaction.response.send_message("⚠️ ЭЭЭээээ слиш ти педрило-хуило, низя больше 135 символов в цитати, "
                                                    "ти миня понеЛ?!!!?!??!11?!?!", 
                                                    ephemeral=True)
        elif len(message.content) < 1:
            await interaction.response.send_message("⚠️ ээээиий вай вах дАрагои, што ти дэлат?! "
                                                    "нужна хатябы 1 букава для цытати, мой дарагои, ваххх", 
                                                    ephemeral=True)
        else:
            quote_generator = QuoteImageCreator('assets/back.jpg')
            quote_image = quote_generator.create_quote_image(message.content, message.author.name)
            await interaction.response.send_message(file=discord.File(quote_image))

    async def get_eblan(self, interaction: discord.Interaction, member: discord.Member) -> None:
        success = await self.__economics.edit_money(interaction.user.id, -250)
        if success:
            eblan_photo = EblanPhoto("assets/eblan.jpg", member.avatar.url)
            eblan_photo.resize_image()
            eblan_photo.add_border()
            eblan_photo.place_image(position=(365, 95))
            result = eblan_photo.save_result('assets/eblan_ready.jpg')
            msg = f"{member.mention}, {interaction.user.mention} потратил `250 Gondons`, чтобы назвать тебя ебланом"
            await interaction.response.send_message(msg, file=discord.File(result))
        else:
            await interaction.response.send_message("🫰🏿 Недостаточно денег на балансе, бичара", ephemeral=True)

async def setup(bot, eco):
    await bot.add_cog(CFun(bot, eco))
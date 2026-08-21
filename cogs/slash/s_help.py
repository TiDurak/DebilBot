from pydoc import describe

from config import settings

import discord
from discord import app_commands
from discord.ext import commands
from textwrap import dedent

class HelpTemplates:
    @staticmethod
    def get_embed_template(title, description) -> discord.Embed:
        embed = discord.Embed(
            title=title,
            description=description,
            color=settings.get("main_embed_color")
        )
        embed.set_thumbnail(url="https://tidurak.github.io/DebilBot_Text.png")
        embed.set_footer(text="https://github.com/TiDurak/DebilBot",
                         icon_url="https://tidurak.github.io/gd_round_low.png")
        return embed

    @staticmethod
    async def help_main():
        title = "❔ Помощь"
        description = dedent("""
            📙 `/help` для вывода этого меню
            📙 `/help` `категория` для вывода команд выбранной категории

            🌍 [Страница DebilBot'а](https://govnoed.de/)
            🪩 [Discord сервер + техподдержка](https://discord.com/invite/4dEmQjt)
            🐞 [GitHub - Репорт бага](https://github.com/TiDurak/DebilBot/issues/new/choose)
            """)
        return title, description

class SHelp(commands.Cog):
    def __init__(self, bot):
        self.__bot = bot
        self.__templates = HelpTemplates

    async def __category_autocomplete(self, interaction: discord.Interaction, current: str):
        choices = []
        for cog in self.__bot.cogs.values():
            category = getattr(cog, "HELP_NAME", None)
            value = getattr(cog, "HELP_NAME_VALUE", None)
            if category is None or value is None:
                continue
            if current.lower() in value.lower() or \
                    current.lower() in category.lower():
                choices.append(
                    app_commands.Choice(
                        name=category,
                        value=value
                    )
                )
        return choices[:25]

    @app_commands.command(name="help", description="Показать список говнокоманд")
    @app_commands.describe(category="Категория команд (необязательно)")
    @app_commands.autocomplete(category=__category_autocomplete)
    async def help(self, interaction: discord.Interaction, category: str = None):
        target_cog = None
        if category is not None:
            for cog in self.__bot.cogs.values():
                if getattr(cog, "HELP_NAME_VALUE", None) == category:
                    target_cog = cog
                    break
        if target_cog is None:
            title, description = await self.__templates.help_main()
            embed = self.__templates.get_embed_template(title, description)
            await interaction.response.send_message(embed=embed)
            return

        embed = self.__templates.get_embed_template(target_cog.HELP_NAME, target_cog.HELP_DESCRIPTION)

        for command in self.__bot.tree.walk_commands():
            if not isinstance(command, app_commands.Command):
                continue
            if command.binding is not target_cog:
                continue

            embed.add_field(
                name=f"/{command.qualified_name}",
                value=f"*{command.description}*" or "Без описания",
                inline=False
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SHelp(bot))
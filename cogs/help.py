import discord
from discord.ext import commands
from config import settings


class HelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        self.no_category = None
        destination = self.get_destination()
        replace_list = [
            ["Convert", "💱 Конвертеры 💱"],
            ["Fun", "🎮 Веселье 🎮"],
            ["Information", "ℹ️ Информация ℹ️"],
            ["Moderation", "🔧 Модерация 🔧"],
            ["Music", "🎵 Музыка 🎵"],
            ["Text", "📝 Текстовые 📝"],
            ["No Category", "❓ Без Категории ❓"]
        ]
        for page in self.paginator.pages:
            for obj in replace_list:
                page = page.replace(obj[0], obj[1])
            embed = discord.Embed(color=0xffcd4c, title='Помощь',
                                  description=page)
            embed.set_thumbnail(url="https://tidurak.github.io/DebilBot_Text.png")
            embed.set_footer(text="Создатель: GamerDisclaimer. https://github.com/TiDurak/DebilBot",
                             icon_url="https://tidurak.github.io/gd_round_low.png")
            await destination.send(embed=embed)

    def get_opening_note(self) -> str:
        return (
            f"**📙 Префикс: `{settings.get('prefix')}`**\n"
            "📙 `help` для вывода списка команд\n"
            "📙 `help` `название команды` для подробного описания команды\n")


async def setup(bot):
    bot.help_command = HelpCommand()

import discord
from discord.ext import commands
from googletrans import Translator
from config import settings


class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, lang, *, text):
        """Переводит текст"""

        warntext = ('d.translate `ru` `Ваш текст`\n\n\n'
                    '`ru` является языком, на который нужно переводить\n'
                    'Вместо `ru` может быть:\n'
                    '`ua`, `en`, `hu`, и т.д.\n')
        try:
            translator = Translator()
            translation = translator.translate(text, dest=lang)

            embed = discord.Embed(color=0xffcd4c, title=f"{ctx.author.name} :: DebilBot Translator")
            embed.add_field(name="Исходный Текст", value=text, inline=False)
            embed.add_field(name="Перевод", value=translation.text, inline=False)
            await ctx.send(embed=embed)
        except ValueError:
            await ctx.send(embed=discord.Embed(color=0xffcd4c,
                                               title="❌ Указан неверный язык!",
                                               description=warntext))

    @commands.command()
    async def echo(self, ctx, *, arg):
        """Повторяет сообщение за тобой"""

        await ctx.message.delete()
        await ctx.send(arg)

async def setup(bot):
    await bot.add_cog(Text(bot))

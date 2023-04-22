import discord
from discord.ext import commands
from config import settings


class Information(commands.Cog):
    def __init__(self, bot):
        self.__bot = bot

    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
        """Показывает аватарку упомянутого персонажа (если никого не указывать, то показывает твоё ебало)"""

        if member is None:
            user_avatar_url = ctx.author.avatar.url
        else:
            user_avatar_url = member.avatar.url
        await ctx.send(user_avatar_url)

    @commands.command(aliases=['user'])
    async def user_info(self, ctx, user: discord.Member = None):
        """Показывает всю информацию о человеке, либо же твою инфу"""
        if user is None:
            user = ctx.author
        is_bot = "Да" if user.bot else "Нет"

        embed = discord.Embed(color=0xffcd4c, title=f'Информация о пользователе {user}')
        embed.add_field(name='Имя Пользователя', value=user)
        embed.add_field(name='Пользователь На Сервере', value=user.mention)
        embed.add_field(name='ID Пользователя', value=user.id)
        embed.add_field(name='Бот', value=is_bot, inline=False)
        embed.add_field(name='Зашёл На Сервер', value=user.joined_at.strftime("%#d %B %Y, %H:%M"))
        embed.add_field(name='Дата Регистрации', value=user.created_at.strftime("%#d %B %Y, %H:%M"))
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_footer(text=f"Запросил {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["server", "guild", "guild_info"])
    async def server_info(self, ctx):
        """Показывает инфу о сервере"""

        embed = discord.Embed(color=0xffcd4c, title=f'Информация о сервере')
        embed.add_field(name='Имя Сервера', value=ctx.guild)
        embed.add_field(name='ID Сервера', value=ctx.guild.id)
        embed.add_field(name='Число Участников', value=ctx.guild.member_count, inline=False)
        embed.add_field(name='Дата Содания Сервера', value=ctx.guild.created_at.strftime("%#d %B %Y, %H:%M"))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(text=f"Запросил {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Information(bot))

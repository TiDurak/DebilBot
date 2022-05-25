import discord
from discord.ext import commands
from config import settings

class Information(commands.Cog):
    def __init__(self, bot):
        self.__bot = bot

    @commands.command()
    async def avatar(self, ctx, *,  member : discord.Member=None):
        if member is None:
            user_avatar_url = ctx.author.avatar_url
        else:
            user_avatar_url = member.avatar_url
        await ctx.send(user_avatar_url)

    @commands.command(aliases = ['user'])
    async def user_info(self, ctx, user : discord.Member=None):
        if user is None:
            user = ctx.author
        is_bot = "Да" if user.bot else "Нет"

        embed = discord.Embed(color = 0xffcd4c , title = f'Информация о пользователе {user}')
        embed.add_field(name = 'Имя Пользователя', value = user)
        embed.add_field(name = 'Пользователь На Сервере', value = user.mention)
        embed.add_field(name = 'ID Пользователя', value = user.id)
        embed.add_field(name = 'Бот', value = is_bot, inline = False)
        embed.add_field(name = 'Зашёл На Сервер', value = user.joined_at.strftime("%#d %B %Y, %I:%M %p"))
        embed.add_field(name = 'Дата Регистрации', value = user.created_at.strftime("%#d %B %Y, %I:%M %p"))
        embed.set_thumbnail(url = user.avatar_url)
        embed.set_footer(text = f"Запросил {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ["server", "guild", "guild_info"])
    async def server_info(self, ctx):
        embed = discord.Embed(color = 0xffcd4c , title = f'Информация о сервере')
        embed.add_field(name = 'Имя Сервера', value = ctx.guild)
        embed.add_field(name = 'ID Сервера', value = ctx.guild.id)
        embed.add_field(name = 'Число Участников', value = ctx.guild.member_count, inline = False)
        embed.add_field(name = 'Дата Содания Сервера', value = ctx.guild.created_at.strftime("%#d %B %Y, %I:%M %p"))
        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = f"Запросил {ctx.author}", icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Information(bot))
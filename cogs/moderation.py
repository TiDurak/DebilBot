import discord
from discord.ext import commands
from discord.errors import NotFound
from discord.ext.commands import has_permissions, CommandNotFound, MissingPermissions, CommandInvokeError, MemberNotFound, BotMissingPermissions
from config import settings

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_messages = True)
    @commands.command(aliases = ['clean', 'purge'])
    async def clear(self, ctx, arg1):
        amount = int(arg1)
        await ctx.message.delete()
        await ctx.channel.purge(limit = amount)
        await ctx.send(f'{self.bot.get_emoji(settings["emojis"]["squid_cleaning"])} Очищено {amount} сообщений! Запрос на очистку от {ctx.author.mention}')

    @has_permissions(kick_members = True)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, reason = 'Не указано'):
        await member.kick(reason=reason)
        await ctx.send(f"Изгоняем участника {member} по причине: {reason}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send('❌ У бота нету привилегий кика! Пожалуйста, удалите бота из сервера, и добавьте его снова по следующей ссылке: https://discord.com/api/oauth2/authorize?client_id=699912361481470032&permissions=8&scope=bot')
            raise error


    @has_permissions(ban_members = True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason = 'Не указано'):
        await member.ban(reason=reason)
        await ctx.send("Баним участника {0} по причине: {1}".format(member, reason))

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send('❌ У бота нету привилегий бана! Пожалуйста, удалите бота из сервера, и добавьте его снова по следующей ссылке: https://discord.com/api/oauth2/authorize?client_id=699912361481470032&permissions=8&scope=bot')
    @has_permissions(manage_messages = True)
    
    @commands.command()
    async def idclear(self, ctx, arg1):
        await ctx.message.delete()
        try:
            msg = await ctx.channel.fetch_message(arg1)
            await msg.delete(arg1)
        except NotFound as e:
            await ctx.send('❌ Введите корректный ID сообщения! *Для того, чтобы скопировать ID сообщения, перейдите в настройки пользователя > расширенные, и включите режим разработчика. После этого вы сможете копировать ID сообщений.*')
        
    @idclear.error
    async def idclear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send('❌ Извините, но у вас нету привилегий для доступа к этой команде. Для выполнения команды нужны привилегии `управление сообщениями`.')
        elif isinstance(error, CommandInvokeError):
            await ctx.send('❌ У бота нету привилегий управления сообщениями! Пожалуйста, удалите бота из сервера, и добавьте его снова по следующей ссылке: https://discord.com/api/oauth2/authorize?client_id=699912361481470032&permissions=8&scope=bot')

def setup(bot):
    bot.add_cog(Moderation(bot))
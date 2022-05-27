import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
from config import settings

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.group(invoke_without_command=True)
    async def help(self, ctx, command = None):
        helptext = (f'**📙 Префикс: `{settings.get("prefix")}`**\n'
                     '📙 `help` для вывода списка команд\n'
                     '📙 `help` `название команды` для подробного описания команды\n')
        helpmusic = ('`play` `pause` `resume` `stop` `leave` `skip` `queue`')
        helpmoderation = ('`clear` `idclear` `kick` `ban`')
        helpinformation = ('`avatar` `user_info` `server_info`')
        helptextch = ('`translate` `poll` `echo`')
        helpconv = ('`encode_b64` `decode_b64` `encode_binary` `decode_binary`')

        helpgames = ('`slots` `janken`')

        embed = discord.Embed(color = 0xffcd4c , title = 'Помощь', description = helptext)
        embed.add_field(name = '🎵 ***Музыка*** 🎵', value = helpmusic, inline=False)
        embed.add_field(name = '🔧 ***Модерация*** 🔧', value = helpmoderation, inline=False)
        embed.add_field(name = 'ℹ️ ***Информация*** ℹ️', value = helpinformation, inline=False)
        embed.add_field(name = '📝 ***Текстовые*** 📝', value = helptextch, inline=False)
        embed.add_field(name = '💱 ***Конвертеры*** 💱', value = helpconv, inline=False)
        embed.add_field(name = '🎮 ***Недоигры*** 🎮', value = helpgames, inline=False)
        embed.set_thumbnail(url = "https://tidurak.github.io/DebilBot_Text.png")
        embed.set_footer(text="Создатель: GamerDisclaimer. https://github.com/TiDurak/DebilBot" , icon_url = "https://tidurak.github.io/gd_round_low.png")
        await ctx.send(embed = embed)
                        
    @help.command()
    async def play(self, ctx):
        helptext = ('```d.play <название песни, или URL>```\n'
                    'Воспроизводит песню с YouTube, или добавляет её в список')
        embed = discord.Embed(color = 0xffcd4c , title = 'play', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def queue(self, ctx):
        helptext = ('```d.queue```\n'
                    'Выводит список воспроизведения на экран')
        embed = discord.Embed(color = 0xffcd4c , title = 'queue', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def skip(self, ctx):
        helptext = ('```d.skip```\n'
                    'Пропускает песню, которая сейчас проигрывается, и начинает проигрываать следующую')
        embed = discord.Embed(color = 0xffcd4c , title = 'skip', description = helptext)
        await ctx.send(embed = embed)
                
    @help.command()
    async def pause(self, ctx):
        helptext = ('```d.pause```\n'
                    'Приостанавливает воспроизведение песни\n'
                    'В дальнейшем, если бот не выходил из голосового чата, её можно будет воспроизвести снова командой `d.resume`')
        embed = discord.Embed(color = 0xffcd4c , title = 'pause', description = helptext)
        await ctx.send(embed = embed)
                
    @help.command()
    async def resume(self, ctx):
        helptext = ('```d.resume```\n'
                    'Убирает паузу, и начинает воспроизведение с последнего момента перед паузой')
        embed = discord.Embed(color = 0xffcd4c , title = 'resume', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def stop(self, ctx):
        helptext = ('```d.stop```\n'
                    'Окончательно останавливает воспроизведение, и очищае список')
        embed = discord.Embed(color = 0xffcd4c , title = 'stop', description = helptext)
        await ctx.send(embed = embed)
    
    @help.command()
    async def leave(self, ctx):
        helptext = ('```d.leave```\n'
                    'Выкидывает бота из голосового чата')
        embed = discord.Embed(color = 0xffcd4c , title = 'leave', description = helptext)
        await ctx.send(embed = embed)


    @help.command()
    async def clear(self, ctx):
        helptext = ('```d.clear <кол-во сообщений>```\n'
                    'Массовое удаление сообщение из текущего канала\n'
                    'Нужны привилегии управления сообщениями')
        embed = discord.Embed(color = 0xffcd4c , title = 'clear', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def idclear(self, ctx):
        helptext = ('```d.idclear <ID Сообщения>```\n'
                    'Удаляет одно сообщение по MessageID. Команда вводится в канале с тем самым сообщением\n'
                    'Нужны привилегии управления сообщениями')
        embed = discord.Embed(color = 0xffcd4c , title = 'idclear', description = helptext)
        await ctx.send(embed = embed)
    
    @help.command()
    async def kick(self, ctx):
        helptext = ('```d.kick <@упоминание_пользователя>```\n'
                    'Кикает пользователя по пинку\n'
                    'Нужны привилегии кика пользователей')
        embed = discord.Embed(color = 0xffcd4c , title = 'kick', description = helptext)
        await ctx.send(embed = embed)
        
    @help.command()
    async def ban(self, ctx):
        helptext = ('```d.ban <@упоминание_пользователя>```\n'
                    'Банит пользователя по пинку\n'
                    'Нужны привилегии бана пользователей')
        embed = discord.Embed(color = 0xffcd4c , title = 'ban', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def avatar(self, ctx):
        helptext = ('```d.avatar```\n'
                    '```d.avatar @упоминание_пользователя```\n'
                    'Отправляет вам аватар пользователя (или ваш)\n')
        embed = discord.Embed(color = 0xffcd4c , title = 'avatar', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def user_info(self, ctx):
        helptext = ('```d.user_info```\n'
                    '```d.user_info @упоминание_пользователя```\n'
                    'Отправляет вам информацию о пользователе (если никого не упоминали, то информацию о вас)\n'
                    'Алиасы: user\n')
        embed = discord.Embed(color = 0xffcd4c , title = 'user_info', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def server_info(self, ctx):
        helptext = ('```d.server_info```\n'
                    'Отправляет вам информацию о сервере\n'
                    'Алиасы: server, guild, guild_info\n')
        embed = discord.Embed(color = 0xffcd4c , title = 'server_info', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def translate(self, ctx):
        helptext = ('```d.translate <язык> <текст>```\n'
                    'Переводит ваш текст, язык указывается по стандарту ISO 639-1\n'
                    'Полный список наименований будет доступен после нажатия на кнопку ниже')
        embed = discord.Embed(color = 0xffcd4c , title = 'translate', description = helptext)
        await ctx.send(
        embed = embed,
        components = [
        Button(style = ButtonStyle.URL, url = 'https://snipp.ru/handbk/iso-639-1', label='Коды ISO 639-1')
        ])
        
    @help.command()
    async def poll(self, ctx):
        helptext = ('```d.poll "вопрос" "вариант 1" "вариант 2"```\n'
                    'Начинает голосование\n'
                    'Вопросы, и варианты ответа ОБЯЗАТЕЛЬНО указываются в "двойных кавычках"\n'
                    'Пример:\n'
                    '```d.poll "Какие чипсы вы предпочитаете" "Lais" "Prongls" "2 корочки"```\n'
                    'Плохой пример:\n'
                    '```d.poll Какие чипсы вы предпочитаете Lais Prongls 2 корочки```\n'
                    'В плохом примере нету кавычек, соответственно, за вопрос будет считыватся только `Какие`, остальное будет вариантами ответа\n'
                    '**Для вывода результата плохого примера, нажмите на кнопку ниже**')
        embed = discord.Embed(color = 0xffcd4c , title = 'poll', description = helptext)
        await ctx.send(
        embed = embed,
        components = [[Button(style = ButtonStyle.blue, label = 'Результат Плохого Примера')]])
                
    @help.command()
    async def echo(self, ctx):
        helptext = ('```d.echo <текст>```\n'
                    'Повторяет сообщение за вами')
        embed = discord.Embed(color = 0xffcd4c , title = 'echo', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def enchode_b64(self, ctx):
        helptext = ('```d.encode_b64 <текст>```\n'
                    'Конвертирует текст в Base64')
        embed = discord.Embed(color = 0xffcd4c , title = 'encode_b64', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def decode_b64(self, ctx):
            helptext = ('```d.decode_b64 <base64 текст>```\n'
                        'Конвертирует ваш Base64 код в ноормальный, понятный любому человеку (кроме фаната а4) текст')
            embed = discord.Embed(color = 0xffcd4c , title = 'decode_b64', description = helptext)
            await ctx.send(embed = embed)

    @help.command()
    async def encode_binary(self, ctx):
        helptext = ('```d.encode_binary <текст>```\n'
                    'Конвертирует текст в бинарный код')
        embed = discord.Embed(color = 0xffcd4c , title = 'encode_binary', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def decode_binary(self, ctx):
        helptext = ('```d.decode_binary <бинарный код>```\n'
                    'Конвертирует бинарный код в текст')
        embed = discord.Embed(color = 0xffcd4c , title = 'decode_binary', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def slots(self, ctx):
        helptext = ('```d.slots```\n'
                    'Игра в однорукого бандита (бесплатно, без регистрации и смс)')
        embed = discord.Embed(color = 0xffcd4c , title = 'slots', description = helptext)
        await ctx.send(embed = embed)

    @help.command()
    async def janken(self, ctx):
        helptext = ('```d.janken```\n'
                    'Классические камень-ножницы-бумага.\n'
                    'Правила обьяснять не буду, ибо их итак все знают\n'
                    '(Кстать, *это первая команда с алиасами!*)\n'
                    'Алиасы: `d.rockpaperscissors`, `d.rps`\n')
        embed = discord.Embed(color = 0xffcd4c , title = 'Камень-Ножницы-Бумага', description = helptext)
        await ctx.send(embed = embed)

def setup(bot):
        bot.add_cog(Help(bot))
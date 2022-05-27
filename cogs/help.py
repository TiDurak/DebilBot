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
        help_text = (f'**📙 Префикс: `{settings.get("prefix")}`**\n'
                     '📙 `help` для вывода списка команд\n'
                     '📙 `help` `название команды` для подробного описания команды\n')
        help_music = ('`play` `pause` `resume` `stop` `leave` `skip` `queue`')
        help_moderation = ('`clear` `idclear` `kick` `ban`')
        help_information = ('`avatar` `user_info` `server_info`')
        help_text_channels = ('`translate` `poll` `echo`')
        help_conv = ('`encode_b64` `decode_b64` `encode_binary` `decode_binary`')

        helpgames = ('`slots` `janken`')

        embed = discord.Embed(color = 0xffcd4c , title = 'Помощь', description = help_text)
        embed.add_field(name = '🎵 ***Музыка*** 🎵', value = help_music, inline=False)
        embed.add_field(name = '🔧 ***Модерация*** 🔧', value = help_moderation, inline=False)
        embed.add_field(name = 'ℹ️ ***Информация*** ℹ️', value = help_information, inline=False)
        embed.add_field(name = '📝 ***Текстовые*** 📝', value = help_text_channels, inline=False)
        embed.add_field(name = '💱 ***Конвертеры*** 💱', value = help_conv, inline=False)
        embed.add_field(name = '🎮 ***Недоигры*** 🎮', value = help_games, inline=False)
        embed.set_thumbnail(url = "https://tidurak.github.io/DebilBot_Text.png")
        embed.set_footer(text="Создатель: GamerDisclaimer. https://github.com/TiDurak/DebilBot" , icon_url = "https://tidurak.github.io/gd_round_low.png")
        await ctx.send(embed = embed)
                        
    @help.command()
    async def play(self, ctx):
        help_text = (f'```d.play <название песни, или URL>```\n'
                      'Воспроизводит песню с YouTube, или добавляет её в список')
        embed = discord.Embed(color = 0xffcd4c , title = 'play', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def queue(self, ctx):
        help_text = ('```d.queue```\n'
                    'Выводит список воспроизведения на экран')
        embed = discord.Embed(color = 0xffcd4c , title = 'queue', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def skip(self, ctx):
        help_text = ('```d.skip```\n'
                    'Пропускает песню, которая сейчас проигрывается, и начинает проигрываать следующую')
        embed = discord.Embed(color = 0xffcd4c , title = 'skip', description = help_text)
        await ctx.send(embed = embed)
                
    @help.command()
    async def pause(self, ctx):
        help_text = ('```d.pause```\n'
                    'Приостанавливает воспроизведение песни\n'
                    'В дальнейшем, если бот не выходил из голосового чата, её можно будет воспроизвести снова командой `d.resume`')
        embed = discord.Embed(color = 0xffcd4c , title = 'pause', description = help_text)
        await ctx.send(embed = embed)
                
    @help.command()
    async def resume(self, ctx):
        help_text = ('```d.resume```\n'
                    'Убирает паузу, и начинает воспроизведение с последнего момента перед паузой')
        embed = discord.Embed(color = 0xffcd4c , title = 'resume', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def stop(self, ctx):
        help_text = ('```d.stop```\n'
                    'Окончательно останавливает воспроизведение, и очищае список')
        embed = discord.Embed(color = 0xffcd4c , title = 'stop', description = help_text)
        await ctx.send(embed = embed)
    
    @help.command()
    async def leave(self, ctx):
        help_text = ('```d.leave```\n'
                    'Выкидывает бота из голосового чата')
        embed = discord.Embed(color = 0xffcd4c , title = 'leave', description = help_text)
        await ctx.send(embed = embed)


    @help.command(aliases = ['clean', 'purge'])
    async def clear(self, ctx):
        help_text = ('```d.clear <кол-во сообщений>```\n'
                    'Массовое удаление сообщение из текущего канала\n'
                    'Нужны привилегии управления сообщениями')
        embed = discord.Embed(color = 0xffcd4c , title = 'clear', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def idclear(self, ctx):
        help_text = ('```d.idclear <ID Сообщения>```\n'
                    'Удаляет одно сообщение по MessageID. Команда вводится в канале с тем самым сообщением\n'
                    'Нужны привилегии управления сообщениями')
        embed = discord.Embed(color = 0xffcd4c , title = 'idclear', description = help_text)
        await ctx.send(embed = embed)
    
    @help.command()
    async def kick(self, ctx):
        help_text = ('```d.kick <@упоминание_пользователя>```\n'
                    'Кикает пользователя по пинку\n'
                    'Нужны привилегии кика пользователей')
        embed = discord.Embed(color = 0xffcd4c , title = 'kick', description = help_text)
        await ctx.send(embed = embed)
        
    @help.command()
    async def ban(self, ctx):
        help_text = ('```d.ban <@упоминание_пользователя>```\n'
                    'Банит пользователя по пинку\n'
                    'Нужны привилегии бана пользователей')
        embed = discord.Embed(color = 0xffcd4c , title = 'ban', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def avatar(self, ctx):
        help_text = ('```d.avatar```\n'
                    '```d.avatar @упоминание_пользователя```\n'
                    'Отправляет вам аватар пользователя (или ваш)\n')
        embed = discord.Embed(color = 0xffcd4c , title = 'avatar', description = help_text)
        await ctx.send(embed = embed)

    @help.command(aliases = ['user'])
    async def user_info(self, ctx):
        help_text = ('```d.user_info```\n'
                    '```d.user_info @упоминание_пользователя```\n'
                    'Отправляет вам информацию о пользователе (если никого не упоминали, то информацию о вас)\n'
                    'Алиасы: user\n')
        embed = discord.Embed(color = 0xffcd4c , title = 'user_info', description = help_text)
        await ctx.send(embed = embed)

    @help.command(aliases = ['server', 'guild', 'guild_info'])
    async def server_info(self, ctx):
        help_text = ('```d.server_info```\n'
                    'Отправляет вам информацию о сервере\n'
                    'Алиасы: server, guild, guild_info\n')
        embed = discord.Embed(color = 0xffcd4c , title = 'server_info', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def translate(self, ctx):
        help_text = ('```d.translate <язык> <текст>```\n'
                    'Переводит ваш текст, язык указывается по стандарту ISO 639-1\n'
                    'Полный список наименований будет доступен после нажатия на кнопку ниже')
        embed = discord.Embed(color = 0xffcd4c , title = 'translate', description = help_text)
        await ctx.send(
        embed = embed,
        components = [
        Button(style = ButtonStyle.URL, url = 'https://snipp.ru/handbk/iso-639-1', label='Коды ISO 639-1')
        ])
        
    @help.command()
    async def poll(self, ctx):
        help_text = ('```d.poll "вопрос" "вариант 1" "вариант 2"```\n'
                    'Начинает голосование\n'
                    'Вопросы, и варианты ответа ОБЯЗАТЕЛЬНО указываются в "двойных кавычках"\n'
                    'Пример:\n'
                    '```d.poll "Какие чипсы вы предпочитаете" "Lais" "Prongls" "2 корочки"```\n'
                    'Плохой пример:\n'
                    '```d.poll Какие чипсы вы предпочитаете Lais Prongls 2 корочки```\n'
                    'В плохом примере нету кавычек, соответственно, за вопрос будет считыватся только `Какие`, остальное будет вариантами ответа\n'
                    '**Для вывода результата плохого примера, нажмите на кнопку ниже**')
        embed = discord.Embed(color = 0xffcd4c , title = 'poll', description = help_text)
        await ctx.send(embed = embed, components = [[Button(style = ButtonStyle.blue, label = 'Результат Плохого Примера')]])
                
    @help.command()
    async def echo(self, ctx):
        help_text = ('```d.echo <текст>```\n'
                    'Повторяет сообщение за вами')
        embed = discord.Embed(color = 0xffcd4c , title = 'echo', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def enchode_b64(self, ctx):
        help_text = ('```d.encode_b64 <текст>```\n'
                    'Конвертирует текст в Base64')
        embed = discord.Embed(color = 0xffcd4c , title = 'encode_b64', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def decode_b64(self, ctx):
        help_text = ('```d.decode_b64 <base64 текст>```\n'
                    'Конвертирует ваш Base64 код в ноормальный, понятный любому человеку (кроме фаната а4) текст')
        embed = discord.Embed(color = 0xffcd4c , title = 'decode_b64', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def encode_binary(self, ctx):
        help_text = ('```d.encode_binary <текст>```\n'
                    'Конвертирует текст в бинарный код')
        embed = discord.Embed(color = 0xffcd4c , title = 'encode_binary', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def decode_binary(self, ctx):
        help_text = ('```d.decode_binary <бинарный код>```\n'
                    'Конвертирует бинарный код в текст')
        embed = discord.Embed(color = 0xffcd4c , title = 'decode_binary', description = help_text)
        await ctx.send(embed = embed)

    @help.command()
    async def slots(self, ctx):
        help_text = ('```d.slots```\n'
                    'Игра в однорукого бандита (бесплатно, без регистрации и смс)')
        embed = discord.Embed(color = 0xffcd4c , title = 'slots', description = help_text)
        await ctx.send(embed = embed)

    @help.command(aliases = ['rockpaperscissors', 'rps'])
    async def janken(self, ctx):
        help_text = ('```d.janken```\n'
                    'Классические камень-ножницы-бумага.\n'
                    'Правила обьяснять не буду, ибо их итак все знают\n'
                    '(Кстать, *это первая команда с алиасами!*)\n'
                    'Алиасы: `d.rockpaperscissors`, `d.rps`\n')
        embed = discord.Embed(color = 0xffcd4c , title = 'Камень-Ножницы-Бумага', description = help_text)
        await ctx.send(embed = embed)

def setup(bot):
        bot.add_cog(Help(bot))
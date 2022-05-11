import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle


class Help(commands.Cog):
        def __init__(self, bot):
                self.bot = bot
                bot.remove_command('help')

        @commands.command()
        async def help(self, ctx, command = None):
                if command == None:
                        helptext = (''':regional_indicator_d: :regional_indicator_e: :regional_indicator_b: :regional_indicator_i: :regional_indicator_l: :regional_indicator_b: :regional_indicator_o: :regional_indicator_t:\n'''
                                    '''***🤪 Префикс: `d.`***\n'''
                                    '''**❤️‍🔥 Создатель: GamerDisclaimer. https://youtube.com/c/gamerdisclaimer**\n'''
                                    '''**🏛️ Сервер, на который ты должен зайти (ну пазязя): https://discord.gg/4dEmQjt**\n''')
                        helpmusic = ('''**play** `название песни или URL` - подключает бота к голосовому каналу и воспроизводит песню (или добавляет её в список)\n'''
                                     '''**pause** - останавливает воспроизведение\n'''
                                    '''**resume** - снимает паузу\n'''
                                    '''**stop** - останавливает воспроизведение\n'''
                                    '''**leave** - выкидывает бота из чата (жаль бота, хнык)\n'''
                                    '''**skip** - пропуск одной песни из списка\n'''
                                    '''**queue** - просмотр очереди проигрывания\n''')
                        helpmoderation = ('''**clear** *<кол-во сообщений>* - удаляет сообщения\n'''
                                          '''**idclear** `id сообщения` - удаляет сообщение по MessageID\n'''
                                          '''**kick** `@упоминание пользователя` `причина (необязательно)` - кик пользователя\n'''
                                          '''**ban** `@упоминание пользователя` `причина (необязательно)` - бан пользователя\n''')
                        helptextch = ('''**translate** `Язык в формате ISO 639-1` `текст` - переводчик\n'''
                                      '''**poll** `"вопрос (ОБЯЗАТЕЛЬНО В КАВЫЧКАХ!)"` `"вариант ответа (В КАВЫЧКАХ!)"` - голосование, **вопрос и варианты ответа указываются в кавычках!**\n'''
                                      '''**echo** `текст` - просто повторяет всё, что вы ввели после echo\n''')
                        helpconv = ('''**encode_b64** `текст` - конвертирует ваш текст в base64\n'''
                                    '''**decode_b64** `base64 текст` - конвертирует base64 в человеческий, читаемый текст\n'''
                                    '''**encode_binary** `текст` - конвертирует ваш текст в бинарный код (1 и 0)\n'''
                                    '''**decode_binary** `бинарный код` - конвертирует бинарный код в текст, который вы скорее всего, умеете читать\n''')

                        helpgames = ('''**slots** - Азино777\n'''
                                     '''**janken** - Камень-Ножницы-Бумага\n''')
                        helphelp = ('''**help** - вывод меню с командами\n'''
                                    '''**help** `название команды` - более подробное описание команды, и её использование\n''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'Помощь', description = helptext) # Создание Embed'a
                        embed.add_field(name = '🎵 ***Музыка*** 🎵', value = helpmusic, inline=False)
                        embed.add_field(name = '🔧 ***Модерация*** 🔧', value = helpmoderation, inline=False)
                        embed.add_field(name = '📝 ***Текстовые*** 📝', value = helptextch, inline=False)
                        embed.add_field(name = '💱 ***Конвертеры*** 💱', value = helpconv, inline=False)
                        embed.add_field(name = '🎮 ***Недоигры*** 🎮', value = helpgames, inline=False)
                        embed.add_field(name = '❓ ***Помощь*** ❓', value = helphelp, inline=False)
                        await ctx.send(embed = embed) # Отправляем Embed
                        
                elif command == 'play':
                        helptext = ('''```d.help <название песни, или URL>```\n'''
                                    '''Воспроизводит песню с YouTube, если бот не подключен к голосовому чату, то подключает его к нему''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'play', description = helptext)
                        await ctx.send(embed = embed)
                elif command == 'pause':
                        helptext = ('''```d.pause```\n'''
                                    '''Приостанавливает воспроизведение песни\n'''
                                    '''В дальнейшем, если бот не выходил из голосового чата, её можно будет воспроизвести снова командой `d.resume`''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'pause', description = helptext)
                        await ctx.send(embed = embed)
                elif command == 'resume':
                        helptext = ('''```d.resume```\n'''
                                    '''Убирает паузу, и начинает воспроизведение с последнего момента перед паузой''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'resume', description = helptext)
                        await ctx.send(embed = embed)
                elif command == 'stop':
                        helptext = ('''```d.stop```\n'''
                                     '''Окончательно останавливает воспроизведение''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'stop', description = helptext)
                        await ctx.send(embed = embed)
                elif command == 'leave':
                        helptext = ('''```d.leave```\n'''
                                    '''Выкидывает бота из голосового чата''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'leave', description = helptext)
                        await ctx.send(embed = embed)


                elif command == 'clear':
                        helptext = ('''```d.clear <кол-во сообщений>```\n'''
                                    '''Массовое удаление сообщение из текущего канала\n'''
                                    '''Нужны привилегии управления сообщениями''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'clear', description = helptext)
                        await ctx.send(embed = embed)
                elif command == 'idclear':
                        helptext = ('''```d.idclear <ID Сообщения>```\n'''
                                    '''Удаляет одно сообщение по MessageID. Команда вводится в канале с тем самым сообщением\n'''
                                    '''Нужны привилегии управления сообщениями''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'idclear', description = helptext)
                        await ctx.send(embed = embed)
                elif command == 'kick':
                        helptext = ('''```d.kick <@упоминание_пользователя>```\n'''
                                    '''Кикает пользователя по пинку\n'''
                                    '''Нужны привилегии кика пользователей''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'kick', description = helptext)
                        await ctx.send(embed = embed)
                elif command == 'ban':
                        helptext = ('''```d.ban <@упоминание_пользователя>```\n'''
                                    '''Банит пользователя по пинку\n'''
                                    '''Нужны привилегии бана пользователей''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'ban', description = helptext)
                        await ctx.send(embed = embed)


                elif command == 'translate':
                        helptext = ('''```d.translate <язык> <текст>```\n'''
                                    '''Переводит ваш текст, язык указывается по стандарту ISO 639-1\n'''
                                    '''Полный список наименований будет доступен после нажатия на кнопку ниже''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'translate', description = helptext)
                        await ctx.send(
                        embed = embed,
                        components = [
                        Button(style = ButtonStyle.URL, url = 'https://snipp.ru/handbk/iso-639-1', label='Коды ISO 639-1')
                        ])
                elif command == 'poll':
                        helptext = ('''```d.poll "вопрос" "вариант 1" "вариант 2"```\n'''
                                    '''Начинает голосование\n'''
                                    '''Вопросы, и варианты ответа ОБЯЗАТЕЛЬНО указываются в "двойных кавычках"\n'''

                                    '''Пример:\n'''
                                    '''```d.poll "Какие чипсы вы предпочитаете" "Lais" "Prongls" "2 корочки"```\n'''

                                    '''Плохой пример:\n'''
                                    '''```d.poll Какие чипсы вы предпочитаете Lais Prongls 2 корочки```\n'''

                                    '''В плохом примере нету кавычек, соответственно, за вопрос будет считыватся только `Какие`, остальное будет вариантами ответа\n'''
                                    '''**Для вывода результата плохого примера, нажмите на кнопку ниже**''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'poll', description = helptext)
                        await ctx.send(
                        embed = embed,
                        components = [[Button(style = ButtonStyle.blue, label = 'Результат Плохого Примера')]]
                        )

                        responce = await self.bot.wait_for('button_click', check = lambda message: message.author == ctx.author)
                        if responce.component.label == 'Результат Плохого Примера':
                                Desc = ('''1⃣ чипсы \n'''
                                        '''2⃣ вы\n'''
                                        '''3⃣ предпочитаете\n'''
                                        '''4⃣ Lais \n'''
                                        '''5⃣ Prongls\n'''
                                        '''6⃣ 2\n'''
                                        '''7⃣ корочки''')
                                BadExample = discord.Embed(color = 0xffcd4c , title = f'{self.bot.get_emoji(879411306157985862)} GamerDisclaimer#7647: Какие', description=Desc)
                                await responce.respond(embed=BadExample)


                elif command == 'echo':
                        helptext = ('''```d.echo <текст>```\n'''
                                   '''Повторяет сообщение за вами''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'echo', description = helptext)
                        await ctx.send(embed = embed)



                elif command == 'encode_b64':
                        helptext = ('''```d.encode_b64 <текст>```\n'''
                                    '''Конвертирует текст в Base64''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'encode_b64', description = helptext)
                        await ctx.send(embed = embed)

                elif command == 'decode_b64':
                        helptext = ('''```d.decode_b64 <base64 текст>```\n'''
                                    '''Конвертирует ваш Base64 код в ноормальный, понятный любому человеку (кроме фаната а4) текст''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'decode_b64', description = helptext)
                        await ctx.send(embed = embed)

                elif command == 'encode_binary':
                        helptext = ('''```d.encode_binary <текст>```\n'''
                                    '''Конвертирует текст в бинарный код''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'encode_binary', description = helptext)
                        await ctx.send(embed = embed)

                elif command == 'decode_binary':
                        helptext = ('''```d.decode_binary <бинарный код>```\n'''
                                    '''Конвертирует бинарный код в текст''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'decode_binary', description = helptext)
                        await ctx.send(embed = embed)

                elif command == 'slots':
                        helptext = ('''```d.slots```\n'''
                                    '''Игра в однорукого бандита (бесплатно, без регистрации и смс)''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'slots', description = helptext)
                        await ctx.send(embed = embed)

                elif command == 'janken':
                        helptext = ('''```d.janken```\n'''
                                   '''Классические камень-ножницы-бумага.\n'''
                                   '''Правила обьяснять не буду, ибо их итак все знают\n'''
                                   '''(Кстать, *это первая команда с алиасами!*)\n'''

                                   '''Алиасы: `d.rockpaperscissors`, `d.rps`\n''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'Камень-Ножницы-Бумага', description = helptext)
                        await ctx.send(embed = embed)

                elif command == 'help':
                        helptext = ('''У этой команды есть два варианта:\n'''

                                    '''1. ```d.help```\n'''
                                    '''Вывод меню со списком команд\n'''

                                    '''2. ```d.help poll```\n'''
                                    '''Вывод подробного описания команды (в нашем случае `poll`)''')
                        embed = discord.Embed(color = 0xffcd4c , title = 'help', description = helptext)
                        await ctx.send(embed = embed)

                else:
                        await ctx.send(f'❌ К сожалению, для команды {command} страницы с применением не существует :(. ***Подсказка: команды указываются БЕЗ ПРЕФИКСОВ, вот так: ***`d.help poll`')

def setup(bot):
        bot.add_cog(Help(bot))
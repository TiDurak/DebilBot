############################## IMPORTS ##############################

### Config ###
from config import settings
### Config ###

### Discord Libs ###
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions, CommandInvokeError, MemberNotFound, BotMissingPermissions
from discord.errors import NotFound
from discord import NotFound as NotFound_DS
from discord.ext.commands import CommandNotFound

from discord_components import DiscordComponents, Button, ButtonStyle
### Discord Libs ###

### JSON libs ###
import json
import requests
### JSON libs ###

### Youtube-DL to the music bot ###
from youtube_dl import YoutubeDL
### Youtube-DL to the music bot ###

### Colorama to the logs ###
import colorama
from colorama import Fore, Back, Style
### Colorama to the logs ###

### Translator ###
from googletrans import Translator
### Translator ###

### Some other libs ###
from asyncio import sleep
import traceback
import random
### Some other libs ###

############################## IMPORTS ##############################



### Colorama initialisation ###
colorama.init()
### Colorama initialisation ###

### YTDL and FFmpeg configs ###
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
### YTDL and FFmpeg configs ###

### Discord.Py and discord_components initialisation ###
bot = commands.Bot(command_prefix = settings['prefix'])
DiscordComponents(bot)
### Discord.Py and discord_components initialisation ###

### Errors catching ###
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('❌ Комманда не существует!')
    elif isinstance(error, MissingPermissions):
        await ctx.send('❌ У вас нету привилегий управления сообщениями!')
    elif isinstance(error, MemberNotFound):
        await ctx.send('❌ Участник не найден!')

    raise error
### Errors catching ###

### Bot status changer
@bot.event
async def on_ready():
    while True:
        RandomInteger = random.randint(0, 10)

        if RandomInteger == 0:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ровный базар"))
        elif RandomInteger == 1:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="порнушку"))
        elif RandomInteger == 2:
            await bot.change_presence(activity=discord.Game(name="игру"))
        elif RandomInteger == 3:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="зомбоящик"))
        elif RandomInteger == 4:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="на писюны"))


        await sleep(5)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("d.help"))
        await sleep(5)
### Bot status changer ###    





############################## HELP COMMAND ##############################

bot.remove_command('help') # Removes standard help method

@bot.command()
async def help(ctx, command = None):
    if command == None:
        helptext = (''':regional_indicator_d: :regional_indicator_e: :regional_indicator_b: :regional_indicator_i: :regional_indicator_l: :regional_indicator_b: :regional_indicator_o: :regional_indicator_t:
            
***🤪 Префикс: `d.`***
**❤️‍🔥 Создатель: GamerDisclaimer. https://youtube.com/c/gamerdisclaimer**
**🏛️ Сервер, на который ты должен зайти (ну пазязя): https://discord.gg/4dEmQjt**''')
        helpmusic = ('''**play** `название песни или URL` - подключает бота к голосовому каналу и воспроизводит песню (потом автоматически отключает)
**pause** - останавливает воспроизведение
**resume** - снимает паузу
**stop** - останавливает воспроизведение
**leave** - выкидывает бота из чата (жаль бота, хнык)''')
        helpmoderation = ('''**clear** *<кол-во сообщений>* - удаляет сообщения
**idclear** `id сообщения` - удаляет сообщение по MessageID
**kick** `@упоминание пользователя` `причина (необязательно)` - кик пользователя
**ban** `@упоминание пользователя` `причина (необязательно)` - бан пользователя''')
        helptextch = ('''**translate** `Язык в формате ISO 639-1` `текст` - переводчик
**poll** `"вопрос (ОБЯЗАТЕЛЬНО В КАВЫЧКАХ!)"` `"вариант ответа (В КАВЫЧКАХ!)"` - голосование, **вопрос и варианты ответа указываются в кавычках!** 
**echo** `текст` - просто повторяет всё, что вы ввели после echo''')
        helpconv = ('''**encode_b64** `текст` - конвертирует ваш текст в base64
**decode_b64** `base64 текст` - конвертирует base64 в человеческий, читаемый текст
**encode_binary** `текст` - конвертирует ваш текст в бинарный код (1 и 0)
**decode_binary** `бинарный код` - конвертирует бинарный код в текст, который вы скорее всего, умеете читать''')

        helpgames = ('''**slots** - Азино777
**janken** - Камень-Ножницы-Бумага''')
        helphelp = ('''**help** - вывод меню с командами
**help** `название команды` - более подробное описание команды, и её использование''')
        embed = discord.Embed(color = 0xffcd4c , title = 'Помощь', description = helptext) # Создание Embed'a
        embed.add_field(name = '🎵 ***Музыка*** 🎵', value = helpmusic, inline=False)
        embed.add_field(name = '🔧 ***Модерация*** 🔧', value = helpmoderation, inline=False)
        embed.add_field(name = '📝 ***Текстовые*** 📝', value = helptextch, inline=False)
        embed.add_field(name = '💱 ***Конвертеры*** 💱', value = helpconv, inline=False)
        embed.add_field(name = '🎮 ***Недоигры*** 🎮', value = helpgames, inline=False)
        embed.add_field(name = '❓ ***Помощь*** ❓', value = helphelp, inline=False)
        await ctx.send(embed = embed) # Отправляем Embed
        
    elif command == 'play':
        helptext = ('''```d.help <название песни, или URL>```
Воспроизводит песню с YouTube, если бот не подключен к голосовому чату, то подключает его к нему''')
        embed = discord.Embed(color = 0xffcd4c , title = 'play', description = helptext)
        await ctx.send(embed = embed)
    elif command == 'pause':
        helptext = ('''```d.pause```
Приостанавливает воспроизведение песни
В дальнейшем, если бот не выходил из голосового чата, её можно будет воспроизвести снова командой `d.resume`''')
        embed = discord.Embed(color = 0xffcd4c , title = 'pause', description = helptext)
        await ctx.send(embed = embed)
    elif command == 'resume':
        helptext = ('''```d.resume```
Убирает паузу, и начинает воспроизведение с последнего момента перед паузой''')
        embed = discord.Embed(color = 0xffcd4c , title = 'resume', description = helptext)
        await ctx.send(embed = embed)
    elif command == 'stop':
        helptext = ('''```d.stop```
Окончательно останавливает воспроизведение''')
        embed = discord.Embed(color = 0xffcd4c , title = 'stop', description = helptext)
        await ctx.send(embed = embed)
    elif command == 'leave':
        helptext = ('''```d.leave```
Выкидывает бота из голосового чата''')
        embed = discord.Embed(color = 0xffcd4c , title = 'leave', description = helptext)
        await ctx.send(embed = embed)


    elif command == 'clear':
        helptext = ('''```d.clear <кол-во сообщений>```
Массовое удаление сообщение из текущего канала
Нужны привилегии управления сообщениями''')
        embed = discord.Embed(color = 0xffcd4c , title = 'clear', description = helptext)
        await ctx.send(embed = embed)
    elif command == 'idclear':
        helptext = ('''```d.idclear <ID Сообщения>```
Удаляет одно сообщения по MessageID. Команда вводится в канале с тем самым сообщением
Нужны привилегии управления сообщениями''')
        embed = discord.Embed(color = 0xffcd4c , title = 'idclear', description = helptext)
        await ctx.send(embed = embed)
    elif command == 'kick':
        helptext = ('''```d.kick <@упоминание_пользователя>```
Кикает пользователя по пинку
Нужны привилегии кика пользователей''')
        embed = discord.Embed(color = 0xffcd4c , title = 'kick', description = helptext)
        await ctx.send(embed = embed)
    elif command == 'ban':
        helptext = ('''```d.ban <@упоминание_пользователя>```
Банит пользователя по пинку
Нужны привилегии бана пользователей''')
        embed = discord.Embed(color = 0xffcd4c , title = 'ban', description = helptext)
        await ctx.send(embed = embed)


    elif command == 'translate':
        helptext = ('''```d.translate <язык> <текст>```
Переводит ваш текст, язык указывается по стандарту ISO 639-1
Полный список наименований будет доступен после нажатия на кнопку ниже''')
        embed = discord.Embed(color = 0xffcd4c , title = 'translate', description = helptext)
        await ctx.send(
            embed = embed,
            components = [
            Button(style = ButtonStyle.URL, url = 'https://snipp.ru/handbk/iso-639-1', label='Коды ISO 639-1')
            ])
    elif command == 'poll':
        helptext = ('''```d.poll <"вопрос"> <"вариант 1"> <"вариант 2">```
Начинает голосование
Вопросы, и варианты ответа ОБЯЗАТЕЛЬНО указываются в "двойных кавычках"

Пример:
```d.poll "Какие чипсы вы предпочитаете" "Lais" "Prongls" "2 корочки"```

Плохой пример:
```d.poll Какие чипсы вы предпочитаете Lais Prongls 2 корочки```

В плохом примере нету кавычек, соответственно, за вопрос будет считыватся только `Какие`, остальное будет вариантами ответа
**Для вывода результата плохого примера, нажмите на кнопку ниже**''')
        embed = discord.Embed(color = 0xffcd4c , title = 'poll', description = helptext)
        await ctx.send(
            embed = embed,
            components = [[Button(style = ButtonStyle.blue, label = 'Результат Плохого Примера')]]
            )

        responce = await bot.wait_for('button_click', check = lambda message: message.author == ctx.author)
        if responce.component.label == 'Результат Плохого Примера':
            Desc = ('''1⃣ чипсы 
2⃣ вы
3⃣ предпочитаете
4⃣ Lais 
5⃣ Prongls
6⃣ 2
7⃣ корочки''')
            BadExample = discord.Embed(color = 0xffcd4c , title = f'{bot.get_emoji(879411306157985862)} GamerDisclaimer#7647: Какие', description=Desc)
            await responce.respond(embed=BadExample)


    elif command == 'echo':
        helptext = '''```d.echo <текст>```
Повторяет сообщение за вами'''
        embed = discord.Embed(color = 0xffcd4c , title = 'echo', description = helptext)
        await ctx.send(embed = embed)



    elif command == 'encode_b64':
        helptext = ('''```d.encode_b64 <текст>```
Конвертирует текст в Base64''')
        embed = discord.Embed(color = 0xffcd4c , title = 'encode_b64', description = helptext)
        await ctx.send(embed = embed)

    elif command == 'decode_b64':
        helptext = ('''```d.decode_b64 <base64 текст>```
Конвертирует ваш Base64 код в ноормальный, понятный любому человеку (кроме фаната а4) текст''')
        embed = discord.Embed(color = 0xffcd4c , title = 'decode_b64', description = helptext)
        await ctx.send(embed = embed)

    elif command == 'encode_binary':
        helptext = ('''```d.encode_binary <текст>```
Конвертирует текст в бинарный код''')
        embed = discord.Embed(color = 0xffcd4c , title = 'encode_binary', description = helptext)
        await ctx.send(embed = embed)

    elif command == 'decode_binary':
        helptext = ('''```d.decode_binary <бинарный код>```
Конвертирует бинарный код в текст''')
        embed = discord.Embed(color = 0xffcd4c , title = 'decode_binary', description = helptext)
        await ctx.send(embed = embed)

    elif command == 'slots':
        helptext = ('''```d.slots```
Игра в однорукого бандита (бесплатно, без регистрации и смс)''')
        embed = discord.Embed(color = 0xffcd4c , title = 'slots', description = helptext)
        await ctx.send(embed = embed)

    elif command == 'janken':
        helptext = '''```d.janken```
Классические камень-ножницы-бумага.
Правила обьяснять не буду, ибо их итак все знают
(Кстать, *это первая команда с алиасами!*)

Алиасы: `d.rockpaperscissors`, `d.rps`'''
        embed = discord.Embed(color = 0xffcd4c , title = 'Камень-Ножницы-Бумага', description = helptext)
        await ctx.send(embed = embed)

    elif command == 'help':
        helptext = ('''У этой команды есть два варианта:

1. ```d.help```
Вывод меню со списком команд

2. ```d.help poll```
Вывод подробного описания команды (в нашем случае `poll`)''')
        embed = discord.Embed(color = 0xffcd4c , title = 'help', description = helptext)
        await ctx.send(embed = embed)

    else:
        await ctx.send('❌ Данная команда не существует. ***Подсказка: команды указываются БЕЗ ПРЕФИКСОВ, вот так: ***`d.help poll`')

############################## HELP COMMAND ##############################



######################################################################
############################## COMMANDS ##############################
######################################################################

### Test command, lol ###
@bot.command()
async def hello(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')


############################## MUSIC BOT ##############################
@bot.command()
async def play(ctx, *, arg):
    global vc
    if not ctx.message.author.voice:
        await ctx.send('❌ **ЛОХ ТУПОЙ!** Сначало подключись к голосовому чату, а потом мне мозги !@?%#&')
        return
    try:
        voice_channel = ctx.message.author.voice.channel
        print(voice_channel)
        vc = await voice_channel.connect()
    except Exception as e:
        print('Уже подключен или не удалось подключиться')
        print(e)


    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            global firstmessage
            def search(arg):
                global video
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    try:
                        get(arg) 
                    except:
                        video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
                    else:
                        video = ydl.extract_info(arg, download=False)

                return video

            search(arg)
            URL = video['formats'][0]['url']
            

            # Time Converter #
            total_seconds = video.get('duration')                               # Here we get a TOTAL COUNT OF SECONDS
            hours = (total_seconds - ( total_seconds % 3600))/3600              # Here we get a HOURS
            seconds_minus_hours = (total_seconds - hours*3600)                  # Here SECONDS - HOURS
            minutes = (seconds_minus_hours - (seconds_minus_hours % 60) )/60    # Here we get a MINUTES
            seconds = seconds_minus_hours - minutes*60                          # Here we get a SECONDS

            time = '{}:{}:{}'.format(int(hours), int(minutes), int(seconds))    # Here we get a normal TIME
            # Time Converter #


            if vc.is_playing() or vc.is_paused():
                vc.stop()
            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source = URL, **FFMPEG_OPTIONS))

            embed = (discord.Embed(title = f'{bot.get_emoji(878537811601555466)} Играет',
                                   description = '**' + video.get('title') + '**',
                                   color = 0xff2a2a)
                    .add_field(name = '⌛ Продолжительность', value = time)
                    .add_field(name = '🙃 Запросил', value = ctx.author.mention)
                    .set_thumbnail(url = video.get('thumbnail'))  )
            firstmessage = await ctx.send(
            embed = embed,
            components = [
                [
                    Button(style = ButtonStyle.red, label = 'Выход', emoji = '🚪'),
                    Button(style = ButtonStyle.red, label = 'Стоп', emoji = '🛑'),
                    Button(style = ButtonStyle.blue, label = 'Пауза / Продолжить', emoji = '⏯️'),
                ]
            ])
            while vc.is_playing:

                responce = await bot.wait_for('button_click', check = lambda message: message.author == ctx.author)
                
                if responce.component.label == 'Выход':
                    if vc.is_playing():
                        vc.stop()
                    await vc.disconnect()
                    await firstmessage.edit(embed=embed, components=[])
                    await responce.respond(content = '🚪 Бот вышел из голосового чата')

                elif responce.component.label == 'Стоп':
                    vc.stop()
                    await firstmessage.edit(embed=embed, components=[Button(style = ButtonStyle.red, label = 'Выход', emoji = '🚪')])
                    await responce.respond(content = '🛑 Остановлено!')

                elif responce.component.label == 'Пауза / Продолжить':
                    if vc.is_playing():
                        vc.pause()
                        await responce.respond(content = '⏯️ Пауза!')

                    elif vc.is_paused():
                        vc.resume()
                        await responce.respond(content = '⏯️ Продолжим...')

            
    except Exception as e:
        await ctx.send('?! ОШИБКА!!', delete_after = 3)
        print(e)



@bot.command()
async def leave(ctx):
    try:
        await vc.disconnect()
        await ctx.send('🚪 Бот вышел из голосового чата')
    except:
        await ctx.send( f'{bot.get_emoji(518051242807787520)} Опять нашёлся умник, который пытается обхитрить систему, и хочет выгнать бота из голосового чата, который даже к нему не подключен...')

@bot.command()
async def stop(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send('🛑 Остановлено!')
    elif vc.is_paused():
        vc.stop()
        await ctx.send('🛑 Остановлено!')

@bot.command()
async def pause(ctx):
    if not vc.is_paused():
        vc.pause()
        await ctx.send('🔇 Воспроизведение приостановлено!')
    elif vc.is_paused():
        await ctx.send(f'{bot.get_emoji(518051242807787520)} Лол, я на паузе, что ты ещё хочешь от меня?!')

@bot.command()
async def resume(ctx):
    if not vc.is_playing():
        vc.resume()
        await ctx.send('🎵 Идёт Воспроизведение!')
    elif vc.is_playing():
        await ctx.send('🤪 Лол, я не на паузе, зачем ты ввёл эту команду?!')

############################## MUSIC BOT ##############################


############################## CONVERTERS ##############################

@bot.command()
async def encode_b64(ctx, *, arg):
    response = requests.get(f'https://some-random-api.ml/base64?encode={arg}') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff8080, title = 'Base64 Encoder', description = json_data['base64']) # Создание Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command()
async def decode_b64(ctx, *, arg):
    response = requests.get(f'https://some-random-api.ml/base64?decode={arg}') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff8080, title = 'Base64 Decoder', description = json_data['text']) # Создание Embed'a
    await ctx.send(embed = embed) # Отправляем Embed


@bot.command()
async def encode_binary(ctx, *, arg):
    response = requests.get(f'https://some-random-api.ml/binary?encode={arg}') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff8080, title = 'Binary Encoder', description = json_data['binary']) # Создание Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command()
async def decode_binary(ctx, *, arg):
    response = requests.get(f'https://some-random-api.ml/binary?decode={arg}') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0xff8080, title = 'Binary Decoder', description = json_data['text']) # Создание Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

############################## CONVERTERS ##############################

############################## TEXT COMMANDS ##############################
@bot.command()
async def translate(ctx, lang, *, thing):
    warntext = '''
        ❌ Указан неверный язык! Использование команды:
        d.translate `ru` `Ваш текст`
        `ru` является языком, на который нужно переводить
        Вместо `ru` может быть:
        `ua`, `en`, `hu`, и т.д.'''
    try:
        translator = Translator()
        translation = translator.translate(thing, dest=lang)
        await ctx.send(translation.text)
    except ValueError:
        await ctx.send(warntext)


@bot.command()
async def echo(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(arg)



@bot.command()
async def poll(ctx, question, *options: str):
    await ctx.message.delete()
    if len(options) <= 1:
        await ctx.send('❌ Для создания голосования нужно хотя-бы 1 ответ!')
        return
    if len(options) > 10:
        await ctx.send('❌ Нельзя использовать более 10 ответов!')
        return

    if len(options) == 2 and options[0] == 'да' and options[1] == 'нет':
        reactions = ['✅', '❌']
    else:
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

    description = []
    for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)
    embed = discord.Embed(color = 0xffcd4c , title = f'{bot.get_emoji(879411306157985862)} {ctx.message.author}: {question}', description=''.join(description))
    react_message = await ctx.send(embed=embed)
    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)
    embed.set_footer(text= f'Poll ID: {react_message.id} \nКстати! Вопрос нужно указывать в кавычках!' )
    await react_message.edit(embed=embed)

############################## TEXT COMMANDS ##############################

############################## GAMES ##############################

@bot.command(aliases=['rps', 'rockpaperscissors'])
async def janken(ctx):
    desc = 'Сыграй со мной в камень ножницы бумагу! выбери один из вариантов ниже:'
    embed = discord.Embed(color = 0xffcd4c, title = f'{ctx.message.author}: Камень Ножницы Бумага', description = desc)
    gamebar = await ctx.send(
        embed = embed,
        components = [
            [
                Button(style = ButtonStyle.blue, label = 'Камень', emoji = '🗿'),
                Button(style = ButtonStyle.red, label = 'Ножницы', emoji = '✂️'),
                Button(style = ButtonStyle.gray, label = 'Бумага', emoji = '📄'),
            ]
    ])
    dictionary = {
        1: 'Камень',
        2: 'Ножницы',
        3: 'Бумага',
    }
    SomeChoice = random.choice(dictionary)
    responce = await bot.wait_for('button_click', check = lambda message: message.author == ctx.author)
                
    if responce.component.label == 'Камень':
        await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{desc} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}`' ), components=[])

    elif responce.component.label == 'Ножницы':
        await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{desc} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}`' ), components=[])

    elif responce.component.label == 'Бумага':
        await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{desc} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}`' ), components=[])


    # Заметка для себя:
    # responce.component.label - выбор юзера
    # SomeChoice - выбор бота

    # Ничья
    if responce.component.label == SomeChoice:
        await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Ничья!'), components=[])

    # Победа
    elif responce.component.label == 'Камень' and SomeChoice == 'Ножницы':
        await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Победа!!!'), components=[])

    elif responce.component.label == 'Ножницы' and SomeChoice == 'Бумага':
        await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Победа!!!'), components=[])
    
    elif responce.component.label == 'Бумага' and SomeChoice == 'Камень':
        await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Победа!!!'), components=[])

    else:
        await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Проигрыш :('), components=[])


@bot.command()
async def slots(ctx):
    author_id = str(ctx.author.id)

    symbols = ['🍒', '🔔', '7️⃣', '👑', '☠️']




    percentage = random.uniform(0,100)
    if percentage <= 30:
        slot1 = symbols[4]
    elif percentage <= 55 and percentage > 30:
        slot1 = symbols[3]
    elif percentage <= 70 and percentage > 55:
        slot1 = symbols[2]
    elif percentage <= 85 and percentage > 70:
        slot1 = symbols[1]
    elif percentage <= 100 and percentage > 85:
        slot1 = symbols[0]

    percentage = random.uniform(0,100)
    if percentage <= 20:
        slot2 = symbols[4]
    elif percentage <= 40 and percentage > 20:
        slot2 = symbols[3]
    elif percentage <= 60 and percentage > 40:
        slot2 = symbols[2]
    elif percentage <= 87 and percentage > 60:
        slot2 = symbols[1]
    elif percentage <= 100 and percentage > 87:
        slot2 = symbols[0]

    percentage = random.uniform(0,100)
    if percentage <= 35:
        slot3 = symbols[4]
    elif percentage <= 41 and percentage > 35:
        slot3 = symbols[3]
    elif percentage <= 60 and percentage > 41:
        slot3 = symbols[2]
    elif percentage <= 94 and percentage > 60:
        slot3 = symbols[1]
    elif percentage <= 100 and percentage > 95:
        slot3 = symbols[0]

    if slot1 == slot2 == slot3 == symbols[4]:
        footer = 'Лузер! Ваш баланс обнулён'
    elif slot1 == slot2 == slot3 == symbols[3]:
        footer = '+ 5 000 баксов на ваш счёт'
    elif slot1 == slot2 == slot3 == symbols[2]:
        footer = '+ 10 000 баксов на ваш счёт'
    elif slot1 == slot2 == slot3 == symbols[1]:
        footer = '+ 15 000 баксов на ваш счёт'
    elif slot1 == slot2 == slot3 == symbols[0]:
        footer = 'ДЖЕКПОТ!!! + 1 000 000 баксов на ваш счёт'
    elif slot1 == slot2 == symbols[0] or slot1 == slot3 == symbols[0] or slot2 == slot3 == symbols[0]:
        footer = '+ 3 500 баксов на ваш счёт'
    elif slot1 == symbols[0] or slot2 == symbols[0] or slot3 == symbols[0]:
        footer = '+ 1 500 баксов на ваш счёт'
    else:
        footer = 'Ничего('
    embed = discord.Embed(color = 0x36c600, title = '🎰 Slots Azino777', description = str(slot1) + str(slot2) + str(slot3))
    embed.set_footer(text = footer, icon_url = "https://i.imgur.com/uZIlRnK.png")
    await ctx.send(embed = embed)

############################## GAMES ##############################

############################## MODERATION ##############################

@has_permissions(manage_messages = True)
@bot.command()
async def clear(ctx, arg1):
    amount = int(arg1)
    await ctx.message.delete()
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'{bot.get_emoji(880326444356612116)} Очищено {amount} сообщений! Запрос на очистку от {ctx.author.mention}')



@has_permissions(kick_members = True)
@bot.command()
async def kick(ctx, member: discord.Member, reason = 'Не указано'):
    await member.kick(reason=reason)
    await ctx.send("Изгоняем участника {0} по причине: {1}".format(member, reason))

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, CommandInvokeError):
        await ctx.send('❌ У бота нету привилегий кика! Пожалуйста, удалите бота из сервера, и добавьте его снова по следующей ссылке: https://discord.com/api/oauth2/authorize?client_id=699912361481470032&permissions=8&scope=bot')
        raise error


@has_permissions(ban_members = True)
@bot.command()
async def ban(ctx, member: discord.Member, reason = 'Не указано'):
    await member.ban(reason=reason)
    await ctx.send("Баним участника {0} по причине: {1}".format(member, reason))

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, CommandInvokeError):
        await ctx.send('❌ У бота нету привилегий бана! Пожалуйста, удалите бота из сервера, и добавьте его снова по следующей ссылке: https://discord.com/api/oauth2/authorize?client_id=699912361481470032&permissions=8&scope=bot')
@has_permissions(manage_messages = True)
@bot.command()
async def idclear(ctx, arg1):
    await ctx.message.delete()
    try:
        msg = await ctx.channel.fetch_message(arg1)
        await msg.delete(arg1)
    except NotFound as e:
        await ctx.send('❌ Введите корректный ID сообщения! *Для того, чтобы скопировать ID сообщения, перейдите в настройки пользователя > расширенные, и включите режим разработчика. После этого вы сможете копировать ID сообщений.*')
    except NotFound_DS as e:
        await ctx.send('❌ Введите корректный ID сообщения! *Для того, чтобы скопировать ID сообщения, перейдите в настройки пользователя > расширенные, и включите режим разработчика. После этого вы сможете копировать ID сообщений.*')


    
@idclear.error
async def idclear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('❌ Извините, но у вас нету привилегий для доступа к этой команде. Для выполнения команды нужны привилегии `управление сообщениями`.')
    elif isinstance(error, (NotFound, NotFound_DS)):
        await ctx.send('❌ Введите корректный ID сообщения! *Для того, чтобы скопировать ID сообщения, перейдите в настройки пользователя > расширенные, и включите режим разработчика. После этого вы сможете копировать ID сообщений.*')
    elif isinstance(error, CommandInvokeError):
        await ctx.send('❌ У бота нету привилегий управления сообщениями! Пожалуйста, удалите бота из сервера, и добавьте его снова по следующей ссылке: https://discord.com/api/oauth2/authorize?client_id=699912361481470032&permissions=8&scope=bot')

############################## MODERATION ##############################

############################## MODERATION (GD ONLY!) ##############################

@bot.command()
async def clear_gd(ctx, arg1):
    await ctx.message.delete()
    amount = int(arg1)
    if ctx.author.id == 432111233672675340:
        await ctx.channel.purge(limit = amount)
    else:
        await ctx.send('❌ Ты не GamerDisclaimer!!!')
        print(Back.RED + str(ctx.author) + ' пытался выполнить команду clear_gd!!!' + Style.RESET_ALL)

@bot.command()
async def ban_gd(ctx, member: discord.Member):
    await ctx.message.delete()
    if ctx.author.id == 432111233672675340:
        await member.ban(reason='sex)')
    else:
        await ctx.send('❌ Ты не GamerDisclaimer!!!')
        print(Back.RED + str(ctx.author) + ' пытался выполнить команду ban_gd!!!' + Style.RESET_ALL)


@bot.command()
async def fetch_gd(ctx, arg1):
    await ctx.message.delete()
    if ctx.author.id == 432111233672675340:
        msg = await ctx.channel.fetch_message(arg1)
        await msg.delete()
    else:
        await ctx.send('❌ Ты не GamerDisclaimer!!!')
        print(Back.RED + str(ctx.author) + ' пытался выполнить команду fetch_gd!!!' + Style.RESET_ALL)

############################## MODERATION (GD ONLY!) ##############################




#########################################################################
############################## BOT RUNNING ##############################
#########################################################################

bot.run(settings['token'])
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
from youtube_dl import YoutubeDL
from config import settings

### YTDL and FFmpeg configs ###
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
### YTDL and FFmpeg configs ###

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, arg):
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
                vc.play(discord.FFmpegPCMAudio(executable=settings['path_to_ffmpeg'], source = URL, **FFMPEG_OPTIONS))

                embed = (discord.Embed(title = f'{self.bot.get_emoji(878537811601555466)} Играет',
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

                    responce = await self.bot.wait_for('button_click', check = lambda message: message.author == ctx.author)
                    
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



    @commands.command()
    async def leave(self, ctx):
        try:
            await vc.disconnect()
            await ctx.send('🚪 Бот вышел из голосового чата')
        except:
            await ctx.send( f'{self.bot.get_emoji(518051242807787520)} Опять нашёлся умник, который пытается обхитрить систему, и хочет выгнать бота из голосового чата, который даже к нему не подключен...')

    @commands.command()
    async def stop(self, ctx):
        if vc.is_playing():
            vc.stop()
            await ctx.send('🛑 Остановлено!')
        elif vc.is_paused():
            vc.stop()
            await ctx.send('🛑 Остановлено!')

    @commands.command()
    async def pause(self, ctx):
        if not vc.is_paused():
            vc.pause()
            await ctx.send('🔇 Воспроизведение приостановлено!')
        elif vc.is_paused():
            await ctx.send(f'{self.bot.get_emoji(518051242807787520)} Лол, я на паузе, что ты ещё хочешь от меня?!')

    @commands.command()
    async def resume(self, ctx):
        if not vc.is_playing():
            vc.resume()
            await ctx.send('🎵 Идёт Воспроизведение!')
        elif vc.is_playing():
            await ctx.send('🤪 Лол, я не на паузе, зачем ты ввёл эту команду?!')

def setup(bot):
        bot.add_cog(Music(bot))
import asyncio
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
from youtube_dl import YoutubeDL
from config import settings

### YTDL and FFmpeg configs ###
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
### YTDL and FFmpeg configs ###

class Queue():
    def __init__(self):
        self.__vc = None
        self.__queue = []
        self.__playing_now = None
        self.__playing_now_embed = None

    def add_track(self, title):
        self.__queue.append(title)

    def play_next(self):
        if len(self.__queue) > 0:
            next_track = self.__queue.pop(0)
            self.__playing_now = next_track
            return next_track
        else:
            return 0

    def get_playing_now(self):
        print(self.__playing_now)
        return self.__playing_now

    def set_playing_now(self, track):
        self.__playing_now = track

    def clear(self):
        self.__queue = []
        self.__playing_now = None

    def is_empty(self):
        if len(self.__queue):
            return False
        else:
            return True

    def length(self):
        return len(self.__queue)

    def get_by_id(self, id):
        return self.__queue[id]



class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__client = discord.Client()
        self.__queue = Queue()

    async def __connect(self, ctx):
        try:
            if not ctx.message.author.voice:
                await ctx.send('❌ **ЛОХ ТУПОЙ!** Сначало подключись к голосовому чату, а потом мне мозги !@?%#&')
                return
            
            voice_channel = ctx.message.author.voice.channel
            print(voice_channel)
            self.__vc = await voice_channel.connect()
        except:
            pass

    def __search(self, arg):
        video = None
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                get(arg) 
            except:
                video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else:
                video = ydl.extract_info(arg, download=False)
            return video

    def __get_url(self, extracted):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            url = extracted['formats'][0]['url']
            return url

    def __get_duration(self, video):
        total_seconds = video.get('duration')
        hours = (total_seconds - ( total_seconds % 3600))/3600
        seconds_minus_hours = (total_seconds - hours*3600)
        minutes = (seconds_minus_hours - (seconds_minus_hours % 60) )/60
        seconds = seconds_minus_hours - minutes*60

        time = '{}:{}:{}'.format(int(hours), int(minutes), int(seconds))
        return time

    async def __play(self, context, url, video):
        duration = self.__get_duration(video)
        embed = (discord.Embed(title = f'{self.bot.get_emoji(settings["emojis"]["youtube"])} Играет',
                               description = f"**{video.get('title')}**",
                               color = 0xff2a2a)
                .add_field(name = '⌛ Продолжительность', value = duration)
                .add_field(name = '🙃 Запросил', value = context.author.mention)
                .set_thumbnail(url = video.get('thumbnail'))  )
        firstmessage = await context.send(
        embed = embed,
        components = [
            [
                Button(style = ButtonStyle.red, label = 'Выход', emoji = '🚪'),
                Button(style = ButtonStyle.red, label = 'Стоп', emoji = '🛑'),
                Button(style = ButtonStyle.blue, label = 'Пауза / Продолжить', emoji = '⏯️'),
                Button(style = ButtonStyle.blue, label = 'Пропустить', emoji = '⏭️'),
            ]
        ])

        self.__playing_now_embed = firstmessage
        self.__vc.play(discord.FFmpegPCMAudio(executable=settings['path_to_ffmpeg'], source = url, **FFMPEG_OPTIONS), after = lambda e: self.__skip(context = context))
        title = video.get('title')
        self.__queue.set_playing_now(title)
        while self.__vc.is_playing:
            responce = await self.bot.wait_for('button_click', check = lambda message: message.author == context.author)
            
            match responce.component.label:
                case 'Выход':
                    await self.__playing_now_embed.edit(embed=embed, components=[])
                    self.__leave(context)
                    await responce.respond(content = '🚪 Бот вышел из голосового чата')
                    return
                case 'Стоп':
                    await self.__playing_now_embed.edit(embed=embed, components=[Button(style = ButtonStyle.red, label = 'Выход', emoji = '🚪')])
                    self.__stop(context)
                    await responce.respond(content = '🛑 Остановлено!')
                    return
                case 'Пауза / Продолжить':
                    if self.__vc.is_playing():
                        self.__vc.pause()
                        await responce.respond(content = '⏯️ Пауза')
                    elif self.__vc.is_paused():
                        self.__vc.resume()
                        await responce.respond(content = '⏯️ Продолжаю...')
                    return
                case 'Пропустить':
                    await self.__playing_now_embed.edit(embed=embed, components=[])
                    await responce.respond(content = '⏭️ Скипаю...')
                    self.__skip(context)


    def __skip(self, context):
        asyncio.run_coroutine_threadsafe(self.__playing_now_embed.edit(components=[]), self.bot.loop)
        if self.__vc.is_playing():
            self.__vc.pause()
        if not self.__queue.is_empty():
            next_track = self.__queue.play_next()
            url = self.__get_url(next_track)
            asyncio.run_coroutine_threadsafe(self.__play(context, url, next_track), self.bot.loop)
            if self.__playing_now_embed is not None:
                self.__playing_now_embed = None
        else:
            asyncio.run_coroutine_threadsafe(context.send("Список воспроизведения пуст.", delete_after = 3), self.bot.loop)

    def __stop(self, context):
        self.__queue.clear()
        if self.__vc.is_playing():
            self.__vc.stop()
        elif self.__vc.is_paused():
            self.__vc.stop()
        self.__playing_now_embed = None

    def __leave(self, context):
        self.__pause(context)
        asyncio.run_coroutine_threadsafe(self.__vc.disconnect(), self.bot.loop)

    def __pause(self, context):
        if not self.__vc.is_paused():
            self.__vc.pause()
        elif self.__vc.is_paused():
            asyncio.run_coroutine_threadsafe(context.send(f'{self.bot.get_emoji(settings["emojis"]["wuuut"])} Лол, я на паузе, что ты ещё хочешь от меня?! Для этого есть `{settings.get("prefix")}resume`'), self.bot.loop)

    def __resume(self, context):
        if not self.__vc.is_playing():
            self.__vc.resume()
        elif self.__vc.is_playing():
            asyncio.run_coroutine_threadsafe(context.send('🤪 Лол, я не на паузе, зачем ты ввёл эту команду?!'), self.bot.loop)

    @commands.command()
    async def play(self, ctx, *, arg):
        await self.__connect(ctx)
        try:
            vid = self.__search(arg)
        except IndexError:
            await ctx.send(":x: Песня не была найдена :(")
            await self.__vc.disconnect()
            return
            
        if not self.__vc.is_playing():
            url = self.__get_url(vid)
            await self.__play(ctx, url, vid)
        else:
            self.__queue.add_track(vid)
            await ctx.send(f"**{vid.get('title')}** добавлен в список, бля.")

    @commands.command()
    async def skip(self, ctx):
        await ctx.send("⏭️ Скипаю")
        self.__skip(ctx)

    @commands.command(name="queue")
    async def queue_embed(self, ctx):
        now = self.__queue.get_playing_now()
        if now != None:
            embed = (discord.Embed(title = "📜 Список Воспроизведения", color = 0xf0cd4f))
            embed.add_field(name = "▶️ Сейчас Играет", value = now, inline = False)
            for i in range(self.__queue.length()):
                video = self.__queue.get_by_id(i)
                embed.add_field(name = i+1, value = video.get('title'), inline = False)
            await ctx.send(embed = embed)
        else:
            embed = (discord.Embed(title = "📜 Список Воспроизведения", 
                                   color = 0xf0cd4f,
                                   description = "Список воспроизведения пуст."))
            await ctx.send(embed = embed)
        


    @commands.command()
    async def leave(self, ctx):
        try:
            self.__leave(ctx)
            await сtx.send('🚪 Бот вышел из голосового чата')
        except: 
            await ctx.send(f'{self.bot.get_emoji(settings["emojis"]["wuuut"])} Опять нашёлся умник, который пытается обхитрить систему, и хочет выгнать бота из голосового чата, который даже к нему не подключен...')
            

    @commands.command()
    async def stop(self, ctx):
        self.__stop(ctx)
        await ctx.send('🛑 Остановлено!')


    @commands.command()
    async def pause(self, ctx):
        self.__pause(ctx)
        await ctx.send('🔇 Воспроизведение приостановлено!')

    @commands.command()
    async def resume(self, ctx):
        self.__resume(ctx)
        await ctx.send('🎵 Идёт Воспроизведение!')

def setup(bot):
    bot.add_cog(Music(bot))
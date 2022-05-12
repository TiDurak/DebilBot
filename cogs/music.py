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
        return self.__playing_now

    def set_playing_now(self, track):
        self.__playing_now = track

    def clear(self):
        self.__queue = []
        self.__playing_now = None

    def is_empty(self):
        if len(self.__queue):
            return True
        else:
            return False

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

    async def __play(self, context, url, video):
        embed = (discord.Embed(title = f'{self.bot.get_emoji(878537811601555466)} Играет',
                               description = f"**{video.get('title')}**",
                               color = 0xff2a2a)
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
                    return
                case 'Пауза / Продолжить':
                    if self.__vc.is_playing():
                        self.__vc.pause()
                        await responce.respond(content = '⏯️')
                    elif self.__vc.is_paused():
                        self.__vc.resume()
                        await responce.respond(content = '⏯️')
                    return
                case 'Пропустить':
                    await self.__playing_now_embed.edit(embed=embed, components=[])
                    await responce.respond(content = '⏭️ Скипаю...')
                    self.__skip(context)


    def __skip(self, context):
        if self.__vc.is_playing():
            self.__vc.pause()
        if self.__queue.is_empty():
            asyncio.run_coroutine_threadsafe(self.__playing_now_embed.delete(), self.bot.loop)
            next_track = self.__queue.play_next()
            vid = self.__search(next_track)
            url = self.__get_url(vid)
            asyncio.run_coroutine_threadsafe(self.__play(context, url, vid), self.bot.loop)
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
        asyncio.run_coroutine_threadsafe(context.send('🛑 Остановлено!'), self.bot.loop)
        self.__playing_now_embed = None

    def __leave(self, context):
        try:
            self.__stop(context)
            asyncio.run_coroutine_threadsafe(self.__vc.disconnect(), self.bot.loop)
            asyncio.run_coroutine_threadsafe(context.send('🚪 Бот вышел из голосового чата'), self.bot.loop)
        except:
            asyncio.run_coroutine_threadsafe(context.send( f'{self.bot.get_emoji(518051242807787520)} Опять нашёлся умник, который пытается обхитрить систему, и хочет выгнать бота из голосового чата, который даже к нему не подключен...'), self.bot.loop)

    def __pause(self, context):
        if not self.__vc.is_paused():
            self.__vc.pause()
            asyncio.run_coroutine_threadsafe(context.send('🔇 Воспроизведение приостановлено!'), self.bot.loop)
        elif self.__vc.is_paused():
            asyncio.run_coroutine_threadsafe(context.send(f'{self.bot.get_emoji(518051242807787520)} Лол, я на паузе, что ты ещё хочешь от меня?! Для этого есть `{settings.get("prefix")}resume`'), self.bot.loop)

    def __resume(self, context):
        if not self.__vc.is_playing():
            self.__vc.resume()
            asyncio.run_coroutine_threadsafe(ctx.send('🎵 Идёт Воспроизведение!'), self.bot.loop)
        elif self.__vc.is_playing():
            asyncio.run_coroutine_threadsafe(ctx.send('🤪 Лол, я не на паузе, зачем ты ввёл эту команду?!'), self.bot.loop)

    @commands.command()
    async def play(self, ctx, *, arg):
        await self.__connect(ctx)
        vid = self.__search(arg)
        if not self.__vc.is_playing() or not self.__vc.is_paused():
            url = self.__get_url(vid)
            await self.__play(ctx, url, vid)
        else:
            self.__queue.add_track(arg)
            await ctx.send(f"**{vid.get('title')}** добавлен в список.")

    @commands.command()
    async def skip(self, ctx):
        ctx.send("⏭️ Скипаю")
        self.__skip(ctx)

    @commands.command(name="queue")
    async def queue_embed(self, ctx):
        now = self.__queue.get_playing_now()
        if now != None:
            embed = (discord.Embed(title = "📜 Список Воспроизведения", color = 0xf0cd4f))
            video_now = self.__search(now)
            embed.add_field(name = "▶️ Сейчас Играет", value = video_now.get('title'), inline = False)
            for i in range(self.__queue.length()):
                embed.add_field(name = i+1, value = self.__queue.get_by_id(i), inline = False)
            await ctx.send(embed = embed)
        else:
            embed = (discord.Embed(title = "📜 Список Воспроизведения", 
                                   color = 0xf0cd4f,
                                   description = "Список воспроизведения пуст."))
            await ctx.send(embed = embed)
        


    @commands.command()
    async def leave(self, ctx):
        self.__leave(ctx)

    @commands.command()
    async def stop(self, ctx):
        self.__stop(ctx)


    @commands.command()
    async def pause(self, ctx):
        self.__pause(ctx)

    @commands.command()
    async def resume(self, ctx):
        self.__resume(ctx)

def setup(bot):
    bot.add_cog(Music(bot))
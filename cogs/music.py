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
        self.__queue = []

    def add_track(self, title):
        self.__queue.append(title)

    def play_next(self):
        if len(self.__queue) > 0:
            next_track = self.__queue.pop(0)
            return next_track
        else:
            return 0

    def clear(self):
        self.__queue = []

    def now_playing(self):
        if len(self.__queue) > 0:
            return self.__queue[0]
        else:
            return 0

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
            global vc
            if not ctx.message.author.voice:
                await ctx.send('❌ **ЛОХ ТУПОЙ!** Сначало подключись к голосовому чату, а потом мне мозги !@?%#&')
                return
            
            voice_channel = ctx.message.author.voice.channel
            print(voice_channel)
            vc = await voice_channel.connect()
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

        vc.play(discord.FFmpegPCMAudio(executable=settings['path_to_ffmpeg'], source = url, **FFMPEG_OPTIONS), after = lambda e: self.__skip(context = context, embed_to_delete = firstmessage))

        while vc.is_playing:
            responce = await self.bot.wait_for('button_click', check = lambda message: message.author == context.author)
            
            match responce.component.label:
                case 'Выход':
                    if vc.is_playing():
                        vc.stop()
                    await vc.disconnect()
                    await firstmessage.edit(embed=embed, components=[])
                    await responce.respond(content = '🚪 Бот вышел из голосового чата')
                    return
                case 'Стоп':
                    self.__stop(context)
                    await firstmessage.edit(embed=embed, components=[Button(style = ButtonStyle.red, label = 'Выход', emoji = '🚪')])
                    return
                case 'Пауза / Продолжить':
                    if vc.is_playing():
                        vc.pause()
                        await responce.respond(content = '⏯️')
                    elif vc.is_paused():
                        vc.resume()
                        await responce.respond(content = '⏯️')
                    return
                case 'Пропустить':
                    await firstmessage.edit(embed=embed, components=[])
                    await responce.respond(content = '⏭️ Скипаю...')
                    self.__skip(context, firstmessage)


    def __skip(self, context, embed_to_delete):
        if vc.is_playing():
            vc.pause()
        if self.__queue.is_empty():
            asyncio.run_coroutine_threadsafe(embed_to_delete.delete(), self.bot.loop)
            next_track = self.__queue.play_next()
            vid = self.__search(next_track)
            url = self.__get_url(vid)
            asyncio.run_coroutine_threadsafe(self.__play(context, url, vid), self.bot.loop)
        else:
            asyncio.run_coroutine_threadsafe(context.send("Список воспроизведения пуст.", delete_after = 3), self.bot.loop)

    def __stop(self, context):
        self.__queue.clear()
        if vc.is_playing():
            vc.stop()
        elif vc.is_paused():
            vc.stop()
        asyncio.run_coroutine_threadsafe(context.send('🛑 Остановлено!'), self.bot.loop)

    @commands.command()
    async def play(self, ctx, *, arg):
        await self.__connect(ctx)
        vid = self.__search(arg)
        if not vc.is_playing():
            url = self.__get_url(vid)
            await self.__play(ctx, url, vid)
        else:
            self.__queue.add_track(arg)
            await ctx.send(f"**{vid.get('title')}** добавлен в список.")

    @commands.command()
    async def skip(self, ctx):
        await self.__skip(self, ctx)

    @commands.command(name="queue")
    async def queue_embed(self, ctx):
        embed = (discord.Embed(title = "📜 Список Воспроизведения", color = 0xf0cd4f))
        now = self.__queue.now_playing()
        if now != 0:
            video_now = self.__search(now)
            embed.add_field(name = "Сейчас Играет", value = video_now.get('title'), inline = False)
        for i in range(self.__queue.length()):
            embed.add_field(name = i+1, value = self.__queue.get_by_id(i), inline = False)
        await ctx.send(embed = embed)


    @commands.command()
    async def leave(self, ctx):
        try:
            await vc.disconnect()
            await ctx.send('🚪 Бот вышел из голосового чата')
        except:
            await ctx.send( f'{self.bot.get_emoji(518051242807787520)} Опять нашёлся умник, который пытается обхитрить систему, и хочет выгнать бота из голосового чата, который даже к нему не подключен...')

    @commands.command()
    async def stop(self, ctx):
        self.__stop(ctx)


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
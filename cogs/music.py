import asyncio
import datetime
import discord
from discord.ext import commands
from yt_dlp import YoutubeDL, utils
from config import settings

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'quiet': True}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


class Queue:
    def __init__(self):
        self.__vc = None
        self.__queue = []
        self.__playing_now = None

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
    def __init__(self, bot, intents):
        self.bot = bot
        self.__client = discord.Client(intents=intents)
        self.__queue = Queue()

    async def __connect(self, ctx):
        try:
            if not ctx.message.author.voice:
                await ctx.send('❌ **ЛОХ ТУПОЙ!** Сначала подключись к голосовому чату, а потом мне мозги !@?%#&')
                return

            voice_channel = ctx.message.author.voice.channel
            self.__vc = await voice_channel.connect()
        except:
            pass

    def __extract(self, arg):
        video = None
        with YoutubeDL(YDL_OPTIONS) as ydl:
            # noinspection PyExceptClausesOrder
            try:
                video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
                return video
            except utils.DownloadError:  # If not found video by basic searching
                video = ydl.extract_info(arg, download=False)
                return video
            except utils.DownloadError:  # If url was not found
                raise IndexError()

    def __get_url(self, extracted):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            url = extracted['url']
            return url

    # noinspection PyUnresolvedReferences
    class PlayerButtons(discord.ui.View):
        def __init__(self, voice_chat, context, leave, stop, pause, resume, skip):
            super().__init__()
            self.__vc = voice_chat
            self.__ctx = context
            self.__leave = leave
            self.__stop = stop
            self.__pause = pause
            self.__resume = resume
            self.__skip = skip

        @discord.ui.button(style=discord.ButtonStyle.red, label='Выход', emoji='🚪')
        async def button_leave(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Хорошо блин, ухожу, тупой ты дебил", tts=True, delete_after=8)
            self.__leave(self.__ctx)

        @discord.ui.button(style=discord.ButtonStyle.red, label='Стоп', emoji='🛑')
        async def button_stop(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Хорошо, тормознул", tts=True, delete_after=8)
            self.__stop(self.__ctx)

        @discord.ui.button(style=discord.ButtonStyle.blurple, label='Пауза / Продолжить', emoji='⏯️')
        async def button_pause_resume(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.__vc.is_playing():
                await interaction.response.send_message("Усё, усё, пауза", tts=True, delete_after=8)
                self.__vc.pause()
            elif self.__vc.is_paused():
                await interaction.response.send_message("Играем дальше, значит. Ты задолбал", tts=True, delete_after=8)
                self.__vc.resume()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label='Пропустить', emoji='⏭️')
        async def button_skip(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Эту песню мы попускаем, потому что гивно", tts=True,
                                                    delete_after=8)
            self.__skip(self.__ctx)

    async def __play(self, context, url, video):
        self.__vc.play(discord.FFmpegPCMAudio(executable=settings['path_to_ffmpeg'], source=url, **FFMPEG_OPTIONS),
                       after=lambda e: self.__skip(context=context))
        duration = video.get("duration")
        embed = (discord.Embed(title=f'{self.bot.get_emoji(settings["emojis"]["youtube"])} Играет',
                               description=f"**{video.get('title')}**",
                               color=0xff2a2a)
                 .add_field(name='⌛ Продолжительность', value=datetime.timedelta(seconds=duration))
                 .add_field(name='🙃 Запросил', value=context.author.mention)
                 .set_thumbnail(url=video.get('thumbnail')))
        await context.send(embed=embed, view=self.PlayerButtons(self.__vc,
                                                                context,
                                                                self.__leave,
                                                                self.__stop,
                                                                self.__pause,
                                                                self.__resume,
                                                                self.__skip))

        title = video.get('title')
        self.__queue.set_playing_now(title)

    def __skip(self, context):
        if self.__vc.is_playing():
            self.__vc.pause()
        if not self.__queue.is_empty():
            next_track = self.__queue.play_next()
            url = self.__get_url(next_track)
            asyncio.run_coroutine_threadsafe(self.__play(context, url, next_track), self.bot.loop)
        else:
            asyncio.run_coroutine_threadsafe(context.send("Список воспроизведения пуст.", delete_after=3),
                                             self.bot.loop)

    def __stop(self, context):
        self.__queue.clear()
        if self.__vc.is_playing():
            self.__vc.stop()
        elif self.__vc.is_paused():
            self.__vc.stop()

    def __leave(self, context):
        self.__pause(context)
        asyncio.run_coroutine_threadsafe(self.__vc.disconnect(), self.bot.loop)

    def __pause(self, context):
        if not self.__vc.is_paused():
            self.__vc.pause()

    def __resume(self, context):
        if not not self.__vc.is_playing():
            self.__vc.resume()
        elif self.__vc.is_playing():
            asyncio.run_coroutine_threadsafe(context.send("🤪 Лол, я не на паузе, "
                                                          "зачем ты ввёл эту команду?!"), self.bot.loop)

    @commands.command()
    async def play(self, ctx, *, arg):
        """Воспроизводит песню с YouTube, или добавляет её в список, если сейчас играет другая песня"""
        await self.__connect(ctx)
        try:
            vid = self.__extract(arg)
        except IndexError:
            await ctx.send(":x: Ты дебилка тупая! ЧТО ЗА ГОВНО ТЫ ВЫСРАЛ?! "
                           "КАК Я МОГУ ТЕБЕ ЭТУ ХЕРЕСЬ НАЙТИ?!!??!?!?!?1!!7!?!")
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
        """Пропускает текущую песню"""

        try:
            self.__skip(ctx)
            await ctx.send("⏭️ Скипаю")
        except AttributeError:
            await ctx.message.add_reaction("🤡")
            await ctx.send(f":face_with_symbols_over_mouth: ДА ТЫ ЗАЕБААААЛ! Сорянчик. {ctx.author.mention}, "
                           f"Как ты хочешь скипнуть музон, если Я БЛЯДЬ НЕ ПОДКЛЮЧЁН К ГОЛОСОВОМУ ЧААТУ! "
                           f"БЛЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯДЬ!!")
            await ctx.send("С такими додиками, как ты, я сталкиваюсь 24/7")

    @commands.command(name="queue")
    async def queue_embed(self, ctx):
        """Показывает список следующих песен"""

        now = self.__queue.get_playing_now()
        if now != None:
            embed = (discord.Embed(title="📜 Список Воспроизведения", color=0xf0cd4f))
            embed.add_field(name="▶️ Сейчас Играет", value=now, inline=False)
            for i in range(self.__queue.length()):
                video = self.__queue.get_by_id(i)
                embed.add_field(name=i + 1, value=video.get('title'), inline=False)
            await ctx.send(embed=embed)
        else:
            embed = (discord.Embed(title="📜 Список Воспроизведения",
                                   color=0xf0cd4f,
                                   description="Список воспроизведения пуст."))
            await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        """Кикает бота из голосового чата"""

        try:
            self.__leave(ctx)
            await ctx.send('🚪 Бот вышел из голосового чата')
        except AttributeError:
            await ctx.message.add_reaction("🤡")
            await ctx.send(f'{self.bot.get_emoji(settings["emojis"]["wuuut"])} Опять нашёлся умник, '
                           f'который пытается обхитрить систему, и хочет выгнать бота из голосового чата, '
                           f'который даже к нему не подключен...')

    @commands.command()
    async def stop(self, ctx):
        """Останавливает текущую песню, и очищает список проигрывания"""

        try:
            if self.__vc.is_playing():
                self.__stop(ctx)
                await ctx.send('🛑 Остановлено!')
            else:
                await ctx.message.add_reaction("🤡")
                await ctx.send(f"ТЫЖДУБИНА. Я не могу остановить музон, которого не существует. "
                               f"Фейспалм всей толпой, ребятки. Накидайте ему реакций клоуна")
        except AttributeError:
            await ctx.message.add_reaction("🤡")
            await ctx.send(
                f'{self.bot.get_emoji(settings["emojis"]["wuuut"])} ТЫЖДУБИНА. Я не могу остановить музон, которого не существует. '
                f'Фейспалм всей толпой, ребятки. Накидайте ему реакций клоуна')

    @commands.command()
    async def pause(self, ctx):
        """Ставит песню на паузу"""

        try:
            if not self.__vc.is_paused():
                self.__pause(ctx)
                await ctx.send('🔇 Воспроизведение приостановлено!')
            else:
                await ctx.message.add_reaction("🤡")
                await ctx.send(f"🤡 Я на паузе, упырь конченный. Для этого есть `{settings.get('prefix')}resume`")
        except AttributeError:
            await ctx.message.add_reaction("🤡")
            await ctx.send(f'{self.bot.get_emoji(settings["emojis"]["wuuut"])} Ты... решил.. поставить на паузу... '
                           f'музыку, которая не играет. Долбаёб всратый...')

    @commands.command()
    async def resume(self, ctx):
        """То же самое, что и пауза, только наоборот (ты лох, и докажи что нет)"""

        try:
            if self.__vc.is_paused():
                self.__resume(ctx)
                await ctx.send('🎵 Идёт Воспроизведение!')
            else:
                await ctx.message.add_reaction("🤡")
                await ctx.send("Дебилка, я не на паузе. Что ты там играть хотел? Ты задолбала")
        except:
            await ctx.message.add_reaction("🤡")
            await ctx.send(f"{self.bot.get_emoji(settings['emojis']['wuuut'])} Ты дауна сын, для начала введи"
                           f"`{settings.get('prefix')}play [название_песни]`")


async def setup(bot, intents):
    await bot.add_cog(Music(bot, intents))

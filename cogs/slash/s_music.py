from config import settings

import asyncio
import datetime

import discord
from discord.errors import ClientException
from discord import app_commands
from discord.ext import commands

from yt_dlp import YoutubeDL, utils

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'quiet': True}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


class Queue:
    def __init__(self):
        self.__vc = None
        self.__queue = {}
        self.__playing_now = {}

    def add_track(self, title, guild_id):
        if guild_id not in self.__queue:
            self.__queue[guild_id] = []
        self.__queue[guild_id].append(title)

    def play_next(self, guild_id):
        if guild_id in self.__queue and len(self.__queue[guild_id]) > 0:
            next_track = self.__queue[guild_id].pop(0)
            self.__playing_now[guild_id] = next_track
            return next_track
        else:
            return 0

    def get_playing_now(self, guild_id):
        track = self.__playing_now.get(guild_id)
        print(track)
        return track

    def set_playing_now(self, track, guild_id):
        self.__playing_now[guild_id] = track

    def clear(self, guild_id):
        if guild_id in self.__queue:
            self.__queue[guild_id] = []
        self.__playing_now[guild_id] = None

    def is_empty(self, guild_id):
        if guild_id not in self.__queue or len(self.__queue[guild_id]) == 0:
            return True
        else:
            return False

    def length(self, guild_id):
        return len(self.__queue.get(guild_id, []))

    def get_by_id(self, index, guild_id):
        if guild_id in self.__queue and 0 <= index < len(self.__queue[guild_id]):
            return self.__queue[guild_id][index]
        return None


class SMusic(commands.Cog):
    """Music"""

    def __init__(self, bot):
        self.bot = bot
        self.__queue = Queue()
        self.vc = None

    def __get_info(self, song):
        video = None
        with YoutubeDL(YDL_OPTIONS) as ydl:
            # noinspection PyExceptClausesOrder
            try:
                video = ydl.extract_info(f"ytsearch3:{song}", download=False)['entries']
                return video
            except utils.DownloadError:  # If not found video by basic searching
                video = ydl.extract_info(song, download=False)
                return video
            except utils.DownloadError:  # If url was not found
                raise IndexError()

    class PlayerButtons(discord.ui.View):
        def __init__(self, voice_chat, leave, stop, pause, resume, skip):
            super().__init__()
            self.__vc = voice_chat
            self.__leave = leave
            self.__stop = stop
            self.__pause = pause
            self.__resume = resume
            self.__skip = skip

        @discord.ui.button(style=discord.ButtonStyle.red, label='Выход', emoji='🚪')
        async def button_leave(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Хорошо блин, ухожу, тупой ты дебил",
                                                    ephemeral=True)
            self.__leave()

        @discord.ui.button(style=discord.ButtonStyle.red, label='Стоп', emoji='🛑')
        async def button_stop(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Хорошо, тормознул",
                                                    ephemeral=True)
            self.__stop(interaction.guild.id)

        @discord.ui.button(style=discord.ButtonStyle.blurple, label='Пауза / Продолжить', emoji='⏯️')
        async def button_pause_resume(self, interaction: discord.Interaction, button: discord.ui.Button):
            if self.__vc.is_playing():
                await interaction.response.send_message("Усё, усё, пауза",
                                                        ephemeral=True)
                self.__vc.pause()
            elif self.__vc.is_paused():
                await interaction.response.send_message("Играем дальше, значит. Ты задолбал",
                                                        ephemeral=True)
                self.__vc.resume()

        @discord.ui.button(style=discord.ButtonStyle.blurple, label='Пропустить', emoji='⏭️')
        async def button_skip(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Эту песню мы попускаем, потому что гивно",
                                                    ephemeral=True)
            self.__skip(interaction)

    async def __play(self, interaction, video):
        self.vc.play(discord.FFmpegPCMAudio(executable=settings['path_to_ffmpeg'],
                                            source=video.get("url"), **FFMPEG_OPTIONS),
                     after=lambda e: self.__skip(interaction=interaction))

        duration = video.get("duration")
        upload_date = video.get("upload_date")
        upload_date = f"{upload_date[:4]}.{upload_date[4:6]}.{upload_date[6:]}"
        embed = (discord.Embed(title=f'{self.bot.get_emoji(settings["emojis"]["youtube"])} Щас шпилит',
                               description=f"**{video.get('title')}**",
                               color=0xff2a2a)
                 .add_field(name="👤 Автор", value=video.get("uploader"), inline=False)
                 .add_field(name="⌛ Длительность", value=datetime.timedelta(seconds=duration))
                 .add_field(name="📅 Дата Загрузки", value=upload_date)
                 .add_field(name="👍 Кол-во Лайков", value=video.get('like_count', 'Скрыто'), inline=False)
                 .add_field(name="🔔 Запросил", value=interaction.user.name, inline=False)
                 .set_thumbnail(url=video.get("thumbnail")))
        await interaction.followup.send(embed=embed, view=self.PlayerButtons(self.vc,
                                                                             self.__leave,
                                                                             self.__stop,
                                                                             self.__pause,
                                                                             self.__resume,
                                                                             self.__skip))

        title = video.get('title')
        self.__queue.set_playing_now(title, interaction.guild.id)
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=title))

    def __skip(self, interaction):
        asyncio.run_coroutine_threadsafe(self.bot.change_presence(status=discord.Status.online,
                                         activity=discord.Game(f"{settings.get('prefix')}help")), self.bot.loop)
        if self.vc.is_playing():
            self.vc.pause()
        if not self.__queue.is_empty(interaction.guild.id):
            next_track = self.__queue.play_next(interaction.guild.id)
            asyncio.run_coroutine_threadsafe(self.__play(interaction, next_track), self.bot.loop)

    def __stop(self, guild_id):
        asyncio.run_coroutine_threadsafe(
            self.bot.change_presence(status=discord.Status.online,
                                     activity=discord.Game(f"{settings.get('prefix')}help")),
            self.bot.loop)

        self.__queue.clear(guild_id)
        if self.vc.is_playing():
            self.vc.stop()
        elif self.vc.is_paused():
            self.vc.stop()

    def __leave(self):
        asyncio.run_coroutine_threadsafe(
            self.bot.change_presence(status=discord.Status.online,
                                     activity=discord.Game(f"{settings.get('prefix')}help")),
            self.bot.loop)
        self.__pause()
        asyncio.run_coroutine_threadsafe(self.vc.disconnect(), self.bot.loop)

    def __pause(self):
        if not self.vc.is_paused():
            self.vc.pause()

    def __resume(self):
        if not not self.vc.is_playing():
            self.vc.resume()

    class SelectSongButtons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
            self.value = None

        @discord.ui.button(style=discord.ButtonStyle.blurple, emoji='1️⃣')
        async def button_first(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Харош, выбрана первая песня", ephemeral=True)
            self.value = 0
            self.stop()

        @discord.ui.button(style=discord.ButtonStyle.blurple, emoji='2️⃣')
        async def button_second(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Окей, будет тебе вторая песня", ephemeral=True)
            self.value = 1
            self.stop()

        @discord.ui.button(style=discord.ButtonStyle.blurple, emoji='3️⃣')
        async def button_third(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Лана, врубаю третью", ephemeral=True)
            self.value = 2
            self.stop()

    @app_commands.command(name="play", description="Врубает песню")
    @app_commands.describe(song="текст поиска")
    async def play(self, interaction: discord.Interaction,
                   song: str):
        if interaction.user.voice is not None:
            try:
                self.vc = await interaction.user.voice.channel.connect()
            except ClientException:
                pass
        else:
            await interaction.response.send_message("Ты не подрублен к голосовому чату")
            return

        await interaction.response.send_message(f"Ищу песню по запросу **\"{song}\"**, подождите немного")
        reply = await interaction.original_response()

        videos = self.__get_info(song)
        view = self.SelectSongButtons()
        embed = (discord.Embed(title=f"🔍 Результаты поиска по запросу \"{song}\"", color=0xf0cd4f))
        for i in range(3):
            upload_date = f"{videos[i]['upload_date'][:4]}.{videos[i]['upload_date'][4:6]}.{videos[i]['upload_date'][6:]}"
            embed.add_field(name=f"{i + 1}. {videos[i].get('title')}",
                            value=f"👤 {videos[i]['uploader']} \n"
                                  f"⏳ {datetime.timedelta(seconds=videos[i]['duration'])} \n"
                                  f"📅 {upload_date}",
                            inline=False)
        await reply.edit(content="", embed=embed, view=view)
        await view.wait()

        if view.value is None:
            await reply.edit(content="## ⌛ Таймаут \n"
                                     "В следующий раз быстрее думай, **кретин**. \n"
                                     "Больше 30 секунд ждать не собираюсь, **уродина** белопольная", embed=None, view=None)
            return
        try:
            vid = videos[view.value]
        except IndexError:
            await interaction.response.send_message(":x: Ты дебилка тупая! ЧТО ЗА ГОВНО ТЫ ВЫСРАЛ?! "
                                                    "КАК Я МОГУ ТЕБЕ ЭТУ ХЕРЕСЬ НАЙТИ?!!??!?!?!?1!!7!?!")
            await self.vc.disconnect()
            return

        if not self.vc.is_playing():
            await self.__play(interaction, vid)
        else:
            self.__queue.add_track(vid, interaction.guild.id)
            await interaction.followup.send(f"**{vid.get('title')}** добавлен в список, бля.")

    @app_commands.command(name="switch_pause", description="Ставит на паузу/врубает твой говномузон")
    async def switch_pause(self, interaction: discord.Interaction):
        if self.vc is not None:
            if self.vc.is_playing():
                await interaction.response.send_message("Усё, усё, пауза")
                self.vc.pause()
            elif self.vc.is_paused():
                await interaction.response.send_message("Играем дальше, значит. Ты задолбал")
                self.vc.resume()
        else:
            await interaction.response.send_message("Бот не подрублен к голосовому чату")

    @app_commands.command(name="skip", description="Скипает музон")
    async def skip(self, interaction: discord.Interaction):
        if self.vc is not None:
            self.__skip(interaction)
            await interaction.response.send_message("Я скипаю твою хреномузыку")
        else:
            await interaction.response.send_message("Бот не подрублен к голосовому чату")

    @app_commands.command(name="stop", description="Стопает музон, и чистит список воспроизведения")
    async def stop(self, interaction: discord.Interaction):
        if self.vc is not None:
            self.__stop(interaction.guild.id)
            await interaction.response.send_message("Я СТОПАЮ МУЗООН НАХ🔞УУЙ")
        else:
            await interaction.response.send_message("Бот не подрублен к голосовому чату")

    @app_commands.command(name="leave", description="Выходит из голосового чата")
    async def leave(self, interaction: discord.Interaction):
        if self.vc is not None:
            await self.vc.disconnect()
            await interaction.response.send_message("Я ЛИВАЮ НАХ🔞УУЙ")
        else:
            await interaction.response.send_message("Бот не подрублен к голосовому чату")

    @app_commands.command(name="queue", description="Показывает список следующих песен")
    async def queue_embed(self, interaction: discord.Interaction):
        now = self.__queue.get_playing_now(interaction.guild.id)
        if now != None:
            embed = (discord.Embed(title="📜 Список Воспроизведения", color=0xf0cd4f))
            embed.add_field(name="▶️ Сейчас Играет", value=now, inline=False)
            for i in range(self.__queue.length(interaction.guild.id)):
                video = self.__queue.get_by_id(i, interaction.guild.id)
                embed.add_field(name=f"{i + 1} по списку", value=video.get('title'), inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            embed = (discord.Embed(title="📜 Список Воспроизведения",
                                   color=0xf0cd4f,
                                   description="Список воспроизведения пуст."))
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SMusic(bot))

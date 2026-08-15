import config
from config import settings
from classes.music import music_buttons, music_manager

import asyncio
import datetime
import discord
from yt_dlp import YoutubeDL, utils
from discord.errors import ClientException

class MusicPlayer:
    def __init__(self, bot):
        self.vc = None
        self.bot = bot
        self.music_manager = music_manager.MusicManager()
        self.__YDL_OPTIONS = config.YDL_OPTIONS
        self.__FFMPEG_OPTIONS = config.FFMPEG_OPTIONS

    def get_info(self, song):
        video = None
        with YoutubeDL(self.__YDL_OPTIONS) as ydl:
            # noinspection PyExceptClausesOrder
            try:
                video = ydl.extract_info(f"ytsearch3:{song}", download=False)['entries']
                return video
            except utils.DownloadError:  # If not found video by basic searching
                video = ydl.extract_info(song, download=False)
                return video
            except utils.DownloadError:  # If url was not found
                raise IndexError()

    async def make_song_embed(self, interaction, song) -> discord.Embed:
        duration = song.get("duration")
        upload_date = song.get("upload_date")
        upload_date = f"{upload_date[:4]}.{upload_date[4:6]}.{upload_date[6:]}"
        embed = (discord.Embed(title=f'{self.bot.get_emoji(settings["emojis"]["youtube"])} Щас шпилит',
                               description=f"**{song.get('title')}**",
                               color=settings.get("main_embed_color"))
                 .add_field(name="👤 Автор", value=song.get("uploader"), inline=False)
                 .add_field(name="⌛ Длительность", value=datetime.timedelta(seconds=duration))
                 .add_field(name="📅 Дата Загрузки", value=upload_date)
                 .add_field(name="👍 Кол-во Лайков", value=song.get('like_count', 'Скрыто'), inline=False)
                 .add_field(name="🔔 Запросил", value=interaction.user.name, inline=False)
                 .set_thumbnail(url=song.get("thumbnail")))
        return embed


    async def search_songs(self, search_request):
        search_results = self.get_info(search_request)
        return search_results

    async def connect_vc(self, interaction):
        if interaction.user.voice is not None:
            try:
                self.vc = await interaction.user.voice.channel.connect()
            except ClientException:
                pass
        else:
            await interaction.response.send_message("Ты не подрублен к голосовому чату")
            return

    async def disconnect_vc(self):
        self.vc.disconnect()

    async def play(self, interaction, song):
        self.vc.play(discord.FFmpegPCMAudio(executable=settings['path_to_ffmpeg'],
                                            source=song.get("url"), **self.__FFMPEG_OPTIONS),
                     after=lambda e: self.skip(interaction=interaction))

        guild_queue = self.music_manager.get_guild_queue(interaction.guild.id)
        guild_queue.queue.set_playing_now(song)
        embed = await self.make_song_embed(interaction, song)
        await interaction.followup.send(embed=embed, view=music_buttons.PlayerButtons(self.vc,
                                                                                      self.leave,
                                                                                      self.stop,
                                                                                      self.pause,
                                                                                      self.resume,
                                                                                      self.skip))

    def skip(self, interaction):
        guild_queue = self.music_manager.get_guild_queue(interaction.guild.id)
        if self.vc.is_playing():
            self.vc.pause()
        if not guild_queue.queue.is_empty():
            next_track = guild_queue.queue.play_next()
            asyncio.run_coroutine_threadsafe(self.play(interaction, next_track), self.bot.loop)

    def stop(self, guild_id):
        guild_queue = self.music_manager.get_guild_queue(guild_id)
        guild_queue.queue.clear(guild_id)
        if self.vc.is_playing():
            self.vc.stop()
        elif self.vc.is_paused():
            self.vc.stop()

    def leave(self):
        self.pause()
        asyncio.run_coroutine_threadsafe(self.vc.disconnect(), self.bot.loop)

    def pause(self):
        if not self.vc.is_paused():
            self.vc.pause()

    def resume(self):
        if not not self.vc.is_playing():
            self.vc.resume()

    def get_vc(self):
        return self.vc

    def is_playing(self) -> bool:
        return self.vc.is_playing()
from config import settings
from classes.music import music_buttons, music_manager, music_player

import asyncio
import datetime

import discord
from discord import app_commands
from discord.ext import commands

class SMusic(commands.Cog):
    """Music"""

    def __init__(self, bot):
        self.bot = bot
        self.music_manager = music_manager.MusicManager()
        self.music_player = music_player.MusicPlayer(self.bot, self.music_manager)
        self.vc = None



    @app_commands.command(name="play", description="Врубает песню")
    @app_commands.describe(search_request="текст поиска")
    async def play(self, interaction: discord.Interaction, search_request: str):
        guild_queue = self.music_manager.get_guild_queue(interaction.guild.id)
        await self.music_player.connect_vc(interaction)

        await interaction.response.send_message(f"Ищу песню по запросу **\"{search_request}\"**, подождите немного")
        reply = await interaction.original_response()
        view = music_buttons.SelectSongButtons()
        found_songs = await self.music_player.search_songs(search_request)
        embed = (
            discord.Embed(title=f"🔍 Результаты поиска по запросу \"{search_request}\"", color=settings.get("main_embed_color")))
        for i in range(3):
            upload_date = f"{found_songs[i]['upload_date'][:4]}.{found_songs[i]['upload_date'][4:6]}.{found_songs[i]['upload_date'][6:]}"
            embed.add_field(name=f"{i + 1}. {found_songs[i].get('title')}",
                            value=f"👤 {found_songs[i]['uploader']} \n"
                                  f"⏳ {datetime.timedelta(seconds=found_songs[i]['duration'])} \n"
                                  f"📅 {upload_date}",
                            inline=False)
        await reply.edit(content="", embed=embed, view=view)
        await view.wait()

        if view.value is None:
            await reply.edit(content="## ⌛ Таймаут \n"
                                     "В следующий раз быстрее думай, **кретин**. \n"
                                     "Больше 30 секунд ждать не собираюсь, **уродина** белопольная", embed=None,
                             view=None)
            return
        try:
            selected_song = found_songs[view.value]
        except IndexError:
            await interaction.response.send_message(":x: Ты дебилка тупая! ЧТО ЗА ГОВНО ТЫ ВЫСРАЛ?! "
                                                    "КАК Я МОГУ ТЕБЕ ЭТУ ХЕРЕСЬ НАЙТИ?!!??!?!?!?1!!7!?!")
            await self.music_player.disconnect_vc()
            return

        if not self.music_player.is_playing():
            await self.music_player.play(interaction, selected_song)
            guild_queue.queue.set_playing_now(selected_song)
        else:
            guild_queue.queue.add_track(selected_song)
            await interaction.followup.send(f"**{selected_song.get('title')}** добавлен в список, бля.")


    @app_commands.command(name="switch_pause", description="Ставит на паузу/врубает твой говномузон")
    async def switch_pause(self, interaction: discord.Interaction):
        if self.vc is not None:
            if self.music_player.is_playing():
                await interaction.response.send_message("Усё, усё, пауза")
                await self.music_player.pause()
            elif self.vc.is_paused():
                await interaction.response.send_message("Играем дальше, значит. Ты задолбал")
                await self.music_player.resume()
        else:
            await interaction.response.send_message("Бот не подрублен к голосовому чату")

    @app_commands.command(name="skip", description="Скипает музон")
    async def skip(self, interaction: discord.Interaction):
        vc = self.music_player.get_vc()
        if vc is not None:
            self.music_player.skip(interaction)
            await interaction.response.send_message("Я скипаю твою хреномузыку")
        else:
            await interaction.response.send_message("Бот не подрублен к голосовому чату")

    @app_commands.command(name="stop", description="Стопает музон, и чистит список воспроизведения")
    async def stop(self, interaction: discord.Interaction):
        vc = self.music_player.get_vc()
        if vc is not None:
            self.music_player.stop(interaction.guild.id)
            await interaction.response.send_message("Я СТОПАЮ МУЗООН НАХ🔞УУЙ")
        else:
            await interaction.response.send_message("Бот не подрублен к голосовому чату")

    @app_commands.command(name="leave", description="Выходит из голосового чата")
    async def leave(self, interaction: discord.Interaction):
        vc = self.music_player.get_vc()
        if vc is not None:
            await self.music_player.disconnect_vc()
            await interaction.response.send_message("Я ЛИВАЮ НАХ🔞УУЙ")
        else:
            await interaction.response.send_message("Бот не подрублен к голосовому чату")

    @app_commands.command(name="queue", description="Показывает список следующих песен")
    async def queue_embed(self, interaction: discord.Interaction):
        guild_queue = self.music_manager.get_guild_queue(interaction.guild.id)
        playing_now = guild_queue.queue.get_playing_now()
        print(playing_now)
        if playing_now is not None:
            embed = (discord.Embed(title="📜 Список Воспроизведения", color=settings.get("main_embed_color")))
            embed.add_field(name="▶️ Сейчас Играет", value=playing_now.get("title"), inline=False)
            for i in range(guild_queue.queue.length()):
                song = guild_queue.queue.get_by_id(i)
                embed.add_field(name=f"{i + 1} по списку", value=song.get('title'), inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            embed = (discord.Embed(title="📜 Список Воспроизведения",
                                   color=settings.get("main_embed_color"),
                                   description="Список воспроизведения пуст."))
            await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SMusic(bot))

import discord

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
        await self.__skip(interaction)

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
import random
import discord
from discord.ext import commands

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # noinspection PyUnresolvedReferences
    class JankenButtons(discord.ui.View):
        def __init__(self):
            super().__init__()

        @discord.ui.button(label="Камень", emoji="🗿", style=discord.ButtonStyle.blurple)
        async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Камень")

        @discord.ui.button(label="Ножницы", emoji="✂️", style=discord.ButtonStyle.red)
        async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Ножницы")

        @discord.ui.button(label="Бумага", emoji="📄", style=discord.ButtonStyle.gray)
        async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Бумага")

    @commands.command(aliases=['rps', 'rockpaperscissors'])
    async def janken(self, ctx):
        description = 'Сыграй со мной в камень ножницы бумагу! выбери один из вариантов ниже:'
        embed = discord.Embed(color = 0xffcd4c, title = f'{ctx.message.author}: Камень Ножницы Бумага', description = description)
        await ctx.send(embed = embed)
        answers = ['Камень', 'Ножницы', 'Бумага']
        choice = random.choice(answers)

        #await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{choice}` \n Проигрыш :('), components=[])


    @commands.command()
    async def slots(self, ctx):
        author_id = str(ctx.author.id)

        symbols = ['🍒', '🔔', '7️⃣', '👑', '☠️']

        slot = [0, 1, 2]

        for i in range(3):
            slot[i] = symbols[random.randint(0,3)]

        is_same = True if slot[0] == slot[1] == slot[2] else False

        if is_same and symbols[4] in slot:
            footer = 'Лузер! Ваш баланс обнулён'
        elif is_same and symbols[3] in slot:
            footer = '+ 5 000 баксов на ваш счёт'
        elif is_same and symbols[2] in slot:
            footer = '+ 10 000 баксов на ваш счёт'
        elif is_same and symbols[1] in slot:
            footer = '+ 15 000 баксов на ваш счёт'
        elif is_same and symbols[0] in slot:
            footer = 'ДЖЕКПОТ!!! + 1 000 000 баксов на ваш счёт'
        elif symbols[0] == slot[0] == slot[1] or slot[0] == slot[2] == symbols[0] or slot[1] == slot[2] == symbols[0]:
            footer = '+ 3 500 баксов на ваш счёт'
        elif symbols[0] in slot:
            footer = '+ 1 500 баксов на ваш счёт'
        else:
            footer = 'Ничего('
        embed = discord.Embed(color = 0x36c600, title = '🎰 Slots Azino777', description = str(slot[0]) + str(slot[1]) + str(slot[2]))
        embed.set_footer(text = footer, icon_url = "https://i.imgur.com/uZIlRnK.png")
        await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Games(bot))
import random
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['rps', 'rockpaperscissors'])
    async def janken(self, ctx):
        desc = 'Сыграй со мной в камень ножницы бумагу! выбери один из вариантов ниже:'
        embed = discord.Embed(color = 0xffcd4c, title = f'{ctx.message.author}: Камень Ножницы Бумага', description = desc)
        gamebar = await ctx.send(
            embed = embed,
            components = [
                [
                    Button(style = ButtonStyle.blue, label = 'Камень', emoji = '🗿'),
                    Button(style = ButtonStyle.red, label = 'Ножницы', emoji = '✂️'),
                    Button(style = ButtonStyle.gray, label = 'Бумага', emoji = '📄'),
                ]
        ])
        dictionary = {
            1: 'Камень',
            2: 'Ножницы',
            3: 'Бумага',
        }
        SomeChoice = random.choice(dictionary)
        responce = await self.bot.wait_for('button_click', check = lambda message: message.author == ctx.author)
                    
        if responce.component.label == 'Камень':
            await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{desc} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}`' ), components=[])

        elif responce.component.label == 'Ножницы':
            await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{desc} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}`' ), components=[])

        elif responce.component.label == 'Бумага':
            await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{desc} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}`' ), components=[])


        # Заметка для себя:
        # responce.component.label - выбор юзера
        # SomeChoice - выбор бота

        # Ничья
        if responce.component.label == SomeChoice:
            await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Ничья!'), components=[])

        # Победа
        elif responce.component.label == 'Камень' and SomeChoice == 'Ножницы':
            await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Победа!!!'), components=[])

        elif responce.component.label == 'Ножницы' and SomeChoice == 'Бумага':
            await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Победа!!!'), components=[])
        
        elif responce.component.label == 'Бумага' and SomeChoice == 'Камень':
            await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Победа!!!'), components=[])

        else:
            await gamebar.edit(embed=discord.Embed(color = embed.color, title = embed.title, description = f'{embed.description} \n Ты выбрал `{responce.component.label}`, а я выбрал `{SomeChoice}` \n Проигрыш :('), components=[])


    @commands.command()
    async def slots(self, ctx):
        author_id = str(ctx.author.id)

        symbols = ['🍒', '🔔', '7️⃣', '👑', '☠️']




        percentage = random.uniform(0,100)
        if percentage <= 30:
            slot1 = symbols[4]
        elif percentage <= 55 and percentage > 30:
            slot1 = symbols[3]
        elif percentage <= 70 and percentage > 55:
            slot1 = symbols[2]
        elif percentage <= 85 and percentage > 70:
            slot1 = symbols[1]
        elif percentage <= 100 and percentage > 85:
            slot1 = symbols[0]

        percentage = random.uniform(0,100)
        if percentage <= 20:
            slot2 = symbols[4]
        elif percentage <= 40 and percentage > 20:
            slot2 = symbols[3]
        elif percentage <= 60 and percentage > 40:
            slot2 = symbols[2]
        elif percentage <= 87 and percentage > 60:
            slot2 = symbols[1]
        elif percentage <= 100 and percentage > 87:
            slot2 = symbols[0]

        percentage = random.uniform(0,100)
        if percentage <= 35:
            slot3 = symbols[4]
        elif percentage <= 41 and percentage > 35:
            slot3 = symbols[3]
        elif percentage <= 60 and percentage > 41:
            slot3 = symbols[2]
        elif percentage <= 94 and percentage > 60:
            slot3 = symbols[1]
        elif percentage <= 100 and percentage > 95:
            slot3 = symbols[0]

        if slot1 == slot2 == slot3 == symbols[4]:
            footer = 'Лузер! Ваш баланс обнулён'
        elif slot1 == slot2 == slot3 == symbols[3]:
            footer = '+ 5 000 баксов на ваш счёт'
        elif slot1 == slot2 == slot3 == symbols[2]:
            footer = '+ 10 000 баксов на ваш счёт'
        elif slot1 == slot2 == slot3 == symbols[1]:
            footer = '+ 15 000 баксов на ваш счёт'
        elif slot1 == slot2 == slot3 == symbols[0]:
            footer = 'ДЖЕКПОТ!!! + 1 000 000 баксов на ваш счёт'
        elif slot1 == slot2 == symbols[0] or slot1 == slot3 == symbols[0] or slot2 == slot3 == symbols[0]:
            footer = '+ 3 500 баксов на ваш счёт'
        elif slot1 == symbols[0] or slot2 == symbols[0] or slot3 == symbols[0]:
            footer = '+ 1 500 баксов на ваш счёт'
        else:
            footer = 'Ничего('
        embed = discord.Embed(color = 0x36c600, title = '🎰 Slots Azino777', description = str(slot1) + str(slot2) + str(slot3))
        embed.set_footer(text = footer, icon_url = "https://i.imgur.com/uZIlRnK.png")
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Games(bot))
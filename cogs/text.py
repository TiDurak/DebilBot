import discord
from discord.ext import commands
from googletrans import Translator
from config import settings

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, lang, *, text):
        warntext = ('❌ Указан неверный язык! Использование команды:\n',
                    'd.translate `ru` `Ваш текст`\n'
                    '`ru` является языком, на который нужно переводить\n'
                    'Вместо `ru` может быть:\n'
                    '`ua`, `en`, `hu`, и т.д.\n')
        try:
            translator = Translator()
            translation = translator.translate(text, dest=lang)

            embed = discord.Embed(color = 0xffcd4c , title = f"{ctx.author} :: DebilBot Translator")
            embed.add_field(name = "Исходный Текст", value = text, inline = False)
            embed.add_field(name = "Перевод", value = translation.text, inline = False)
            await ctx.send(embed = embed)
        except ValueError:
            await ctx.send(warntext)


    @commands.command()
    async def echo(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)



    @commands.command()
    async def poll(self, ctx, question, *options: str):
        lowercase = [opts.lower() for opts in options]

        await ctx.message.delete()
        if len(options) < 1:
            await ctx.send('❌ Для создания голосования нужно хотя-бы 1 ответ!')
            return
        if len(options) > 10:
            await ctx.send('❌ Нельзя использовать более 10 ответов!')
            return

        if len(options) == 2 and lowercase[0] in ('да', 'yes') and lowercase[1] in ('нет', 'no'):
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n{} {}'.format(reactions[x], option)

        embed = discord.Embed(color = 0xffcd4c , title = f'{self.bot.get_emoji(settings["emojis"]["stonks"])} {ctx.message.author}: {question}', description=''.join(description))
        
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text= f'Poll ID: {react_message.id} \nКстати! Вопрос нужно указывать в кавычках!' )
        await react_message.edit(embed=embed)

def setup(bot):
    bot.add_cog(Text(bot))
import discord
from discord.ext import commands
from googletrans import Translator

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, lang, *, thing):
        warntext = '''
            ❌ Указан неверный язык! Использование команды:
            d.translate `ru` `Ваш текст`
            `ru` является языком, на который нужно переводить
            Вместо `ru` может быть:
            `ua`, `en`, `hu`, и т.д.'''
        try:
            translator = Translator()
            translation = translator.translate(thing, dest=lang)
            await ctx.send(translation.text)
        except ValueError:
            await ctx.send(warntext)


    @commands.command()
    async def echo(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)



    @commands.command()
    async def poll(self, ctx, question, *options: str):
        await ctx.message.delete()
        if len(options) <= 1:
            await ctx.send('❌ Для создания голосования нужно хотя-бы 1 ответ!')
            return
        if len(options) > 10:
            await ctx.send('❌ Нельзя использовать более 10 ответов!')
            return

        if len(options) == 2 and options[0] == 'да' and options[1] == 'нет':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(color = 0xffcd4c , title = f'{self.bot.get_emoji(879411306157985862)} {ctx.message.author}: {question}', description=''.join(description))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text= f'Poll ID: {react_message.id} \nКстати! Вопрос нужно указывать в кавычках!' )
        await react_message.edit(embed=embed)

def setup(bot):
    bot.add_cog(Text(bot))